from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import json
import os
from typing import List, Dict

def load_questions(category):
    """Load questions from JSON file for a specific category."""
    file_path = f"data/questions/{category}.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data["questions"]
    return []

# Track user's current question
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("JavaScript Fundamentals", callback_data="js_fundamentals"),
            InlineKeyboardButton("React/Modern Frameworks", callback_data="react_quiz")
        ],
        [
            InlineKeyboardButton("HTML/CSS", callback_data="html_css"),
            InlineKeyboardButton("System Design", callback_data="system_design")
        ],
        [
            InlineKeyboardButton("Coding Challenges", callback_data="coding"),
            InlineKeyboardButton("Behavioral Questions", callback_data="behavioral")
        ],
        [
            InlineKeyboardButton("Daily Practice", callback_data="daily"),
            InlineKeyboardButton("Interview Tips", callback_data="tips")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Handle both direct commands and callback queries
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "Welcome to Frontend Interview Prep Bot! 🚀\n\n"
            "I'll help you prepare for your frontend interviews. Choose a category to get started:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Welcome to Frontend Interview Prep Bot! 🚀\n\n"
            "I'll help you prepare for your frontend interviews. Choose a category to get started:",
            reply_markup=reply_markup
        )

async def show_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE, quiz_type: str):
    query = update.callback_query
    user_id = query.from_user.id
    
    # Initialize user state if not exists
    if user_id not in user_states:
        user_states[user_id] = {"current_question": 0, "score": 0, "quiz_type": quiz_type}
    
    # Reset question counter if switching quizzes
    if user_states[user_id].get("quiz_type") != quiz_type:
        user_states[user_id] = {"current_question": 0, "score": 0, "quiz_type": quiz_type}
    
    current_question = user_states[user_id]["current_question"]
    questions = load_questions(quiz_type)
    
    if current_question >= len(questions):
        # Quiz completed
        score = user_states[user_id]["score"]
        total = len(questions)
        keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            f"Quiz completed! Your score: {score}/{total}\n\nWould you like to try another quiz?",
            reply_markup=reply_markup
        )
        return
    
    question = questions[current_question]
    keyboard = []
    
    # Format options as a numbered list in the message
    options_text = "\n\nOptions:\n"
    for i, option in enumerate(question["options"]):
        options_text += f"{chr(65 + i)}. {option}\n"
        keyboard.append([InlineKeyboardButton(
            f"Option {chr(65 + i)}",
            callback_data=f"{quiz_type}_answer_{i}"
        )])
    
    # Add navigation buttons
    keyboard.append([
        InlineKeyboardButton("Next Question", callback_data=f"{quiz_type}_next"),
        InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"Question {current_question + 1}/{len(questions)}:\n\n"
        f"{question['question']}"
        f"{options_text}",
        reply_markup=reply_markup
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, quiz_type: str):
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"current_question": 0, "score": 0, "quiz_type": quiz_type}
    
    current_question = user_states[user_id]["current_question"]
    questions = load_questions(quiz_type)
    question = questions[current_question]
    
    # Extract the selected answer index from the callback data
    selected_answer = int(query.data.split("_")[-1])
    
    # Check if the answer is correct
    is_correct = selected_answer == question["correct"]
    if is_correct:
        user_states[user_id]["score"] += 1
    
    # Show the explanation
    keyboard = [[InlineKeyboardButton("Next Question", callback_data=f"{quiz_type}_next")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"{'✅ Correct!' if is_correct else '❌ Incorrect!'}\n\n"
    message += f"Explanation: {question['explanation']}"
    
    await query.message.reply_text(message, reply_markup=reply_markup)
    
    # Move to the next question
    user_states[user_id]["current_question"] += 1

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        await start(update, context)
    elif query.data == "js_fundamentals":
        keyboard = [
            [InlineKeyboardButton("JavaScript Methods Quiz", callback_data="js_methods_quiz")],
            [InlineKeyboardButton("JavaScript Types & Coercion Quiz", callback_data="js_types_quiz")],
            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Choose a JavaScript Fundamentals quiz:",
            reply_markup=reply_markup
        )
    elif query.data == "js_methods_quiz":
        await show_quiz(update, context, "js_methods")
    elif query.data == "js_types_quiz":
        await show_quiz(update, context, "js_types")
    elif query.data == "js_methods_next":
        await show_quiz(update, context, "js_methods")
    elif query.data == "js_types_next":
        await show_quiz(update, context, "js_types")
    elif query.data == "react_quiz":
        keyboard = [
            [InlineKeyboardButton("React Hooks Quiz", callback_data="react_hooks_quiz")],
            [InlineKeyboardButton("React Context & State Management Quiz", callback_data="react_context_quiz")],
            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Choose a React quiz:",
            reply_markup=reply_markup
        )
    elif query.data == "react_hooks_quiz":
        await show_quiz(update, context, "react_hooks")
    elif query.data == "react_context_quiz":
        await show_quiz(update, context, "react_context")
    elif query.data == "react_hooks_next":
        await show_quiz(update, context, "react_hooks")
    elif query.data == "react_context_next":
        await show_quiz(update, context, "react_context")
    elif query.data.startswith("js_methods_answer_"):
        await handle_answer(update, context, "js_methods")
    elif query.data.startswith("js_types_answer_"):
        await handle_answer(update, context, "js_types")
    elif query.data.startswith("react_hooks_answer_"):
        await handle_answer(update, context, "react_hooks")
    elif query.data.startswith("react_context_answer_"):
        await handle_answer(update, context, "react_context")
    else:
        await query.edit_message_text(text="Please select a valid category")

# Initialize bot
app = ApplicationBuilder().token("7634212120:AAFMy9LcXVNqKfrOogEePDy1Ns-iN-PYbF4").build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Run the bot
app.run_polling() 
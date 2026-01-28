from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

NAME, CALORIES, PROTEIN, FAT, CARBS, SUMMARY = range(6)

async def createfood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Name: ")
    return NAME

async def food_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Calories per 100g: ")
    return CALORIES

async def food_calories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['calories'] = update.message.text
    await update.message.reply_text("Protein per 100g: ")
    return PROTEIN #ConversationHandler.END

async def food_protein(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['protein'] = update.message.text
    await update.message.reply_text("Fat per 100g: ")
    return FAT

async def food_fat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fat'] = update.message.text
    await update.message.reply_text("Carbs per 100g: ")
    return CARBS

async def food_carbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['carbs'] = update.message.text
    return await summary(update, context)

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data['name']
    calories = context.user_data['calories']
    protein = context.user_data['protein']
    fat = context.user_data['fat']
    carbs = context.user_data['carbs']
    
    await update.message.reply_text(
        f"Succesfully created:\n"
        f"Food: {name}\n"
        f"Calories per 100g: {calories}\n"
        f"Protein per 100g: {protein}\n"
        f"Fat per 100g: {fat}\n"
        f"Carbs per 100g: {carbs}\n"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Clean up any temporary state
    context.user_data.clear()

    await update.message.reply_text(
        "Operation cancelled."
    )

    return ConversationHandler.END

conv = ConversationHandler(
    entry_points=[CommandHandler("createfood", createfood)],

    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_name)],
        CALORIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_calories)],
        PROTEIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_protein)],
        FAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_fat)],
        CARBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, food_carbs)],

        SUMMARY: [MessageHandler(filters.ALL, summary)],
    },  

    fallbacks=[CommandHandler("cancel", cancel)],
)

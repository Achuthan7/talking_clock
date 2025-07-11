import datetime
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import pytz
from gtts import gTTS
import os
import pygame

API_TOKEN = ''
CHAT_ID = ''

scheduled_tasks = []
skipped_tasks = []
task_running = False

async def send_messages(bot):
    indian_timezone = pytz.timezone('Asia/Kolkata')

    while task_running:
        current_time = datetime.datetime.now(indian_timezone).time()
        current_minute = current_time.minute

        for scheduled_minute, task in scheduled_tasks:
            if current_minute == scheduled_minute and task not in skipped_tasks:
                await bot.send_message(chat_id=CHAT_ID, text=f"{task}")

                myobj = gTTS(text=task, lang='en', slow=False)
                audio_file_path = "welcome.mp3"
                myobj.save(audio_file_path)

                pygame.mixer.init()
                pygame.mixer.music.load(audio_file_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                os.remove(audio_file_path)

        await asyncio.sleep(20)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global task_running
    bot = context.bot

    if not task_running:
        task_running = True
        context.application.create_task(send_messages(bot))
        await update.message.reply_text("Task scheduler started.")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global task_running
    if task_running:
        task_running = False
        await update.message.reply_text("Task scheduler stopped.")

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the time and task in the format 'HH:MM - Task Description'")
    context.user_data['awaiting_schedule'] = True

async def skip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            skipped_time = context.args[0]
            skipped_minute = int(skipped_time.split(':')[1])

            removed_tasks = []
            for scheduled_minute, task in scheduled_tasks:
                if scheduled_minute == skipped_minute:
                    scheduled_tasks.remove((scheduled_minute, task))
                    removed_tasks.append(task)

            if removed_tasks:
                await update.message.reply_text(f"Tasks scheduled for minute {skipped_minute} have been skipped.")
            else:
                await update.message.reply_text(f"No tasks found scheduled for minute {skipped_minute}.")
        except (ValueError, IndexError):
            await update.message.reply_text("Please provide the time to skip in the format 'HH:MM'.")
    else:
        await update.message.reply_text("Please provide the time to skip in the format 'HH:MM'.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_schedule'):
        user_input = update.message.text

        try:
            time_str, task = user_input.split(' - ', 1)
            scheduled_time = datetime.datetime.strptime(time_str, '%H:%M').time()
            scheduled_minute = scheduled_time.minute
            scheduled_tasks.append((scheduled_minute, task))
            await update.message.reply_text(f"Task scheduled: '{task}' at {time_str} every day.")
            context.user_data['awaiting_schedule'] = False
        except ValueError:
            await update.message.reply_text("Invalid format. Please provide the time and task in the format 'HH:MM - Task Description'.")

def main():
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("skip", skip_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()

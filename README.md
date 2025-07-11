# Talking Clock – Voice Alert Task Scheduler
Talking Clock is a Python Telegram bot for scheduling tasks that is meant to help people with early Alzheimer's or memory loss. It reminds and schedules tasks at the appropriate time using voice reminders so that daily routines are less stressful and easier to manage.

# Features

* Task Scheduling: Tasks can be added using the /schedule command in HH:MM - Task format.

* Voice Alerts: gTTS is utilized to convert scheduled tasks into voice and voice them out.

* Repeated Reminders: The task is reminded repeatedly at the assigned time.

* Easy Telegram Interface: Developed with the Telegram Bot API to provide the utmost ease of use on any platform.

* Start/Stop Control: Employ the /start command to start the reminder engine and /stop to close it down.

* Skip Specific Tasks: /skip HH:MM skips activities timed for that exact minute.

# Tech Stack
# Python 3

* Telegram Bot API (python-telegram-bot)

* gTTS – Google Text-to-Speech for speech output

* Pygame – Plays audio reminders

* Raspberry Pi 4 – Used to run and host the bot 24/7

# How It Works

# User interface via Telegram:

* /Schedule requests a description of the task and time.

* For example:
  * 12:30 - Take medication.

* Scheduler logic (in talkingclockv2.py):

* The bot often queries the current time.

* When the current minute matches a scheduled task, the bot:

* Sends a message to the chat.

* Translates the task description into speech.

* Plays the audio on the local device speaker.

* Recurring reminders: Items appear every day unless skipped manually.

# Use Case

* Problem Solved: Patients of early Alzheimer's are not able to remember their daily routines. Most reminder applications are graphical and require viewing the screen. Talking Clock solves this by providing audio reminders, and thus is very useful for:

* Older users Patients with mild cognitive impairment Visually impaired people
  
![Screenshot_20250711_111923_Telegram](https://github.com/user-attachments/assets/a423224d-926c-462a-8afc-de88a461a8e1)
![Screenshot_20250711_112247_Telegram](https://github.com/user-attachments/assets/c9db434c-0f2d-4066-acea-51519fbdbd80)


https://github.com/user-attachments/assets/2d0af818-221c-4ae4-828b-22c74bc79fb5


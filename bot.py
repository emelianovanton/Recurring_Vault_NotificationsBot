import telebot
import os
import datetime
import time

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)  # YOUR BOT TOKEN SHOULD BE HERE

# A dictionary to store the subscribed users and their chat IDs
subscribed_users = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    # Send a welcome message and instructions on how to subscribe to reminders
    bot.send_message(message.chat.id,
                     "Welcome to the Reminder Bot! To subscribe to weekly reminders, send the command /subscribe.")


@bot.message_handler(commands=['subscribe'])
def subscribe_command(message):
    # Add the user to the list of subscribed users and send a confirmation message
    subscribed_users[message.chat.id] = True
    bot.send_message(message.chat.id,
                     "You have subscribed to weekly reminders. You will receive a reminder every Monday at 11:00 AM.")


def send_reminder(week_number, accumulated_sum):
    # Send a reminder message to all subscribed users
    for chat_id in subscribed_users.keys():
        bot.send_message(chat_id, "Don't forget to add money to your vault! "
                                  f"Accumulated sum so far is {accumulated_sum} €"
                                  f"Today's sum to send is {week_number} € ")


while True:
    now = datetime.datetime.now()
    week_number = now.isocalendar()[1]
    accumulated_sum = week_number * (week_number + 1) / 2
    # Check if it's Sunday and the time is 9:00 AM
    if now.weekday() == 7 and now.hour == 11:
        send_reminder(week_number, accumulated_sum)
        # Wait for 1 week before sending the next reminder
        time.sleep(7 * 24 * 60 * 60)

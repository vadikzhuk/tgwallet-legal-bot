import telebot
import logging
import os
from telebot import types

# Get token from env
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Set up logging to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def calculate_formula(frequency, month, day):
    logging.info('Trying to calculate formula with %s, %s, %s', frequency, month, day)
    MONTH_LIST = [str(month) for month in range(1, 13)]
    MONTH_VALUES = {"January" : "1", "February": "2",
             "March": "3", "April": "4", "May": "5",
             "June": "6", "July": "7", "August": "8",
             "September": "9", "October": "10", "November": "11",
             "December": "12"}
    month = MONTH_VALUES[month]
    month_index = MONTH_LIST.index(month)

    match frequency:
        case "Yearly":
            formula = f"=if(today()>date(year(today()), {month}, {day}), date(year(today())+1, {month}, {day}), (date(year(today()), {month}, {day})))"
        case "Twice a year":
            biyearly_months = sorted([
                MONTH_LIST[month_index],
                MONTH_LIST[(month_index + 6) % 12]
            ], key=int)
            formula = f"=if(today() >= date(year(today()), {biyearly_months[0]}, {day}), date(year(today()), {biyearly_months[1]}, {day}), date(year(today()), {biyearly_months[0]}, {day}))"
        case "Quarterly":
            quarterly_months = sorted([
                MONTH_LIST[month_index],
                MONTH_LIST[(month_index + 3) % 12],
                MONTH_LIST[(month_index + 6) % 12],
                MONTH_LIST[(month_index + 9) % 12]
            ], key=int)
            formula = f"=IF(TODAY()>=DATE(YEAR(TODAY()), {quarterly_months[3]}, {day}), DATE(YEAR(TODAY())+1, {quarterly_months[0]}, {day}), IF(TODAY()>=DATE(YEAR(TODAY()), {quarterly_months[2]}, {day}), DATE(YEAR(TODAY()), {quarterly_months[3]}, {day}), IF(TODAY()>=DATE(YEAR(TODAY()), {quarterly_months[1]}, {day}), DATE(YEAR(TODAY()), {quarterly_months[2]}, {day}), IF(TODAY()>=DATE(YEAR(TODAY()), {quarterly_months[0]}, {day}), DATE(YEAR(TODAY()), {quarterly_months[1]}, {day}), DATE(YEAR(TODAY()), {quarterly_months[0]}, {day})))))"
        case "Monthly":
            formula = f"if(day(today()) < {day}, date(year(today()), month(today()), {day}), date(year(today()), month(today())+1, {day}))"
        case _:
            formula = "Something went wrong, please contact a developer"

    logging.info('Calculated formula: %s', formula)
    return formula

# Store user data
user_data = {}

# Handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_get_formula = types.KeyboardButton('Get formula')
    markup.add(button_get_formula)
    bot.send_message(message.chat.id, "Welcome! Press the button to get your formula.", reply_markup=markup)

# Handle the frequency prompt
@bot.message_handler(func=lambda message: message.text == 'Get formula')
def ask_frequency(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_yearly = types.KeyboardButton('Yearly')
    button_twice_yearly = types.KeyboardButton('Twice a year')
    button_quarterly = types.KeyboardButton('Quarterly')
    button_monthly = types.KeyboardButton('Monthly')
    markup.add(button_yearly, button_twice_yearly, button_quarterly, button_monthly)

    bot.send_message(message.chat.id, "Choose notification frequency", reply_markup=markup)
    user_data[message.chat.id] = {'step': 1}  # Track user step


# Handle frequency selection
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get('step') == 1)
def handle_frequency(message):
    user_data[message.chat.id]['frequency'] = message.text  # Save frequency
    logging.info('User %s chose frequency: %s', message.chat.id, user_data[message.chat.id]['frequency'])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    markup.add(*[types.KeyboardButton(month) for month in months])

    bot.send_message(message.chat.id, "Choose the nearest notification month", reply_markup=markup)
    user_data[message.chat.id]['step'] = 2  # Move to next step


# Handle month selection
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get('step') == 2)
def handle_month(message):
    user_data[message.chat.id]['month'] = message.text  # Save month
    logging.info('User %s chose month: %s', message.chat.id, user_data[message.chat.id]['month'])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*[types.KeyboardButton(str(i)) for i in range(1, 32)])  # Dates from 1 to 31

    bot.send_message(message.chat.id, "Choose the nearest notification date", reply_markup=markup)
    user_data[message.chat.id]['step'] = 3  # Move to next step


# Handle date selection
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get('step') == 3)
def handle_date(message):
    user_data[message.chat.id]['date'] = int(message.text)  # Save date
    logging.info('User %s chose date: %s', message.chat.id, user_data[message.chat.id]['date'])

    frequency = user_data[message.chat.id]['frequency']
    month = user_data[message.chat.id]['month']
    date = user_data[message.chat.id]['date']
    logging.info('All info for calculating formula: %s, %s, %s', frequency, month, date)

    formula = calculate_formula(frequency, month, date)
    logging.info('Calculated formula: %s', formula)

    # Send the formula to the user
    if formula != "Something went wrong, please contact a developer":
        bot.send_message(message.chat.id, "Here's your formula:")
    bot.send_message(message.chat.id, formula)

    # Send the user back to the start loop
    start(message)
    del user_data[message.chat.id]  # Clean up user data after completion


# Polling loop to keep the bot running
bot.polling(none_stop=True)

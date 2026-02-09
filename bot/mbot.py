import traceback

import telebot, random
from telebot import types
from datetime import datetime
from bot.spotify_installer import SpotifyInstaller

try:
    from bot.config import TOKEN, special_message, whitelist, white_list_id, help_message
    from bot.homework import homeworks
except Exception as e:
    print(e)
    TOKEN = ""
    whitelist = True
    special_message = "Welcome, Master!"
    help_message = "Just use the buttons."
    homeworks = {
        "01/01/2026": {
            "dailytask": {"reading": "Read page 10", "listening": "Listen track 2"},
            "homework": {"workbook": "Do ex. 5"}
        },
        "01/23/2026": {
            "dailytask": {"vocabulary": "Learn words"},
            "homework": {"essay": "Write about summer"}
        }
    }

bot = telebot.TeleBot(TOKEN)
spotify_installer = SpotifyInstaller()


def is_authorized(user):
    if user.id == 5104299484: #Admin ID
        return True

    if not whitelist:
        return True

    return user.id in white_list_id.keys()



def get_main_keyboard():
    """Главное меню."""
    markup = types.InlineKeyboardMarkup()
    btn_hw = types.InlineKeyboardButton("📚 Homework", callback_data="menu:dates")
    markup.add(btn_hw)
    return markup


def get_back_button(callback_data):
    return types.InlineKeyboardButton("🔙 Back", callback_data=callback_data)




@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    print(f"{user.first_name} (@{user.username}) (#{user.id}) wrote: {message.text}")

    if not is_authorized(user):
        bot.send_message(message.chat.id, "Well, this bot is not working right now, my apologies :(")
        return

    welcome_words = ["Welcome", "Master", "Hello", "Hi", "What's up", "Glad to see you"]

    text = f"{random.choice(welcome_words)} {user.first_name}!\n\n"


#    text += special_message if is_authorized(user) and whitelist else "Choose action:"
    if user.id == 6502028914 or user.id == 5104299484:
        text += '\nNew command was added.\nType "/s <link to the spotify track"\nTo download track and listen to it totally offline.\n(Visible only for one person)'

    bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard())

@bot.message_handler(commands=['info'])
def info_command(message):

    if not is_authorized(message.from_user):
        return

    t = help_message
    t += f"\n\nSource code of bot (for geniuses 😈): https://github.com/kay1mov/alexandria/tree/main/bot"
    bot.send_message(message.chat.id, t)

@bot.message_handler(commands=['whitelist'])
def whitelist_command(message):

    user = message.from_user

    print(f"{user.first_name} (@{user.username}) (#{user.id}) wrote: {message.text}")
    if not is_authorized(message.from_user):
        return

    text = "📋 Whitelist Users:\n"
    for key, value in white_list_id.items():
        text += f"User #{key}"
        if int(key) == user.id:
            text += " (You)"

        text += "\n"

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['s'])
def spotify_downloader(message):

    user = message.from_user
    print(f"{user.first_name} (@{user.username}) (#{user.id}) wrote: {message.text}")

    try:
        link = message.text.split()[1]
    except IndexError:
        print("No link.")
        bot.send_message(message.chat.id, 'You have to add link to the command.\nExample: \n"/s https://open.spotify.com/track/7fy6O1FnOQb4rKRFX9DbLy"')
        return
    bot.delete_message(message.chat.id, message.message_id)
    try_msg = bot.send_message(message.chat.id, f'⬇️ Downloading...')

    result = spotify_installer.download_track(link)
    if result is not None:
        print("Result is successful")
        with open(result, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
            print("Audio sent")
        bot.delete_message(message.chat.id, try_msg.message_id)
    else:
        bot.send_message(message.chat.id, f"Sorry, I couldn't download this track...")
        print("Could not download")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = call.from_user


    if not is_authorized(user):
        bot.answer_callback_query(call.id, "Access denied")
        return

    buttons = []
    data = call.data.split(":")
    action = data[0]
    print(f"[{datetime.now()}] User: {user.first_name} (@{user.username}) (#{user.id}) interaction:")
    for a in data:
        print(f" - {a}")

    try:
        if action == "menu" and data[1] == "dates":
            markup = types.InlineKeyboardMarkup(row_width=2)
            sorted_dates = sorted(homeworks.keys(), reverse=True)
            sorted_dates = sorted_dates[:4]
            markup.add(types.InlineKeyboardButton(f"📔 Today", callback_data="date:today"))

            buttons = []
            for date in sorted_dates:
                buttons.append(types.InlineKeyboardButton(f"🗓 {date}", callback_data=f"date:{date}"))

            markup.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="📅 Choose date:", reply_markup=markup)

        elif action == "date":
            selected_date = data[1]
            if selected_date not in homeworks:
                if selected_date == "today":
                    print("Today")
                    date = datetime.now()
                    str_format = f'{str(0) if date.month < 10 else ""}{date.month}/{str(0) if date.day < 10 else ""}{date.day}/{date.year}'
                    selected_date = str_format

                else:
                    bot.answer_callback_query(call.id, "No data for this date.")
                    return

            markup = types.InlineKeyboardMarkup()
            try:
                task_types = homeworks[selected_date].keys()
            except KeyError:
                bot.answer_callback_query(call.id, "No homeworks for today")
                return


            for t_type in task_types:
                display_name = "📝 Daily Task" if t_type == "dailytask" else "book: Homework"
                if t_type == "homework": display_name = "🏠 Homework"

                markup.add(types.InlineKeyboardButton(display_name, callback_data=f"type:{selected_date}:{t_type}"))

            markup.add(get_back_button("menu:dates"))

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"📂 Date: {selected_date}\nChoose type of homework:", reply_markup=markup)

        elif action == "type":
            selected_date = data[1]
            task_type = data[2]

            tasks_dict = homeworks[selected_date].get(task_type, {})

            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons.clear()

            buttons.append(
                types.InlineKeyboardButton("🔥 Show ALL", callback_data=f"show:{selected_date}:{task_type}:all"))

            for subtype in tasks_dict.keys():
                buttons.append(types.InlineKeyboardButton(subtype.capitalize(),
                                                          callback_data=f"show:{selected_date}:{task_type}:{subtype}"))

            markup.add(*buttons)
            markup.add(get_back_button(f"date:{selected_date}"))

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"📂 {selected_date} -> {task_type.capitalize()}\nChoose certain task:",
                                  reply_markup=markup)

        elif action == "show":
            selected_date = data[1]
            task_type = data[2]
            subtype = data[3]

            tasks_dict = homeworks[selected_date].get(task_type, {})

            result_text = f"=== 🗓 {selected_date} | {task_type.capitalize()} ===\n\n"

            if subtype == "all":
                for key, value in tasks_dict.items():
                    result_text += f"🔹 <b>{key.capitalize()}:</b>\n{value}\n\n"
            else:
                value = tasks_dict.get(subtype, "No data")
                result_text += f"🔹 <b>{subtype.capitalize()}:</b>\n{value}"

            markup = types.InlineKeyboardMarkup()
            markup.add(get_back_button(f"type:{selected_date}:{task_type}"))

            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=result_text, parse_mode="HTML", reply_markup=markup)
            except Exception as error:
                print(error)
                print(traceback.format_exc())
                bot.send_message(call.message.chat.id, result_text, parse_mode="HTML")

    except Exception as error:
        print(f"Error in callback: {error}")
        print(traceback.format_exc())
        try:
            bot.answer_callback_query(call.id, "ERROR")
        except Exception as error:
            print(error)
            print(traceback.format_exc())


if __name__ == "__main__":
    print("🤖 Бот запущен и готов к работе...")
    try:
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60
        )
    except Exception as err:
        print(err, " skip...")

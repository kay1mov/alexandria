from pathlib import Path

TOKEN = "TOKEN"

white_list_id = {

    123456789: {
        "name": "Abcde",
        "status": "Active",
        "hidden": False
}

#special_message = f'No need to explain how “cool" you are just because you’re on the whitelist and blah-blah-blah.\nEnjoy 🎯\n\nType "/info - for information"'
special_message = f'If the button is not working, try restarting the bot by typing /start again.\nIf it did not help - then bot is not working."\n\nType "/info - for information"'
whitelist = True

help_message = f'''
/start - Start bot
/whitelist - List of people in staff
/info - Few information about the bot

🚫 Non-whitelisted individuals are not welcome under any circumstances 🚫
'''

root = Path(__file__).parent.parent
bot_directory = root / "bot"
homework_directory = bot_directory / "data" / "homework.json"
audio_files_directory = bot_directory / "data" / "audio_files"

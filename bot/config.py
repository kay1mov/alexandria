TOKEN = "8403247650:AAEfur_7b00rpGTVghnM51Dx5NVs6ORZozM"

# white_list_id = {
#     1125142016: "Doston",
#     6502028914: "Amina",
# #    7355193913: "Anis",
#     6494875059: "Farzona",
#     1277811720: "Azizjon",
#     1633342686: "Khursandbek"
# }

white_list_id = {

    1125142016: {
        "name": "Doston",
        "status": "Active",
        "hidden": True
    },
    6502028914: {
        "name": "Amina",
        "status": "Active",
        "hidden": True
    },
    6494875059: {
        "name": "Farzona",
        "status": "Active",
        "hidden": True
    },
    7355193913: {
        "name": "Anis",
        "status": "Inactive",
        "hidden": True
    },
    1277811720: {
        "name": "Azizjon",
        "status": "Active",
        "hidden": True
    },
    1633342686: {
        "name": "Khursandbek",
        "status": "Active",
        "hidden": True
    },
    5104299484: {
        "name": "Umarbek",
        "status": "Active",
        "hidden": True
    }
}

#special_message = f'No need to explain how “cool" you are just because you’re on the whitelist and blah-blah-blah.\nEnjoy 🎯\n\nType "/info - for information"'
special_message = f'Is not working due to technical updates.\n\nType "/info - for information"'
whitelist = True

help_message = f'''
/start - Start bot
/whitelist - List of people in staff
/s <link to the Spotify track> - Download spotify track
/info - Few information about the bot

🚫 Non-whitelisted individuals are not welcome under any circumstances 🚫
'''

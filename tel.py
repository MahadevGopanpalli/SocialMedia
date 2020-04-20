
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import csv
import random
import time

api_id = 1315298

api_hash = 'd9b222c6943d39f5640f24109461b556'

phone = '+917776808085'

username = 'Vaibhav Gopanpalli'

SLEEP_TIME = 30
client = TelegramClient(phone, api_id, api_hash)
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
 

user = '+918600370481'
 
messages= ["Hello {}, How are you?", "Hi {}, What's up?", "Hey {}, do you want to gotrained?"]

receiver = client.get_input_entity(user)
message = random.choice(messages)

print("Sending Message to:", user)
client.send_message(receiver, message.format(user))

client.disconnect()
print("Done. Message sent ")
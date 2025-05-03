# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re 
import sys
import asyncio 
import logging 
from database import Db, db
from config import Config, temp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from pyrogram.errors import FloodWait
from config import Config
from script import Script
from typing import Union, Optional, AsyncGenerator
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)]\[buttonurl:/{0,2}(.+?)(:same)?])")
BOT_TOKEN_TEXT = "<b>1) create a bot using @BotFather\n2) Then you will get a message with bot token\n3) Forward that message to me</b>"
SESSION_STRING_SIZE = 351

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

class CLIENT: 
  def __init__(self):
     self.api_id = Config.API_ID
     self.api_hash = Config.API_HASH

  def user_session(self, data):
      return Client("USERBOT", self.api_id, self.api_hash, session_string=data)
     
  async def add_bot(self, bot, message):
     user_id = int(message.from_user.id)
     msg = await bot.ask(chat_id=user_id, text=BOT_TOKEN_TEXT)
     if msg.text=='/cancel':
        return await msg.reply('<b>process cancelled !</b>')
     elif not msg.forward_date:
       return await msg.reply_text("<b>This is not a forward message</b>")
     elif str(msg.forward_from.id) != "93372553":
       return await msg.reply_text("<b>This message was not forward from bot father</b>")
     bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', msg.text, re.IGNORECASE)
     bot_token = bot_token[0] if bot_token else None
     if not bot_token:
       return await msg.reply_text("<b>There is no bot token in that message</b>")
     try:
       _client = Client("BOT", Config.API_ID, Config.API_HASH, bot_token=bot_token, in_memory=True)
       client = await _client.start()
     except Exception as e:
       await msg.reply_text(f"<b>BOT ERROR:</b> `{e}`")
       return
     _bot = _client.me
     details = {
       'id': _bot.id,
       'is_bot': True,
       'user_id': user_id,
       'name': _bot.first_name,
       'token': bot_token,
       'username': _bot.username 
     }
     await db.add_bot(details)
     return True
      async def add_session(self, bot, message):
     user_id = int(message.from_user.id)
     text = "<b>⚠️ DISCLAIMER ⚠️</b>\n\n<code>You can use your session for forward messages from private chats to another chat.\nPlease add your Pyrogram session with your own risk. There is a chance of your account being banned. My developer is not responsible if your account gets banned.</code>\n\n<b>Please send your Pyrogram session string.</b>\n\n<b>You can get your session string using tools like:</b>\n- <a href='https://my.telegram.org/apps'>Telegram Core (for API ID and Hash)</a> and then a Pyrogram session generator.\n- Other third-party Pyrogram session generator bots/tools (use with caution!)."
     await bot.send_message(user_id, text=text, disable_web_page_preview=True)
     session_string_msg = await bot.ask(chat_id=user_id, text="<b>Paste your session string here:</b>\n\n/cancel - <code>cancel this process</code>")

     if session_string_msg.text == '/cancel':
        return await session_string_msg.reply('<b>Process cancelled !</b>')

     string_session = session_string_msg.text.strip()

     if len(string_session) < SESSION_STRING_SIZE:
        return await session_string_msg.reply('<b>Invalid session string (too short).</b>')

     try:
       _client = Client("USERBOT", self.api_id, self.api_hash, session_string=string_session)
       await _client.connect()
       user = await _client.get_me()
       await _client.disconnect()

       details = {
         'id': user.id,
         'is_bot': False,
         'user_id': user_id,
         'name': user.first_name,
         'session': string_session,
         'username': user.username
       }
       await db.add_userbot(details)
       await session_string_msg.reply_text("<b>Session string successfully added for your userbot.</b>")
       return True

     except Exception as e:
       return await session_string_msg.reply_text(f"<b>USER BOT ERROR:</b> `{e}`\n\n<b>Please ensure your session string is valid.</b>")
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command('reset'))
async def forward_tag(bot, m):
   default = await db.get_configs("01")
   await db.update_configs(m.from_user.id, default)
   await m.reply("successfully settings reseted ✔️")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command('resetall') & filters.user(Config.BOT_OWNER))
async def resetall(bot, message):
  users = await db.get_all_users()
  sts = await message.reply("**processing**")
  TEXT = "total: {}\nsuccess: {}\nfailed: {}\nexcept: {}"
  total = success = failed = already = 0
  ERRORS = []
  async for user in users:
      user_id = user['id']
      default = await get_configs(user_id)
      default['db_uri'] = None
      total += 1
      if total %10 == 0:
         await sts.edit(TEXT.format(total, success, failed, already))
      try: 
         await db.update_configs(user_id, default)
         success += 1
      except Exception as e:
         ERRORS.append(e)
         failed += 1
  if ERRORS:
     await message.reply(ERRORS[:100])
  await sts.edit("completed\n" + TEXT.format(total, success, failed, already))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_configs(user_id):
  configs = await db.get_configs(user_id)
  return configs

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def update_configs(user_id, key, value):
  current = await db.get_configs(user_id)
  if key in ['caption', 'duplicate', 'db_uri', 'forward_tag', 'protect', 'min_size', 'max_size', 'extension', 'keywords', 'button']:
     current[key] = value
  else: 
     current['filters'][key] = value
  await db.update_configs(user_id, current)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def iter_messages(
    self,
    chat_id: Union[int, str],
    limit: int,
    offset: int = 0,
    filters: dict = None,
    max_size: int = None,
) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        dup_files = []
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return

            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                if any(getattr(message, media_type, False) for media_type in filters):
                    yield "FILTERED"
                else:
                    yield message
                    
                current += 1

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_client(bot_token, is_bot=True):
  if is_bot:
    return Client("BOT", Config.API_ID, Config.API_HASH, bot_token=bot_token, in_memory=True)
  else:
    return Client("USERBOT", Config.API_ID, Config.API_HASH, session_string=bot_token)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def parse_buttons(text, markup=True):
    buttons = []
    for match in BTN_URL_REGEX.finditer(text):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        if n_escapes % 2 == 0:
            if bool(match.group(4)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", "")))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", ""))])
    if markup and buttons:
       buttons = InlineKeyboardMarkup(buttons)
    return buttons if buttons else None

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

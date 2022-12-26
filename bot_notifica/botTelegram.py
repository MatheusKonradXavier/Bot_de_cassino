import telebot
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_BOT = os.getenv('bot_notifica')
bot = telebot.TeleBot(CHAVE_BOT)

def enviarMensagem(mensagem):
  try :
    bot.send_message(os.getenv('grupo_telegram'), mensagem)
    return True
  except :
    return False
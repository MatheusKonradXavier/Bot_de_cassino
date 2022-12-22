import telebot
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_BOT = os.environ['bot_notifica']
bot = telebot.TeleBot(CHAVE_BOT)

def enviarMensagem(mensagem):
  try :
    bot.send_message(os.environ['grupo_telegram'], mensagem)
    return True
  except :
    return False
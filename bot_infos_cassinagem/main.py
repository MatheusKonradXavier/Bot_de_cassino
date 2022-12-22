import telebot
import pandas as pd
import requests as r
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_BOT = os.environ['bot_infos']
link =  os.environ['link_api']
bot = telebot.TeleBot(CHAVE_BOT)

@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    resultados = r.get(link + 'mostra_resultados').json()
    ubd = r.get(link + 'mostra_brancoduplo').json()
    resultados = pd.DataFrame(resultados)
    contaBranco = 0
    contaCasa = 0
    start = False
    for i,j in resultados.iterrows():
        if(j.horas == ubd[0]):
            start = True
        if(start):
            if(j.valores == ' 0 '):
                contaBranco +=1
            contaCasa+=1 
    resposta = "O último branco duplo aconteceu na hora : " + ubd[0] + "\n"  + "O número de jogadas sem branco duplo é : " + str(contaCasa) + "\n" + "O número de brancos desde o último branco duplo é : " + str(contaBranco)
    bot.send_message(mensagem.chat.id, resposta)

@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    resultados = r.get(link + 'mostra_resultados').json()
    ubd = r.get(link + 'mostra_brancodentado').json()
    resultados = pd.DataFrame(resultados)
    contaBranco = 0
    contaCasa = 0
    start = False
    for i,j in resultados.iterrows():
        if(str(j.horas).replace(' ', '') ==  str(ubd[0]).replace(' ', '')):
            start = True
        if(start):
            if(j.valores == ' 0 '):
                contaBranco +=1
            contaCasa+=1 
    resposta = "O último branco dentado aconteceu na hora : " + ubd[0] + "\n"  + "O número de jogadas sem branco dentado é : " + str(contaCasa) + "\n" + "O número de brancos desde o último branco dentado é : " + str(contaBranco)
    bot.send_message(mensagem.chat.id, resposta)

""" @bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    
    bot.send_message(mensagem.chat.id, resposta) """

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     /opcao1 Informações do último branco duplo
     /opcao2 Informações do último branco dentado
     Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

bot.polling()
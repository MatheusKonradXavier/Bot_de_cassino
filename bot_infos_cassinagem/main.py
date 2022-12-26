import telebot
import pandas as pd
import requests as r
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_BOT = os.environ['bot_infos']
link = os.environ['link_api']
bot = telebot.TeleBot(CHAVE_BOT)


@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    resultados = r.get(link + 'mostra_resultados').json()
    ubd = r.get(link + 'mostra_brancoduplo').json()
    dados = r.get(link + 'dados_analisados').json()
    resultados = pd.DataFrame(resultados)
    contaBranco = 0
    contaCasa = 0
    start = False
    aux = False
    contaDuplo = 0
    contaCasa2 = 0
    contaBranco2 = 0
    for i, j in resultados.iterrows():
        if ((j.valores == ' 0 ') and (aux == True)):
            contaDuplo += 1
            aux = False
            contaCasa2 -= 1
            contaBranco2 -= 1
        elif ((j.valores == ' 0 ') and (aux == False)):
            aux = True
            contaCasa2 += 1
            contaBranco2 += 1
        else:
            aux = False
            contaCasa2 += 1
        if (j.horas == ubd[0]):
            start = True
        if (start):
            if (j.valores == ' 0 '):
                contaBranco += 1
            contaCasa += 1
    resposta = "O último branco duplo aconteceu na hora: " + ubd[0] + "\n" + "O número de jogadas desde o ultimo branco duplo é : " + str(
        contaCasa) + "\n" + "O número de brancos desde o último branco duplo é : " + str(contaBranco) + "\nA média de rodadas sem brancos duplos é: {:.2f}".format(contaCasa2/contaDuplo) + "\nA média de brancos entre brancos duplos é: {:.2f}".format(contaBranco2/contaDuplo)

    bot.send_message(mensagem.chat.id, resposta)


@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    resultados = r.get(link + 'mostra_resultados').json()
    ubd = r.get(link + 'mostra_brancodentado').json()
    resultados = pd.DataFrame(resultados)
    contaBranco = 0
    contaCasa = 0
    start = False
    for i, j in resultados.iterrows():
        if (str(j.horas).replace(' ', '') == str(ubd[0]).replace(' ', '')):
            start = True
        if (start):
            if (j.valores == ' 0 '):
                contaBranco += 1
            contaCasa += 1
    resposta = "O último branco dentado aconteceu na hora : " + ubd[0] + "\n" + "O número de jogadas sem branco dentado é : " + str(
        contaCasa) + "\n" + "O número de brancos desde o último branco dentado é : " + str(contaBranco)
    bot.send_message(mensagem.chat.id, resposta)


@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    resultados = r.get(link + 'mostra_resultados').json()
    resultados = pd.DataFrame(resultados)
    resposta = "4 5 6 indiozinhos"
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
     /opcao3 1 2 3 indiozinhos
     Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)


bot.polling()

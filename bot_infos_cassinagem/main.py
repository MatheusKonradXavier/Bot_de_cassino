import telebot
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_BOT = os.getenv('bot_infos')
link = os.getenv('link_api')
bot = telebot.TeleBot(CHAVE_BOT)

@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeSemBranco = 0
    vezesSemBranco = 0
    Soma = 0
    vezes = 0
    cont = 0
    start = False
    contBranco = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemBranco += 1
        else :
            contBranco +=1
            if(start) :
                if(recordeSemBranco < vezesSemBranco):
                    recordeSemBranco = vezesSemBranco 
                if(vezesSemBranco>-1):
                    Soma += vezesSemBranco
                    vezes+=1
            start = True
            vezesSemBranco = 0
        cont+=1
    resposta = " NÚMERO ATUAL DE RODADAS SEM BRANCO " + str(vezesSemBranco) + "\n MÉDIA DE RODADAS SEM BRANCOS " + str(Soma//vezes) + "\n RECORDE DE RODADAS SEM BRANCOS " + str(recordeSemBranco)

    bot.send_message(mensagem.chat.id, resposta)


@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeSemDuplo = 0
    recordeBrancoEntreDuplos = 0
    vezesSemDuplo = 0
    Soma = 0
    vezes = 0
    SomaB =0
    vezesB = 0
    contBranco = 0
    entreDuplos = 0
    cont = 0
    start = False

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemDuplo += 1
            contBranco = 0
        else :
            contBranco +=1
            entreDuplos +=1
            if(contBranco >= 2):
                if(start) :
                    if(recordeBrancoEntreDuplos< entreDuplos-2):
                        recordeBrancoEntreDuplos = entreDuplos-2
                    if(entreDuplos-2>3):
                        SomaB+=entreDuplos-2
                        vezesB+=1
                    if(recordeSemDuplo < vezesSemDuplo-2):
                        recordeSemDuplo = vezesSemDuplo-2
                    if(vezesSemDuplo-2>2):
                        Soma += vezesSemDuplo-2
                        vezes+=1
                start = True
                entreDuplos = 0
                contBranco = 0
                vezesSemDuplo = 0
            else:
                vezesSemDuplo += 1
        cont +=1

    resposta = " NÚMERO ATUAL DE RODADAS SEM DUPLOS " + str(vezesSemDuplo) + "\n NÚMERO ATUAL DE BRANCOS SEM DUPLOS " + str(entreDuplos) + "\n MÉDIA DE BRANCOS ENTRE DUPLOS " + str(SomaB//vezesB)+ "\n RECORDE DE BRANCOS ENTRE DUPLOS " + str(recordeBrancoEntreDuplos) + "\n MÉDIA DE RODADAS SEM DUPLOS " + str(Soma//vezes) + "\n RECORDE DE RODADAS SEM DUPLOS " + str(recordeSemDuplo)
    bot.send_message(mensagem.chat.id, resposta)


@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeSemDentado = recordeSemBrancos = jogadasBrancos = 0
    jogadas = vezesSemDentado = contBranco = 0
    soma = somaB = vezes = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemDentado +=1
            jogadas+=1
            if(not(contBranco == 1 and vezesSemDentado == 1)):
                contBranco = 0
        else :
            if(not(vezesSemDentado == 1)):
                jogadas+=1
                vezesSemDentado = 0
                contBranco=1
                jogadasBrancos +=1
            elif(contBranco==1):
                if(jogadasBrancos > recordeSemBrancos):
                    recordeSemBrancos = jogadasBrancos
                if(jogadas > recordeSemDentado):
                    recordeSemDentado = jogadas
                vezes+=1
                somaB +=jogadasBrancos
                soma+=jogadas
                jogadas = 0
                jogadasBrancos = 0
                vezesSemDentado = 0    

    resposta = ("  Recorde de jogadas entre dentados " +str(recordeSemDentado)+ 
                "\n Recorde de brancos entre dentados " +str(recordeSemBrancos)+ 
                "\n Média de brancos entre dentados " +str(somaB//vezes)+ 
                "\n Média de jogadas entre dentados " +str(soma//vezes)+ 
                "\n Número atual de jogadas sem dentado " +str(jogadas)+ 
                "\n Número atual de brancos sem dentado " +str(jogadasBrancos))

    bot.send_message(mensagem.chat.id, resposta)

@bot.message_handler(commands=["opcao4"])
def opcao4(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    vezesSemDentado = 0
    contBranco = 0
    cont = 0
    vezesSemNada =0
    brancoSemNada =0
    recordeDeBrancoSemNada =0
    somaBSN = 0
    vezesBSN = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemDentado +=1
            vezesSemNada +=1
            if(not(contBranco == 1 and vezesSemDentado == 1)):
                contBranco = 0
        else :
            contBranco+=1
            brancoSemNada+=1
            if(not(vezesSemDentado == 1)):
                vezesSemDentado = 0
            if(contBranco == 2 and vezesSemDentado == 1):
                if((brancoSemNada - 2 ) > recordeDeBrancoSemNada):
                    recordeDeBrancoSemNada = brancoSemNada - 2
                if(brancoSemNada - 2 <0 ):
                    somaBSN += 0
                    vezesBSN +=1
                else:
                    somaBSN += brancoSemNada - 2
                    vezesBSN +=1
                brancoSemNada = 0
                vezesSemNada = 0
            elif(contBranco>=2):
                if((brancoSemNada - 2 ) > recordeDeBrancoSemNada):
                    recordeDeBrancoSemNada = brancoSemNada - 2
                if(brancoSemNada - 2 <0 ):
                    somaBSN += 0
                    vezesBSN +=1
                else:
                    somaBSN += brancoSemNada - 2
                    vezesBSN +=1
                brancoSemNada = 0
                vezesSemNada = 0
        cont +=1

    resposta = " O NÚMERO DE BRANCOS SEM DENTADO OU DUPLO É "+str(brancoSemNada) + "\n O RECORDE DE BRANCOS SEM NADA É "+ str(recordeDeBrancoSemNada) + "\n A MÉDIA DE BRANCOS SEM NADA É " + str(somaBSN//vezesBSN)
    bot.send_message(mensagem.chat.id, resposta)

def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     /opcao1 Informações do último branco
     /opcao2 Informações do último branco duplo
     /opcao3 Informações do último branco dentado
     /opcao4 Infos sobre dentados e duplos juntos
     Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

def iniciaBot(bot):
    try:
        bot.polling()
    except:
        iniciaBot(bot)

if __name__ == "__main__":
    iniciaBot(bot)
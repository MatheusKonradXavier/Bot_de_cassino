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
    dados = requests.get(link + 'dados_analisados/1').json()
    tamanho = int(''.join(map(str, dados['dadosB'])))
    resultados = requests.get(
        link + 'mostra_resultados/' + str(tamanho)).json()
    resultados = pd.DataFrame(resultados)
    contaBranco = int(''.join(map(str, dados['contaBrancoB'])))
    contaCasa = int(''.join(map(str, dados['contaCasaB'])))
    contaCasa_depoisDoBranco = int(
        ''.join(map(str, dados['contaCasa_depoisDoBranco'])))
    recordeBranco = int(''.join(map(str, dados['recordB'])))
    hora = dados['hora'][0]

    for i, j in resultados.iterrows():
        if (j.valores == ' 0 '):
            contaBranco += 1
            hora = j.horas
            if (contaCasa_depoisDoBranco > recordeBranco):
                recordeBranco = contaCasa_depoisDoBranco
            contaCasa = 0
        elif (j.valores != ' 0 '):
            if (i != 0):
                contaCasa += 1
                contaCasa_depoisDoBranco += 1

    if (len(resultados) > 1):
        tamanho -= i

    resposta = "Número de elementos contidos no banco: " + str(
        abs(tamanho)) + "\nO número de brancos é: " + str(
            contaBranco) + "\nO número de rodadas sem branco é: " + str(
        contaCasa_depoisDoBranco) + "\nO ultímo branco aconteceu na hora: " + str(
                hora) + "\nO número de jogadas sem branco desde o ultimo branco é: " + str(
                    contaCasa) + "\nA média de rodadas sem branco é: {:.2f}".format(
                        contaCasa_depoisDoBranco/contaBranco) + "\nO recorde de jogadas sem branco é: " + str(
                            recordeBranco)

    ultimo = {
        "dadosB": str(tamanho),
        "contaBrancoB": str(contaBranco),
        "contaCasaB": str(contaCasa),
        "contaCasa_depoisDoBranco": str(contaCasa_depoisDoBranco),
        "hora": str(hora).replace(" ", ""),
        "recordB": str(recordeBranco)
    }

    requests.post(os.getenv('link_api') +
                  '/salva_dados_analisados/1', json=ultimo)

    bot.send_message(mensagem.chat.id, resposta)


@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    dados = requests.get(link + 'dados_analisados/2').json()
    tamanho = int(''.join(map(str, dados['dados'])))
    resultados = requests.get(
        link + 'mostra_resultados/' + str(tamanho)).json()
    resultados = pd.DataFrame(resultados)
    aux = False
    recordJ = int(''.join(map(str, dados['recordJ'])))
    recordB = int(''.join(map(str, dados['recordB'])))
    contaCasa_depoisDoDuplo = int(
        ''.join(map(str, dados['contaCasa_depoisDoDuplo'])))
    contaBranco_depoisDoDuplo = int(
        ''.join(map(str, dados['contaBranco_depoisDoDuplo'])))
    contaCasa = int(''.join(map(str, dados['contaCasa'])))
    contaDuplo = int(''.join(map(str, dados['contaDuplo'])))
    contaCasa_semDuplos = int(''.join(map(str, dados['contaCasa_semDuplos'])))
    contaBranco_normal = int(''.join(map(str, dados['contaBranco_normal'])))
    hora = dados['hora'][0]

    for i, j in resultados.iterrows():
        if ((j.valores == ' 0 ') and (aux == True)):
            contaDuplo += 1
            aux = False
            contaCasa_semDuplos -= 1
            contaBranco_normal -= 1
            contaCasa_depoisDoDuplo -= 1
            contaBranco_depoisDoDuplo -= 1
            hora = j.horas
            if (contaCasa_depoisDoDuplo > recordJ):
                recordJ = contaCasa_depoisDoDuplo
            if (contaBranco_depoisDoDuplo > recordB):
                recordB = contaBranco_depoisDoDuplo
            contaCasa_depoisDoDuplo = 0
            contaBranco_depoisDoDuplo = 0
        elif ((j.valores == ' 0 ') and (aux == False)):
            if (i != 0):
                aux = True
                contaCasa_semDuplos += 1
                contaBranco_normal += 1
                contaCasa_depoisDoDuplo += 1
                contaBranco_depoisDoDuplo += 1
        else:
            if (i != 0):
                aux = False
                contaCasa_semDuplos += 1
                contaCasa_depoisDoDuplo += 1

    if (len(resultados) > 1):
        tamanho -= i

    resposta = "Número de elementos contidos no banco: " + str(abs(tamanho)) + "\nO número de brancos duplos é: " + str(contaDuplo) + "\nO último branco duplo aconteceu na hora: " + str(hora) + "\n" + "O número de jogadas sem branco duplo é : " + str(
        contaCasa_semDuplos) + "\nO número de brancos desde o último branco duplo é : " + str(
            contaBranco_depoisDoDuplo) + "\nA média de rodadas sem brancos duplos é: {:.2f}".format(contaCasa_semDuplos/contaDuplo) + "\nA média de brancos entre brancos duplos é: {:.2f}".format(
                contaBranco_normal/contaDuplo) + "\nO recorde de jogadas sem branco duplo é: " + str(
                    recordJ) + "\nO recorde de brancos sem branco duplo é: " + str(recordB)

    ultimo = {
        "dados": str(tamanho),
        "contaBranco_normal": str(contaBranco_normal),
        "contaCasa": str(contaCasa),
        "contaCasa_semDuplos": str(contaCasa_semDuplos),
        "contaDuplo": str(contaDuplo),
        "recordJ": str(recordJ),
        "recordB": str(recordB),
        "contaCasa_depoisDoDuplo": str(contaCasa_depoisDoDuplo),
        "contaBranco_depoisDoDuplo": str(contaBranco_depoisDoDuplo),
        "hora": str(hora).replace(" ", "")
    }

    requests.post(os.getenv('link_api') +
                  '/salva_dados_analisados/2', json=ultimo)

    bot.send_message(mensagem.chat.id, resposta)


@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    dados = requests.get(link + 'dados_analisados/3').json()
    tamanho = int(''.join(map(str, dados['dadosD'])))
    resultados = requests.get(
        link + 'mostra_resultados/' + str(tamanho)).json()
    resultados = pd.DataFrame(resultados)
    detectaBranco = False
    detectaCasa_depoisDoBranco = False
    contaCasa_semDentado = int(
        ''.join(map(str, dados['contaCasa_semDentado'])))
    contaCasa_depoisDoDentado = int(
        ''.join(map(str, dados['contaCasa_depoisDoDentado'])))
    contaBranco_depoisDoDentado = int(
        ''.join(map(str, dados['contaBranco_depoisDoDentado'])))
    brancoDentadoD = int(''.join(map(str, dados['brancoDentadoD'])))
    contaBranco_normal = int(''.join(map(str, dados['contaBranco_normal'])))
    recordJ = int(''.join(map(str, dados['recordJD'])))
    recordB = int(''.join(map(str, dados['recordBD'])))
    hora = dados['hora'][0]
    for i, j in resultados.iterrows():
        if ((j.valores == ' 0 ') and (detectaBranco == False)):
            if (i != 0):
                detectaBranco = True
                contaCasa_semDentado += 1
                contaBranco_normal += 1
                contaCasa_depoisDoDentado += 1
                contaBranco_depoisDoDentado += 1
        elif ((j.valores == ' 0 ') and (detectaBranco == True) and (detectaCasa_depoisDoBranco == False)):
            if (i != 0):
                detectaBranco = False
                contaBranco_normal += 1
                contaCasa_semDentado += 1
                contaCasa_depoisDoDentado += 1
                contaBranco_depoisDoDentado += 1
        elif ((j.valores == ' 0 ') and (detectaBranco == True) and (detectaCasa_depoisDoBranco == True)):
            brancoDentadoD += 1
            detectaBranco = False
            detectaCasa_depoisDoBranco = False
            contaCasa_semDentado -= 1
            contaBranco_normal -= 1
            contaCasa_depoisDoDentado -= 2
            contaBranco_depoisDoDentado -= 1
            hora = j.horas
            if (contaCasa_depoisDoDentado > recordJ):
                recordJ = contaCasa_depoisDoDentado
            if (contaBranco_depoisDoDentado > recordB):
                recordB = contaBranco_depoisDoDentado
            contaCasa_depoisDoDentado = 0
            contaBranco_depoisDoDentado = 0
        if ((j.valores != ' 0 ') and (detectaBranco == True) and (detectaCasa_depoisDoBranco == False)):
            if (i != 0):
                detectaCasa_depoisDoBranco = True
                contaCasa_semDentado += 1
                contaCasa_depoisDoDentado += 1
        elif ((j.valores != ' 0 ') and (detectaCasa_depoisDoBranco == True)):
            if (i != 0):
                detectaCasa_depoisDoBranco = False
                detectaBranco = False
                contaCasa_semDentado += 1
                contaCasa_depoisDoDentado += 1
        elif ((j.valores != ' 0 ') and (detectaBranco == False) and (detectaCasa_depoisDoBranco == False)):
            if (i != 0):
                contaCasa_semDentado += 1
                contaCasa_depoisDoDentado += 1
    if (len(resultados) > 1):
        tamanho -= i

    resposta = "Número de elementos contidos no banco: " + str(abs(tamanho)) + "\nO último branco dentado aconteceu na hora : " + str(hora) + "\nO número de jogadas sem branco dentado é : " + str(
        contaCasa_semDentado) + "\n" + "O número de brancos desde o último branco dentado é : " + str(
            contaBranco_depoisDoDentado) + "\nO número de branco dentado é: " + str(
                brancoDentadoD) + "\nA média de jogadas sem branco dentado é: {:.2f}".format(
                    contaCasa_semDentado/brancoDentadoD) + "\nA média de brancos entre brancos dentados é: {:.2f}".format(
                        contaBranco_normal/brancoDentadoD) + "\nO recorde de jogadas sem brancos dentados é: " + str(
                            recordJ) + "\nO recorde de brancos sem branco dentado é: " + str(recordB)

    ultimo = {
        "dadosD": str(tamanho),
        "contaCasa_semDentado": str(contaCasa_semDentado),
        "contaCasa_depoisDoDentado": str(contaCasa_depoisDoDentado),
        "contaBranco_depoisDoDentado": str(contaBranco_depoisDoDentado),
        "brancoDentadoD": str(brancoDentadoD),
        "contaBranco_normal": str(contaBranco_normal),
        "recordJD": str(recordJ),
        "recordBD": str(recordB),
        "hora": str(hora).replace(" ", "")
    }

    requests.post(os.getenv('link_api') +
                  '/salva_dados_analisados/3', json=ultimo)

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
     Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)


bot.polling()

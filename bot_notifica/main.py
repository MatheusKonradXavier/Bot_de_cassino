import scraperV2
import pandas as pd
import time
import botTelegram
import geraLog
import requests
import pytz
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
timezone = pytz.timezone('America/Sao_Paulo')

def avisaBranco(lista):
    vezesSemBranco = vezesBranco = nRodadas = 0

    for i, j in lista:
        if (int(j.Valores) != 0):
            vezesSemBranco += 1
            if (i != 98):
                vezesBranco = 0
        else:
            if (vezesBranco == 0):
              if(i == 99):
                  nRodadas = vezesSemBranco
              vezesSemBranco = 0
            vezesBranco += 1
        ultimo = {
            "resultado": j.Valores,
            "horaBlaze": j.Horas
        }

    try:
        requests.post(os.environ['link_api']+'salva_resultado', json=ultimo)
    except:
        geraLog.geraLog("ERRO AO SALVAR OS VALORES DO KITBLAZE AS " +
                        datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))

    resultado = True
    if (vezesBranco != 0 and vezesSemBranco != 0):
        resultado = botTelegram.enviarMensagem("🦷🦷🦷 BRANQUINHO DENTADO 🦷🦷🦷")
        try:
            requests.post(os.environ['link_api'] +
                          'salva_brancodentado', json=ultimo)
        except:
            geraLog.geraLog("ERRO AO SALVAR OS VALORES DO KITBLAZE AS " +
                            datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))
    elif (vezesSemBranco != 0):
        if (vezesSemBranco in [50, 60, 70, 80, 90, 100]):
            resultado = botTelegram.enviarMensagem(
                "🚨🚨🚨 HORA DE APOSTAR MERMÃO, " + str(vezesSemBranco) + " RODADAS SEM BRANCO 🚨🚨🚨")
    else:
        if (vezesBranco == 1):
            resultado = botTelegram.enviarMensagem(
                 "🌝🌝🌝 BRANQUINHO NA SUA CARA APÓS "+ str(nRodadas) +" RODADAS 🌝🌝🌝 ")
        else:
            resultado = botTelegram.enviarMensagem(
                "💦💦💦 UUUUUUUIIIIIIIIII BRANQUINHO " + str(vezesBranco) + " VEZES NA SUA CARA 💦💦💦")
            try:
                requests.post(os.environ['link_api'] +
                              'salva_brancoduplo', json=ultimo)
            except:
                geraLog.geraLog("ERRO AO SALVAR OS VALORES DO KITBLAZE AS " +
                                datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))
    if (not resultado):
        geraLog.geraLog("ERRO AO ENVIAR A MENSAGEM AS : " +
                        datetime.now(timezone).strftime('%H:%M'))


def start_notification():
    antigo = pd.DataFrame({
        'Valores': list(),
        'Horas': list(),
        'Id': list()
    })

    atual = pd.DataFrame({
        'Valores': list(),
        'Horas': list(),
        'Id': list()
    })

    botTelegram.enviarMensagem("BOT INICIADO")

    while (True):
        try:
            atual = scraperV2.pegaValoresKitBlaze()
        except:
            geraLog.geraLog("ERRO AO PEGAR OS VALORES DO KITBLAZE AS " +
                            datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))
            atual = antigo.copy()
            time.sleep(1)
        if (not atual.equals(antigo)):
            # diferentes = pd.concat([atual,antigo]).drop_duplicates(keep=False)
            antigo = atual.copy()
            avisaBranco(atual.iterrows())
            time.sleep(25)
        time.sleep(1)


if (__name__ == '__main__'):
    start_notification()

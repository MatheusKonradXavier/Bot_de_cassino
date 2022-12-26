import threading
import os

def inicia_programa(nome_arquivo):
    os.system('python3 -u {}'.format(nome_arquivo))

if __name__ == "__main__":
    cwd = os.getcwd()
    arquivos = [cwd+'/api_cassinagem/main.py',cwd+'/bot_notifica/main.py', cwd+'/bot_infos_cassinagem/main.py']

    processos = []
    for arquivo in arquivos:
        processos.append(threading.Thread(target=inicia_programa, args=(arquivo,)))

    for processo in processos:
        processo.start()
import pandas as pd
import requests
import os
import time
import telebot
from dotenv import load_dotenv

load_dotenv()
CHAVE_BOT = os.getenv('bot_infos')
link = os.getenv('link_api')
bot = telebot.TeleBot(CHAVE_BOT)

@bot.message_handler(commands=["op1"])
def op1(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeSemBranco = vezesSemBranco =  soma = nBrancos = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemBranco += 1
        else :
            if(recordeSemBranco < vezesSemBranco):
                recordeSemBranco = vezesSemBranco 
            soma+=vezesSemBranco
            nBrancos+=1
            vezesSemBranco = 0

    resposta = ("Número atual de jogadas sem branco " + str(vezesSemBranco) + 
                "\nMédia de jogadas entre brancos " + str(soma//nBrancos) +
                "\nRecorde de jogadas entre brancos " + str(recordeSemBranco+1))

    bot.send_message(mensagem.chat.id, resposta)

@bot.message_handler(commands=["op2"])
def op2(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeSemDuplo = recordeBrancoEntreDuplos = jogadasBranco = 0
    jogadas = nDuplos =  contBranco = soma = somaB = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            jogadas+=1
            contBranco=0
        else :
            if(contBranco == 1):
                if(jogadasBranco-1 > recordeBrancoEntreDuplos):
                    recordeBrancoEntreDuplos = jogadasBranco-1
                if(jogadas-1 > recordeSemDuplo):
                    recordeSemDuplo = jogadas-1          
                somaB+=jogadasBranco-1
                soma+=jogadas-1
                nDuplos+=1
                jogadasBranco = jogadas = 0
            else:
                jogadasBranco+=1
                jogadas+=1
                contBranco=1

    resposta = ("Recorde de jogadas entre duplos " + str(recordeSemDuplo)+ 
                "\nRecorde de brancos entre duplos " + str(recordeBrancoEntreDuplos)+
                "\nMédia de brancos entre duplos " + str(somaB//nDuplos)+ 
                "\nMédia de jogadas entre duplos " + str(soma//nDuplos)+
                "\nNúmero atual de jogadas sem duplos " + str(jogadas)+ 
                "\nNúmero atual de brancos sem duplos " + str(jogadasBranco))
    
    bot.send_message(mensagem.chat.id, resposta)

@bot.message_handler(commands=["op3"])
def op3(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeSemDentado = recordeSemBrancos = jogadasBrancos = 0
    jogadas = vezesSemBranco = contBranco = 0
    soma = somaB = nDentados = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemBranco +=1
            jogadas+=1
            if(contBranco != 1 or vezesSemBranco != 1):
                contBranco = 0
        else :
            if(vezesSemBranco != 1):
                vezesSemBranco = 0
                contBranco=1
                jogadas+=1
                jogadasBrancos +=1
            elif(contBranco==1):
                if(jogadasBrancos > recordeSemBrancos):
                    recordeSemBrancos = jogadasBrancos
                if(jogadas > recordeSemDentado):
                    recordeSemDentado = jogadas
                nDentados+=1
                somaB +=jogadasBrancos
                soma+=jogadas
                jogadas = jogadasBrancos = vezesSemBranco = 0

    resposta = ("Recorde de jogadas entre dentados " +str(recordeSemDentado)+ 
                "\nRecorde de brancos entre dentados " +str(recordeSemBrancos)+ 
                "\nMédia de brancos entre dentados " +str(somaB//nDentados)+ 
                "\nMédia de jogadas entre dentados " +str(soma//nDentados)+ 
                "\nNúmero atual de jogadas sem dentado " +str(jogadas)+ 
                "\nNúmero atual de brancos sem dentado " +str(jogadasBrancos))

    bot.send_message(mensagem.chat.id, resposta)

@bot.message_handler(commands=["op4"])
def op4(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()

    recordeBrancosSN = recordeJogadasSN = vezesSemBranco = 0
    contBranco = somaJSN = somaBSN = vezesSN =  0
    jogadas = jogadasBranco = 0

    for i in pd.DataFrame(lista)['valores'] :
        if( not i == ' 0 '):
            vezesSemBranco+=1
            jogadas+=1
            if(contBranco != 1 or vezesSemBranco != 1):
                contBranco = 0
        else :
            if(contBranco==1):
                if(jogadasBranco-1 > recordeBrancosSN):
                    recordeBrancosSN = jogadasBranco-1
                if(jogadas-1 > recordeJogadasSN):
                    recordeJogadasSN = jogadas-1
                somaBSN += jogadasBranco-1
                somaJSN += jogadas-1
                vezesSN +=1
                jogadasBranco = jogadas =  0
            else :
                vezesSemBranco = 0
                contBranco=1
                jogadas+=1
                jogadasBranco+=1

    resposta = ("Recorde de jogadas entre duplos ou dentados " +str(recordeJogadasSN) +
                "\nRecorde de brancos entre duplos ou dentados " +str(recordeBrancosSN)+ 
                "\nA média de brancos entre duplos ou dentados " +str(somaBSN//vezesSN)+
                "\nA média de jogadas entre duplos ou dentados " +str(somaJSN//vezesSN)+
                "\nNúmero atual de jogadas sem duplos ou dentados " +str(jogadas)+
                "\nNúmero atual de brancos sem duplos ou dentados " +str(jogadasBranco))

    bot.send_message(mensagem.chat.id, resposta)

@bot.message_handler(commands=["op5"])
def op5(mensagem):
    lista = requests.get(
          link + '/mostra_resultados/' + str(0)).json()
    
    if(mensagem.json['text'].strip()=="/op5"):
        return bot.send_message(mensagem.chat.id, "Digite /op5  -valorApostaInicial-jogadasTotais-bancaInicial-quandoComeca")

    if(len(mensagem.json['text'].split("-"))<5):
       #print(len(mensagem.json['text'].strip().split("-")))
       return bot.send_message(mensagem.chat.id, "Erro nos parâmetros")

    inputs = list()
    try:
        for i in mensagem.json['text'].split("-"):
            if(i.strip()!="/op5"):
                inputs.append(float(i))
    except:
        return bot.send_message(mensagem.chat.id, "Erro nos parâmetros")
    
    apostaInicial,jogadasTotais,bancaInicial,comeca = inputs
    if(comeca<0 or jogadasTotais<0 or apostaInicial<1.10 or bancaInicial<0):
        return bot.send_message(mensagem.chat.id, "Erro nos parâmetros")
    jogadasIniciais = 14
    recordebaixo = bancaInicial
    recordealtura = cont = 0
    a = list()

    recordeSemBranco = vezesSemBranco =  soma = nBrancos = 0
    listaVezes = list()

    for i in pd.DataFrame(lista)['valores']:
        if( not i == ' 0 '):
            vezesSemBranco += 1
        else :
            if(recordeSemBranco < vezesSemBranco):
                recordeSemBranco = vezesSemBranco 
            listaVezes.append(vezesSemBranco)
            soma+=vezesSemBranco
            nBrancos+=1
            vezesSemBranco = 0

    def martinGale(valorInicial,jogadasIniciais,jogadasTotais,crash,comeca):
        if(crash<comeca):
            return 0.0
        crash+=1
        crash-=comeca
        if(jogadasTotais>=crash):
            if(jogadasIniciais<14):
                return((valorInicial*14 )-(valorInicial*(crash)))

            if(crash<=jogadasIniciais):
                aux = jogadasIniciais -crash
                return ((aux*valorInicial))
        
            aux = crash-jogadasIniciais
            vezes2= (aux-1)//(jogadasIniciais//2)
            valorAposta = (2**(vezes2+1))*valorInicial
            
            if(crash%(jogadasIniciais//2)==0):
                return 0.0

            valor = crash%(jogadasIniciais//2)
            if(round(valor)==0):
                valor = 1
            return ((valorAposta*(jogadasIniciais//2))-(valorAposta*(valor)))
        
        else:
            if(jogadasTotais<=14):
                return (-(jogadasTotais*valorInicial))
            aux = jogadasTotais-jogadasIniciais
            vezes2= (aux-1)//(jogadasIniciais//2)
            valorAposta = (2**(vezes2+1))*valorInicial

            valor = jogadasTotais%(jogadasIniciais//2)
            if(round(valor)==0):
                valor = jogadasIniciais//2

            return -((valorAposta*(jogadasIniciais//2))+(valorAposta*(valor)))    

    if((martinGale(apostaInicial,jogadasIniciais,jogadasTotais,jogadasTotais+comeca,comeca)*-1)>bancaInicial):
      return bot.send_message(mensagem.chat.id, ("Lhe falta banca irmão, pra esse tanto de jogada tu precisa de " + str(round((martinGale(apostaInicial,jogadasIniciais,jogadasTotais,jogadasTotais+comeca,comeca)*-1),2))))
    
    #print(martinGale(apostaInicial,jogadasIniciais,jogadasTotais,2,comeca))
    #print(listaVezes)
    for i in listaVezes:
        cont+=1
        if(bancaInicial>recordealtura):
            recordealtura = bancaInicial
        if(bancaInicial<recordebaixo):
            recordebaixo = bancaInicial
        bancaInicial+=martinGale(apostaInicial,jogadasIniciais,jogadasTotais,i,comeca)
        if(martinGale(apostaInicial,jogadasIniciais,jogadasTotais,i,comeca)!=0.0):
            a.append(bancaInicial)
        """ if(martinGale(apostaInicial,jogadasIniciais,jogadasTotais,i,comeca)>0):
            print("Número de rodadas",i+1)
            print("LUCRO OU DERROTA ",round(martinGale(apostaInicial,jogadasIniciais,jogadasTotais,i,comeca),2))
            print("BANCA ", round(bancaInicial,2))
            print("\n") """
        if(bancaInicial<(martinGale(apostaInicial,jogadasIniciais,jogadasTotais,jogadasTotais+comeca,comeca)*-1)):
            if(bancaInicial>recordealtura):
                recordealtura = bancaInicial
            if(bancaInicial<recordebaixo):
                recordebaixo = bancaInicial
            break

    #print(pd.DataFrame(lista).loc[:60000])
    #plt.clf()
    #plt.plot(a)
    #plt.savefig('testplot.png')
    #plt.clf()
    resposta = "Resultado final:" if len(listaVezes)==cont else ("Falido após "+str(cont)+" jogadas")
    resposta += ("\nAs suas jogadas totais custavam " +str(round((martinGale(apostaInicial,jogadasIniciais,jogadasTotais,jogadasTotais+comeca,comeca)*-1),2))+
                "\nBanca final "+ str(round(bancaInicial,2)) +
                "\nBanca mais alta detectada "+ str(round(recordealtura,2)) +
                "\nBanca mais baixa detectada "+ str(round(recordebaixo,2)))

    bot.send_message(mensagem.chat.id, resposta)
    #bot.send_photo(mensagem.chat.id, photo=open('testplot.png','rb'))
    #time.sleep(1)
    #plt.clf()
    #os.remove('testplot.png')

def verificar(mensagem):
    """ print(mensagem)
    for i in mensagem.__dict__:
        print(i, " : ", mensagem.__dict__[i]) """
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     /op1 Informações sobre os brancos
     /op2 Informações sobre os brancos duplos
     /op3 Informações sobre os brancos dentados
     /op4 Informações sobre os dentados e duplos juntos"""
    bot.reply_to(mensagem, texto)

def iniciaBot(bot):
    try:
        bot.polling()
    except:
        time.sleep(2)
        iniciaBot(bot)

if __name__ == "__main__":
    iniciaBot(bot)
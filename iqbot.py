from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import sys

def muda_dir(dir):
    if dir == 'put':
        return 'call'
    return 'put'

def stop(lucro, gain):
    if stop_loss <= 0:
        print('Stop Loss batido!')
        sys.exit()

    if lucro >= float(abs(gain)):
        print('Stop Gain Batido!')
        sys.exit()

BOT = IQ_Option('rafaelmafr4@hotmail.com', 'rafa1988')
BOT.connect()
BOT.change_balance('PRACTICE')  # PRACTICE / REAL
OPERACAO = 1 # 1 - Digital\n  2 - Binaria
TIPO_MHI = 1 # 1 - Minoria\n  2 - Maioria\
PAR = 'EURUSD' #PARIDADE para operar
dir = 'put'
multiplicador = 2 #valor da multiplicacao
valor_entrada = 2 #valor entrada
valor_operacao = valor_entrada
stop_loss = 100
stop_gain = 10
lucro = 0


if BOT.check_connect():
    print(' Conectado com sucesso!')

else:
    print(' Erro ao conectar')
    input('\n\n Aperte enter para sair')
    sys.exit()

while True:
    minutos = float(((datetime.now()).strftime('%S')))
    entrar = True if minutos >= 58 and minutos <= 59 else False
    print('Hora de entrar?', entrar, '/ Minutos:', minutos)

    if entrar:
        while True:
            print('\n\nIniciando operação!')
            status, id = BOT.buy_digital_spot(PAR, valor_operacao, dir, 1) if OPERACAO == 1 else BOT.buy(
            valor_operacao, PAR, dir, 1)
            if status:
                while True:
                    try:
                        status, valor = BOT.check_win_digital_v2(id) if OPERACAO == 1 else BOT.check_win_v3(id)

                    except:
                        status = True
                        valor = 0
                    if status:
                        valor = valor if valor > 0 else float('-' + str(abs(valor_operacao)))
                        lucro += round(valor, 2)

                        print('Resultado operação: ', end='')
                        print('WIN /' if valor > 0 else 'LOSS /', round(valor, 2), '/', round(lucro, 2))
                        if valor < 0:
                            dir = muda_dir(dir)
                            valor_operacao *= multiplicador
                            stop_loss += round(valor, 2)
                        else:
                            valor_operacao = valor_entrada
                        stop(lucro,stop_gain)
                        break

            else:
                print('\nERRO AO REALIZAR OPERAÇÃO\n\n')

    time.sleep(0.5)
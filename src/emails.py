import email.message
import configparser
import smtplib
import os
import sys

caminho_exe = os.path.abspath(sys.argv[0])
caminho_parameters_ini = os.path.dirname(caminho_exe) + r"\parameters.ini"

ini = configparser.ConfigParser()
ini.read(caminho_parameters_ini)

email_remetente = ini.get('EMAIL', 'EnderecoRemetente')
email_destinatario = ini.get('EMAIL', 'EnderecoDestinatario')
senha = ini.get('EMAIL', 'Senha')


def envia_email(titulo, mensagem):
    msg = email.message.Message()

    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg['Subject'] = titulo

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(mensagem)

    smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()

    smtp.login(msg['From'], senha)
    smtp.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    smtp.quit()

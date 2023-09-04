from src.utils.utils import *
import email.message
import configparser
import smtplib


class Email:

    # Envia um email com os dados passados
    @staticmethod
    def envia_email(remetente, destinatario, senha, titulo, mensagem):
        try:
            msg = email.message.Message()

            msg['From'] = remetente
            msg['To'] = destinatario
            msg['Subject'] = titulo

            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(mensagem)

            smtp = smtplib.SMTP('smtp.gmail.com: 587')
            smtp.starttls()

            smtp.login(msg['From'], senha)
            smtp.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

            smtp.quit()
        except Exception as e:
            Utils.gera_log_erro("Erro ao enviar o email! Log gerado em: ", str(e), sys._getframe().f_code.co_name)
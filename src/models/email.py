import email.message
import configparser
import smtplib


class Email:

    @staticmethod
    def envia_email(remetente, destinatario, senha, titulo, mensagem):
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

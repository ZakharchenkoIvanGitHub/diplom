import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import yaml
import datetime


def send_message_to_email(sender_email, recipient_email, password, filename):
    """
    Функция формирования и отправки письма с отчетом о тестировании на электронную почту
    :param sender_email: электронная почта отправителя
    :param recipient_email: электронная почта получателя
    :param password: пароль почты отправителя
    :param filename: файл отчета
    """
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    time_format = "%Y-%m-%d %H:%M:%S"
    subject = f"report {now:{time_format}}"
    message_body = 'Отчет о тестировании.'

    # Создание объекта MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Добавление текста сообщения
    msg.attach(MIMEText(message_body, 'plain'))

    # Добавляем файл во вложение
    try:
        with open(filename, 'rb') as f:
            attach = MIMEBase('application', 'octet-stream')
            attach.set_payload(f.read())
            encoders.encode_base64(attach)
            attach.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(attach)
    except Exception as e:
        logging.exception(f"File reading error {e}")
        msg.attach(MIMEText("Файл отчета не был найден", 'plain'))

    # Настройка SMTP-сервера Mail.ru
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587  # Порт для шифрованного соединения (TLS)

    try:
        # Создание объекта SMTP и установка соединения
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Включение шифрованного соединения

        # Вход в почтовый аккаунт
        server.login(sender_email, password)

        # Отправка письма
        server.sendmail(sender_email, recipient_email, msg.as_string())
        logging.info("Test_1 Starting")
    except Exception as e:
        logging.exception(f"Exception of sending a report {e}")
    finally:
        # Завершение соединения с SMTP-сервером
        server.quit()


def send_message_default():
    with open("testdata.yaml") as f:
        testdata = yaml.safe_load(f)
    send_message_to_email(testdata['fromaddr_report'],
                          testdata['toaddr_report'],
                          testdata['mail_password'],
                          "report.html")


if __name__ == "__main__":
    send_message_default()

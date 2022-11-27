import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def connect_to_smtp():

    serv = smtplib.SMTP('smtp.yandex.ru', 587)
    serv.starttls()
    serv.ehlo()
    serv.login(os.environ.get('FROM_ADDR'), os.environ.get('FROM_ADDR_PASSWORD'))
    return serv


def send_email(serv, info, is_creator):
    from_addr = os.environ.get('FROM_ADDR')

    msg = MIMEMultipart()
    msg['From'] = from_addr
    if is_creator is True:
        msg['To'] = info['email']
        msg['Subject'] = 'Создание события'

        body = f"Здравствуйте, {info['first_name']} {info['last_name']} \n" \
               f"Вы успешно создали событие под названием {info['name_event']}. \n" \
               f"Место проведения: {info['place_event']} \n" \
               f"Дата проведения: {info['date_event']} \n" \
               f"Время проведения: {info['time_event']} \n\n" \
               f"В дальнейшем вам будет приходить сообщения с информацией о тех, кто записался. \n\n\n" \
               f"С уважением, служба поддержки {from_addr}"

        msg.attach(MIMEText(body, 'plain'))

        serv.send_message(msg)

        serv.quit()

# if __name__ == '__main__':
#     send_email('pm93.galstyan@gmail.com', is_creator=True)

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


def send_email(serv, info, is_creator, participant=None):
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
    else:
        # Отправляем сообщение тому, кто записался
        msg['To'] = participant['email']
        msg['Subject'] = 'Успешная запись'

        body = f"Здравствуйте, {participant['first_name']} {participant['last_name']}\n" \
               f"Вы успешно записались на событие {info[0]}\n" \
               f"Ссылка на Google Sheet: {info[1]}\n\n\n" \
               f"С уважением, служба поддержки {from_addr}"

        msg.attach(MIMEText(body, 'plain'))
        serv.send_message(msg)

        # Отправляем сообщение создателю события о том, кто записался
        msg_second = MIMEMultipart()
        msg_second['From'] = from_addr
        msg_second['To'] = info[4]
        msg_second['Subject'] = 'Запись на ваше событие'

        body = f"Здравствуйте,\n" \
               f"На созданное вами событие '{info[0]}' записался новый участник.\n" \
               f"Имя участника: {participant['first_name']}\n" \
               f"Фамилия участника: {participant['last_name']}\n" \
               f"Электронная почта участника: {participant['email']} \n\n" \
               f"С уважением, служба поддержки {from_addr}"

        msg_second.attach(MIMEText(body, 'plain'))
        serv.send_message(msg_second)

        serv.quit()


# if __name__ == '__main__':
#     send_email('pm93.galstyan@gmail.com', is_creator=True)

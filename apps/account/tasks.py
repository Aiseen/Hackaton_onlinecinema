import time

from django.core.mail import send_mail

from cinema.celery import app


@app.task
def spam_email():
    # time.sleep(1)
    full_link = f'Привет!'

    send_mail(
        'Кино от Айсена',
        full_link,
        'sagynbaevajsen@gmail.com',
        ['sagynbaevajsen@gmail.com']
    )

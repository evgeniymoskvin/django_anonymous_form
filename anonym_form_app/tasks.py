import datetime
import os
import time
from django.conf import settings
from django.core.mail import EmailMessage

from django_anonymous_form.celery import app
from anonym_form_app.models import SubdivisionModel, QuestionModel


@app.task()
def celery_send_email_to_subdivision_responsible(task_id):
    task = QuestionModel.objects.get(id=task_id)
    try:
        email_subdivision_responsible = EmailMessage(f'Новое обращение в {task.subdivision.subdivision_name} №{task.id}',
                                                     f'Текст обращения: \n {task.question} \n Срочность: {task.get_important_of_question_display()} \n Тип: {task.get_type_of_question_display()}',
                                                     to=[task.subdivision.subdivision_responsible.user.email])
        email_subdivision_responsible.send()
        print(f'Письмо с обращением №{task.id} отправлено {task.subdivision.subdivision_responsible.user.email}')
    except Exception as e:
        print(f'Письмо не отправлено. Ошибка: {e}')


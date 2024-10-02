from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _


class SubdivisionModel(models.Model):
    """Таблица, кому направляется вопрос"""
    who_answer = models.CharField(verbose_name="Ответственное подразделение", max_length=250)

    class Meta:
        verbose_name = _('ответственное подразделение')
        verbose_name_plural = _('ответственные подразделения')

    def __str__(self):
        return f'{self.who_answer}'


class QuestionModel(models.Model):
    """Таблица вопросов"""

    class ImportantStatusChoice(models.IntegerChoices):
        """Срочность"""
        LOWER = 1, _('Низкая')
        ACTUAL = 2, _('Средняя')
        HIGH = 3, _('Высокая')

    class TypeOfQuestionChoice(models.IntegerChoices):
        """Тип жалобы/предложения"""
        COMPLAINT = 1, _('Жалоба')
        OFFER = 2, _('Предложение')

    important_of_question = models.IntegerField(verbose_name="Важность обращения", choices=ImportantStatusChoice.choices, default=2)
    type_of_question = models.IntegerField(verbose_name="Тип обращения", choices=TypeOfQuestionChoice.choices, default=2)
    subdivision = models.ForeignKey(SubdivisionModel, verbose_name="Ответственное подразделение", on_delete=models.PROTECT, null=True, blank=True)
    question = models.TextField(verbose_name="Текст обращения", max_length=5000)
    date_add = models.DateField(verbose_name='Дата подачи', auto_now_add=True, null=False)
    done_flag = models.BooleanField(verbose_name="Отработано", default=False)
    done_date = models.DateField(verbose_name='Дата выполнения', null=True)

    class Meta:
        verbose_name = _('обращение')
        verbose_name_plural = _('обращения')

    def __str__(self):
        return f'{self.question[:50]} - {self.done_flag}'


from os import path

from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractUser


class JobTitleModel(models.Model):
    """ Таблица должностей """

    job_title = models.CharField("Должность", max_length=200)

    class Meta:
        verbose_name = _("должность")
        verbose_name_plural = _("должности")
        managed = False
        db_table = 'ToDo_tasks_jobtitlemodel'

    def __str__(self):
        return f'{self.job_title}'


class CityDepModel(models.Model):
    """Таблица городов"""
    city = models.CharField(verbose_name="Город", max_length=100)
    name_dep = models.CharField(verbose_name="Наименование организации", max_length=350)

    class Meta:
        managed = False
        verbose_name = _("город/организация")
        verbose_name_plural = _("города/организации")
        db_table = 'admin_panel_app_citydepmodel'

    def __str__(self):
        return f'{self.city} - {self.name_dep}'


class GroupDepartmentModel(models.Model):
    """Таблица управлений"""
    group_dep_abr = models.CharField("Сокращенное название управления", max_length=10)
    group_dep_name = models.CharField("Полное название управления", max_length=250)
    city_dep = models.ForeignKey(CityDepModel, verbose_name="Город", on_delete=models.SET_NULL, null=True, blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.group_dep_abr}, {self.group_dep_name}'

    class Meta:
        verbose_name = _("управление")
        verbose_name_plural = _("управления")
        managed = False
        db_table = 'ToDo_tasks_groupdepartmentmodel'


class CommandNumberModel(models.Model):
    """Таблица отделов"""
    command_number = models.IntegerField("Номер отдела/Сокращение")
    command_name = models.CharField("Наименование отдела", max_length=150)
    department = models.ForeignKey(GroupDepartmentModel, verbose_name="Управление", on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.command_number}, {self.command_name}'

    class Meta:
        verbose_name = _("номер отдела")
        verbose_name_plural = _("номера отделов")
        managed = False
        db_table = 'ToDo_tasks_commandnumbermodel'


class EmployeeModel(models.Model):
    """Таблица сотрудников"""
    user = models.OneToOneField(User, models.PROTECT, verbose_name="Пользователь", related_name='phonebook_emp_user')
    last_name = models.CharField("Фамилия", max_length=150)
    first_name = models.CharField("Имя", max_length=150)
    middle_name = models.CharField("Отчество", max_length=150)
    personnel_number = models.CharField("Табельный номер", max_length=20, null=True, default=None)
    job_title = models.ForeignKey(JobTitleModel, on_delete=models.PROTECT, null=True, verbose_name="Должность")
    department = models.ForeignKey(CommandNumberModel, on_delete=models.PROTECT, null=True, verbose_name="№ отдела")
    user_phone = models.IntegerField("№ телефона внутренний", null=True, default=None, blank=True)
    department_group = models.ForeignKey(GroupDepartmentModel, on_delete=models.SET_NULL, default=None, null=True,
                                         verbose_name="Управление")
    right_to_sign = models.BooleanField(verbose_name="Право подписывать задания", default=False)
    check_edit = models.BooleanField("Возможность редактирования задания", default=True)
    can_make_task = models.BooleanField("Возможность выдавать задания", default=True)
    cpe_flag = models.BooleanField("Флаг ГИП (техническая метка)", default=False)
    mailing_list_check = models.BooleanField("Получать рассылку", default=True)
    work_status = models.BooleanField("Сотрудник работает", default=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        managed = False
        verbose_name = _("сотрудник")
        verbose_name_plural = _("сотрудники")
        db_table = 'ToDo_tasks_employee'


def upload_to(instance, filename):
    name_to_path = str(instance.emp.id)
    new_path = path.join('files',
                         # "media", filename)
                         name_to_path,
                         filename)
    print(new_path)
    return new_path


class MoreDetailsEmployeeModel(models.Model):
    """Дополнительная информация по сотрудникам"""
    emp = models.OneToOneField(EmployeeModel, models.CASCADE, verbose_name="Пользователь")
    photo = models.ImageField(verbose_name="Файл", null=True, blank=True,
                              upload_to=upload_to)
    outside_email = models.EmailField(verbose_name="Внешняя почта", null=True, blank=True)
    mobile_phone = models.CharField(verbose_name="Мобильный телефон", null=True, blank=True, max_length=30)
    date_birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    room = models.CharField(verbose_name="Номер комнаты", null=True, blank=True, max_length=30)
    date_birthday_show = models.BooleanField(verbose_name="Отображать день рождения", default=False, null=True)
    city_dep = models.ForeignKey(CityDepModel, on_delete=models.PROTECT, null=True, verbose_name="Город/Подразделение",
                                 blank=True)
    send_email_salary_blank = models.BooleanField(verbose_name="Отсылать расчетный листок", default=False)

    class Meta:
        managed = False
        verbose_name = _("дополнительная информация по сотруднику")
        verbose_name_plural = _("дополнительная информация по сотрудникам")
        db_table = 'admin_panel_app_moredetailsemployeemodel'

    def __str__(self):
        return f'{self.emp}'


class SubdivisionModel(models.Model):
    """Таблица, кому направляется вопрос"""
    subdivision_name = models.CharField(verbose_name="Ответственное подразделение", max_length=260)
    subdivision_responsible = models.ForeignKey(EmployeeModel, verbose_name="Кому присылать email",
                                                on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('ответственное подразделение')
        verbose_name_plural = _('ответственные подразделения')

    def __str__(self):
        return f'{self.subdivision_name} ({self.subdivision_responsible})'


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

    class StatusChoice(models.IntegerChoices):
        """Тип жалобы/предложения"""
        INBOX = 0, _('Поступило')
        IN_WORK = 1, _('В работе')
        DONE = 2, _('Выполнено')

    important_of_question = models.IntegerField(verbose_name="Важность обращения",
                                                choices=ImportantStatusChoice.choices, default=2)
    type_of_question = models.IntegerField(verbose_name="Тип обращения", choices=TypeOfQuestionChoice.choices,
                                           default=2)
    subdivision = models.ForeignKey(SubdivisionModel, verbose_name="Ответственное подразделение",
                                    on_delete=models.PROTECT, null=True, blank=True)
    question = models.TextField(verbose_name="Текст обращения", max_length=5100)
    date_add = models.DateField(verbose_name='Дата подачи', auto_now_add=True, null=False)
    done_flag = models.BooleanField(verbose_name="Отработано", default=False)
    done_date = models.DateField(verbose_name='Дата выполнения', null=True)
    status = models.IntegerField(verbose_name="Статус обращения", choices=StatusChoice.choices,
                                 default=0)

    class Meta:
        verbose_name = _('обращение')
        verbose_name_plural = _('обращения')

    def __str__(self):
        return f'{self.question[:60]} - {self.done_flag}'

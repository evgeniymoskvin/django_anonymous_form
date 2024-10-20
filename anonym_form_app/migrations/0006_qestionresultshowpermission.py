# Generated by Django 5.1.1 on 2024-10-03 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anonym_form_app', '0005_alter_questionmodel_done_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QestionResultShowPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anonym_form_app.employeemodel', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'сотрудник имеющий доступ',
                'verbose_name_plural': 'сотрудники имеющие доступ',
            },
        ),
    ]

from django.contrib import admin
from .models import SubdivisionModel, EmployeeModel, QuestionModel, QestionResultShowPermission


# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["last_name", "first_name", "middle_name"]
    search_fields = ["last_name", "first_name", "middle_name", "personnel_number", "user_phone"]
    list_filter = ("department_group__city_dep__city", "department_group__group_dep_abr", "department__command_number")

class QuestionAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_filter = ("important_of_question", "type_of_question", "subdivision", "status")

admin.site.register(SubdivisionModel)
admin.site.register(EmployeeModel, EmployeeAdmin)
admin.site.register(QuestionModel, QuestionAdmin)
admin.site.register(QestionResultShowPermission)

from django.contrib import admin
from .models import SubdivisionModel, EmployeeModel


# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["last_name", "first_name", "middle_name"]
    search_fields = ["last_name", "first_name", "middle_name", "personnel_number", "user_phone"]
    list_filter = ("department_group__city_dep__city", "department_group__group_dep_abr", "department__command_number")


admin.site.register(SubdivisionModel)
admin.site.register(EmployeeModel, EmployeeAdmin)

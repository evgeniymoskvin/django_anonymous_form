import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import SubdivisionModel, QuestionModel, QestionResultShowPermission


# Create your views here.

class IndexView(View):
    """
    Главная страница проекта
    """

    def get(self, request):
        content = {
            'subdivisions': SubdivisionModel.objects.all()
        }
        return render(request, 'anonym_form_app/index.html', content)

    def post(self, request):
        print(f'request.POST: {request.POST}')
        new_question = QuestionModel()
        new_question.subdivision_id = int(request.POST['subdivision_id'])
        new_question.important_of_question = int(request.POST['important_of_question'])
        new_question.type_of_question = int(request.POST['type_of_question'])
        new_question.question = request.POST['question_text']
        new_question.save()
        content = {
            'new_question': new_question
        }
        return render(request, 'anonym_form_app/ajax/send_question_done.html', content)


class AnalyticView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_exist = QestionResultShowPermission.objects.filter(emp__user=request.user).exists()
        if user_exist is False:
            content = {}
            return render(request, 'anonym_form_app/error_permission.html', content)
        tasks = QuestionModel.objects.all().filter(done_flag=False).order_by('-id')
        content = {
            'tasks': tasks,
            'subdivisions': SubdivisionModel.objects.all()
        }
        return render(request, 'anonym_form_app/analytic.html', content)


class AnalyticAllView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_exist = QestionResultShowPermission.objects.filter(emp__user=request.user).exists()
        if user_exist is False:
            content = {}
            return render(request, 'anonym_form_app/error_permission.html', content)
        tasks = QuestionModel.objects.all().order_by('-id')
        content = {
            'tasks': tasks,
            'subdivisions': SubdivisionModel.objects.all()
        }
        return render(request, 'anonym_form_app/analytic_all.html', content)


class GetTasksWithFilters(View):
    def get(self, request):
        subdivision_id = request.GET['subdivision_id']
        important_of_question = request.GET['important_of_question']
        type_of_question = request.GET['type_of_question']
        status_id = request.GET['status_id']
        tasks = QuestionModel.objects.all().filter(done_flag=False).filter().order_by('-id')
        if subdivision_id:
            tasks = tasks.filter(subdivision_id=subdivision_id)
        if important_of_question:
            tasks = tasks.filter(important_of_question=important_of_question)
        if type_of_question:
            tasks = tasks.filter(type_of_question=type_of_question)
        if status_id:
            tasks = tasks.filter(status=status_id)
        content = {
            'tasks': tasks,
        }
        return render(request, 'anonym_form_app/ajax/tasks_in_work.html', content)


class GetAllTasksWithFilters(View):
    def get(self, request):
        subdivision_id = request.GET['subdivision_id']
        important_of_question = request.GET['important_of_question']
        type_of_question = request.GET['type_of_question']
        status_id = request.GET['status_id']
        tasks = QuestionModel.objects.all().order_by('-id')
        if subdivision_id:
            tasks = tasks.filter(subdivision_id=subdivision_id)
        if important_of_question:
            tasks = tasks.filter(important_of_question=important_of_question)
        if type_of_question:
            tasks = tasks.filter(type_of_question=type_of_question)
        if status_id:
            tasks = tasks.filter(status=status_id)
        content = {
            'tasks': tasks,
        }
        return render(request, 'anonym_form_app/ajax/tasks_all.html', content)


class ModalDetailView(View):
    def get(self, request):
        task_id = request.GET['task_id']
        print(task_id)
        content = {
            'task': QuestionModel.objects.get(id=task_id)
        }
        return render(request, 'anonym_form_app/ajax/detail_modal.html', content)

    def post(self, request):
        print(request.POST)
        task_id = int(request.POST['obj_id_for_change_status'])
        task_to_change_status = QuestionModel.objects.get(id=task_id)
        task_to_change_status.status = request.POST['status_id']
        task_to_change_status.description_canceled = request.POST['WhyCancel']
        if int(request.POST['status_id']) == 2:
            task_to_change_status.start_work_date = datetime.datetime.now()
        elif int(request.POST['status_id']) == 0 or int(request.POST['status_id']) == 3:
            task_to_change_status.done_flag = True
            task_to_change_status.done_date = datetime.datetime.now()
        task_to_change_status.save()
        return HttpResponse(status=200)


class BlankDetailView(View):
    def get(self, request, pk):
        content = {
            'task': QuestionModel.objects.get(id=pk)
        }
        return render(request, 'anonym_form_app/blank_page.html', content)

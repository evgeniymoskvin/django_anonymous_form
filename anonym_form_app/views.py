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


class GetTasksWithFilters(View):
    def get(self, request):
        subdivision_id = request.GET['subdivision_id']
        important_of_question = request.GET['important_of_question']
        type_of_question = request.GET['type_of_question']
        tasks = QuestionModel.objects.all().filter(done_flag=False).filter().order_by('-id')
        if subdivision_id:
            tasks = tasks.filter(subdivision_id=subdivision_id)
        if important_of_question:
            tasks = tasks.filter(important_of_question=important_of_question)
        if type_of_question:
            tasks = tasks.filter(type_of_question=type_of_question)
        content = {
            'tasks': tasks,
        }
        return render(request, 'anonym_form_app/ajax/tasks_in_work.html', content)

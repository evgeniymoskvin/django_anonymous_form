from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import SubdivisionModel, QuestionModel

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
        return HttpResponse(status=200)

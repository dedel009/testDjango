# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question
from django.core.paginator import Paginator


#질문 목록 화면
def main(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


#질문 상세보기 화면
def detail(request, qid):
    question = get_object_or_404(Question, pk=qid)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


#답변 추가
@login_required(login_url='common:login')
def answer_create(request, qid):
    question = get_object_or_404(Question, pk=qid)
    # question.answers.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('pybo:detail', qid=qid)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.save()
            return redirect('pybo:detail', qid=qid)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


#질문 추가
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            print("question 객체 :", question)
            question.author = request.user
            question.save()
            return redirect('pybo:main')
    else:
        form = QuestionForm()
        print("저장 하기 화면")
    return render(request, 'pybo/question_form.html', {'form': form})

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


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


#질문 수정
@login_required(login_url='common:login')
def question_modify(request, qid):
    question = get_object_or_404(Question, pk=qid)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', qid=qid)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', qid=qid)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'qid': qid}
    return render(request, 'pybo/question_form.html', context)


#질문 삭제
@login_required(login_url='common:login')
def question_delete(request, qid):
    question = get_object_or_404(Question, pk=qid)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', qid=qid)
    question.delete()
    return redirect('pybo:main')

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


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


#답변 수정
@login_required(login_url='common:login')
def answer_modify(request, aid):
    answer = get_object_or_404(Answer, pk=aid)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', qid=answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', qid=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form': form, 'answer': answer}
    return render(request, 'pybo/answer_form.html', context)


#답변 삭제
@login_required(login_url='common:login')
def answer_delete(request, aid):
    answer = get_object_or_404(Answer, pk=aid)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', qid=answer.question.id)
    answer.delete()
    return redirect('pybo:main')

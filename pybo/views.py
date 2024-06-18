# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer


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
    answer = question.answers.order_by('-create_date')
    context = {'question': question, 'answer_list': answer}
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



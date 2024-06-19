from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import Question


#질문 목록 화면
def main(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answers__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answers__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()  # 중복 제거
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


#질문 상세보기 화면
def detail(request, qid):
    question = get_object_or_404(Question, pk=qid)
    answer = question.answers.order_by('-create_date')
    context = {'question': question, 'answer_list': answer}
    return render(request, 'pybo/question_detail.html', context)


from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer

from quickstart.models import Snippet
from quickstart.serializers import SnippetSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    사용자를 보거나 편집할 수 있는 API endPoint
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    그룹을 보거나 편집할 수 있는 API endPoint
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])  #  api_view 데코레이터를 이용하여 지원하는 메소드를 지정
def snippet_list(request, format=None):
    """
    snippets의 모든 목록을 조회하거나 새로운 snippet을 생성하는 함수
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(reqeust, pk, format=None):
    """
    snippet 조회, 업데이트, 삭제 함수
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if reqeust.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif reqeust.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=reqeust.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif reqeust.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


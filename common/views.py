from django.contrib.auth import logout
from django.shortcuts import redirect


# Create your views here.

#로그아웃
def logout_view(request):
    logout(request)
    return redirect('main')

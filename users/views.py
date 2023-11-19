from django.shortcuts import render
from django.views import View


def index(request):
    return render(request, 'home_page.html')

class LoginUser(View):
    def get(self, request):
        return render(request, 'login.html')

class SignUp(View):
    def get(self, request):
        return render(request, 'sign_up.html')
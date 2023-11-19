from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('home/', views.index, name="home_page"),
    path('login/',views.LoginUser.as_view(), name="login_user"),
    path('sign-up/', views.SignUp.as_view(), name="signup_user"),
]
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('request', views.requestAttendance, name="request"),
    path('accept', views.acceptAttendance, name="accept"),
]
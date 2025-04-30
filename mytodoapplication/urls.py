from django.contrib import admin
from django.urls import path
from user.views import UserRegisterView , UserLoginView , TodoListView

urlpatterns = [
    path("api/user/register/" ,UserRegisterView.as_view()),
    path("api/user/login/" , UserLoginView.as_view()),
    path("api/user/todo/" , TodoListView.as_view()),
    path('admin/', admin.site.urls),
]

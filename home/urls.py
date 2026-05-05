from django.urls import path
from .views import student_api, student, login, signup
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('student_api/', student_api, name='student_api'),
    path('student/<int:id>/', student, name='student_detail'),
    path('login/', login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(),),
]
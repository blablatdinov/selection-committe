from django.urls import path
from django.contrib.auth.views import LoginView
from main.views import main, ProfileView, Login

urlpatterns = [
	path('', main),
	path('profile', ProfileView.as_view(), name='profile'),
	path('login', Login.as_view(template_name='main/auth.html', redirect_field_name='profile'), name='login'),
]

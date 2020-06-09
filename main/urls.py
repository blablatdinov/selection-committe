from django.urls import path
from django.contrib.auth.views import LoginView
from main.views import main


urlpatterns = [
	path('', main),
	path('login', LoginView.as_view(template_name='main/auth.html', redirect_field_name='profile'), name='login'),
]

from django.shortcuts import render
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
	...


def main(request):
	return render(request, 'main/base_main.html')

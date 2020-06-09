from django.shortcuts import render


def main(request):
	return render(request, 'main/base_main.html')

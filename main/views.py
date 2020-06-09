from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from main.models import AbiturStatement, Abitur


class Login(LoginView):
    template = 'main/auth.html'

    def get_success_url(self):
        return reverse('profile')


class ProfileView(View):
    template = 'main/profile.html'

    def get(self, request):
        user = request.user
        abitur = Abitur.objects.get(pk=user.pk)
        data = AbiturStatement.objects.filter(abitur=abitur)
        context = {
            'data': data
        }
        z = data
        for i in range(len(data)):
            data[i].place_on_rating = 0
        # --- Сортировка пузырьком по результатам экзаменов по убыванию ---
        for k in range(len(data)):
            abiturs = data[k].study_group.calculate_exam_point()
            n = 1
            while n < len(abiturs):
                for i in range(len(abiturs) - n):
                    if abiturs[i].required_exams_points < abiturs[i + 1].required_exams_points:
                        abiturs[i], abiturs[i + 1] = abiturs[i + 1], abiturs[i]
                n += 1
            # print(f'{data[k].study_group}\n')
            # for a in abiturs:
            #     print(f'  {a.FIO} {a.required_exams_points}')
            # print()
        # --- Конец сортировки ---
            for j in range(len(abiturs)):
                if abiturs[j] == abitur:
                    data[k].place_on_rating = j + 1
                    print(data[k].place_on_rating)
        #     print(data[k].place_on_rating)

        return render(request, self.template, context=context)


def main(request):
    return render(request, 'main/base_main.html')

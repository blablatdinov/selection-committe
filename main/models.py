from django.db import models

from django.contrib.auth import get_user_model

from main.choices import PERSONAL_ACHIEVEMENTS_CHOICES

from datetime import datetime


User = get_user_model()


class Exam(models.Model):
    """ Класс, описывающий экзамены """
    title = models.CharField(max_length=64, verbose_name="Название экзамена")

    def __str__(self):
        return self.title


class StudyDirection(models.Model):
    """ 
    Название, очная/заочная форма(каждое направление может быть в 2х формах обучения и 2х формах 
    оплаты), количество мест для различных форм и способов оплаты (вероятно потребуется создание 
    4х разных направлений в зависимости от формы и способа оплаты), экзамены требуемые в 
    направлении.
    """
    title = models.CharField(max_length=128, verbose_name='Название направления подготовки')
    required_exams = models.ManyToManyField(Exam, related_name='study_directions')

    def __str__(self):
        return self.title


class StudyGroup(models.Model): # FIXME: class name
    """ Конкретные данные по направлению подготовки на этот год """
    study_direction = models.ForeignKey(StudyDirection, related_name='study_group', on_delete=models.CASCADE)  # FIXME: related_name
    year = models.IntegerField(default=datetime.now().year, verbose_name='Год набора')
    budget_fulltime = models.IntegerField(default=0, verbose_name='Кол-во бюджетных очных мест')
    budget_distance = models.IntegerField(default=0, verbose_name='Кол-во бюджетных заочных мест')
    commerce_fulltime = models.IntegerField(default=0, verbose_name='Кол-во платных очных мест')
    commerce_distance = models.IntegerField(default=0, verbose_name='Кол-во платных заочных мест')

    def __str__(self):
        return f'{self.study_direction.title} : {self.year}'
    


class Abitur(User):
    """ ФИО, Логин, Пароль, балл Математика, балл Русский язык, балл Химия, балл Физика, 
    балл Инфоратика, балл Биология, балл Рисунок, балл Обществознание, балл Медаль 
    (если нет 0, если есть 5), балл личные достижения (0 – нет, вариации 5/7/10), 
    выбранные направления обучения (может быть несколько, одно из которых может быть с 
    "оригинал" документами, каждое направление в отдельности может быть как бюджет или платная 
    форма обучения) """
    FIO = models.CharField(max_length=128)
    medal = models.BooleanField(default=False)
    personal_achievement = models.IntegerField(choices=PERSONAL_ACHIEVEMENTS_CHOICES, null=True, blank=True)
    
    def get_medal_points(self):
        return 5 if self.medal else 0

    def __str__(self):
        return self.FIO


class ExamResult(models.Model):
    """ Класс объеденяющий Экзамен и Абитуриента, в котором добавляется поле результат экзамена """
    exam = models.ForeignKey(Exam, related_name='exam_results', on_delete=models.CASCADE)
    abitur = models.ForeignKey(Abitur, related_name='exam_results', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.exam.title} - {self.points}'



class AbiturStatement(models.Model):
    """ 
    Заявление абитуриента на поступление с указанием параметров направления и наличием оригинала документов 
    """
    study_group = models.ForeignKey(StudyGroup, related_name='abitur_statements', on_delete=models.CASCADE)
    abitur = models.ForeignKey(Abitur, related_name='abitur_statements', on_delete=models.CASCADE)
    fulltime_learning = models.BooleanField(default=True)
    budget_learning = models.BooleanField(default=True)
    is_original_documents = models.BooleanField(default=False)

    def __str__(self):
        return self.abitur.FIO

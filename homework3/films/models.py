from django.db import models


# Create your models here.

class Film(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name='ID фильма')
    genre = models.CharField(max_length=150, verbose_name='Жанр фильма')
    year = models.IntegerField(verbose_name='Год выпуска')
    time = models.IntegerField(verbose_name='Продолжительность занятия (мин)')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.theme} [{self.uid}]'

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

from django.db import models


class User(models.Model):
    login = models.CharField(max_length=100, verbose_name="Логин")
    password = models.CharField(max_length=256, verbose_name="Пароль")
    age = models.IntegerField(verbose_name="Возраст")


class Film(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название фильма")
    description = models.CharField(max_length=300, verbose_name="Описание фильма", null=True)
    genre = models.CharField(max_length=150, verbose_name='Жанр фильма')
    year = models.IntegerField(verbose_name='Год выпуска')
    time = models.IntegerField(verbose_name='Продолжительность фильма (мин)')
    director = models.CharField(max_length=100, verbose_name="Режиссер")
    summ_rating = models.IntegerField(verbose_name="Сумма оценок")
    count_rating = models.IntegerField(verbose_name="Колическтво оценок")


class Rating(models.Model):
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rate = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'film_id'], name='rating_film-user')
        ]


class UserLike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'film_id'], name='userlike_film-user')
        ]
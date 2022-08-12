from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.TextField(max_length=100)
    slug = models.SlugField(primary_key=True,
                            max_length=100,
                            unique=True,
                            blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Film(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='films',
                              null=True,
                              blank=False)
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='films')
    image = models.ImageField(upload_to='films', blank=True, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='films')
    film = models.ForeignKey(Film, on_delete=models.CASCADE,
                             related_name='images',
                             verbose_name='images')


class Like(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='likes',
                              verbose_name='Владелец лайка')
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='likes',
                             verbose_name='film')
    like = models.BooleanField('лайк', default=True)

    def __str__(self):
        return f'{self.film} {self.like}'


class Review(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='review')
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'отзыв от {self.owner} на фильм {self.film}'


class Rating(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='ratings',
                              verbose_name='Рейтинг от')
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='ratings',
                             verbose_name='Фильм')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], default=0
    )

    def __str__(self):
        return f'{self.film} -- {self.rating}'


class Favourite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='favourits')
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='favourits')
    Favourite = models.BooleanField('фаворит', default=True)


    def __str__(self):
        return f'Ваш фильм-фаворит : {self.film}'

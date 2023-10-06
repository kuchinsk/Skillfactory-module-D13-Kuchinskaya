from urllib import request

from django.contrib.auth.models import User
from django.db import models

# from profile.models import MyUser


# class Author(models.Model):
#     authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.authorUser}'


class Category(models.Model):
    TANK = 'TN'
    HEALER = 'HL'
    DD = 'DD'
    DEALER = 'DL'
    GUILDMASTER = 'GM'
    QUESTGIVERS = 'QG'
    BLACKSMITHS = 'BS'
    TAIRMANS = 'TM'
    ZELEVARY = 'ZL'
    WIZARD = 'WZ'
    TYPE_CHOICES = (
        (TANK, 'Танки'),
        (HEALER, 'Хилы'),
        (DD, 'ДД'),
        (DEALER, 'Торговцы'),
        (GUILDMASTER, 'Гилдмастеры'),
        (QUESTGIVERS, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (TAIRMANS, 'Кожевники'),
        (ZELEVARY, 'Зелевары'),
        (WIZARD, 'Мастера заклинаний'),
    )
    name = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TANK)

    def __str__(self):
        return self.get_name_display()


class Post(models.Model):
    title = models.CharField(max_length=255)
    textPost = models.TextField()
    img = models.ImageField(upload_to='media/img_uploaded', blank=True, null=True)
    video = models.FileField(upload_to='videos_uploaded', blank=True, null=True)
    file = models.FileField(upload_to='files_uploaded', blank=True, null=True)
    # filePost = models.FileField(default="", upload_to='media/%Y/%m/%d/', verbose_name="Медиа", blank=True)
    timePost = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.textPost}'

    # def get_file_fields(self):
    #     return [{"label": field.verbose_name, "field": getattr(self, field.name)} for field in self._meta.get_fields()
    #             if isinstance(field, models.FileField)]


class Response(models.Model):
    textResponse = models.TextField()
    timeResponse = models.DateTimeField(auto_now_add=True)
    acceptResponse = models.BooleanField(default=False)

    responsePost = models.ForeignKey(Post, on_delete=models.CASCADE)
    responseUser = models.ForeignKey(User, on_delete=models.CASCADE)






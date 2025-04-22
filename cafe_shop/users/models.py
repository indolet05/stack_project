from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    phone = models.CharField(
        'Телефон',
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+999999999'."
            )
        ]
    )
    address = models.TextField('Адрес', blank=True, null=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    email_confirmed = models.BooleanField('Email подтвержден', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created_at']

    def __str__(self):
        return f'Профиль {self.user.username}'
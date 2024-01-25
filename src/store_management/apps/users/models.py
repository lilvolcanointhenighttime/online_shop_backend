import binascii
import os
from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser):
    # groups = models.ManyToManyField('Group', related_name='custom_users')
    # user_permissions = models.ManyToManyField('Permission', related_name='custom_users')

    username = models.CharField(max_length=250,
                                verbose_name='Username',
                                unique=True,
                                blank=True,
                                null=False)
    email = models.EmailField(unique=True,
                              verbose_name='E-mail',
                              null=False)
    full_name = models.CharField(max_length=250,
                                 verbose_name='Full name',
                                 blank=True,
                                 null=True)
    is_staff = models.BooleanField(verbose_name='Staff status', default=False)
    is_superuser = models.BooleanField(
        verbose_name='Superuser status', default=False)
    is_active = models.BooleanField(
        verbose_name='User activated', default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(
        verbose_name='Last login', null=True, blank=True)
    date_joined = models.DateTimeField(
        verbose_name='Date joined', auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username}, {self.full_name}'

    def save(self, *args, **kwargs):
        if self._state.adding and (
                not self.username or User.objects.filter(username=self.username).exists()
        ):
            email = self.email
            self.username = User.objects.generate_username(email)
        if '@' not in self.username:
            self.username = '@' + self.username
        super(User, self).save(*args, **kwargs)


class UserToken(models.Model):
    TOKEN_TYPES = (
        ('su', 'SignUp token'),
        ('ce', 'Change email token'),
        ('pr', 'Password reset token')
    )
    token = models.CharField(unique=True,
                             max_length=32,
                             verbose_name='Token',
                             blank=True,
                             null=True)
    token_type = models.CharField(max_length=2, choices=TOKEN_TYPES,
                                  verbose_name='Token type',
                                  blank=True,
                                  null=True)
    token_owner = models.EmailField(verbose_name='Token owner email',
                                    blank=True,
                                    null=True)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Token creation date')
    expired = models.BooleanField(default=False,
                                  verbose_name='Token expired')

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'Tokens'

    def __str__(self):
        return f'{self.token}, {self.token_type}'

    def generate_token(self):
        return binascii.hexlify(os.urandom(16)).decode()

    def save(self, *args, **kwargs):
        if self._state.adding and (not self.token or
                                   UserToken.objects.filter(token=self.token).exists()):
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    @classmethod
    def get_token_from_str(cls, token_value: str, token_owner: str):
        return cls.objects.get(token=token_value, token_owner=token_owner)


class UserBonusesBalance(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='bonuses_balance')
    balance = models.IntegerField(default=0,
                                  verbose_name='User balance')

    def __str__(self):
        return f'{self.balance}$'


class UserShippingInfo(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='shipping_info',
                                blank=True,
                                null=True)
    session_id = models.CharField(max_length=32,
                                  blank=True,
                                  null=True)
    name = models.CharField(max_length=180,
                            verbose_name='Name')
    surname = models.CharField(max_length=190,
                               verbose_name='Surname')
    patronymic = models.CharField(max_length=180,
                                  verbose_name='Patronymic',
                                  blank=True,
                                  null=True)
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=200,
                               verbose_name='Address')
    city = models.CharField(max_length=170,
                            verbose_name='City')
    post_office = models.CharField(max_length=450,
                                   verbose_name='Post office')

    class Meta:
        verbose_name = 'shipping info'
        verbose_name_plural = 'Shipping Infos'

    def __str__(self):
        return f'Shipping info of: {self.name} {self.surname} {self.patronymic}'

# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from common.models import CoreModel

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if username is None:
            raise ValueError('必须输入用户名')
        if password is None:
            raise ValueError('必须输入密码')
        user = self.model(username=username)
        user.is_staff = False
        user.set_password(password)
        self.save = user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username,
                                password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AbstractUser(AbstractBaseUser, PermissionsMixin, CoreModel):
    """
    抽象用户
    """
    username = models.CharField(max_length=11, verbose_name='用户名', unique=True)
    fullname = models.CharField(max_length=80, blank=True, verbose_name='名称')
    thumbnail = models.ImageField(upload_to="thumbnail", verbose_name='头像', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.fullname

    def get_full_name(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return self.is_superuser or perm in self.get_all_permissions()

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        else:
            return True

    class Meta:
        abstract = True



class User(AbstractUser):
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    owner = models.ForeignKey('User', null=True, blank=True,on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        permissions = (
            ("view_user", "Can drive"),
        )

    def __str__(self):
        return self.username

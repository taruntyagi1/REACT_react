from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,password=None):
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self,first_name,last_name,email,username,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13,unique=True,blank=True)
    email = models.EmailField(max_length=500,unique=True)
    username = models.CharField(max_length=200,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']

    def __str__(self):
        return self.username


    def has_perm(self,perm,obj=None):
        return self.is_admin


    def has_module_perms(perms,app_label):
        return True


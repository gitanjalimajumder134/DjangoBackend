from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin, BaseUserManager)
# Create your models here.

class UserManager(BaseUserManager):
     
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            # with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique= True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=100, default=email, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, force_insert=False, force_update=False):

        self.username = self.email
        super(User, self).save(force_insert, force_update)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    class Meta:
        ordering = ('-id',)
        verbose_name = 'User'


class Category(models.Model):
    name = models.CharField(max_length=251)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'

    def __str__(self):
        return str(self.name)

class Quizzes(models.Model):
    title = models.CharField(max_length=255, default='New Quiz', verbose_name='Quize Title')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Quiz'

    def __str__(self):
        return str(self.title)

class Updated(models.Model):
    updated = models.DateField(verbose_name='Last Updated', auto_now=True)

    class Meta:
        abstract = True
 

class Question(Updated):
    Scale = (
        (0, ('Fundamental')),
        (1, ('Beginner')),
        (2, ('Intermediate')),
        (3, ('Advanced')),
        (4, ('Expert')),
    )

    Type = (
        (0, ('Multiple Choice')),
    )
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, related_name='question')
    technique = models.IntegerField(choices=Type, default=0, verbose_name='Type of Question')
    title = models.CharField(max_length=255, verbose_name='Title')
    difficulty = models.IntegerField(choices=Scale, default=0, verbose_name='Difficulty')
    created_at = models.DateField(auto_now_add=True, verbose_name='Date Created')
    is_active = models.BooleanField(default=False, verbose_name='Active Status')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Question'

    def __str__(self):
        return str(self.title)

class Answer(Updated):
    category = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.CharField(max_length=255, verbose_name='Answer Text')
    is_right = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Answer'

    def __str__(self):
        return str(self.answer_text)
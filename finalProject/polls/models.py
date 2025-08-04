
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class ReaderManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email or len(email) <= 0:
            raise ValueError('The email must be valid')
        if not password:
            raise ValueError('The password must be valid')

        reader = self.model(
            email=self.normalize_email(email),
        )
        reader.set_password(password)
        reader.save(using=self._db)
        return reader
    def create_superuser(self, email, password):
       reader =  self.create_user(email = self.normalize_email(email), password = password)
       reader.is_superuser = False
       reader.is_staff = False
       reader.is_admin = False
       return reader


class Reader(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ReaderManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'age']

    def __str__(self):
        return self.username

class AuthorManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email or len(email) <= 0:
            raise ValueError('The email must be valid')
        if not password:
            raise ValueError('The password must be valid')
        author = self.model(email=self.normalize_email(email))
        author.set_password(password)
        author.save(using=self._db)
        return author
    def create_superuser(self, email, password):
        author = self.create_user(email = self.normalize_email(email), password = password)
        author.is_superuser = False
        author.is_staff = False
        author.is_admin = False
        return author

class Author(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    BrithOfDate = models.DateField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AuthorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'age']

    def __str__(self):
        return self.first_name , self.last_name



class AdminManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email or len(email) <= 0:
            raise ValueError('The email must be valid')
        if not password:
            raise ValueError('The password must be valid')
        admin = self.model(
            email=self.normalize_email(email),
        )
        admin.set_password(password)
        admin.save(using=self._db)
        return admin
    def create_superuser(self, email, password):
        admin = self.create_user(email = self.normalize_email(email), password = password)
        admin.is_superuser = True
        admin.is_admin = True
        admin.is_staff = False
        return admin


class Admin(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'age']

    def __str__(self):
        return self.first_name, self.last_name


class Category(models.Model):
    type = models.CharField(max_length=100)
    number_of_articles = models.IntegerField()


class Article(models.Model):
    title = models.CharField(max_length=100)
    Publication_date = models.DateField()
    EstimatedReadingTime = models.IntegerField()
    Author_id = models.ManyToManyField("Author")
    category_id = models.ForeignKey(Category , null=True, on_delete=models.CASCADE ,blank=True)

class BookMarks(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE , null=True, blank=True)
    reader_id = models.ForeignKey( Reader, on_delete=models.CASCADE , null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
        date_of_like = models.DateTimeField(auto_now_add=True)
        article_id = models.ForeignKey(Article, on_delete=models.CASCADE , null=True, blank=True)
        reader_id = models.ForeignKey(Reader, on_delete=models.CASCADE , null=True, blank=True)

class Comments(models.Model):
    date_of_comment = models.DateTimeField(auto_now_add=True)
    reader_id = models.ForeignKey(Reader, on_delete=models.CASCADE, null=True, blank=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

class Tags(models.Model):
    article_id = models.ManyToManyField(Article, related_name="tags")



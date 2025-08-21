from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ckeditor_uploader.fields import RichTextUploadingField
# from ckeditor.fields import RichTextField
from django.conf import settings


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True ,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [("reader", "Reader"), ("author", "Author"), ("admin", "Admin")]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "role", "age"]

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_reader(self):
        return self.role == "reader"

    @property
    def is_author(self):
        return self.role == "author"


class Category(models.Model):
    CHOICES_CATEGORY = [
        ('TECH', 'Technology'),
        ('HEALTH', 'Health'),
        ('EDU', 'Education'),
        ('LIFESTYLE', 'Lifestyle'),
        ('BUSINESS', 'Business'),
        ('SPORTS', 'Sports'),
        ('TRAVEL', 'Travel'),
        ('FOOD', 'Food'),
        ('POLITICS','politics')
    ]
    type = models.CharField(
        max_length=20,
        choices=CHOICES_CATEGORY,
        default='TECH',
        verbose_name='Category Type',
        help_text='Select the type of this category'
    )
    # photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.type

    # def number_of_article(self):
    #     return Article.objects.filter(category=self.id).count()


class Article(TimeStampedModel):
    title = models.CharField(
        max_length=100,
        verbose_name='Article title',
        help_text='Enter the title of your article'
    )
    publication_date = models.DateField(
        verbose_name='Publication date',
        help_text='Enter the publication date of your article',
        null=True, blank=True
    )
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE , related_name='articles')
    content = RichTextUploadingField(null=True, blank=True)
    isFreatured = models.BooleanField(default=False, null=True, blank=True)

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        return getattr(user, "role","") in ("admin", "author")

    def can_create_article(self, user):
        if not user.is_authenticated:
            return False
        return getattr(user, "role", None) == "author" or self.authors.filter(id=user.id).exists()

class BookMarks(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE , null=True, blank=True , related_name='bookmarks')
    reader = models.ForeignKey( User, on_delete=models.CASCADE , null=True, blank=True,related_name='reader')

class Likes(models.Model):
        date_of_like = models.DateTimeField(auto_now_add=True)
        article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article_likes', null=True, blank=True)
        reader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Comments(models.Model):
    date_of_comment = models.DateTimeField(auto_now_add=True)
    reader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.reader} on {self.article}"

class Tag(models.Model):
    articles = models.ManyToManyField(Article, related_name="tags")


class ReaderProxy(User):
    class Meta:
        proxy = True
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    def save(self, *args, **kwargs):
        self.role = "reader"
        super().save(*args, **kwargs)


class AuthorProxy(User):
    class Meta:
        proxy = True
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    def save(self, *args, **kwargs):
        self.role = "author"
        super().save(*args, **kwargs)


class AdminProxy(User):
    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
    def save(self, *args, **kwargs):
        self.role = "admin"
        super().save(*args, **kwargs)
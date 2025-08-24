# <project>/<your_app>/management/commands/seed.py
import logging
import random
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker


from polls.models import Category, Article, BookMarks, Likes, Comments, Tag

logger = logging.getLogger(__name__)
fake = Faker()

MODE_REFRESH = "refresh"
MODE_CLEAR = "clear"


NUM_AUTHORS = 4
NUM_READERS = 8
NUM_ARTICLES = 25
MAX_COMMENTS_PER_ARTICLE = 5
MAX_LIKES_PER_ARTICLE = 8
MAX_BOOKMARKS_PER_ARTICLE = 5
NUM_TAGS = 10
class Command(BaseCommand):
    help = "Seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            type=str,
            default=MODE_REFRESH,
            choices=[MODE_REFRESH, MODE_CLEAR],
            help="Mode: refresh | clear",
        )

    def handle(self, *args, **options):
        mode = options["mode"]
        self.stdout.write(self.style.WARNING("Seeding..."))
        if mode == MODE_CLEAR:
            clear_data()
        else:
            run_seed()
        self.stdout.write(self.style.SUCCESS("Done."))


def clear_data():
    logger.info("Clearing data...")
    Article.tags.through.objects.all().delete()
    BookMarks.objects.all().delete()
    Likes.objects.all().delete()
    Comments.objects.all().delete()
    Article.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()

    # get_user_model().objects.exclude(is_superuser=True).delete()

    logger.info("All cleared.")


@transaction.atomic
def run_seed():

    clear_data()

    User = get_user_model()

    logger.info("Creating users...")
    if not User.objects.filter(email="admin@example.com").exists():
        User.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            username="admin",
            first_name="Site",
            last_name="Admin",
            role="admin",
            age=28,
        )

    # مؤلفون
    authors = []
    for i in range(NUM_AUTHORS):
        email = f"author{i+1}@example.com"
        user = User.objects.create_user(
            email=email,
            password="pass12345",
            username=f"author{i+1}",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role="author",
            age=random.randint(20, 45),
        )
        authors.append(user)

    # قرّاء
    readers = []
    for i in range(NUM_READERS):
        email = f"reader{i+1}@example.com"
        user = User.objects.create_user(
            email=email,
            password="pass12345",
            username=f"reader{i+1}",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role="reader",
            age=random.randint(16, 60),
        )
        readers.append(user)

    logger.info("Creating categories...")
    # أنشئ كل الخيارات المعرفة في الموديل (مفاتيح الاختيارات)
    choice_keys = [c[0] for c in Category.CHOICES_CATEGORY]
    categories = []
    for key in choice_keys:
        cat, _ = Category.objects.get_or_create(type=key)
        categories.append(cat)

    logger.info("Creating tags...")
    # موديل Tag بدون حقل اسم — سننشئ عددًا منها للربط فقط
    tags = [Tag.objects.create() for _ in range(NUM_TAGS)]

    logger.info("Creating articles (with authors, tags)...")
    articles = []
    for _ in range(NUM_ARTICLES):
        title = fake.sentence(nb_words=6).rstrip(".")
        pub_date = fake.date_between(start_date=date(2024, 1, 1), end_date=timezone.now().date())
        category = random.choice(categories)
        html_content = "".join(f"<p>{p}</p>" for p in fake.paragraphs(nb=random.randint(3, 8)))

        article = Article.objects.create(
            title=title,
            publication_date=pub_date,
            category=category,
            content=html_content,
            isFreatured=random.choice([True, False, False, False]),  # نسبة بسيطة يكون Featured
        )
        # أربِط مؤلفين (1–2) عشوائيًا
        article.authors.set(random.sample(authors, k=random.randint(1, min(2, len(authors)))))

        # أربط Tags عشوائيًا
        if tags:
            article.tags.add(*random.sample(tags, k=random.randint(0, min(3, len(tags)))))

        articles.append(article)

    logger.info("Creating comments, likes, bookmarks...")
    # تعليقات
    comment_objs = []
    for article in articles:
        for _ in range(random.randint(0, MAX_COMMENTS_PER_ARTICLE)):
            reader = random.choice(readers)
            comment_objs.append(
                Comments(
                    reader=reader,
                    article=article,
                    content=fake.paragraph(nb_sentences=random.randint(1, 3)),
                )
            )
    Comments.objects.bulk_create(comment_objs, batch_size=200)

    # لايكات (من قرّاء مختلفين لنفس المقال)
    like_objs = []
    for article in articles:
        sample_readers = random.sample(readers, k=min(len(readers), random.randint(0, MAX_LIKES_PER_ARTICLE)))
        for r in sample_readers:
            like_objs.append(Likes(article=article, reader=r))
    Likes.objects.bulk_create(like_objs, batch_size=200)

    # بوكماركس
    bm_objs = []
    for article in articles:
        sample_readers = random.sample(readers, k=min(len(readers), random.randint(0, MAX_BOOKMARKS_PER_ARTICLE)))
        for r in sample_readers:
            bm_objs.append(BookMarks(article=article, reader=r))
    BookMarks.objects.bulk_create(bm_objs, batch_size=200)

    logger.info("Seeding finished.")

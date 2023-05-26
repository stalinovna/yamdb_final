from django.core.management.base import BaseCommand
import csv
from django.contrib.auth import get_user_model

from reviews.models import Review, Comment
from reviews.models_categories import Titles, Genres, Categories, GenreTitle
from api_yamdb.settings import BASE_DIR

User = get_user_model()


class Command(BaseCommand):
    """
    To run the command - python3 manage.py load_csv
    To remove database - python3 manage.py flush
    """
    help = 'command to load data from csv-files'

    def load_user(self):
        with open(f'{BASE_DIR}/static/data/users.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    )

    def load_category(self):
        with open(f'{BASE_DIR}/static/data/category.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Categories.objects.get_or_create(
                        id=row[0], name=row[1], slug=row[2]
                    )

    def load_genre(self):
        with open(f'{BASE_DIR}/static/data/genre.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Genres.objects.get_or_create(
                        id=row[0], name=row[1], slug=row[2]
                    )

    def load_titles(self):
        with open(f'{BASE_DIR}/static/data/titles.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Titles.objects.get_or_create(
                        id=row[0], name=row[1], year=row[2], category_id=row[3]
                    )

    def load_genre_title(self):
        with open(f'{BASE_DIR}/static/data/genre_title.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    GenreTitle.objects.get_or_create(
                        id=row[0], title_id=row[1], genre_id=row[2]
                    )

    def load_review(self):
        with open(f'{BASE_DIR}/static/data/review.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.get_or_create(
                        id=row[0],
                        title_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        score=row[4],
                        pub_date=row[5]
                    )

    def load_comments(self):
        with open(f'{BASE_DIR}/static/data/comments.csv',
                  newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Comment.objects.get_or_create(
                        id=row[0],
                        review_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        pub_date=row[4]
                    )

    def handle(self, *args, **options):
        self.load_user()
        self.load_category()
        self.load_genre()
        self.load_titles()
        self.load_genre_title()
        self.load_review()
        self.load_comments()

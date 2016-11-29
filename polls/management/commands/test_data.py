from django.core.management.base import BaseCommand, CommandError
from polls.models import Question, Answer, Tag, Profile
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        usernames = ['Vasya', 'Petya', 'Vova', 'Gena', 'Dima', 'Sasha', 'Kolya']
        tagsnames = ['Google', 'Yandex', 'Mail', 'MySql', 'Postgre', 'MongoDB', 'InnoDB']
        questions_count = 3
        answers_max = 5

        users = []
        for name in usernames:
            a = User(username=name, password='123456qwerty')
            try:
                a.save()
                users.append(a)
            except IntegrityError:
                # Уже такой есть
                users.append(User.objects.filter(username=name))

        tags = []
        for tagname in tagsnames:
            t = Tag(word=tagname)
            try:
                t.save()
                tags.append(t)
            except IntegrityError:
                # Уже такой есть
                tags.append(Tag.objects.filter(word=tagname))

        for num in range(questions_count):
            q = Question(
                header='test title' + str(num),
                content='test content' + str(num),
                author=users[random.randint(0, len(users) - 1)].first()
            )

            q.save()
            q.tags.add(tags[random.randint(0, len(tags) - 1)])
            q.tags.add(tags[random.randint(0, len(tags) - 1)])

            answers_count = random.randint(0, answers_max)
            for i in range(0, answers_count):
                a = Answer(
                    content='test answer' + str(num),
                    author=users[random.randint(0, len(users) - 1)].first(),
                    question=q
                )
                a.save()
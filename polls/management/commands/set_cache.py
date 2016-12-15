from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, Sum, F, Case, When, IntegerField
from django.core.cache import cache
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from polls.models import User, Tag


class Command(BaseCommand):
    help = 'Caches data for top_users and top_tags block'

    def handle(self, *args, **options):
        cache.set('top_users', User.objects.extra(
            select={'total': '(SELECT COUNT(*) FROM polls_answer WHERE author_id ='
                             ' auth_user.id AND publicationDate >= DATE_SUB(CURDATE(),'
                             ' INTERVAL 3 MONTH)) + (SELECT COUNT(*) FROM polls_question'
                             ' WHERE author_id = auth_user.id AND publicationDate >= '
                             'DATE_SUB(CURDATE(), INTERVAL 3 MONTH))'},
            order_by=['-total']
        )[:10], 600)

        cache.set('top_tags', Tag.objects.annotate(q=Sum(
            Case(
                When(question__publicationDate__gte=timezone.now() - relativedelta(months=3), then=1),
                default=0, output_field=IntegerField()
            ))).order_by('-q')[:10], 600)

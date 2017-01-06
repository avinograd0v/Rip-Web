from django.db.models import Count
import operator
from django.db.models import Q
from functools import reduce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Tag

def paginate(questions, request):
    per_page = 5

    paginator = Paginator(questions, per_page)

    page = request.POST.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return questions


def sort_questions(new_sort, queryset):
    questions = []

    if new_sort == 'date_down':
        questions = queryset.order_by('-publicationDate')
    elif new_sort == 'date_up':
        questions = queryset.order_by('publicationDate')
    elif new_sort == 'rating_down':
        questions = queryset.order_by('-rating')
    elif new_sort == 'rating_up':
        questions = queryset.order_by('rating')

    return questions


def filter_by_tags(active_tags_ids, queryset):
    if len(active_tags_ids):
        active_tags = []

        for tag_id in reversed(active_tags_ids):
            active_tags.append(Tag.objects.get(id=tag_id))

        questions = queryset.filter(tags__in=active_tags)\
                                                 .annotate(num_tags=Count('tags'))\
                                                 .filter(num_tags=len(active_tags))
    else:
        questions = queryset
    return questions


def filter_by_search(query, queryset):
    if query:
        questions = queryset.search(query + '*')
        #query_list = query.split()
        #questions = queryset.filter(reduce(operator.and_, (Q(header__icontains=q) for q in query_list)) |
                                    #reduce(operator.and_, (Q(content__icontains=q) for q in query_list)))
    else:
        questions = queryset

    return questions

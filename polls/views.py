from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from .forms import UserForm, ProfileForm, AnswerForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from .models import User, Question, Answer, Tag
import json
from django.db.models import Count
import operator
from django.db.models import Q
from functools import reduce
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def index(request):
    return render(request, 'polls/index.html')


class AddFilterTag(View):
    template_name = 'polls/question_template.html'

    def post(self, request, *args, **kwargs):
        tag_pk = int(QueryDict(request.body).get('tagpk'))
        tags = request.session.get('tags', [])

        if tag_pk not in tags:
            tags.append(tag_pk)

        request.session['tags'] = tags

        questions = filter_by_tags(self.request.session.get('tags'), Question.objects.all())
        questions = filter_by_search(self.request.session.get('query'), questions)
        questions = sort_questions(self.request.session.get('sort_by'), questions)

        return render(request, self.template_name, {'all_questions': questions})


class RemoveFilterTag(View):
    template_name = 'polls/question_template.html'

    def post(self, request, *args, **kwargs):
        tag_pk = int(QueryDict(request.body).get('tagpk'))
        tags = request.session.get('tags', [])

        if tag_pk in tags:
            tags.remove(tag_pk)

        request.session['tags'] = tags

        questions = filter_by_tags(self.request.session.get('tags'), Question.objects.all())
        questions = filter_by_search(self.request.session.get('query'), questions)
        questions = sort_questions(self.request.session.get('sort_by'), questions)

        return render(request, self.template_name, {'all_questions': questions})


class QuestionsView(generic.ListView):
    model = Question
    template_name = "polls/questions.html"
    context_object_name = "all_questions"

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '').strip()
        self.request.session['query'] = query
        context = super(QuestionsView, self).get_context_data(**kwargs)
        context['active_tags'] = []
        active_tags_ids = self.request.session.get('tags', [])

        for tag_id in reversed(active_tags_ids):
            context.get('active_tags').append(Tag.objects.get(id=tag_id))

        tagged_questions = filter_by_tags(active_tags_ids, self.model.objects.all())

        context['title'] = query if query else "All questions"

        all_questions = filter_by_search(query, tagged_questions)

        self.request.session['sort_by'] = self.request.session.get('sort_by', 'date_down')
        context['all_questions'] = sort_questions(self.request.session.get('sort_by'), all_questions)

        context['tags'] = Tag.objects.all()
        return context


class QuestionsSort(generic.ListView):
    model = Question
    template_name = 'polls/question_template.html'

    def post(self, request, *args, **kwargs):
        new_sort = request.POST.get('sortby')
        questions = filter_by_tags(self.request.session.get('tags'), Question.objects.all())
        questions = filter_by_search(self.request.session.get('query'), questions)
        questions = sort_questions(new_sort, questions)

        request.session['sort_by'] = new_sort
        return render(request, self.template_name, {'all_questions': questions})


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
        query_list = query.split()
        questions = queryset.filter(reduce(operator.and_, (Q(header__icontains=q) for q in query_list)) |
                                    reduce(operator.and_, (Q(content__icontains=q) for q in query_list)))
    else:
        questions = queryset

    return questions


class QuestionDetail(generic.DetailView):
    model = Question
    template_name = 'polls/question.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['add_answer_form'] = AnswerForm(None)
        context['edit_question_form'] = QuestionForm(None)
        return context


class UserDetail(generic.DeleteView):
    model = User
    template_name = 'polls/user_profile.html'


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['header', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)


class QuestionUpdate(LoginRequiredMixin, View):
    model = Question
    fields = ['header', 'content']

    def post(self, request, *args, **kwargs):
        new_content = request.POST.get('new_content')
        new_header = request.POST.get('new_header')
        question = self.model.objects.get(pk=int(QueryDict(request.body).get('questionpk')))

        print(new_header)
        question.content = new_content
        question.header = new_header
        question.save()

        response_data = {}
        response_data['content'] = new_content
        response_data['header'] = new_header

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User

    fields = ['username', 'email', 'password']
    template_name = "polls/edit_profile_form.html"


class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('polls:questions', kwargs={'tag_name': 'all'})


class CheckAnswer(LoginRequiredMixin, View):
    model = Answer

    def post(self, request, *args, **kwargs):
        answer = self.model.objects.get(pk=int(QueryDict(request.body).get('answerpk')))

        answer.isRight = not answer.isRight
        answer.save()
        return HttpResponse(answer.isRight, content_type="text/plain")


class AnswerApprove(LoginRequiredMixin, View):
    model = Answer

    def post(self, request, *args, **kwargs):
        answer = self.model.objects.get(pk=int(QueryDict(request.body).get('answerpk')))

        if request.user in answer.disapproved_by.all():
            answer.disapproved_by.remove(request.user)
            answer.approved_by.add(request.user)
            answer.rating += 2
        elif request.user not in answer.approved_by.all():
            answer.approved_by.add(request.user)
            answer.rating += 1
        else:
            answer.approved_by.remove(request.user)
            answer.rating -= 1

        answer.save()

        return HttpResponse(answer.rating, content_type="text/plain")


class QuestionApprove(LoginRequiredMixin, View):
    model = Question

    def post(self, request, *args, **kwargs):
        question = self.model.objects.get(pk=int(QueryDict(request.body).get('questionpk')))

        if request.user in question.disapproved_by.all():
            question.disapproved_by.remove(request.user)
            question.approved_by.add(request.user)
            question.rating += 2
        elif request.user not in question.approved_by.all():
            question.approved_by.add(request.user)
            question.rating += 1
        else:
            question.approved_by.remove(request.user)
            question.rating -= 1

        question.save()

        return HttpResponse(question.rating, content_type="text/plain")


class QuestionDisapprove(LoginRequiredMixin, View):
    model = Question

    def post(self, request, *args, **kwargs):
        question = self.model.objects.get(pk=int(QueryDict(request.body).get('questionpk')))

        if request.user in question.approved_by.all():
            question.approved_by.remove(request.user)
            question.disapproved_by.add(request.user)
            question.rating -= 2
        elif request.user not in question.disapproved_by.all():
            question.disapproved_by.add(request.user)
            question.rating -= 1
        else:
            question.disapproved_by.remove(request.user)
            question.rating += 1

        question.save()

        return HttpResponse(question.rating, content_type="text/plain")


class AnswerDisapprove(LoginRequiredMixin, View):
    model = Answer

    def post(self, request, *args, **kwargs):
        answer = self.model.objects.get(pk=int(QueryDict(request.body).get('answerpk')))

        if request.user in answer.approved_by.all():
            answer.approved_by.remove(request.user)
            answer.disapproved_by.add(request.user)
            answer.rating -= 2
        elif request.user not in answer.disapproved_by.all():
            answer.disapproved_by.add(request.user)
            answer.rating -= 1
        else:
            answer.disapproved_by.remove(request.user)
            answer.rating += 1

        answer.save()

        return HttpResponse(answer.rating, content_type="text/plain")


class AnswerCreate(LoginRequiredMixin, View):
    model = Answer
    template_name = 'polls/answer_template.html'
    fields = ['content']

    def post(self, request, *args, **kwargs):
        answer_text = request.POST.get('the_answer')
        question = Question.objects.get(id=self.kwargs['pk'])
        answer = self.model(content=answer_text, question=question, author=request.user)
        answer.save()

        context = dict()
        context['answer'] = answer
        context['add_answer_form'] = AnswerForm(instance=answer)
        return render(request, self.template_name, context)


class AnswerUpdate(LoginRequiredMixin, View):
    model = Answer
    fields = ['content']

    def post(self, request, *args, **kwargs):
        new_text = request.POST.get('new_text')
        answer = self.model.objects.get(pk=int(QueryDict(request.body).get('answerpk')))

        answer.content = new_text
        answer.save()
        return HttpResponse(new_text, content_type="text/plain")


class AnswerDelete(LoginRequiredMixin, View):

    model = Answer

    def delete(self, request, *args, **kwargs):
        answer = self.model.objects.get(pk=int(QueryDict(request.body).get('answerpk')))

        if answer.author != request.user:
            return False

        answer.delete()

        response_data = {}
        response_data['msg'] = 'Answer was deleted.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class UserFormView(View):
    user_class = UserForm
    profile_class = ProfileForm
    template_name = 'polls/signup_form.html'

    # display blank form
    def get(self, request):
        user_form = self.user_class(None)
        profile_form = self.profile_class(None)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    # process form data
    def post(self, request):
        user_form = self.user_class(request.POST)
        profile_form = self.profile_class(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)

            # cleaned data
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user.profile.avatar = profile_form.cleaned_data['avatar']
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('polls:index')

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })


#def questions(request, tag_name):
#    if tag_name != "all":
#        tag_name = tag_name.replace("-", " ").title()
#        title = tag_name
#        all_questions = list(filter(lambda que: que.tags.filter(word=tag_name).exists(), Question.objects.all()))
#    else:
#        query = request.GET.get('q', False)
#        if query:
#            title = query
#            all_questions = list(filter(lambda que: que.header.find(query) != -1, Question.objects.all()))
#        else:
#            title = "All questions"
#            all_questions = Question.objects.all()
#    return render(request, "polls/questions.html", {
#        'all_questions': all_questions,
#        'title': title
#    })

#def login(request):
#    return render(request, 'polls/login.html')

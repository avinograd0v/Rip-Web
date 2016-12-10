from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^signup/$', views.UserFormView.as_view(), name='signup'),

    url(r'^question/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view(), name='question'),

    url(r'^questions/(?P<tag_name>[a-z, -]+)/$', views.QuestionsView.as_view(), name='questions'),

    url(r'^question/add/$', views.QuestionCreate.as_view(), name='add-question'),

    url(r'^question/(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='delete-question'),

    url(r'^question/(?P<pk>[0-9]+)/edit_answer/$', views.AnswerUpdate.as_view(), name='edit-answer'),

    url(r'^question/(?P<pk>[0-9]+)/delete_answer/$', views.AnswerDelete.as_view(), name='delete-answer'),

    url(r'^question/(?P<pk>[0-9]+)/add_answer/$', views.AnswerCreate.as_view(), name='add-answer'),

    url(r'^question/(?P<pk>[0-9]+)/approve_answer/$', views.AnswerApprove.as_view(), name='approve-answer'),

    url(r'^question/(?P<pk>[0-9]+)/disapprove_answer/$', views.AnswerDisapprove.as_view(), name='disapprove-answer'),

    url(r'^question/(?P<pk>[0-9]+)/check_answer/$', views.CheckAnswer.as_view(), name='check-answer'),

    url(r'^approve_question/$', views.QuestionApprove.as_view(), name='approve-question'),

    url(r'^disapprove_question/$', views.QuestionDisapprove.as_view(), name='disapprove-question'),

    url(r'^question/(?P<pk>[0-9]+)/edit_question/$', views.QuestionUpdate.as_view(), name='edit-question'),

    url(r'^logout/$', auth_views.logout, name='user-logout'),

    url(r'^signin/$', auth_views.login, {'template_name': 'polls/login.html'}, name='user-login'),

    url(r'^add_tag/$', views.AddFilterTag.as_view(), name='add-tag'),

    url(r'^remove_tag/$', views.RemoveFilterTag.as_view(), name='remove-tag'),

    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-profile'),

    url(r'^user/(?P<pk>[0-9]+)/edit/$', views.UserUpdate.as_view(), name='edit-user'),

    url(r'^sort_questions/$', views.QuestionsSort.as_view(), name='sort-questions'),

    url(r'^get_maybe_tags/$', views.GetMaybeTags.as_view(), name='get-maybe-tags'),
]
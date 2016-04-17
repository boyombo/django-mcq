from django.conf.urls import url
from exam import views


urlpatterns = [
    url(r'^start/(?P<id>\d+)/$', views.start, name='start_exam'),
    url(r'^question/(?P<exam_id>\d+)/(?P<question_id>\d+)/$',
        views.get_question, name='exam_question'),
]

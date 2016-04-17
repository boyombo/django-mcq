from django.conf.urls import url
from exam import views


urlpatterns = [
    url(r'^start/(?P<id>\d+)/$', views.start, name='exam_start'),
    url(r'^end/(?P<exam_id>\d+)/$', views.end, name='exam_end'),
    url(r'^result/(?P<exam_id>\d+)/$', views.exam_result, name='exam_result'),
    url(r'^question/(?P<exam_id>\d+)/(?P<question_id>\d+)/$',
        views.get_question, name='exam_question'),
]

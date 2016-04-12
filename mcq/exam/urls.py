from django.conf.urls import url
from exam import views


urlpatterns = [
    url(r'start/(?P<id>\d+)/$', views.start, name='start_exam'),
]

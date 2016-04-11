from django.conf.urls import url
from question import views


urlpatterns = [
    url(r'batch/$', views.new_batch, name='new_batch'),
]

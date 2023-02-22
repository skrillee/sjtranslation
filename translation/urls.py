__author__ = 'Yan.zhe 2021.09.28'

from django.conf.urls import url
from translation import views
from django.views.generic import RedirectView
app_name = 'wechat'

urlpatterns = [
    url(r'^v1/translation/$', views.Translation.as_view()),
    url(r'^v1/translation/xml$', views.TranslationXml.as_view()),
]

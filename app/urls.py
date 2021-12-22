from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from tornado.web import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rest/<fact>/<reponse>', views.rest, name='rest'),
    #path('quiz_form', views.iframe, name='iframe'),
    path('quiz_form/', TemplateView.as_view(template_name="quizform.html"),
                   name='quizform'),
]

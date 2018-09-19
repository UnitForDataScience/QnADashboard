from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:question_id>', views.vote, name='vote'),
    path('results/<int:question_id>', views.results, name='vote'),
    path('details/<int:question_id>', views.detail, name='vote')
]

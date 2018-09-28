from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:question_id>', views.vote, name='vote'),
    path('results/<int:question_id>', views.results, name='vote'),
    path('summary', views.get_summary_keywords, name='vote')
]

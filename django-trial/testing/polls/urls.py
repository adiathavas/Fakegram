from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('Loginsuccess/', views.LoginsuccessView.as_view(), name='loginsuccess'),
    path('Post/', views.posting, name='posting'),
    path('Topic/', views.TopicView.as_view(), name='topic'),
]


from django.urls import path
from . import views


urlpatterns = [
    path('login', views.sign_in, name="sign in"),
    path('meta', views.MetaAPIView.as_view(), name="meta"),
    path('register/user', views.sign_up, name="sign up"),
    path('register/mentor', views.sign_up_mentor, name="sign up mentor"),
    path('users', views.UserView.as_view(), name="users"),
    path('users/<int:pk>', views.UserView.as_view(), name="users-by-id"),
    path('mentors', views.MentorView.as_view(), name="mentors"),
    path('mentors/<int:pk>', views.MentorView.as_view(), name="mentors-by-id"),
    path('posts/', views.ArticleView.as_view(), name="articles"),
    path('posts/<int:pk>', views.ArticleView.as_view(), name="articles-by-id"),
    path('contacts', views.ContactView.as_view(), name="contacts"),
    path('contacts/<int:pk>', views.ContactView.as_view(), name="contacts-by-id"),
    path('appointments', views.MentorAppointmentView.as_view(), name="appointments"),
    path('appointments/<int:pk>', views.MentorAppointmentView.as_view(), name="appointments-by-id"),
    path('categories', views.CategoryView.as_view(), name="categories"),
    path('categories/<int:pk>', views.CategoryView.as_view(), name="categories-by-id"),
    path('results', views.ResultView.as_view(), name="results"),
    path('results/<int:pk>', views.ResultView.as_view(), name="results-by-id"),
    path('events', views.EventView.as_view(), name="events"),
    path('events/<int:pk>', views.EventView.as_view(), name="events-by-id"),
]

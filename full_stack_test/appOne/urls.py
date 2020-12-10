from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('quotes', views.quotes),
    path('create', views.create),
    path('login', views.login),
    path('logout', views.logout),
    path('create_quote', views.create_quote),
    path('profile/<int:id>', views.profile),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('delete_quote/<int:id>', views.delete),
    path('like/<int:id>', views.like)
]

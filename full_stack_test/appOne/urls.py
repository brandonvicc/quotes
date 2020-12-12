from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name= 'create_account_page'),
    path('quotes', views.quotes, name= 'quotes'),
    path('create', views.create),
    path('login', views.login, name='login'),
    path('logout', views.logout),
    path('create_quote', views.create_quote),
    path('profile/<int:id>', views.profile),
    path('edit/<int:id>', views.edit, name= 'edit'),
    path('update/<int:id>', views.update),
    path('delete_quote/<int:id>', views.delete),
    path('like/<int:id>', views.like)
]

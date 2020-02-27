from django.urls import path

from . import views

urlpatterns = [

    # ********** paths that render page **********

    path('', views.index),
    path('user_dashboard', views.user_dashboard),
    path('add_book', views.add_book),
    path('book_info', views.book_info),
    path('user_page', views.user_page),


    # ***** paths that redirect to render page *****

    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('book_page', views.book_page),
    path('create_new_book', views.create_new_book),

]

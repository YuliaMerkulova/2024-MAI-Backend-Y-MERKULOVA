from django.urls import path
from films import views

urlpatterns = [
    path('all-profiles/', views.users, name='get_all_profiles'),
    path('all-films/', views.films, name='get_all_films'),
    path('profile/<int:user_id>', views.user, name='manage_profile'),
    path('profile/', views.user, name='create_profile'),
    path('film/<int:film_id>', views.film, name='manage_film'),
    path('film/', views.film, name='create_film'),
    path('rating/<int:user_id>/<int:film_id>', views.change_rating, name='change_rating'),
    path('likes/<int:user_id>/<int:film_id>', views.update_like, name='update_like'),
    path('search/q=<str:q>', views.search_films_by_filter, name='search_films'),
    path('search/', views.search_films_by_filter, name='search_films'),
]
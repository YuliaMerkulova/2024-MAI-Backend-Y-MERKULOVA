import json

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from homework3.films.models import Film, User, UserLike, Rating


@csrf_exempt
@require_http_methods(['GET'])
def films(request):
    film_objects = Film.objects.all()
    return JsonResponse({'films': [model_to_dict(film) for film in film_objects]})


@csrf_exempt
@require_http_methods(['GET'])
def users(request):
    film_objects = User.objects.all()
    return JsonResponse({'users': [model_to_dict(film) for film in film_objects]})


@csrf_exempt
@require_http_methods(['GET'])
def user(request, user_id):
    if request.method == "GET":
        current_user = User.objects.get(pk=user_id)
        return JsonResponse({'user': model_to_dict(current_user)})


@csrf_exempt
@require_http_methods(['GET'])
def film(request, film_id):
    if request.method == "GET":
        current_user = Film.objects.get(pk=film_id)
        return JsonResponse({'film': model_to_dict(current_user)})



@csrf_exempt
@require_http_methods(['PUT', 'POST'])
def change_rating(request, film_id, user_id):
    if film_id is None or user_id is None:
        return HttpResponseBadRequest({'error': 'film or user id is missing'})
    current_user = User.objects.get(pk=user_id)
    current_film = Film.objects.get(pk=film_id)
    if request.method == "PUT":
        rate = int(json.loads(request.body)['rate'])
        old_rate = Rating.objects.get(user_id=current_user, film_id=current_film)
        rate_delta = rate - old_rate['summ_rating']
        old_rate.update(summ_rating=rate)
        summ_rating = current_film['summ_rating'] + rate_delta
        current_film.update(summ_rating=summ_rating)
        return JsonResponse({'status': "ok"})
    elif request.method == "POST":
        rate = int(json.loads(request.body)['rate'])
        Rating.objects.create(user_id=current_user, film_id=current_film, rate=rate)
        summ_rating = current_film['summ_rating'] + rate
        count_rating = current_film['count_rating'] + 1
        current_film.update(summ_rating=summ_rating, count_rating=count_rating)
        return JsonResponse({'status': "ok"})


@csrf_exempt
@require_http_methods(['DELETE', 'POST'])
def update_like(request, film_id, user_id):
    if film_id is None or user_id is None:
        return HttpResponseBadRequest({'error': 'film or user id is missing'})
    current_user = User.objects.get(pk=user_id)
    current_film = Film.objects.get(pk=film_id)
    if request.method == 'DELETE':
        UserLike.objects.get(film_id=current_film, user_id=current_user).delete()
        return JsonResponse({'status': 'ok'})
    elif request.method == 'POST':
        UserLike.objects.create(film_id=current_film, user_id=current_user)
        return JsonResponse({'status': 'ok'})

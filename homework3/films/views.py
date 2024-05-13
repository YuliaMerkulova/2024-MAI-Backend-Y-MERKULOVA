import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from films.models import Film, User, UserLike, Rating


@csrf_exempt
@require_http_methods(['GET'])
def films(request):
    film_objects = Film.objects.all()
    return JsonResponse({'films': [model_to_dict(film) for film in film_objects]})


@csrf_exempt
@require_http_methods(['GET'])
def users(request):
    user_objects = User.objects.all()
    return JsonResponse({'users': [model_to_dict(film) for film in user_objects]})


@csrf_exempt
@require_http_methods(['GET', 'DELETE', 'POST'])
def user(request, user_id=None):
    if request.method == "GET":
        if user_id is None or user_id <= 0:
            return HttpResponseBadRequest('Invalid or missing user id')
        try:
            current_user = User.objects.get(pk=user_id)
        except:
            return HttpResponseBadRequest('Invalid user id')
        return JsonResponse({'user': model_to_dict(current_user)})

    elif request.method == "DELETE":
        if user_id is None or user_id <= 0:
            return HttpResponseBadRequest('Invalid or missing user id')
        try:
            current_user = User.objects.get(pk=user_id).delete()
        except:
            return HttpResponseBadRequest('Invalid user id')
        return JsonResponse({'status': 'ok'})

    elif request.method == "POST":
        user_data = json.loads(request.body)['user']
        User.objects.create(login=user_data['login'], age=user_data['age'], password=user_data['password'])
        return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_http_methods(['GET', 'DELETE', 'POST'])
def film(request, film_id=None):
    if request.method == "GET":
        if film_id is None or film_id <= 0:
            return HttpResponseBadRequest('Invalid or missing film id')
        try:
            current_film = Film.objects.get(pk=film_id)
        except:
            return HttpResponseBadRequest('Invalid film id')

        return JsonResponse({'film': model_to_dict(current_film)})

    elif request.method == "DELETE":
        if film_id is None or film_id <= 0:
            return HttpResponseBadRequest('Invalid or missing film id')
        try:
            current_film = Film.objects.get(pk=film_id).delete()
        except:
            return HttpResponseBadRequest('Invalid film id')

        return JsonResponse({'status': 'ok'})

    elif request.method == "POST":
        film_data = json.loads(request.body)
        Film.objects.create(
            name=film_data['name'],
            description=film_data['description'],
            genre=film_data['genre'],
            year=film_data['year'],
            time=film_data['time'],
            director=film_data['director'],
            summ_rating=0, count_rating=0
        )
        return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_http_methods(['PUT', 'POST'])
def change_rating(request, film_id, user_id):
    if film_id is None or user_id is None:
        return HttpResponseBadRequest({'error': 'film or user id is missing'})
    try:
        current_user = User.objects.get(pk=user_id)
    except:
        return HttpResponseBadRequest({'error': 'Invalid user id'})

    try:
        current_film = Film.objects.get(pk=film_id)
    except:
        return HttpResponseBadRequest({'error': 'Invalid film id'})

    if request.method == "PUT":
        rate = int(json.loads(request.body)['rate'])
        try:
            old_rate = Rating.objects.get(user_id=current_user, film_id=current_film)
        except:
            return HttpResponseBadRequest({'error': 'Invalid user id or film id'})
        rate_delta = rate - old_rate.rate
        old_rate.summ_rating = rate
        old_rate.save()
        summ_rating = current_film.summ_rating + rate_delta
        current_film.summ_rating = summ_rating
        current_film.save()
        return JsonResponse({'status': "ok"})

    elif request.method == "POST":
        rate = int(json.loads(request.body)['rate'])
        try:
            Rating.objects.create(user_id=current_user, film_id=current_film, rate=rate)
        except:
            return HttpResponseBadRequest({'error': 'You need use PUT to re-rating film'})
        summ_rating = current_film.summ_rating + rate
        count_rating = current_film.count_rating + 1

        current_film.summ_rating = summ_rating
        current_film.count_rating = count_rating
        current_film.save()
        return JsonResponse({'status': "ok"})


@csrf_exempt
@require_http_methods(['DELETE', 'POST'])
def update_like(request, film_id, user_id):
    if film_id is None or user_id is None:
        return HttpResponseBadRequest({'error': 'film or user id is missing'})
    try:
        current_user = User.objects.get(pk=user_id)
    except:
        return HttpResponseBadRequest({'error': 'Invalid user id'})

    try:
        current_film = Film.objects.get(pk=film_id)
    except:
        return HttpResponseBadRequest({'error': 'Invalid film id'})

    if request.method == 'DELETE':
        try:
            UserLike.objects.get(film_id=current_film, user_id=current_user).delete()
        except:
            return HttpResponseBadRequest({'error': 'Invalid film or user id'})
        return JsonResponse({'status': 'ok'})
    elif request.method == 'POST':
        try:
            UserLike.objects.create(film_id=current_film, user_id=current_user)
        except:
            return HttpResponseBadRequest({'error': 'You have already liked this film'})
        return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_http_methods(['GET'])
def search_films_by_filter(request, q=None):

    if q is None or q.isspace() or q == '':
        films = Film.objects.all()
    else:
        films = Film.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

    context = {'films': [model_to_dict(film_) for film_ in films]}
    return JsonResponse(context)

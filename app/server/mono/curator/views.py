from django.http import JsonResponse
from django.core import serializers

from .models import Artist, Exhibition
from .similar import Similar

def exhibition(request, pk):
    content = {
        'artists': [],
        'errors': None,
        'title': None,
        'url': None,
    }
    exh = Exhibition.objects.get(pk=pk)
    content['artists'] = serialize_artists(exh.artist_set.all())
    content['title'] = exh.title
    content['url'] = exh.moma_url
    return JsonResponse(content)

def similar(request, token):
    tokens = Similar().get_ten(token)
    artists = get_artists_from_tokens(tokens)
    content = {
        'original_token': token,
        'artists': serialize_artists(artists),
    }
    return JsonResponse(content)

def get_artists_from_tokens(tokens):
    return [Artist.objects.get(token=t) for t in tokens]

def serialize_artists(artists):
    content = []
    for a in artists:
        content.append({
            'display_name': a.display_name,
            'token': a.token,
            'moma_url': a.moma_url,
        })
    return content
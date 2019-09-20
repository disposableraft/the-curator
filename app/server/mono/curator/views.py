from django.http import JsonResponse
from django.core import serializers

from .models import Exhibition

def exhibition(request, pk):
    content = {
        'artists': [],
        'errors': None,
        'title': None,
    }
    try:
        exh = Exhibition.objects.get(pk=pk)
        content['title'] = exh.title
        content['artists'] = serialize_artists(exh.artist_set.all())
    except Exhibition.DoesNotExist:
        content['errors'] = "Resource does not exist."
    return JsonResponse(content)

def serialize_artists(artists):
    content = []
    for a in artists:
        content.append({
            'first_name': a.first_name,
            'last_name': a.last_name,
            'full_name': a.full_name(),
            'token': a.token,
        })
    return content
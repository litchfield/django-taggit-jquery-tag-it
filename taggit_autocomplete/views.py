from django.http import HttpResponse, HttpResponseBadRequest
try:
    from django.utils import simplejson
except ImportError:
    import json as simplejson  # noqa

from taggit.models import Tag


def list_tags(request):
    """List all tags that start with the given query"""

    query = request.GET.get('q', None)
    if request.method != 'GET' or not query:
        return HttpResponseBadRequest()

    try:
        tags = Tag.objects.filter(
            name__istartswith=query).values_list('name', flat=True)
    except:  # Naked except, we may not have access to hvad
        tags = Tag.objects.language().filter(
            name__istartswith=query).values_list('name', flat=True)

    tags = list(tags)
    return HttpResponse(simplejson.dumps(tags), content_type='text/javascript')

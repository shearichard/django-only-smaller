import inspect
from functools import wraps

from django.http import HttpResponse

from .models import CountLog


def ensure_http_response(view_fn):
    """
    If a view returns a plain string value, convert it into an HttpResponse
    """
    if inspect.iscoroutinefunction(view_fn):

        @wraps(view_fn)
        async def wrapped(*args, **kwargs):
            response = await view_fn(*args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            return HttpResponse(response)

    else:

        @wraps(view_fn)
        def wrapped(*args, **kwargs):
            response = view_fn(*args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            return HttpResponse(response)

    return wrapped


@ensure_http_response
def count(request):
    CountLog.objects.create()
    return f"<p>Number of page loads: {CountLog.objects.count()}</p>"


@ensure_http_response
async def slow(request):
    import asyncio

    await asyncio.sleep(10)
    return "Async views supported"

from typing import List, Union, Callable, Type, Any

from django import urls
from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern
from django.views import View

__all__ = (
    'path',
    're_path',
)


def _url(path_func: Callable[..., URLPattern], urlpatterns: List, partial: str, *args, **kwargs):
    def decorator(view: Union[Callable[..., HttpResponse], Type[View]]) -> Any:
        assert callable(view) or issubclass(view, View)

        urlpatterns.append(path_func(partial, view if callable(view) else view.as_view(), *args, **kwargs))

        return view
    return decorator


def path(urlpatterns: List, partial: str, *args, **kwargs):
    """

    :param urlpatterns:
    :type urlpatterns: list
    :param partial:
    :type partial: str
    :raise AssertionError:
    """

    return _url(urls.path, urlpatterns, partial, *args, **kwargs)


def re_path(urlpatterns: List, partial: str, *args, **kwargs):
    """

    :param urlpatterns:
    :param partial:
    :param args:
    :param kwargs:
    :raise AssertionError:
    """

    return _url(urls.re_path, urlpatterns, partial, *args, **kwargs)

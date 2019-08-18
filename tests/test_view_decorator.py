from unittest import TestCase

from django import urls
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from django_recipes import path, re_path


class TestViewDecorator(TestCase):
    def setUp(self):
        self.urlpatterns = []

        class SomeView(TemplateView):
            pass

        def some_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            pass

        self.SomeView = SomeView
        self.some_view = some_view

    def test_configuring_url_path_for_class_based_view(self):
        partial = '/test/'

        self.assertIs(
            self.SomeView,
            path(self.urlpatterns, partial, name='test')(self.SomeView),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.path('/test/', self.SomeView.as_view(), name='test')]),
        )

    def test_configuring_url_re_path_for_class_based_view(self):
        # language=PythonRegExp
        pattern = r'/\d{3}/'

        self.assertIs(
            self.SomeView,
            re_path(self.urlpatterns, pattern, name='test')(self.SomeView),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.re_path(pattern, self.SomeView.as_view(), name='test')]),
        )

    def test_configuring_url_path_for_function_based_view(self):
        partial = '/test/'

        self.assertIs(
            self.some_view,
            path(self.urlpatterns, partial, name='test')(self.some_view),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.path('/test/', self.some_view, name='test')]),
        )

    def test_configuring_url_re_path_for_function_based_view(self):
        # language=PythonRegExp
        pattern = r'/\d{3}/'

        self.assertIs(
            self.SomeView,
            re_path(self.urlpatterns, pattern, name='test')(self.some_view),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.re_path(pattern, self.some_view, name='test')]),
        )

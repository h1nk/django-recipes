from unittest import TestCase

from django import urls
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from django_recipes import path, re_path


class TestViewDecorator(TestCase):
    def setUp(self):
        self.urlpatterns = []

        self.partial = '/test/'
        # language=PythonRegExp
        self.pattern = r'/\d{3}/'
        self.view_name = 'test'

        class SomeView(TemplateView):
            pass

        def some_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            pass

        self.SomeView = SomeView
        self.some_view = some_view

    def test_configuring_url_path_for_class_based_view(self):

        self.assertIs(
            self.SomeView,
            path(self.urlpatterns, self.partial, self.view_name)(self.SomeView),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.path(self.partial, self.SomeView.as_view(), self.view_name)]),
        )

    def test_configuring_url_re_path_for_class_based_view(self):
        self.assertIs(
            self.SomeView,
            re_path(self.urlpatterns, self.pattern, self.view_name)(self.SomeView),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.re_path(self.pattern, self.SomeView.as_view(), self.view_name)]),
        )

    def test_configuring_url_path_for_function_based_view(self):
        self.assertIs(
            self.some_view,
            path(self.urlpatterns, self.partial, self.view_name)(self.some_view),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.path(self.partial, self.some_view, self.view_name)]),
        )

    def test_configuring_url_re_path_for_function_based_view(self):
        self.assertIs(
            self.some_view,
            re_path(self.urlpatterns, self.pattern, self.view_name)(self.some_view),
        )

        self.assertEqual(
            repr(self.urlpatterns),
            repr([urls.re_path(self.pattern, self.some_view, self.view_name)]),
        )

from unittest import TestCase

from django_recipes import group


class TestGroupFunction(TestCase):
    def test_group_found_equal_sized_slices(self):
        for chunk in group(['A', 'B', 'C']*3, 3):
            self.assertEqual(
                ('A', 'B', 'C'),
                chunk,
            )

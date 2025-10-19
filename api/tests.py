from django.test import TestCase
from api.models import Game, Word
from api.utils import color_word

class ColorWordTestCase(TestCase):
    def test_all_correct(self):
        self.assertEqual(color_word('HELLO', 'HELLO'), 'GGGGG')
    
    def test_all_wrong(self):
        self.assertEqual(color_word('ABCDE', 'FGHIJ'), 'BBBBB')
    
    def test_duplicate_letters(self):
        # Test the bug you fixed!
        self.assertEqual(color_word('SPEED', 'ERASE'), 'YBGBY')
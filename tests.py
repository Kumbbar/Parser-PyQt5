from saver import ParsingSaver
from main import user_settings, headers
import unittest


class TestParsingSaver(unittest.TestCase):
    maxDiff = 4000

    def setUp(self) -> None:
        self.saver = ParsingSaver(user_settings, 'https://dem-blog.herokuapp.com/')

    def test_get_status_code1(self):
        status_code = self.saver.get_status_code(headers)
        self.assertEqual(status_code, 200)

    def test_get_status_code2(self):
        self.saver.url += 'this_page_does_not_exist/'
        status_code = self.saver.get_status_code(headers)
        self.assertNotEqual(status_code, 200)

    def test_get_html(self):
        html = self.saver.get_html(headers)
        self.assertNotEqual(html, '')


if __name__ == '__main__':
    unittest.main()

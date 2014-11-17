from selenium import webdriver
import unittest


class AdminPageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_adminInstalled(self):
        self.browser.get('http://localhost:8000/admin/')
        assert 'Django' in self.browser.title
        assert 'admin' in self.browser.title


if __name__ == '__main__':
    unittest.main()

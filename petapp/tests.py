from django.test import TestCase
from petapp import views

# Create your tests here.
class DemoTest(TestCase):
    def test_demofn(self):
        # assert views.demofn()=='Welcome'
        resp=views.demofn()
        self.assertEqual(first='welcome',second=resp,msg='Got unexpected respose from function')
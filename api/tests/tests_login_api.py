from django.urls import reverse
from rest_framework.test import APITestCase



class LoginUserAPIViewTests(APITestCase):
    #resolvemos la url llamada login
    login_url = reverse("login")
    usuarios_url = reverse("usuarios_list")

    def setUp(self):
        data = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'pruebaLogin',
            'email': 'email@pruebalogin.com',
            'password':  '12345',
            'bank_account': '12345678901234567890'
        }
        self.client.post(self.usuarios_url, data, format='json')


    def test_login_user(self):
        data = {
            'username': 'pruebaLogin',
            'password':  '12345',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    
    def test_bad_password_login_user(self):
        data = {
            'username': 'pruebaLogin',
            'password':  '12325',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 406)
    

    def test_bad_user_login_user(self):
        data = {
            'username': 'nonexist',
            'password':  '12345',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 500)


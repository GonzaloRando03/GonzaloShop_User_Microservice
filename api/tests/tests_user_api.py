from django.urls import reverse
from rest_framework.test import APITestCase


class CreateUserAPIViewTests(APITestCase):
    #resolvemos la url llamada usuarios_list
    usuarios_url = reverse("usuarios_list")

    def setUp(self):
        pass


    def test_post_user(self):
        data = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba',
            'email': 'email@prueba.com',
            'password':  '12345',
            'bank_account': '12345678901234567890'
        }
        response = self.client.post(self.usuarios_url, data, format='json')
        self.assertEqual(response.status_code, 201)



    def test_bad_user_post_user(self):
        databad = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'as',
            'email': 'email@prueba.com',
            'password':  'prueba',
            'bank_account': '12345678901234567890'
        }
        response = self.client.post(self.usuarios_url, databad, format='json')
        self.assertEqual(response.status_code, 411)



    def test_bad_password_post_user(self):
        databad = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba',
            'email': 'email@prueba.com',
            'password':  'as',
            'bank_account': '12345678901234567890'
        }
        response = self.client.post(self.usuarios_url, databad, format='json')
        self.assertEqual(response.status_code, 411)


    def test_bad_bank_account_post_user(self):
        databad = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba',
            'email': 'email@prueba.com',
            'password':  'prueba',
            'bank_account': '678901234567890'
        }
        response = self.client.post(self.usuarios_url, databad, format='json')
        self.assertEqual(response.status_code, 411)

    
    def test_repeat_username_post_user(self):
        data1 = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba',
            'email': 'email@prueba.com',
            'password':  'prueba',
            'bank_account': '12345678901234567890'
        }
        data2 = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba',
            'email': 'email@prueba2.com',
            'password':  'prueba',
            'bank_account': '12345678901234567890'
        }
        self.client.post(self.usuarios_url, data1, format='json')
        response = self.client.post(self.usuarios_url, data2, format='json')
        self.assertEqual(response.status_code, 500)

    
    def test_repeat_email_post_user(self):
        data1 = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba1',
            'email': 'email@prueba.com',
            'password':  'prueba',
            'bank_account': '12345678901234567890'
        }
        data2 = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba2',
            'email': 'email@prueba.com',
            'password':  'prueba',
            'bank_account': '12345678901234567890'
        }
        self.client.post(self.usuarios_url, data1, format='json')
        response = self.client.post(self.usuarios_url, data2, format='json')
        self.assertEqual(response.status_code, 500)



class AddMoneyUserAPIViewTests(APITestCase):
    #resolvemos la url llamada usuarios_list
    usuarios_url = reverse("usuarios_list")

    def setUp(self):
        data = {
            'name': 'prueba',
            'lastname': 'prueba',
            'username': 'prueba',
            'email': 'email@prueba.com',
            'password':  '12345',
            'bank_account': '12345678901234567890'
        }
        self.client.post(self.usuarios_url, data, format='json')


    def test_add_money_user(self):
        data = {
            'username': 'prueba',
            'money': 10,
        }
        response = self.client.put(self.usuarios_url, data, format='json')
        self.assertEqual(response.status_code, 200)


    def test_bad_add_money_user(self):
        data = {
            'username': 'nonexist',
            'money': 10,
        }
        response = self.client.put(self.usuarios_url, data, format='json')
        self.assertEqual(response.status_code, 500)


    def test_add_much_money_user(self):
        data = {
            'username': 'prueba',
            'money': 1001,
        }
        response = self.client.put(self.usuarios_url, data, format='json')
        self.assertEqual(response.status_code, 500)

   



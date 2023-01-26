from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from ..models import Usuario, Monedero
import bcrypt
import json
import jwt
import os

#Creamos las clases que manejen las peticiones http.

class LoginView(View):

    #Función dispatch se ejecuta cada vez que llegue una petición. Usando los decoradores conseguimos que se procesen todas las peticiones
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        pass


    #funcion para loguear usuario
    def post(self, request):
        userRequest = json.loads(request.body)

        try:
            userDB = Usuario.objects.filter(username = userRequest['username']).first()

            if not userDB:
                return JsonResponse({'error': 'Usuario no existente'}, status=500)

            password = str(userRequest['password']).encode()
            hashed = userDB.password

            if bcrypt.checkpw(password, hashed):
                #creamos el token 
                userForToken = {
                    'username': userDB.username,
                    'id': userDB.id
                }
                token = jwt.encode(userForToken, os.environ['TOKEN'], algorithm="HS256")

                userWallet = Monedero.objects.filter(usuario_id = userDB.pk).first()

                responseData = {
                    'id': userDB.id,
                    'name': userDB.name,
                    'lastname': userDB.lastname,
                    'username': userDB.username,
                    'bank_account': userDB.bank_account,
                    'wallet':{
                        'cantidad': userWallet.cantidad,
                        'limite': userWallet.limite,
                        'descuento': userWallet.descuento
                    },
                    'token': token
                }
                
                return JsonResponse(responseData, status=201)

            else:
                return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=406)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=406)


    def put(self, request):
        pass


    def delete(self, request):
        pass
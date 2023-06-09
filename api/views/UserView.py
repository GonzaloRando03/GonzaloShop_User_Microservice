from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db import IntegrityError
from ..models import Usuario, Monedero
import bcrypt
import json
import jwt
import os


#Creamos las clases que manejen las peticiones http.
class UserView(View):

    #Función dispatch se ejecuta cada vez que llegue una petición. Usando los decoradores conseguimos que se procesen todas las peticiones
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        pass


    #funcion para crear usuario
    def post(self, request):
        user = json.loads(request.body)

        try:
            #comprobamos los datos
            if len(user['password']) < 3 or len(user['username']) < 3 or len(user['bank_account']) < 20:
                return JsonResponse({"error": "Username o password demasiado cortos"}, status=411)
            
            #ciframos la contraseña            
            saltRounds = bcrypt.gensalt()
            passwordEncode = str(user['password']).encode()
            passwordHash = bcrypt.hashpw(passwordEncode, saltRounds)
            
            #guardamos al usuario en la db
            userDB = Usuario(
                name = user['name'],
                lastname = user['lastname'],
                username = user['username'],
                email = user['email'],
                password = passwordHash,
                bank_account = user['bank_account']
            )
            userDB.save()
            
            #creamos su monedero
            wallet = Monedero(
                usuario = userDB,
                cantidad = 0,
                limite = 1000,
                descuento = 20
            )
            wallet.save()

            #creamos el token 
            userForToken = {
                'username': userDB.username,
                'id': userDB.id
            }

            token = jwt.encode(userForToken, os.environ['TOKEN'], algorithm="HS256")

            responseData = {
                    'id': userDB.id,
                    'name': userDB.name,
                    'lastname': userDB.lastname,
                    'username': userDB.username,
                    'bank_account': userDB.bank_account,
                    'wallet':{
                        'cantidad': wallet.cantidad,
                        'limite': wallet.limite,
                        'descuento': wallet.descuento
                    },
                    'token': token
                }
            
            return JsonResponse(responseData, status=201)

        
        #execpt para usernames y emails ya guardados en la base de datos.
        except IntegrityError as e:
            error = str(e.args)
            print(error)

            if "email" in error:
                return JsonResponse({"error": "El email está en uso"}, status=500)

            elif "username" in error:
                return JsonResponse({"error": "El nombre de usuario está en uso"}, status=500)

            else:
                 return JsonResponse({"error": "Error en los datos"}, status=500)


        #execpt global
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error en los datos"}, status=500)


    #función para añadir dinero al monedero
    def put(self, request):
        req = json.loads(request.body)
        try:
            user = Usuario.objects.filter(username = req['username']).first()
            userWallet = Monedero.objects.filter(usuario_id = user.pk).first()

            #comprobamos límite del monedero
            if userWallet.cantidad + req['money'] > 1000:
                return JsonResponse({"error": "Límite de monedero alcanzado"}, status=500)

            userWallet.cantidad = userWallet.cantidad + req['money']
            userWallet.save()

            responseData = {
                'cantidad': userWallet.cantidad
            }

            return JsonResponse(responseData, status=200)
            
            
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error al realizar la transferencia"}, status=500)



    #función para eliminar un usuario
    def delete(self, request):
        try:
            token = request.headers['Authorization']
            decodedToken = jwt.decode(token, os.environ['TOKEN'], algorithms=["HS256"])
            

            if not token or not decodedToken['id']:
                return JsonResponse({"error": "Token inválido o ausente"}, status=401)

            user = Usuario.objects.filter(id = decodedToken['id']).first()

            if not user:
                return JsonResponse({"error": "Token inválido"}, status=401)

            monedero = Monedero.objects.filter(usuario_id = decodedToken['id']).first()

            if not monedero:
                return JsonResponse({"error": "Problemas con el monedero"}, status=401)

            monedero.delete()
            user.delete()

            return JsonResponse({"msg": "Eliminado correctamente"}, status=200)
        
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error al eliminar el usuario"}, status=500)
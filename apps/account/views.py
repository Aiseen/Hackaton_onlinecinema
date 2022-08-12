from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from apps.account.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, \
    ForgotPasswordSerializer, ForgotPasswordCompleteSerializer

User = get_user_model()

class RegisterView(APIView):
 def post(self,request):
        data = request.data
        serializers = RegisterSerializer(data=data)

        if serializers.is_valid(raise_exception=True):
            serializers.save()
            message = f'Вы смогли зарегаться.Чекните почту'
            return Response(message, status=201)

class ActivationView(APIView):
    def get(self,request,activation_code):
        try:
            user = User.objects.get(activation_code = activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Успешно'}, status=200 )
        except User.DoesNotExist:
            return Response({'msg': 'Неверный код!'}, status=400)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data,
                                               context={'request': request})

        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Пароль был обновлен успешно.')


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли с аккаунта.')



class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено письмо для восстановления пароля,с уважением КИНО ОТ АЙСЕНА')


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Пароль успешно был обновлен')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .models import *
import jwt, datetime


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            return AuthenticationFailed('User not Found')
        if not user.check_password(password):
            return AuthenticationFailed('Incorrect Password!')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response
    

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('User not found!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully Logout'
        }
        return response
    

class Quiz(generics.ListAPIView):
    serializer_class = QuizSerializer
    queryset = Quizzes.objects.all()


class RandomQuesions(APIView):
    def get(self, request, format: None, **kwargs):
        question = Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1]
        serializer = RandomQuesionsSerializer(question, many = True)
        return Response(serializer.data)
    

class QuizQuesions(APIView):
    def get(self, request, format: None, **kwargs):
        question = Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1]
        serializer = QuizQuesionsSerializer(question, many = True)
        return Response(serializer.data)
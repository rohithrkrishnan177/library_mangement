from django.db.models import fields
from django.conf import settings
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from .models import Student
from .serializers import UserSerializer,StudentSerializer
from django.http import response
from rest_framework.response import Response
from rest_framework import status
import requests
from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.db.models import F
from .models import BookModel, IssueBook, ReturnBook, Student
from .serializers import BookModelSerializer, IssueBookSerializer, ReturnBookSerializer, StudentSerializer
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication



class BookView(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ["admin"]
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer


class StudentView(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ["student"]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class IssueBookView(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ["student"]
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer

    def create(self, request):
        book = BookModel.objects.filter(id=request.data['bookid2'])
        for i in book:
            if i.quantity != 0:
                i.quantity = i.quantity - 1
                BookModel.objects.filter(id=request.data['bookid2']).update(quantity=i.quantity)
                super().create(request)
                return Response("Request Accepeted! ")
            else:
                return Response("book is not available...")


class ReturnBookView(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ["student"]
    queryset = ReturnBook.objects.all()
    serializer_class = ReturnBookSerializer

    def create(self, request):
        super().create(request)
        issue_book = IssueBook.objects.get(id=request.data['issuebook_id'])
        BookModel.objects.filter(id=issue_book.bookid2.id).update(quantity=F('quantity') + 1)

        return Response("success! your Book is returned. ")

class AdminLoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        try:
            r = requests.post(
                settings.URL_TYPE + "/o/token/",
                data={
                    "grant_type": "password",
                    "username": user.username,
                    "password": request.data["password"],
                    "client_id": settings.CLIENT_ID,
                    "client_secret": settings.CLIENT_SECRET,
                    # "scope": "admin",
                },
                verify=False,
            )

            if r.status_code == 200:
                response = r.json()
                details = {}
                details.update(
                    {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                    }
                )

                response.update({"details": details})
                return Response(response)
            else:
                if r.status_code == 500:
                    print(r)
                return Response(r.json(), r.status_code)
        except Exception as e:
            print(e)
            pass
            return Response("error")


class TokenView(APIView):
    def post(self, request):
        try:
            r = requests.post(
                settings.URL_TYPE + "/o/token/",
                data={
                    "grant_type": "refresh_token",

                    "refresh_token": request.data["refresh_token"],
                    "client_id": settings.CLIENT_ID,
                    "client_secret": settings.CLIENT_SECRET,
                    # "scope": "admin",
                },
                verify=False,
            )

            if r.status_code == 200:
                response = r.json()
                # print(response)
                # setRefreshTokenExpiry(response["refresh_token"])
                details = {}
                details.update(
                    {
                        "refresh_token": request.data["refresh_token"]

                    }
                )

                response.update({"details": details})
                return Response(response)
            else:
                if r.status_code == 500:
                    print(r)
                return Response(r.json(), r.status_code)
        except Exception as e:
            print(e)
            pass
            return Response("error")



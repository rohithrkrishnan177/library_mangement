from django.db.models import Q
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate
from .models import User
from django.urls import reverse
from rest_framework import serializers, status


from .models import BookModel, IssueBook, ReturnBook, Student,User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = User.objects.filter(
                (Q(username=username))
            ).first()
            if user and authenticate(username=username, password=password):
                data["user"] = user

            else:
                msg = "Unable to login with given credentials."
                raise exceptions.AuthenticationFailed({"username": [msg]})
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError({"username": [msg]})
        return data





class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = Student
        fields = [
            "id",
            "user_id",
            "student_name",
            "phone",
            "password"
        ]

    def create(self, validated_data):
        user = User()

        user.username = validated_data["student_name"]
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        student = Student()
        student.student_name = validated_data["student_name"]
        student.phone = validated_data["phone"]
        student.user_id = user
        student.save()

        return student


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = '__all__'


class IssueBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueBook
        fields = '__all__'


class ReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnBook
        fields = '__all__'
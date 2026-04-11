# from django.contrib.auth.models import User
# from rest_framework import serilaizers

# class RegisterSerializer(serilaizers.ModelSerializer):
#     class Meta:
#         model = User
#         fields=['username','password','mail']
'''it was not importent to write  if their is anyother function is called instead for User 
    but becasue we have to store password in hassed formed so we hav to use it with
    "create_user" it store the pass in hased form
    It get's auomatically called then .save() is called
    as **validate_data takes all the values and variables to store and valedate the data'''
    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)
'''To be more accurate'''
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    '''all validated_data is automatically called when is _valid() is called and if every data is correct 
    then all the data is in clean formate and goes into validated_data.
    and then .save() is called then create runs auomatically and it has pass validated_data which is valied and verified 
    s it get's created .'''



    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
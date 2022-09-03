import profile
from this import d
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.auth.models import User
from home.models import CompanyEmail
from .models import Profile, Address, UserEmail, UserPhone
from .serializers import ProfileSz, AddressSz, UserEmailSz, UserPhoneSz
from rest_framework import viewsets
from django.core.mail import EmailMultiAlternatives
import pyotp
from django.core.mail import get_connection
from datetime import datetime
import base64
from rest_framework.permissions import IsAuthenticated


class generateKey:
    @staticmethod
    def returnValue(email):
        return str(email) + str(datetime.date(datetime.now())) + "base32secret3232"


def gen_otp(email, counter, key):
    hotp = pyotp.HOTP(key)
    otp = hotp.at(counter)
    print('genrated otp is>>', otp)
    return otp


def send_email(to, subject, text_content):
    try:
        email = CompanyEmail.objects.all().first()
        connection = get_connection(
            host=email.host,
            username=email.user,
            password=email.password,
            use_tls=email.use_tls,
            port=email.port,
        )
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            email,
            [to],
            connection=connection,
        )
        msg.send(fail_silently=True)
    except Exception as e:
        print(f"unable to send email, {e}")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def CreateUserApi(request):
    user = User.objects.create_user(**request.data)
    if "mark_superuser" in request.data and request.data["mark_superuser"] == True:
        request.pop("mark_superuser")
        user.is_superuser = True
        user.save()

    user_email, created = UserEmail.objects.get_or_create(user=user)
    sz = UserEmailSz(instance=user_email, data=request.data, partial=True)
    if sz.is_valid(raise_exception=True):
        user_email = sz.save()
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(user_email.email).encode())
        otp = gen_otp(user_email.email, user_email.counter, key=key)
        user_email.update_count()
        send_email(
            to=user_email.email,
            subject="OTP for Authentication",
            text_content=f"your Authentication OTP is {otp}.",
        )

    user_phone, created = UserPhone.objects.get_or_create(user=user)
    sz = UserPhoneSz(instance=user_phone, data=request.data, partial=True)
    if sz.is_valid(raise_exception=True):
        sz.save()
        return Response({"success": ["user is created successfully"]})

    return Response({"error": ["user not signed in"]}, status=404)


@api_view(["POST"])
def validate_Signup_otp(request):
    otp = request.data.get("OTP", None)
    email = request.data.get("email", None)
    if email is None:
        return Response({"error": ["email not provided"]})
    if otp is None:
        return Response({"error": ["OTP not provided"]})
    user_email = UserEmail.objects.get(email=email)
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(user_email.email).encode())
    OTP = pyotp.HOTP(key)
    if OTP.verify(otp, user_email.counter-1):
        user_email.is_verified = True
        user_email.save()
        profile, created = Profile.objects.get_or_create(
            user=user_email.user, name=user_email.user.username
        )
        sz = ProfileSz(instance=profile)
        return Response(sz.data)
    raise exceptions.ValidationError("provided OTP is not a valid")


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_profileApi(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == "GET":
        sz = ProfileSz(instance=profile)
        return Response(sz.data)
    else:
        sz = ProfileSz(instance=profile, data=request.data, partial=True)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data)


class OrderAddressApi(viewsets.ModelViewSet):
    serializer_class = AddressSz

    def get_queryset(self):
        return Address.objects.all()

    def perform_create(self, serializer):
        return super().perform_create(serializer)


@api_view(["POST"])
def forgot_passwordApi(request):
    """
    # send otp to the given email
    1. genrate the opt for the email
    2. send the opt to the email
    """
    email = request.data.get("email", None)
    if email is None:
        return Response({"error": ["email not provided"]}, status=400)
    user_email = UserEmail.objects.filter(email=email).first()
    if user_email is None:
        return Response({"error":["Email not found"]}, status=404)
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(user_email.email).encode())
    otp = gen_otp(user_email.email, user_email.counter, key=key)
    user_email.update_count()
    send_email(
        to=user_email.email,
        subject="OTP for change password",
        text_content=f"your OTP is {otp}.",
    )
    return Response({"success":True})
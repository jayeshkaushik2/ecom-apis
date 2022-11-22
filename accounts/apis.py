from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import exceptions
from home.models import CompanyEmail
from .models import Profile, Address, UserEmail, UserPhone
from .serializers import (
    ProfileSz,
    AddressSz,
    UserEmailSz,
    UserPhoneSz,
    UserSz,
    UserOrderSz,
)
from rest_framework import viewsets
from django.core.mail import EmailMultiAlternatives
import pyotp
from django.core.mail import get_connection
from datetime import datetime
import base64
from rest_framework.permissions import IsAuthenticated
from order.models import Order
from order.serializers import OrderSz
from django.contrib.auth import get_user_model
import django_filters

User = get_user_model()


class generateKey:
    @staticmethod
    def returnValue(email):
        return str(email) + str(datetime.date(datetime.now())) + "base32secret3232"


def gen_otp(email, counter, key):
    hotp = pyotp.HOTP(key)
    otp = hotp.at(counter)
    print("genrated otp is>>", otp)
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
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def CreateUserApi(request):
    # TODO have to handle unique key constraint failed error
    user = User(
        first_name=request.data.get("first_name"),
        last_name=request.data.get("last_name"),
        username=request.data.get("username"),
        email=request.data.get("email"),
        mobile=request.data.get("mobile"),
    )
    user.set_password(request.data.get("password"))
    user.save()
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
    user_email = UserEmail.objects.filter(email=email).first()
    if user_email is None:
        return Response({"error": ["email not found"]})
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(user_email.email).encode())
    OTP = pyotp.HOTP(key)
    if OTP.verify(otp, user_email.counter - 1):
        user_email.is_verified = True
        user_email.save()
        user_email.update_count()
        profile, created = Profile.objects.get_or_create(
            user=user_email.user, name=user_email.user.username
        )
        sz = ProfileSz(instance=profile)
        return Response(sz.data)
    raise exceptions.ValidationError("provided OTP is not a valid")


# def get_image_full_url(filename):
#     if filename:
#         return os.path.join("http://127.0.0.1:8000", filename)
#     else:
#         return ""


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_profileApi(request):
    user = request.user
    if request.method == "GET":
        sz = UserSz(instance=user)
        # data = sz.data
        # data["profile_image"] = get_image_full_url(data["profile_image"])
        # data["banner_image"] = get_image_full_url(data["banner_image"])
        return Response(sz.data)
    else:
        sz = UserSz(instance=user, data=request.data, partial=True)
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
        return Response({"error": ["Email not found"]}, status=404)
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(user_email.email).encode())
    otp = gen_otp(user_email.email, user_email.counter, key=key)
    user_email.update_count()
    send_email(
        to=user_email.email,
        subject="OTP for change password",
        text_content=f"your OTP is {otp}.",
    )
    return Response({"success": True})


@api_view(["POST"])
def validate_forgot_password_otpApi(request):
    """
    1. get the email and otp from request.data
    2. check verification of otp
    3. if otp verifyed return success true
    4. throw error
    """
    otp = request.data["OTP"]
    email = request.data["email"]
    user_email = UserEmail.objects.filter(email=email).first()
    if user_email is None:
        return Response({"error": ["email not found"]})

    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(user_email.email).encode())
    OTP = pyotp.HOTP(key)
    if OTP.verify(otp, user_email.counter - 1):
        user_email.update_count()
        return Response({"success": True, "post_key": "jkjkkjkjjkjkkjkj"})
    return Response({"success": False})


@api_view(["POST"])
def change_passwordApi(request):
    """
    1. get the new password and confirm password
    2. check if new password and confirm password are valid or not
    3. get the post_key and check for validation
    4. get the uesr email
    5. update the corresponding user's password to user email
    """
    password = request.data.get("password", None)
    confirm_password = request.data.get("confirm_password", None)
    post_key = request.data.get("post_key", None)
    email = request.data.get("email", None)
    if password is None or confirm_password is None:
        raise exceptions.ValidationError("Entered passwords are invalid")
    if password != confirm_password:
        raise exceptions.ValidationError(
            "please confirm that your passwords matches to each other"
        )
    if post_key != "jkjkkjkjjkjkkjkj":
        raise exceptions.ValidationError("post key is not valid")
    if email is None:
        raise exceptions.ValidationError("provided email is not valid")

    user_email = UserEmail.objects.filter(email=email).first()
    if user_email is None:
        return Response({"error": ["user not found"]})
    user_email.user.set_password(password)
    user_email.user.save()
    return Response({"success": True})


class UserOrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {"order_status": ("exact",)}


class UserOrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {"order_status": ("exact",)}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_ordersApi(request, user_id):
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user)
    query = UserOrderFilter(request=request.GET, queryset=orders)
    if query.is_valid():
        orders = query.qs
    sz = UserOrderSz(instance=orders, many=True)
    return Response(sz.data)

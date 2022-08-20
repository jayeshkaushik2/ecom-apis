from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSz

# Create your views here.
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


@api_view(["GET", "POST"])
def CreateUserApi(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            profile = Profile.objects.get(user=user)
            sz = ProfileSz(instance=profile)
            return Response(sz.data)
        else:
            user = request.user
            profile, created = Profile.objects.get_or_create(user=user, name=user.username)
            sz = ProfileSz(instance=profile, data=request.data, partial=True)
            if sz.is_valid(raise_exception=True):
                sz.save()
                return Response(sz.data)
    elif request.method == "POST":
        user = User.objects.create_user(**request.data)
        if "mark_superuser" in request.data and request.data["mark_superuser"] == True:
            request.pop("mark_superuser")
            user.is_superuser = True
            user.save()
        profile, created = Profile.objects.get_or_create(user=user, name=user.username)
        sz = ProfileSz(instance=profile, data=request.data, partial=True)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data)
    return Response({"error":["user not signed in"]}, status=404)

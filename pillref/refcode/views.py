from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Profile
from .forms import SignUpForm
from rest_framework.response import Response
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import ProfileSerializer
import requests

@unauthenticated_user
def index(request):
    return render(request, "index.html")


@login_required(login_url="/")
def home(request):
    profile = Profile.objects.get(user=request.user)
    coins = profile.incentives
    return render(request, "home.html", {'coins':coins})


def signup_view(request):
    profile_id = request.session.get("ref_profile")
    print("profile_id", profile_id)
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Profile.objects.get(id=profile_id)
            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.incentives += 50
            recommended_by_profile.incentives += 100
            registered_profile.save()
            recommended_by_profile.save()
            print(registered_profile)
            messages.success(request, "You have been succesfully register, Please Login now.")
        else:
            form.save()
            messages.success(request, "You have been succesfully register, Please Login now.")
    context = {"form": form}
    return render(request, "signup.html", context)


def login_view(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            password = fm.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username or Password is invalid! Try-again")
                return redirect("index")
    else:
        fm = AuthenticationForm()
    return render(request, "login.html", {"form": fm})


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect("login")


@login_required(login_url="/")
def generate_code(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profileid = profile.id
    response = requests.get("http://127.0.0.1:8000/api").json()
    return render(request, "code.html", {"response": response, "userid": profileid})


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Referral_code_API(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user=user)
            serializers = ProfileSerializer(profile)
            return Response(serializers.data['referral_code'], status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User is not authenticated, please login"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def profile(request,ref_code):
    code = ref_code
    print("code", code)
    try:
        profile = Profile.objects.get(referral_code=code)
        request.session["ref_profile"] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, "home.html", {})


@csrf_exempt
@api_view(["GET"])
def my_recommendations_view(request):
    profile = Profile.objects.get(user=request.user)
    my_refered = profile.get_recommened_profiles()
    coins = profile.incentives
    context = {"my_recs": my_refered, "coins": coins}
    # return Response(serializers.data, status=status.HTTP_200_OK)
    return render(request, "history.html", context)


class ProfileAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class profileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

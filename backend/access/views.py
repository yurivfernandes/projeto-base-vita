import json

import requests
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import CustomUserCreationForm

User = get_user_model()


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


@csrf_exempt
@require_http_methods(["OPTIONS", "POST"])
def api_login(request):
    if request.method == "OPTIONS":
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            response = JsonResponse(
                {"message": "Login successful", "token": token.key}
            )
        else:
            response = JsonResponse(
                {"error": "Invalid credentials"}, status=400
            )

        response["Access-Control-Allow-Origin"] = "*"
        return response

    response = JsonResponse({"error": "Invalid request method"}, status=405)
    response["Access-Control-Allow-Origin"] = "*"
    return response


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@api_view(["GET"])
def check_username(request, username):
    is_available = not User.objects.filter(username=username).exists()
    return Response({"available": is_available})


@csrf_exempt
@api_view(["POST", "OPTIONS"])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == "OPTIONS":
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization"
        )
        return response

    user = request.user
    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")

    if not user.check_password(current_password):
        response = Response({"message": "Senha atual incorreta"}, status=400)
        response["Access-Control-Allow-Origin"] = "*"
        return response

    try:
        validate_password(new_password)
    except ValidationError as e:
        response = Response({"message": str(e)}, status=400)
        response["Access-Control-Allow-Origin"] = "*"
        return response

    user.set_password(new_password)
    user.save()

    response = Response({"message": "Senha alterada com sucesso"}, status=200)
    response["Access-Control-Allow-Origin"] = "*"
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "company_name": user.company_name,
        "is_staff": user.is_staff,  # Adicionar este campo
    }
    return Response(data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def profile_update(request):
    user = request.user
    try:
        for field in ["full_name"]:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        return Response({"message": "Perfil atualizado com sucesso"})
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def docs_proxy(request, path):
    # Apenas usuários staff podem acessar a documentação
    if not request.user.is_staff:
        return Response({"error": "Acesso não autorizado"}, status=403)

    base_url = "http://localhost:8000/api/docs/"
    # Remove barras duplas que possam surgir na concatenação
    full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    try:
        response = requests.get(full_url)
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers["Content-Type"],
        )
    except requests.RequestException as e:
        return Response({"error": str(e)}, status=500)

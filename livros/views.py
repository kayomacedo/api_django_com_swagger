from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import Book , User
from .serializers import RegisterSerializer, BookSerializer


# ============================
#   REGISTRAR USUÁRIO
# ============================

class RegisterView(APIView):
    permission_classes = [AllowAny] #

    @extend_schema(
        summary="Registrar novo usuário",
        request=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


# ============================
#   CRUD LIVROS (NA MÃO)
# ============================

class BookView(APIView):
    #request <---
    permission_classes = [IsAuthenticated]


    # LISTAR
    @extend_schema(
        summary="Listar todos os livros",
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request):
        livros = Book.objects.filter(user=request.user) # retornar apenas os livros cadastrados pelo usuário
        serializer = BookSerializer(livros, many=True)
        return Response(serializer.data)

    # CRIAR (com validação de título duplicado)
    @extend_schema(
        summary="Criar livro",
        request=BookSerializer,
        responses={201: BookSerializer}
    )
    def post(self, request):
        # Informações do livro
        title = request.data.get("title")
        
        # 🔍 Verifica duplicidade de título por usuário
        if Book.objects.filter(user=request.user, title__iexact=title).exists(): 
            return Response(
                {"erro": f"Você já possui um livro com o título '{title}'."},
                status=400
            )

        serializer = BookSerializer(data=request.data) # json class
        serializer.is_valid(raise_exception=True) # ultima verificação
        serializer.save(user=request.user)

        return Response(serializer.data, status=201)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # OBTER UM LIVRO
    @extend_schema(
        summary="Obter detalhes de um livro",
        responses={200: BookSerializer}
    )
    def get(self, request, pk):
        livro = get_object_or_404(Book, pk=pk, user=request.user)
        serializer = BookSerializer(livro)
        return Response(serializer.data)

    # ATUALIZAR
    @extend_schema(
        summary="Atualizar livro",
        request=BookSerializer,
        responses={200: BookSerializer}
    )
    def put(self, request, pk):
        livro = get_object_or_404(Book, pk=pk, user=request.user)
        serializer = BookSerializer(livro, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETAR
    @extend_schema(
        summary="Deletar livro",
        responses={204: None}
    )
    def delete(self, request, pk):
        livro = get_object_or_404(Book, pk=pk, user=request.user)
        livro.delete()
        return Response(status=204)


class TesteView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Endpoint de teste",
        description="Retorna uma mensagem simples confirmando que a API está funcionando.",
        responses={200: str},
    )
    def get(self, request):
        return Response("Teste bem sucedido!")
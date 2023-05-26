from api.serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitlesCreateSerializer,
    TitlesSerializer,
    UserSerializer,
    MeSerializer,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Categories, Genres, Title

from .filters import TitlesFilter
from .mixins import CreateListDestroyMixinSet
from .permissions import (
    IsAdministrator,
    IsAdminModeratorOwnerOrReadOnly,
    IsAdminOrReadOnly)

User = get_user_model()


def send_conf_code(user) -> None:
    """
    Send confirmation code to user.
    """
    confirmation_code = default_token_generator.make_token(user)
    email_with_conf_code = EmailMessage(
        subject="YaMDB: Confirm your email",
        body="To get token, POST your "
        "username and confirmation code "
        "on the 'auth/token' page.\n"
        f"Your confirmation code is: {confirmation_code}",
        to=[user.email],
    )
    email_with_conf_code.send()


class UserViewSet(viewsets.ModelViewSet):
    """
    Create model viewset for User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    http_method_names = ["get", "post", "head", "delete", "patch"]
    permission_classes = (IsAuthenticated, IsAdministrator,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        methods=["get", "patch"], detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Function for /users/ME/ endpoint.
        """

        instance = request.user

        if request.method == "GET":
            serializer = self.get_serializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(
            instance=instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[AllowAny])
def signup_new_user(request):
    """
    api_view function for signing up.
    Make and send confirmation code to user e-mail.
    """

    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    username = serializer.validated_data.get("username")
    user, created = User.objects.get_or_create(
        email=email,
        username=username
    )
    send_conf_code(user)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[AllowAny])
def get_auth_token(request):
    """
    Create view for get token endpoint. Check user and give token.
    """

    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    user = get_object_or_404(
        User,
        username=username
    )
    confirmation_code = serializer.validated_data.get("confirmation_code")

    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {"token": str(refresh.access_token)}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"confirmation_code": ["Invalid confirmation code."]},
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoriesViewSet(CreateListDestroyMixinSet):
    """
    Получение списка всех категорий - доступно для всех пользователей

    Добавление/удаление категории - доступно только Администратору.
    """

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenresViewSet(CreateListDestroyMixinSet):
    """
    Получение списка всех жанров - доступно для всех пользователей

    Добавление/удаление жанра - доступно только Администратору.
    """

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка произведений или отдельного произведения по id -
        доступно для всех пользователей

    Добавление/частичное обновление/удаление произведения -
        доступно только Администратору.
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlesCreateSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for reviews."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for comments."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

from api.validators import validate_me_username
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Categories, Comment, Genres, Review, Title

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """
    Serialize signing up data. Validate username.
    """

    email = serializers.EmailField(max_length=254, validators=[])
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Letters, digits and @ . + - _ only"
            ),
            validate_me_username,
        ],
    )

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        email_exists = User.objects.filter(email=email).exists()
        username_exists = User.objects.filter(username=username).exists()
        # Checking if exists/doesn't exist User exactly with email & username
        if email_exists != username_exists:
            ok, not_ok = (("email", "username") if email_exists
                          else ("username", "email"))
            raise serializers.ValidationError(
                f"Incorrect pair: {ok} exists but {not_ok} doesn't exist.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize User model endpoints.
    """

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_me_username,
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Letters, digits and @ . + - _ only"
            ),
        ]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )
        lookup_field = "username"


class MeSerializer(UserSerializer):
    """
    Serialize User model for /users/me/ endpoint.
    """

    class Meta(UserSerializer.Meta):
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio"
        )


class GetTokenSerializer(serializers.Serializer):
    """
    Serialize get_token response data.
    """

    username = serializers.CharField(validators=[validate_me_username])
    confirmation_code = serializers.CharField()


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serialize Categories model.
    """

    class Meta:
        model = Categories
        fields = ("name", "slug")


class GenresSerializer(serializers.ModelSerializer):
    """
    Serialize Genres model.
    """

    class Meta:
        model = Genres
        fields = ("name", "slug")


class TitlesSerializer(serializers.ModelSerializer):
    """
    Serialize Titles model in "GET" request.
    """

    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    read_only_fields = (
        "id",
        "name",
        "year",
        "description",
        "genre",
        "category",
        "rating",
    )
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating"
        )


class TitlesCreateSerializer(serializers.ModelSerializer):
    """
    Serialize Titles model in "GET" request.
    """

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genres.objects.all(), many=True
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer Review model."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date", "title")

    def validate(self, data):
        if not self.context.get("request").method == "POST":
            return data
        author = self.context.get("request").user
        title_id = self.context.get("view").kwargs.get("title_id")
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError("Отзыв уже существует!")
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer Comment model."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )

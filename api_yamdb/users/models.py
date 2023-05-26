from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"
ROLES: list = [
    (ADMIN, "Administrator"),
    (MODERATOR, "Moderator"),
    (USER, "User"),
]


class User(AbstractUser):
    """
    Create our User model from AbstractUser.
    """

    username: str = models.CharField(
        verbose_name="Логин",
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Letters, digits and @ . + - _ only",
            )
        ],
    )
    first_name: str = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=True,
        null=True,
    )
    last_name: str = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
        null=True,
    )
    email: str = models.EmailField(
        verbose_name="E-mail",
        unique=True,
    )
    bio: str = models.TextField(
        verbose_name="Биография",
        blank=True,
        null=True,
    )
    role: str = models.CharField(
        verbose_name="Права доступа",
        max_length=20,
        choices=ROLES,
        default=USER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    @property
    def is_admin(self):
        """
        If user has admin role.
        """
        return (self.role == ADMIN)

    @property
    def is_moderator(self):
        """
        If user has admin role.
        """
        return (self.role == MODERATOR)

    class Meta:
        """
        Meta class of User model.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("last_login", "username", "is_active")

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="me_is_wrong_username"
            )
        ]

    def __str__(self) -> str:
        """
        String method for User model.
        """
        return str(self.username)

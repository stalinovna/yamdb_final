from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       get_auth_token, signup_new_user)
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", UserViewSet)
router_v1.register(r"categories", CategoriesViewSet, basename="categories")
router_v1.register(r"genres", GenresViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)" r"/comments",
    CommentViewSet,
    basename="comments",
)


urlpatterns = [
    path("v1/auth/signup/", signup_new_user, name="signup"),
    path("v1/auth/token/", get_auth_token, name="get_token"),
    path("v1/", include(router_v1.urls)),
]

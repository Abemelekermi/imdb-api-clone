"""
URL mapping for movie app
"""

from django.urls import(
    path,
    include
)

from rest_framework.routers import DefaultRouter

from movie import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet, 'movie')
router.register('ratings', views.RatingViewSet, 'rating')

app_name = 'movie'

urlpatterns = [
     path('', include(router.urls))
]

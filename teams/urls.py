from django.urls import path
from .views import TeamDetail, TeamView

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<team_id>/", TeamDetail.as_view()),
]

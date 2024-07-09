from django.forms import model_to_dict
from rest_framework.views import APIView, status, Request, Response
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from utils import data_processing
from .models import Team


class TeamView(APIView):
    def post(self, request: Request):
        try:
            data_processing(request.data)
        except NegativeTitlesError as err:
            return Response({"error": err.message}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as err:
            return Response({"error": err.message}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as err:
            return Response({"error": err.message}, status.HTTP_400_BAD_REQUEST)

        new_team: Team = Team.objects.create(**request.data)

        return Response(model_to_dict(new_team), status.HTTP_201_CREATED)

    def get(self, request: Request):

        team_list = Team.objects.all()

        team_dict = [model_to_dict(team) for team in team_list]

        return Response(team_dict, status.HTTP_200_OK)


class TeamDetail(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )

        team_dict = model_to_dict(team)

        return Response(team_dict)

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict)

    def delete(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

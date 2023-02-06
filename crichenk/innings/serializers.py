from rest_framework import serializers
from .models import Batter, Ball, Bowler

class BatterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Batter
        fields = ['id', 'name', 'runs_scored', 'balls_faced', 'dismissal_type', 'sixes_hit', 'fours_hit', 'dots_played']

class BallSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Ball
        fields = ['id', 'main_event', 'runs', 'side_event', 'end', 'crossed_over', 'batter']

class BowlerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Bowler
        fields = ['id', 'name', 'wickets_taken', 'overs_bowled', 'balls_bowled', 'runs_conceded', 'dots_bowled', 'economy']

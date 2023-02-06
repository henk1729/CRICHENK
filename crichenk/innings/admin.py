from django.contrib import admin
from .models import Batter, Ball, Bowler

# registering models

admin.site.register(Batter)
class BatterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'runs_scored', 'balls_faced', 'dismissal_type']

admin.site.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = ['id', 'main_event', 'runs', 'side_event', 'end', 'crossed_over', 'batter']

admin.site.register(Bowler)
class BallAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'wickets_taken', 'overs_bowled', 'balls_bowled', 'runs_conceded', 'dots_bowled', 'economy']
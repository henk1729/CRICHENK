from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("",                    views.home),
    path("index",               views.index,               name="index"),
    path("edit_over",           views.edit_over,           name="edit_over"),
    path("add_batter",          views.add_batter,          name="add_batter"),
    path("add_bowler",          views.add_bowler,          name="add_bowler"),
    path("add_ball",            views.add_ball,            name="add_ball"),
    path("view_score",          views.view_score,          name="view_score"),
    path("on_reload_edit_over", views.on_reload_edit_over, name="on_reload_edit_over"),
    path("innings_end",         views.innings_end,         name="innings_end"),
    path("player_analysis",     views.player_analysis,     name="player_analysis"),
    path("return_analysis",     views.return_analysis,     name="return_analysis"),
    path("show_timeline",       views.show_timeline,       name="show_timeline"),
]
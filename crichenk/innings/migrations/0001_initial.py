# Generated by Django 4.1.5 on 2023-02-06 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Batter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=20)),
                ("runs_scored", models.IntegerField(default=0)),
                ("balls_faced", models.IntegerField(default=0)),
                ("dismissal_type", models.CharField(default="", max_length=10)),
                ("sixes_hit", models.IntegerField(default=0)),
                ("fours_hit", models.IntegerField(default=0)),
                ("dots_played", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Bowler",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("wickets_taken", models.IntegerField(default=0)),
                ("overs_bowled", models.IntegerField(default=0)),
                ("balls_bowled", models.IntegerField(default=0)),
                ("runs_conceded", models.IntegerField(default=0)),
                ("dots_bowled", models.IntegerField(default=0)),
                ("economy", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Ball",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("main_event", models.CharField(default="", max_length=10)),
                ("runs", models.IntegerField(default=0)),
                ("side_event", models.CharField(default="", max_length=10)),
                ("end", models.CharField(default="", max_length=10)),
                ("crossed_over", models.CharField(default="", max_length=10)),
                (
                    "batter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="innings.batter"
                    ),
                ),
            ],
        ),
    ]

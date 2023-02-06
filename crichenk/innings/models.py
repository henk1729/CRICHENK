from django.db import models


class Batter(models.Model):
    name           = models.CharField(max_length=20, null=False, default="")
    runs_scored    = models.IntegerField(default=0)
    balls_faced    = models.IntegerField(default=0)
    dismissal_type = models.CharField(max_length=10, default="")
    sixes_hit      = models.IntegerField(default=0)
    fours_hit      = models.IntegerField(default=0)
    dots_played    = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Ball(models.Model):
    main_event     = models.CharField(max_length=10, null=False, default="")
    runs           = models.IntegerField(null=False, default=0)
    side_event     = models.CharField(max_length=10, default="")
    end            = models.CharField(max_length=10, default="")
    crossed_over   = models.CharField(max_length=10, default="")
    batter         = models.ForeignKey(Batter, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s %s %s %s" %(self.main_event, self.runs, self.side_event, self.end, self.crossed_over, self.batter)


class Bowler(models.Model):
    name          = models.CharField(max_length=20, null=False)
    wickets_taken = models.IntegerField(default=0)
    overs_bowled  = models.IntegerField(default=0)
    balls_bowled  = models.IntegerField(default=0)
    runs_conceded = models.IntegerField(default=0)
    dots_bowled   = models.IntegerField(default=0)
    economy       = models.FloatField(default=round(0.0, 2))
    
    def __str__(self):
        return self.name
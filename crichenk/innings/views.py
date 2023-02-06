from ftplib import all_errors
from json.tool import main
from multiprocessing import context
import this
from django.shortcuts import render
from .models import Batter, Ball, Bowler

# game events
events                      = ['0', '1', '2', '3', '4', '5', '6', 'wide', 'legbye', 'bye', 'noball', 'bowled', 'lbw', 'caught', 'stumped', 'hitwicket', 'runout']
runs_events                 = ['0', '1', '2', '3', '4', '5', '6']
extra_events                = ['wide', 'legbye', 'bye', 'noball']
wicket_events               = ['bowled', 'lbw', 'caught', 'stumped', 'hitwicket']
# batters events
batters_ball_counted_events = ['legbye', 'bye' ,'noball']
batters_runs_counted_events = ['noball']
# bowlers events
bowlers_ball_counted_events = ['legbye', 'bye', 'runout']
bowlers_runs_counted_events = ['wide', 'noball']

# global variables
batters_list = []     # to store batters in the order they bat
bowlers_list = []     # to store bowlers in the order they bowl
strikers     = [1, 2] # to store striker and non-striker
##
overs        = {}     # to store the dictionary 'over'
over         = {}     # to store 'ball' objects
##
free_hit     = False  # to keep a check of free-hit
##
score        = 0      # to store current runs
wickets      = 0      # to store current wicket-count
ball_number  = 0      # to store current ball-number
over_number  = 1      # to store current over-number
##
warning      = ""     # warning message
success      = ""     # batting-success message
failure      = ""     # batting-failure message
this_over    = ""     # current-over contents

############################################################## For 'home.html' ####################################################################

## redirect to home page
def home(request):
    return render(request, 'home.html')

############################################################## For 'index.html' ###################################################################

# add players
def index(request):
    # delete all batters and bowlers present previously
    all_batters=Batter.objects.all()
    all_batters.delete()
    all_bowlers=Bowler.objects.all()
    all_bowlers.delete()

    # clear batters and bowlers lists before adding new players
    global batters_list
    global bowlers_list
    batters_list.clear()
    bowlers_list.clear()

    return render(request, 'index.html')


# adding batter
def add_batter(request):
    if request.method=='POST':
        name           = request.POST.get('name')
        runs_scored    = request.POST.get('runs_scored', 0)
        balls_faced    = request.POST.get('balls_faced', 0)
        dismissal_type = request.POST.get('dismissal_type', "none")
        new_batter     = Batter(name=name, runs_scored=runs_scored, balls_faced=balls_faced, dismissal_type=dismissal_type)
        new_batter.save()

        # adding new batter to list
        batters_list.append(name)
    return render(request, 'index.html')


# adding bowler
def add_bowler(request):
    global bowlers_list
    if request.method=="POST":
        name = request.POST.get('name')
        if name not in bowlers_list: # create new 'Bowler' object if not aleady present
            new_bowler = Bowler(name=name, wickets_taken=0, overs_bowled=0, balls_bowled=0, runs_conceded=0, dots_bowled=0, economy=0.0)
            new_bowler.save()
        bowlers_list.append(name) # adding new bowler to list
    return render(request, 'index.html')
    
############################################################## For 'edit_over.html' ####################################################################

# loading 'edit_over.html'
def edit_over(request):
    # initialize the variables every time you restart
    global overs
    global over
    global score
    global wickets
    global ball_number
    global over_number
    global warning
    global success
    global failure
    global this_over
    overs.clear()
    over.clear()
    score       = 0
    wickets     = 0
    ball_number = 0
    over_number = 1
    warning     = ""
    success     = ""
    failure     = ""
    this_over   = ""

    # delete previous 'Ball' objects
    balls=Ball.objects.all()
    balls.delete()

    # initialize all 'Batter' and 'Bowler' objects to default value
    batters=Batter.objects.all()
    for batter in batters:
        batter.runs_scored    = 0
        batter.balls_faced    = 0
        batter.dismissal_type = ""
        batter.sixes_hit      = 0
        batter.fours_hit      = 0
        batter.dots_played    = 0
        batter.save()
    bowlers=Bowler.objects.all()
    for bowler in bowlers:
        bowler.wickets_taken  = 0
        bowler.overs_bowled   = 0
        bowler.balls_bowled   = 0
        bowler.runs_conceded  = 0
        bowler.dots_bowled    = 0
        bowler.economy        = 0.0
        bowler.save()
        
    # set strikers
    global strikers
    strikers[0] = batters_list[0]
    strikers[1] = batters_list[1]

    # for testing purpose
    print(batters_list)
    print(bowlers_list)
    print(strikers)

    # passing initialised values to 'edit_over.html'
    context={
        'warning'     : warning,
        'success'     : success,
        'failure'     : failure,
        'this_over'   : this_over,
        'score'       : score,
        'wickets'     : wickets,
        'over_number' : over_number-1,
        'ball_number' : ball_number,
        'bowler'      : Bowler.objects.get(name=bowlers_list[over_number-1]),
        'striker'     : Batter.objects.get(name=strikers[0]),
        'non_striker' : Batter.objects.get(name=strikers[1]),
    }
    return render(request, 'edit_over.html', context)


# reloading 'edit_over.html' from other pages
def on_reload_edit_over(request):
    # passing ongoing values to 'edit_over.html'
    context={
        'warning'     : warning,
        'success'     : success,
        'failure'     : failure,
        'this_over'   : this_over,
        'score'       : score,
        'wickets'     : wickets,
        'over_number' : over_number-1,
        'ball_number' : ball_number,
        'bowler'      : Bowler.objects.get(name=bowlers_list[over_number-1]),
        'striker'     : Batter.objects.get(name=strikers[0]),
        'non_striker' : Batter.objects.get(name=strikers[1]),
    }
    return render(request, 'edit_over.html', context)

############################################################## For 'edit_over.html' and 'innings_end.html' ####################################################################

# add ball
def add_ball(request):
    # indicates that global variables are referenced
    global batters_list
    global bowlers_list
    global strikers
    global overs
    global over
    global free_hit
    global score
    global wickets
    global ball_number
    global over_number
    global warning
    global success
    global failure
    global this_over

    if request.method=='POST':
        # set 'Ball' fields
        main_event     = request.POST.get('main_event')
        runs           = request.POST.get('runs')
        side_event     = request.POST.get('side_event', "")
        end            = request.POST.get('end', "")
        crossed_over   = request.POST.get('crossed_over', "")
        batter         = Batter.objects.get(name=strikers[0])
        batter_id      = Batter.objects.get(name=strikers[0]).id
        current_bowler = Bowler.objects.get(name=bowlers_list[over_number-1])

        # messages to display on scoreboard
        warning_flag = False
        warning      = ""
        failure      = ""

        # for 'success message'
        if free_hit==False: # if no free-hit, clear success-message
            success = ""
        if success!="🎉 It's a free hit!": # if any else message on success-message screen, clear it
            success = ""
        # for 'warning message'
        if runs!='0':
            if success!="🎉 It's a free hit!" and main_event in wicket_events: # choosing non-zero runs on wicket-events
                warning      = "⚠️ Invalid event! No run can be scored on a wicket event.";
                warning_flag = True
            else:
                if main_event in runs_events: # choosing non-zero runs on runs-events -> does not make sense
                    warning      = "⚠️ Invalid event! Default auxiliary runs for 'Runs' event is '0'. You chose a non-zero value. Leave 'Runs' event default.";
                    warning_flag = True
                elif main_event=='wide' and side_event=='stumped': # choosing non-zero runs on 'stumped' event
                    warning      = "⚠️ Invalid event! No run can be scored on a stumped event.";
                    warning_flag = True
        else:
            if main_event=='bye': #  choosing zero runs on 'bye' event -> defies bye's definition
                warning      = "⚠️ Invalid event! It's not a bye event if no run is scored. Choose a non-zero value for 'Runs' event.";
                warning_flag = True

        # if warning is raised, pass such message to scoreboard screen without adding ball
        if warning_flag:
            context={
                'warning'     : warning,
                'success'     : success,
                'failure'     : failure,
                'this_over'   : this_over,
                'score'       : score,
                'wickets'     : wickets,
                'over_number' : over_number-1,
                'ball_number' : ball_number,
                'bowler'      : Bowler.objects.get(name=bowlers_list[over_number-1]),
                'striker'     : Batter.objects.get(name=strikers[0]),
                'non_striker' : Batter.objects.get(name=strikers[1]),
            }
            return render(request, 'edit_over.html', context)

        # if no warning is raised...

        # if it's a free-hit ball
        if free_hit:
            if main_event in wicket_events: # if wicket-event is chosen for main-event
                current_batter=Batter.objects.get(name=batter)
                current_batter.runs_scored   += int(runs)
                current_batter.balls_faced   += 1
                current_batter.save()

                current_bowler.runs_conceded += int(runs)
                current_bowler.balls_bowled  += 1

                score                        += int(runs)
                ball_number                  += 1

                if int(runs)%2: # rotate strike for odd runs
                    strikers[0], strikers[1]=strikers[1], strikers[0]
                
                # this-over message
                if runs=='0':
                    this_over += '•   '
                else:
                    this_over += (runs+'   ')

    # main-event belongs to '['0', '1', '2', '3', '4', '5', '6']'
        if main_event in runs_events:
            current_batter=Batter.objects.get(name=batter)
            current_batter.runs_scored   += int(main_event)
            current_batter.balls_faced   += 1

            current_bowler.runs_conceded += int(main_event)
            current_bowler.balls_bowled  += 1

            score                        += int(main_event)
            ball_number                  += 1

            if main_event=='0':
                current_batter.dots_played += 1
                current_bowler.dots_bowled += 1
            elif main_event=='4':
                current_batter.fours_hit   += 1
            elif main_event=='6':
                current_batter.sixes_hit   += 1
            current_batter.save()

            if int(main_event)%2: # rotate strike for odd runs
                strikers[0], strikers[1]=strikers[1], strikers[0]

            # this-over message
            if main_event=='0':
                this_over += '•   '
            else:
                this_over += (main_event+'   ')

    # main-event belongs to '['wide', 'legbye', 'bye', 'noball']' 
        elif main_event in extra_events or main_event=='runout':
            if main_event=="noball": # if current ball is no-ball, declare a free-hit
                free_hit     = True
            if main_event=="noball" or main_event=="wide": # if no-ball or wide, add 1 run to batting team
                score       += 1
            else: # if other delivery, increment ball-count
                ball_number += 1
            
            score           += int(runs)

            # this-over message for extra-events
            this_over     += runs
            if main_event=='wide':
                this_over += 'wd'
            elif main_event=='legbye':
                this_over += 'lb'
            elif main_event=='bye':
                this_over += 'b'
            elif main_event=='noball':
                this_over += 'nb'

            if main_event=='runout' or side_event!='': # if run-out or "side-event is not null -> side-event is 'stumped' or 'run-out'"
                this_over += 'W'
            this_over     += '   '

            current_batter=Batter.objects.get(name=strikers[0])
            # for batter
            if main_event in batters_runs_counted_events: # if main-event suggests runs are counted for batter
                current_batter.runs_scored     += int(runs)
            if main_event in batters_ball_counted_events: # if main-event suggests balls are counted for batter
                current_batter.balls_faced     += 1
                if int(runs)==0: # if ball is counted for batter and was played a dot
                    current_batter.dots_played += 1

            # for bowler
            if main_event in bowlers_runs_counted_events: # if main-event suggests runs are counted for bowler
                current_bowler.runs_conceded   += (int(runs)+1) # '+1' for extra run awarded
            if main_event in bowlers_ball_counted_events: # if main-event suggests balls are counted for bowler
                current_bowler.balls_bowled    += 1
                if int(runs)==0: # if ball is counted for bowler and was played a dot
                    current_bowler.dots_bowled += 1
            
            current_batter.save()

            # side-event or main-event is run-out
            if side_event=='runout' or main_event=='runout':
                # increment wicket-count and set failure-message
                wickets += 1
                failure  = "🏏 Wicket!"

                if int(runs)%2: # rotate strike for odd runs
                    strikers[0], strikers[1]=strikers[1], strikers[0]

                # if team gets all-out
                if wickets==len(batters_list)-1:
                    if crossed_over=="yes": # if batters crossed-over, rotate strike
                        strikers[0], strikers[1]=strikers[1], strikers[0]

                    if end=="batting": # if throw at batting end, dismiss onstrike-batter
                        dismissed_batter=Batter.objects.get(name=strikers[0])
                        dismissed_batter.dismissal_type = 'runout'
                        dismissed_batter.save()
                        strikers[0]                     = ""
                    else: # if throw at bowling end, dismiss nonstrike-batter
                        dismissed_batter=Batter.objects.get(name=strikers[1])
                        dismissed_batter.dismissal_type = 'runout'
                        dismissed_batter.save()
                        strikers[1]                     = ""

                    # save ball
                    new_ball=Ball(main_event=main_event, runs=runs, side_event=side_event, end=end, crossed_over=crossed_over, batter_id=batter_id)
                    new_ball.save()
                    # add ball to 'over' dictionary
                    over[new_ball.id]       = new_ball
                    # add 'over' dictionary to 'overs' dictionary
                    overs[str(over_number)] = over

                    if ball_number: # not if the over has just started
                        total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
                        conceded_runs          = current_bowler.runs_conceded
                        current_bowler.economy = round((6*conceded_runs)/total_balls, 2)
                    
                    if ball_number==6: # over-end
                        ball_number                  = 0
                        overs[str(over_number)]      = over
                        over                         = {} # empty over
                        over_number                 += 1
                        current_bowler.overs_bowled += 1
                        current_bowler.balls_bowled  = 0
                        current_bowler.save()

                    # set economy for bowler
                    if current_bowler.overs_bowled or current_bowler.balls_bowled:
                        total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
                        conceded_runs          = current_bowler.runs_conceded
                        current_bowler.economy = round((6*conceded_runs)/total_balls, 2)

                    current_bowler.save()
                    # redirect to 'innings_end.html'
                    return render(request, "innings_end.html")
                # team not all-out
                else:
                    if crossed_over=="yes": # if batters crossed-over, rotate strike
                        strikers[0], strikers[1]=strikers[1], strikers[0]
                    if end=="batting": # if throw at batting end, dismiss onstrike-batter
                        dismissed_batter                = Batter.objects.get(name=strikers[0])
                        dismissed_batter.dismissal_type = 'runout'
                        dismissed_batter.save()
                        # set onstriker
                        strikers[0]                     = batters_list[wickets+1]
                    else: # if throw at bowling end, dismiss nonstrike-batter
                        dismissed_batter                = Batter.objects.get(name=strikers[1])
                        dismissed_batter.dismissal_type = 'runout'
                        dismissed_batter.save()
                        # set nonstriker
                        strikers[1]                     = batters_list[wickets+1]

            # side-event is stumped
            elif side_event=='stumped' and free_hit==False:
                # increment wicket-count and set failure-message
                wickets += 1
                failure  = "🏏 Wicket!"
                # increment wicket-count for bowler
                current_bowler.wickets_taken += 1

                # if team gets all-out
                if wickets==len(batters_list)-1:
                    dismissed_batter                = Batter.objects.get(name=strikers[0])
                    dismissed_batter.dismissal_type = 'stumped'
                    dismissed_batter.save()
                    strikers[0]                     = ""

                    # save ball
                    new_ball=Ball(main_event=main_event, runs=runs, side_event=side_event, end=end, crossed_over=crossed_over, batter_id=batter_id)
                    new_ball.save()
                    # add ball to 'over' dictionary
                    over[new_ball.id]       = new_ball
                    # add 'over' dictionary to 'overs' dictionary
                    overs[str(over_number)] = over

                    if ball_number: # not if the over has just started
                        total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
                        conceded_runs          = current_bowler.runs_conceded
                        current_bowler.economy = round((6*conceded_runs)/total_balls, 2)
                    
                    if ball_number==6: # over-end
                        ball_number                  = 0
                        overs[str(over_number)]      = over
                        over                         = {} # empty over
                        over_number                 += 1
                        current_bowler.overs_bowled += 1
                        current_bowler.balls_bowled  = 0
                        current_bowler.save()

                    # set economy for bowler
                    if current_bowler.overs_bowled or current_bowler.balls_bowled:
                        total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
                        conceded_runs          = current_bowler.runs_conceded
                        current_bowler.economy = round((6*conceded_runs)/total_balls, 2)

                    current_bowler.save()
                    # redirect to 'innings_end.html'
                    return render(request, "innings_end.html")
                # team not all-out
                dismissed_batter                = Batter.objects.get(name=strikers[0])
                dismissed_batter.dismissal_type = 'stumped'
                dismissed_batter.save()
                # set onstriker
                strikers[0]                     = batters_list[wickets+1]
            # no side-event -> only extra and/or runs scored in extra
            else:
                if int(runs)%2: # rotate strike for odd runs
                    strikers[0], strikers[1]=strikers[1], strikers[0]

    # main-event belongs to '['bowled', 'lbw', 'caught', 'stumped', 'hitwicket']' 
        elif main_event in wicket_events and free_hit==False:
            dismissed_batter                = Batter.objects.get(name=strikers[0])
            dismissed_batter.balls_faced   += 1
            dismissed_batter.dots_played   += 1
            dismissed_batter.dismissal_type = main_event
            dismissed_batter.save()

            wickets                        += 1
            failure                         = "🏏 Wicket!"

            ball_number                    += 1
            this_over                      += 'W   '

            current_bowler.wickets_taken   += 1
            current_bowler.balls_bowled    += 1
            current_bowler.dots_bowled     += 1

            # if team gets all-out
            if wickets==len(batters_list)-1:
                strikers[0]=""
                # save ball
                new_ball=Ball(main_event=main_event, runs=runs, side_event=side_event, end=end, crossed_over=crossed_over, batter_id=batter_id)
                new_ball.save()
                # add ball to 'over' dictionary
                over[new_ball.id]       = new_ball
                # add 'over' dictionary to 'overs' dictionary
                overs[str(over_number)] = over

                if ball_number: # not if the over has just started
                    total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
                    conceded_runs          = current_bowler.runs_conceded
                    current_bowler.economy = round((6*conceded_runs)/total_balls, 2)
                
                if ball_number==6: # over-end
                    ball_number                  = 0
                    overs[str(over_number)]      = over
                    over                         = {} # empty over
                    over_number                 += 1
                    current_bowler.overs_bowled += 1
                    current_bowler.balls_bowled  = 0
                    current_bowler.save()

                # set economy for bowler
                if current_bowler.overs_bowled or current_bowler.balls_bowled:
                    total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
                    conceded_runs          = current_bowler.runs_conceded
                    current_bowler.economy = round((6*conceded_runs)/total_balls, 2)

                current_bowler.save()
                # redirect to 'innings_end.html'
                return render(request, "innings_end.html")
            # team not all-out
            strikers[0]=batters_list[wickets+1] # set onstriker
            
        # free-hit preserved
        if main_event!="wide" and main_event!="noball":
            free_hit=False
            
        # save ball
        new_ball=Ball(main_event=main_event, runs=runs, side_event=side_event, end=end, crossed_over=crossed_over, batter_id=batter_id)
        new_ball.save()
        # general case; only add ball to 'over' dictionary
        over[new_ball.id]=new_ball

        if ball_number==6: # over-end
            ball_number                  = 0
            overs[str(over_number)]      = over
            over                         = {} # empty over
            over_number                 += 1
            this_over                    = ""
            current_bowler.overs_bowled += 1
            current_bowler.balls_bowled  = 0
            current_bowler.save()
            strikers[0], strikers[1]=strikers[1], strikers[0] # change strike after over

        # set economy for bowler
        if current_bowler.overs_bowled or current_bowler.balls_bowled:
            total_balls            = 6*current_bowler.overs_bowled+current_bowler.balls_bowled
            conceded_runs          = current_bowler.runs_conceded
            current_bowler.economy = round((6*conceded_runs)/total_balls, 2)

        current_bowler.save()

        # for testing purpose
        print(score, ' / ', wickets)
        print(strikers)
        print(batters_list)

        # overs completed
        if over_number==len(bowlers_list)+1:
            return render(request, "innings_end.html")

        # set success-message
        if free_hit: # set message for free-hit
            success     = "🎉 It's a free hit!"
        else:
            if main_event=='6' or runs=='6':
                success = "🎉 Whoomp! It's a six!"
            elif main_event=='4' or runs=='4':
                success = "🎉 A boundary!"
            else:
                success = ""
        
        # pass values to 'edit_over.html'
        context={
            'warning'     : warning,
            'success'     : success,
            'failure'     : failure,
            'this_over'   : this_over,
            'score'       : score,
            'wickets'     : wickets,
            'over_number' : over_number-1,
            'ball_number' : ball_number,
            'bowler'      : Bowler.objects.get(name=bowlers_list[over_number-1]),
            'striker'     : Batter.objects.get(name=strikers[0]),
            'non_striker' : Batter.objects.get(name=strikers[1]),
        }
        return render(request, 'edit_over.html', context)

############################################################## For 'view_score.html' ####################################################################

# view scoreboard
def view_score(request):
    batters=Batter.objects.all()
    bowlers=Bowler.objects.all()

    # to calculate extras
    batters_runs=0
    for batter in batters:
        batters_runs+=batter.runs_scored
    extras=score-batters_runs

    # passing values to 'view_score.html'
    context={
        'batters': batters,
        'bowlers': bowlers,
        'extras': extras,
        'score': score,
        'wickets': wickets,
        'overs': over_number-1,
        'balls': ball_number,
    }
    return render(request, 'view_score.html', context)

############################################################## MENU-> For 'innings_end.html' ####################################################################

# redirect end of innings page
def innings_end(request):
    return render(request, 'innings_end.html')

############################################################## For 'show_timeline.html' ####################################################################

# show timeline
def show_timeline(request):
    # pass 'overs' dictionary to 'timeline.html'
    context={
        'overs': overs,
    }
    return render(request, 'timeline.html', context);

############################################################## For 'player_analysis.html' ####################################################################

# show players list for analysis
def player_analysis(request):
    # pass players to 'player_analysis.html'
    context={
        'batters': Batter.objects.all(),
        'bowlers': Bowler.objects.all(),
    }
    return render(request, 'player_analysis.html', context)


# show analysis for chosen player
def return_analysis(request):
    # get player
    player_name=request.POST.get('player_name')

    # initialise values for player characteristics
    strike_rate         = "-"
    dot_ball_percentage = "-"
    boundary_percentage = "-"
    ball_per_boundary   = "-"
    average             = "-"

    # analysis for batter
    if player_name in batters_list:
        # get batter
        batter=Batter.objects.get(name=player_name)

        # check if batter has played any ball, scored any run, and hit any boundary -> to avoid 'ZeroDivision' error
        if batter.balls_faced:
            strike_rate         = round((batter.runs_scored*100)/batter.balls_faced, 2)
            dot_ball_percentage = round((batter.dots_played*100)/batter.balls_faced, 2)
        if batter.runs_scored:
            boundary_percentage = round(((batter.sixes_hit*6+batter.fours_hit*4)*100)/batter.runs_scored, 2)
        if (batter.sixes_hit+batter.fours_hit):
            ball_per_boundary   = round(batter.balls_faced/(batter.sixes_hit+batter.fours_hit), 2)

        context={
            'batter': batter,
            'strike_rate': strike_rate,
            'dot_ball_percentage': dot_ball_percentage,
            'boundary_percentage': boundary_percentage,
            'ball_per_boundary': ball_per_boundary,
        }
    # analysis for bowler
    else:
        # get bowler
        bowler=Bowler.objects.get(name=player_name)

        # check if bowler has taken any wicket -> to avoid 'ZeroDivision' error
        if bowler.wickets_taken:
            strike_rate=round(bowler.runs_conceded/bowler.wickets_taken, 2)
            average=round((bowler.overs_bowled*6+bowler.balls_bowled)/bowler.wickets_taken, 2)

        context={
            'bowler': bowler,
            'strike_rate': strike_rate,
            'average': average,
        }

    #pass values to 'player_analysis.html'
    return render(request, 'player_analysis.html', context)
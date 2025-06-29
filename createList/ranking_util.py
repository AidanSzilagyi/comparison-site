from .models import Thing, SeenThing, Matchup
from django.db.models import Q

def get_available_things(user, list):
    available_things = Thing.objects.filter(list=list).exclude(
        Q(id__in=SeenThing.objects.filter(user=user).values('thing_id')) |
        Q(id__in=Matchup.objects.filter(awaiting_response=True).values('winner_id')) |
        Q(id__in=Matchup.objects.filter(awaiting_response=True).values('loser_id'))).order_by('rating')
    return available_things
        
def reevaluate_awaiting_response():
    print("TODO")
    

# Excludes comparisons that have already been decided or sent to the user
def exclude_used_comparisons(comparisons, sent_matchups):
    sent_matchup_ids = [m.id for m in sent_matchups]
    for comp in comparisons:
        expected_winner = comp[0]
        expected_loser = comp[1]
        if Matchup.objects.filter(Q(winner=expected_winner, loser=expected_loser) |
                                  Q(winner=expected_loser, loser=expected_winner) |
                                  Q(id__in=sent_matchup_ids)).first():
            comparisons.remove(comp)
    return comparisons


def get_matchups_awaiting_response(user, list, sent_matchups):
    sent_matchup_ids = [m.id for m in sent_matchups]
    return Matchup.objects.filter(user=user, awaiting_response=True, winner__list=list).exclude(id__in=sent_matchup_ids)
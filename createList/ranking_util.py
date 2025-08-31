from .models import Thing, Matchup
from django.db.models import Q
import random

def get_available_things(list, sent_matchups=[]):
    excluded_ids = set()
    for m in sent_matchups:
        excluded_ids.add(m.winner_id)
        excluded_ids.add(m.loser_id)

    return Thing.objects.filter(list=list).exclude(id__in=excluded_ids).order_by('rating')
        
def reevaluate_awaiting_response():
    print("TODO")
    

# Excludes comparisons that have already been decided or sent to the user
def exclude_used_comparisons(comparisons, sent_matchups):
    sent_matchup_ids = [m.id for m in sent_matchups]
    for comp in comparisons:
        expected_winner = comp[0]
        expected_loser = comp[1]
        if Matchup.objects.filter(Q(winner=expected_winner, loser=expected_loser) |
                                  Q(winner=expected_loser, loser=expected_winner)).first():
            comparisons.remove(comp)
    return comparisons


def get_matchups_awaiting_response(user, list, sent_matchups):
    sent_matchup_ids = [m.id for m in sent_matchups]
    return Matchup.objects.filter(user=user, awaiting_response=True, winner__list=list).exclude(id__in=sent_matchup_ids)


def get_random_comparisons(tlist):
    comparisons = []
    things = list(Thing.objects.filter(list=tlist))
    random.shuffle(things)
    for i in range(0, list.num_things if list.num_things < 20 else 20, 2):
        comparisons.append(things[i], things[i+1])
    return comparisons
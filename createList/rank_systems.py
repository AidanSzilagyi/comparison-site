from .models import List, Thing, Matchup, SeenThing
import random
from .bradley_terry_model import BradleyTerryModel
from .ranking_util import get_matchups_awaiting_response
import json

def process_matchup_result(user, list, matchup_id, choice):
    matchup = Matchup.objects.get(id=matchup_id)
    matchup.awaiting_response = False
    if choice == 2:
        temp = matchup.loser
        matchup.winner = matchup.loser
        matchup.loser = temp
    matchup.save()
    get_comparison_model(list).update_rankings(user, list, matchup)

def generate_matchup_json(user, list, sent_matchups=[]):
    matchups = generate_matchups(user, list, sent_matchups)
    matchup_json = []
    for matchup in matchups:
        matchup_json.append({
            "id": str(matchup.id),
            "thing1": {
                "name": matchup.winner.name,
                "image": matchup.winner.image.url if matchup.winner.image else None
            },
            "thing2": {
                "name": matchup.loser.name,
                "image": matchup.loser.image.url if matchup.loser.image else None
            }
        })
    return json.dumps(matchup_json)

def generate_matchups(user, tlist, sent_matchups):
    limit = 5
    total = limit * 2
    if tlist.num_things < total:
        total = tlist.num_things - (tlist.num_things % 2)
    
    comparisons = get_comparison_model(tlist).get_comparisons(user, tlist, sent_matchups)
    if len(comparisons) > 5:
            comparisons = comparisons[:5]
    
    matchups = list(get_matchups_awaiting_response(user, tlist, sent_matchups))
    for comparison in comparisons:
        matchups.append(Matchup.objects.create(
            winner=comparison[0], loser=comparison[1], user=user))
    return matchups
    
    # else: return find_random_comparisons(list, total)

def get_comparison_model(list):
    if list.comparison_method == 'bradley_terry':
        return BradleyTerryModel()
    


def find_random_comparisons(thing_list, total):
    things = list(Thing.objects.filter(list=thing_list))
    random.shuffle(things)
    things = things[:total]
    comparisonJSON = []
    for i in range(0, total - 1, 2):
        first_thing = things[i]
        second_thing = things[i + 1]
        comparisonJSON.append({
            "thing1": {
                "name": first_thing.name,
                "image":first_thing.image.url if first_thing.image else None
            },
            "thing2": {
                "name": second_thing.name,
                "image":second_thing.image.url if second_thing.image else None
            }
        })
    return comparisonJSON
from .models import List, Thing, Matchup, SeenThing
import random
from .bradley_terry_model import get_comparisons

def process_matchup_results(user, list, results):
    print("TODO")


def generate_matchup_json(user, list, limit):
    matchups = generate_comparisons(user, list, limit)
    matchup_json = []
    for matchup in matchups:
        matchup_json.append({
            "id": matchup.id,
            "thing1": {
                "name": matchup.winner.name,
                "image": matchup.winner.image.url if matchup.winner.image else None
            },
            "thing2": {
                "name": matchup.loser.name,
                "image": matchup.loser.image.url if matchup.loser.image else None
            }
        })
    return matchup_json
        

def generate_comparisons(user, list, limit):
    total = limit * 2
    if list.num_things < total:
        total = list.num_things - (list.num_things % 2)
    
    #if list.comparison_method == 'bradley_terry':
    
    comparisons = get_comparisons(user, list, total)
    matchups = []
    for comparison in comparisons:
        matchups.append(Matchup.objects.create(
            winner=comparison[0], loser=comparison[1], judge=user))
    return matchups
    
    # else: return find_random_comparisons(list, total)


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
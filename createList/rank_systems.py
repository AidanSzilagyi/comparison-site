from .models import List, Thing, Matchup, SeenThing
import random

def process_matchup_results(user, list, results):
    print("TODO")


def generate_comparisons(user, list, limit):
    total = limit * 2
    if list.num_things < total:
        total = list.num_things - (list.num_things % 2)
    
    available_things = Thing.objects.filter(list=list, in_use=False).exclude(
        id__in=SeenThing.objects.filter(user=user).values('thing_id'))
    
    
    
    #if list.comparison_method == 'bradley_terry':
    #    return bradley_terry_find_comparisons(list, total)
    return find_random_comparisons(list, total)


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
from .models import List, Thing, MatchUp
import random

def generate_comparisons(user, list, limit):
    total = limit * 2
    if list.num_things < total:
        total = list.num_things - (list.num_things % 2)
        
    #if list.comparison_method == 'bradley_terry':
    #    return bradley_terry_find_comparisons(list, total)
    return find_random_comparisons(list, total)

def bradley_terry_find_comparisons(list, total):
    print("ahhh")
    

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
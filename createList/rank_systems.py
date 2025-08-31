from django.utils import timezone
from .models import List, Thing, Matchup, RecentListInteraction
import random
from .bradley_terry_model import BradleyTerryModel
from .ranking_util import get_matchups_awaiting_response
import json

def initialize_list_model(list):
    get_comparison_model(list).initialize_list_model(list)

def process_matchup_result(user, list, matchup_id, choice):
    matchup = Matchup.objects.get(id=matchup_id)
    matchup.awaiting_response = False
    if choice == 2:
        temp = matchup.loser
        matchup.loser = matchup.winner
        matchup.winner = temp
    matchup.save()
    matchup.winner.wins += 1
    matchup.loser.losses += 1
    print(f"winner: {matchup.winner} --- loser: {matchup.loser}")
    matchup.winner.save()
    matchup.loser.save()
    
    list.comparisons_made += 1
    list.save()
    update_recent_lists(user, list)
    get_comparison_model(list).update_rankings(user, list, matchup)

def generate_matchup_json(user, list, additional_matchups_required=0, sent_matchups=[]):
    matchups = generate_matchups(user, list, additional_matchups_required, sent_matchups)
    matchup_json = []
    for matchup in matchups:
        matchup_json.append({
            "id": str(matchup.id),
            "thing1": {
                "name": matchup.winner.name if matchup.winner.name else None,
                "image": matchup.winner.image.url if matchup.winner.image else None
            },
            "thing2": {
                "name": matchup.loser.name if matchup.loser.name else None,
                "image": matchup.loser.image.url if matchup.loser.image else None
            } 
        })
    return json.dumps(matchup_json)

def generate_matchups(user, tlist, additional_matchups_required, sent_matchups):
    total = get_comparison_model(tlist).get_num_matchups_to_send(tlist)
    total += 2 - len(sent_matchups)
    
    matchups = list(get_matchups_awaiting_response(user, tlist, sent_matchups))
    if len(matchups) >= total:
        print("first", matchups[:total])
        return matchups[:total]
        
    comparisons = get_comparison_model(tlist).get_comparisons(user, tlist, sent_matchups)
    for comparison in comparisons[:total - len(matchups)]:
        matchups.append(Matchup.objects.create(
            winner=comparison[0], loser=comparison[1], user=user))
        
    print("second", matchups)
    return matchups

def get_comparison_model(list):
    if list.comparison_method == 'bradley_terry':
        return BradleyTerryModel()


def update_recent_lists(user, list):
    RecentListInteraction.objects.update_or_create(user=user,list=list, 
        defaults={'interaction_time': timezone.now()}
    )
    least_recent_ids = RecentListInteraction.objects.filter(user=user).order_by('-interaction_time') \
                  .values_list('id', flat=True)[5:]
    
    RecentListInteraction.objects.filter(id__in=least_recent_ids).delete()
import math
from .models import List, Thing, Matchup, SeenThing
from django.db.models import Q
from collections import defaultdict
from .ranking_util import get_available_things, exclude_used_comparisons, get_matchups_awaiting_response
import decimal

# TODO: Test for floating point inaccuracy
lr = 0.01 # Learning Rate
random_rounds = 3  # The first few rounds, matchups are randomly chosen
batch_reset_percent = 0.05 # A batch update is performed after the this many comparisons,  
                           # as a percent of the total number of things in the list
min_batch_reset = 1
MIN_PROB = 1e-10
class BradleyTerryModel:
    @staticmethod
    def get_comparisons(user, list, sent_matchups):
        comparisons = []
        available_things = get_available_things(user, list)
        
        info_dict = {}
        for i in range(len(available_things) - 1):
            info_dict[i] = BradleyTerryModel.calculate_info(available_things[i], available_things[i + 1])
        info_list = sorted(info_dict.items(), key=lambda item: item[1], reverse=True)
        for entry in info_list:
            comparisons.append([available_things[entry[0]], available_things[entry[0] + 1]])
        comparisons = exclude_used_comparisons(comparisons, sent_matchups)
        return comparisons

    @staticmethod
    def update_rankings(_, list, matchup):
        s_i = matchup.winner.rating
        s_j = matchup.loser.rating
        win_probability = math.exp(s_i) / (math.exp(s_i) + math.exp(s_j))
        matchup.winner.rating += decimal.Decimal(lr * (1 - win_probability))
        matchup.loser.rating -= decimal.Decimal(lr * (1 - win_probability))
        matchup.winner.save()
        matchup.loser.save()
        if list.batch_countdown > 0:
            list.batch_countdown -= 1
        if (list.batch_countdown == 0 and list.comparisons_made > list.num_things * random_rounds): # subtract the parallelize buffer later
            BradleyTerryModel.batch_update(list)
            list.batch_countdown = max((int) (batch_reset_percent * list.num_things), min_batch_reset)
        list.save()

    @staticmethod
    def batch_update(list):
        things = Thing.objects.filter(list=list)
        all_matchups = Matchup.objects.filter(winner__list=list)
        
        id_to_index = {thing.id: idx for idx, thing in enumerate(things)}
        matchup_records = defaultdict(lambda: {'wins': 0, 'losses': 0})
        for matchup in all_matchups:
            i = id_to_index[matchup.winner_id] 
            j = id_to_index[matchup.loser_id]
            if i < j:
                matchup_records[(i, j)]['wins'] += 1
            else:
                matchup_records[(j, i)]['losses'] += 1
        index_to_id = {idx: thing_id for thing_id, idx in id_to_index.items()}
        
        ratings = BradleyTerryModel.gradient_ascent(matchup_records, list.num_things)

        for i in range(list.num_things):
            thing = Thing.objects.get(id=index_to_id[i])
            thing.rating = decimal.Decimal(ratings[i])
            thing.save()

    def gradient_ascent(matchup_records, num_things):
        ratings = [0.0 for _ in num_things]
        gradients = [0.0 for _ in num_things]
        log_likelihood = 0.0
        prev_log_likelihood = 1.0
        iterations = 0
        while(abs(log_likelihood - prev_log_likelihood) < 1e-5 and iterations < 1000):
            for (i, j), record in matchup_records.items():
                wins = record['wins'], losses = record['losses']
                num_matchups = wins + losses
                # Is num_matchups ever 0?
                
                win_prob = math.exp(ratings[i]) / (math.exp(ratings[i]) + math.exp(ratings[j]))
                win_prob = max(min(win_prob, 1 - MIN_PROB), MIN_PROB)

                gradients[i] += wins - num_matchups * win_prob
                gradients[i] += losses - num_matchups * win_prob
                prev_log_likelihood = log_likelihood
                log_likelihood += wins * math.log(win_prob) + losses * math.log(1 - win_prob)
            
            for i in range(num_things):
                ratings[i] += lr * gradients[i]
                
            iterations += 1
        
        return ratings

    @staticmethod
    def calculate_info(first: Thing, second: Thing):
        wp = math.exp(first.rating) / (math.exp(first.rating) + math.exp(second.rating))
        return wp * (1 - wp) * (1 / (1 + first.times_compared) + 1 / (1 + second.times_compared))    
    
# Given a list of positive real numbers, find their geometric mean m
# and return the list with each value divided by m
def get_normalized_parameters(list):
    product = 1
    for num in list:
        product *= num
    geometric_mean = product ** (1/len(list))
    return [num / geometric_mean for num in list]

# Update after each
# s_i = s_i + learning_rate * (1- p_{ij})
# s_j = s_j + learning_rate * (1- p_{ij})

# After a bunch, run algorithm to update all

# To get a new comparison:
# 1. Keep track of a user's 50% most recently compared items and don't use them
# 2. Info = p_ij (1 - p_ij) * (1/(1+c_i) + 1/(1+c_j))
#    or
#    Random for first 2-3 comparisons of each object
# 3. Parallelize: How?
#       a. Mark first five most info picked as reserved?
#           

# More randomness (ChatGPT gives epsilon-greedy hybrid with 10%
# for pick to be a random one)
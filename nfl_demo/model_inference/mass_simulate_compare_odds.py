from .game_interaction import *
import math
from tqdm import tqdm
import os.path
import statsmodels as sm
import random
import requests
import numpy as np
from scipy import stats
import json
MAX_EFFECTIVE_TIME = 900
def calculate_moneyline_odds(winning_prob):
    """
    Calculate moneyline odds from winning probability.
    For favorites (winning probability > 50%), the odds will be negative.
    For underdogs (winning probability < 50%), the odds will be positive.
    """
    if winning_prob > 0.5:
        # Negative odds for favorites
        moneyline_odds = -100 / (winning_prob - 1)
    else:
        # Positive odds for underdogs
        moneyline_odds = (1 / (winning_prob)) * 100 - 100
    
    return round(moneyline_odds)


def calculate_implied_probability(moneyline_odds):
    """
    Convert moneyline odds to implied probability.
    Positive odds for underdogs and negative odds for favorites.
    """
    if moneyline_odds > 0:
        implied_prob = 100 / (moneyline_odds + 100)
    else:
        implied_prob = -moneyline_odds / (-moneyline_odds + 100)
    
    return implied_prob


def calculate_edge(simulated_prob, market_odds):
    """
    Calculate edge between simulated probability and market odds implied probability.
    """
    implied_prob = calculate_implied_probability(market_odds)
    edge = (simulated_prob - implied_prob) / implied_prob * 100
    return round(edge, 2)


def main():
    # Example: Simulated run data for Team A and Team B
    total_simulations = 10000
    team_a_wins = 6100  # Simulated runs where Team A wins
    team_b_wins = 3900  # Simulated runs where Team B wins

    # Step 1: Calculate winning probabilities
    team_a_prob = team_a_wins / total_simulations
    team_b_prob = team_b_wins / total_simulations

    print(f"Team A Winning Probability: {team_a_prob * 100:.2f}%")
    print(f"Team B Winning Probability: {team_b_prob * 100:.2f}%")

    # Step 2: Calculate moneyline odds based on simulated probabilities
    team_a_moneyline = calculate_moneyline_odds(team_a_prob)
    team_b_moneyline = calculate_moneyline_odds(team_b_prob)

    print(f"Team A Simulated Moneyline: {team_a_moneyline}")
    print(f"Team B Simulated Moneyline: {team_b_moneyline}")

    # Step 3: Compare with market odds and calculate edge
    # Example market odds
    market_team_a_odds = -150  # Market odds for Team A
    market_team_b_odds = +130  # Market odds for Team B

    # Calculate edge for each team
    team_a_edge = calculate_edge(team_a_prob, market_team_a_odds)
    team_b_edge = calculate_edge(team_b_prob, market_team_b_odds)

    print(f"Team A Edge: {team_a_edge}%")
    print(f"Team B Edge: {team_b_edge}%")

# if __name__ == "__main__":
#     main()

def add_to_running_dict_df(running_dict, game):
    if len(running_dict) == 0:
        for key in game:
            running_dict[key] = []
    for key, val in game.items():
        if key not in running_dict:
            print('Not all data have:', key)
            running_dict[key] = []
        running_dict[key].append(val)

def get_predicted_win_loss(H_minus_A_history, odds_row_ML, home_spread_close, home_spread_final):
    count_home_wins = sum(i > 0 for i in H_minus_A_history)
    count_home_ties = sum(i == 0 for i in H_minus_A_history)
    count_home_losses = sum(i < 0 for i in H_minus_A_history)
    if count_home_wins + count_home_losses < 1: # if the first game was a tie
        return None, None

    propo_win = count_home_wins / (count_home_wins + count_home_losses)
    #se = math.sqrt(propo_win * (1 - propo_win) / (count_home_losses + count_home_wins))
    #upper_bound = propo_win + 2*se
    #lower_bound = propo_win - 2*se
    # plotting a couple different intervals for fun
    for method in ['normal', 'beta']: #  'agresti_coull',  'wilson',  ,'jeffreys'
        lower_bound, upper_bound = sm.stats.proportion.proportion_confint(count_home_wins,
                                                                          count_home_wins + count_home_losses,
                                                                          alpha=.05, method=method.lower())
        print(method[0:6], '\tSim W/L %:', round(propo_win, 2), '[', round(lower_bound, 2), ',', round(upper_bound, 2),'] n =', count_home_wins + count_home_losses)
    #lower_bound, upper_bound = sm.stats.proportion.proportion_confint(count_home_wins, count_home_wins + count_home_losses, alpha=.05, method='jeffreys')
    #print('Jeff: \tSim W/L %:', round(propo_win, 2), '[', round(lower_bound,2) , ',', round(upper_bound,2),'] . n =', count_home_wins + count_home_losses)
    #lower_bound, upper_bound = sm.stats.proportion.proportion_confint(count_home_wins, count_home_wins + count_home_losses, alpha=.05, method='wilson')
    #print('Wilson: \tSim W/L %:', round(propo_win, 2), '[', round(lower_bound,2) , ',', round(upper_bound,2),'] . n =', count_home_wins + count_home_losses)

    if home_spread_close > 0:
        ML_WL = odds_row_ML / (100 + odds_row_ML)
        print('ML  W/L %:',round( ML_WL,2))
    elif home_spread_close < 0:
        ML_WL = 100 / (100 + odds_row_ML)
        print('ML  W/L %:',round( ML_WL,2))
    else:
        ML_WL = .5
        print('Vegas says they tie?')
    p_dif = int(abs(ML_WL - propo_win)*100)
    return better_propo_win_than_vegas(propo_win, ML_WL, home_spread_final), p_dif

def better_propo_win_than_vegas(propo_win, ML_WL, final):
    if final > 0:
        win = 1
    elif final < 0:
        win = 0
    else:
        win = .5
    return is_better_than_vegas_over_under(propo_win, ML_WL, win)

def print_percentiles(history, percentile_break):
    history.sort()
    percentile_results_str = 'n = ' + str(len(history)) + '. '
    for percentile in frange(0, 1.0, step=percentile_break):
        n_tile = int(len(history) * percentile)
        score_dif = history[n_tile]
        if str(round(percentile, 2)) == '.5':
            percentile_results_str = percentile_results_str + ' | ' + colored(str(round(percentile, 2)) + '%: = ' + str(score_dif), 'magenta')
        else:
            percentile_results_str = percentile_results_str + ' | ' + str(round(percentile, 2)) + '%: = ' + str(score_dif)
    print(percentile_results_str)

def is_better_than_vegas_over_under(my_over_under, vegas_over_under, final_total):
    if abs(my_over_under - final_total) > abs(vegas_over_under - final_total):
        return 0
    elif abs(my_over_under - final_total) < abs(vegas_over_under - final_total):
        return 1
    else:
        return 0.5 # vegas and I had equally accurate predictions

def accuracy_dif(A, B, correct):
    return abs(abs(A - correct) - abs(B - correct))

def extract_info(H_minus_A_history, H_plus_A_history, odds_row, home_spread_open, home_spread_close, percentile_break):

    # print('Actual:', odds_row['final_real_home_minus_away'])

    AST_open_dif = accuracy_dif(stat.median(H_minus_A_history), home_spread_open,
                                odds_row['final_real_home_minus_away'])
    better_ATS_open = is_better_than_vegas_over_under(stat.median(H_minus_A_history), home_spread_open,
                                                      odds_row['final_real_home_minus_away'])
    if better_ATS_open:
        print(colored('My spread line is better than vegas open', 'green'), 'by',
              colored(str(AST_open_dif) + ' points!', 'magenta'))
    else:
        print(colored('My spread line is worse than vegas open', 'red'), 'by',
              colored(str(AST_open_dif) + ' points.', 'magenta'))
        AST_open_dif = AST_open_dif * -1

    better_ATS_close = is_better_than_vegas_over_under(stat.median(H_minus_A_history), home_spread_close,
                                                       odds_row['final_real_home_minus_away'])
    AST_close_dif = accuracy_dif(stat.median(H_minus_A_history), home_spread_close,
                                 odds_row['final_real_home_minus_away'])
    if better_ATS_close:
        print(colored('My spread line is better than vegas close', 'green'), 'by',
              colored(str(AST_close_dif) + ' points!', 'magenta'))
    else:
        print(colored('My spread line is worse than vegas close', 'red'), 'by',
              colored(str(AST_close_dif) + ' points.', 'magenta'))
        AST_close_dif = AST_close_dif * -1

    print('Final difference:', odds_row['final_real_home_minus_away'])
    WL_better_than_vegas, p_dif_temp = get_predicted_win_loss(H_minus_A_history, odds_row['ML'], home_spread_close,
                                                              odds_row['final_real_home_minus_away'])
    if p_dif_temp is not None:
        p_dif = p_dif_temp
    else:
        p_dif = 0
    if WL_better_than_vegas:
        print(colored('My WL is better than vegas!', 'green'), 'by', colored(str(p_dif) + '%!', 'magenta'))
    else:
        print(colored('My WL is worse than vegas.', 'red'), 'by', colored(str(p_dif) + '%.', 'magenta'))
        p_dif = p_dif * -1  # giving it a sign for saving

    print('-')
    print('Median predicted total:', stat.median(H_plus_A_history))
    print('Over-under open:', odds_row['over_under_open'], ', close:', odds_row['over_under_close'])
    print_percentiles(H_plus_A_history, percentile_break)
    final_total = odds_row['final_real_home_score'] + odds_row['final_real_away_score']
    print('Final total:', final_total)
    over_under_better_open = is_better_than_vegas_over_under(stat.median(H_plus_A_history), odds_row['over_under_open'],
                                                             final_total)
    over_under_better_close = is_better_than_vegas_over_under(stat.median(H_plus_A_history),
                                                              odds_row['over_under_close'], final_total)
    OU_open_better_dif = accuracy_dif(stat.median(H_plus_A_history), odds_row['over_under_open'], final_total)
    OU_close_better_dif = accuracy_dif(stat.median(H_plus_A_history), odds_row['over_under_close'], final_total)

    if over_under_better_open:
        print(colored('My over under better than vegas open', 'green'), 'by',
              colored(str(OU_open_better_dif) + ' points!', 'magenta'))
    else:
        print(colored('My over under worse than vegas open.', 'red'), 'by',
              colored(str(OU_open_better_dif) + ' points.', 'magenta'))
        OU_open_better_dif = OU_open_better_dif * -1
    if over_under_better_close:
        print(colored('My over under better than vegas close', 'green'), 'by',
              colored(str(OU_close_better_dif) + ' points!', 'magenta'))
    else:
        print(colored('My over under worse than vegas close.', 'red'), 'by',
              colored(str(OU_close_better_dif) + ' points.', 'magenta'))
        OU_close_better_dif = OU_close_better_dif * -1
    print()
    print()
    return over_under_better_open, over_under_better_close, WL_better_than_vegas, better_ATS_open, better_ATS_close, AST_open_dif, AST_close_dif, OU_open_better_dif, OU_close_better_dif, final_total


def simulate_game_and_analyze(odds_row, running_dict, n_sims=25, percentile_break=0.1, week=14, excl_vs_before=False,home_mod=None):

    if odds_row['week'] != week:
        return

    print('Focus on week:', week)

    H_team = odds_row['home']
    A_team = odds_row['away']
    #if 'GB' not in [H_team, A_team]:
    #    return
    if excl_vs_before:
        excl_str = '_excl'
    else:
        excl_str = ''

    if home_mod is not None:
        excl_str = excl_str + str('_hm.' + str(home_mod))

    fn = 'results_save\\yr.' + str(odds_row['year']) + '_wk.' + str(odds_row['week']) + excl_str + '_H.' + H_team + '_A.' + A_team + '_n.' + str(n_sims) + '_results.pkl'
    if os.path.exists(fn):
        return

    df = get_df(odds_row['year'], odds_row['week'], excl_vs_before=excl_vs_before) # False = df is based on data before some week. True = df is based on all other weeks

    H_minus_A_history = []
    H_plus_A_history = []

    if odds_row['favorite'] == odds_row['home']:
        home_spread_open = odds_row['spread_open']
        home_spread_close = odds_row['spread_close']
    else:
        home_spread_open = -1*odds_row['spread_open']
        home_spread_close = -1*odds_row['spread_close']

    n_home_wins = 0
    n_away_wins = 0
    n_ties = 0
    p_dif = 0
    for sim_num in tqdm(range(0, n_sims)):
        game = Game(H_team, A_team, df, print=False, max_effective_time=MAX_EFFECTIVE_TIME)
        for i in range(0, 300): # second number can be anything big
            is_game_ended = game.simulate_play()
            if is_game_ended:
                final_score = game.scores
                break
        if home_mod is not None:
            H_minus_A_history.append(final_score[H_team] - final_score[A_team] + home_mod)
        else:
            H_minus_A_history.append(final_score[H_team] - final_score[A_team])
        H_plus_A_history.append(final_score[H_team] + final_score[A_team])

        if final_score[H_team] - final_score[A_team] > 0:
            n_home_wins += 1
        elif final_score[H_team] - final_score[A_team] < 0:
            n_away_wins += 1
        else:
            n_ties += 1

        print()
        print('Week:', odds_row['week'])
        print('Home:', H_team, 'Away:', A_team)
        print('Expected favorite:', odds_row['favorite'], '. Home Spread open:', home_spread_open,
              '. Home Spread close:',
              home_spread_close)
        print('Median Home:', H_team, 'minus Away:', A_team, 'score:', stat.median(H_minus_A_history))
        print_percentiles(H_minus_A_history, percentile_break)

        over_under_better_open, over_under_better_close, WL_better_than_vegas, better_ATS_open, better_ATS_close, AST_open_dif, AST_close_dif, OU_open_better_dif, OU_close_better_dif, final_total = \
            extract_info(H_minus_A_history, H_plus_A_history, odds_row, home_spread_open, home_spread_close, percentile_break)


    if odds_row['final_real_home_minus_away'] > 0:
        H_win = 1
    elif odds_row['final_real_home_minus_away'] < 0:
        H_win = 0
    else:
        H_win = .5

    n_games = n_home_wins + n_away_wins + n_ties
    p_home_win = n_home_wins / n_games
    p_away_win = n_away_wins / n_games
    p_tie = n_ties / n_games
    final_data = {'home': H_team, 'away': A_team, 'p_home_win': p_home_win, 'p_away_win': p_away_win, 'p_tie': p_tie,
                  'home_spread_open': home_spread_open, 'home_spread_close': home_spread_close,
                  'pred_spread_median': stat.median(H_minus_A_history), 'pred_spread_avg': stat.mean(H_minus_A_history),
                  'over_under_better_open': over_under_better_open, 'over_under_better_close': over_under_better_close,
                  'WL_better_vegas': WL_better_than_vegas, 'better_ATS_open': better_ATS_open,
                  'better_ATS_close': better_ATS_close, 'n_sims': n_sims, 'excl_vs_before': excl_vs_before,
                  'True_H_win': H_win, 'True_H_minus_A': odds_row['final_real_home_minus_away'], 'True_total_score': final_total,
                  'n_ties': n_ties,
                  'AST_open_dif': AST_open_dif, 'AST_close_dif': AST_close_dif, 'p_dif': p_dif,
                  'OU_open_better_dif': OU_open_better_dif, 'OU_close_better_dif': OU_close_better_dif, 'H_minus_A_history': H_minus_A_history,
                  'H_plus_A_history': H_plus_A_history}
    print('Final data:', final_data)
    with open(fn, 'wb') as file:
        pickle.dump(final_data, file)
    add_to_running_dict_df(running_dict, final_data)

def load_odds_history_df(year):
    with open('historical_odds\\compiled' + str(year) + '.pkl', 'rb') as file:
        odds_data_df = pickle.load(file)
    return odds_data_df

def calculate_spread_win_probability(simulated_margins, spread_line):
    cover_count = sum(1 for margin in simulated_margins if margin > spread_line)
    return cover_count / len(simulated_margins)

# Function to calculate implied probability from odds
def calculate_implied_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)
def calculate_derived_edge_and_line(history_a, history_b, bookmaker_total, bookmaker_odds):
    # Calculate mean and standard deviation of total scores
    total_scores = np.array(history_a) + np.array(history_b)
    mean_total = np.mean(total_scores)
    std_total = np.std(total_scores, ddof=1)
    
    # Calculate probability of over based on normal distribution
    z_score = (bookmaker_total - mean_total) / std_total
    prob_over = 1 - stats.norm.cdf(z_score)
    
    # Convert bookmaker odds to implied probability
    over_odds, under_odds = bookmaker_odds
    implied_prob_over = 1 / (1 + over_odds / 100) if over_odds > 0 else -over_odds / (-over_odds + 100)
    implied_prob_under = 1 / (1 + under_odds / 100) if under_odds > 0 else -under_odds / (-under_odds + 100)
    
    # Calculate edge
    edge_over = prob_over - implied_prob_over
    edge_under = (1 - prob_over) - implied_prob_under
    
    # Calculate fair line
    fair_odds_over = (1 / prob_over - 1) * 100
    fair_odds_under = (1 / (1 - prob_over) - 1) * 100
    
    return {
        "Derived Over/Under Line": mean_total,
        "Edge Over": edge_over,
        "Edge Under": edge_under,
        "Fair Odds Over": fair_odds_over,
        "Fair Odds Under": fair_odds_under
    }

# Function to calculate edge based on simulated probability and implied probability from market odds
def calculate_edge(simulated_prob, market_odds):
    implied_prob = calculate_implied_probability(market_odds)
    return (simulated_prob - implied_prob) * 100  # Edge as a percentage

import statistics

def calculate_american_odds(wins, total_games):
    probability = wins / total_games
    if probability > 0.5:
        return int(round(-100 * (probability / (1 - probability))))
    elif probability < 0.5:
        return int(round(100 * ((1 - probability) / probability)))
    else:
        return 100  # Even odds

def analyze_games(team_a_history, team_b_history):
    total_games = len(team_a_history)
    team_a_wins = sum(1 for a, b in zip(team_a_history, team_b_history) if a > b)
    team_b_wins = sum(1 for a, b in zip(team_a_history, team_b_history) if b > a)

    team_a_odds = calculate_american_odds(team_a_wins, total_games)
    team_b_odds = calculate_american_odds(team_b_wins, total_games)

    total_scores = [a + b for a, b in zip(team_a_history, team_b_history)]
    over_under = statistics.mean(total_scores)

    return {
        "Team A Odds": team_a_odds,
        "Team B Odds": team_b_odds,
        "Over/Under": over_under
    }

def adjust_odds_to_100_120_range(odds1, odds2):
    # Store the original signs
    sign1 = 1 if odds1 >= 0 else -1
    sign2 = 1 if odds2 >= 0 else -1
    
    # Work with absolute values
    abs_odds1, abs_odds2 = abs(odds1), abs(odds2)
    
    # Find the minimum and maximum of the absolute odds
    min_odds = min(abs_odds1, abs_odds2)
    max_odds = max(abs_odds1, abs_odds2)
    
    # Calculate the scaling factor
    scale_factor = 20 / (max_odds - min_odds) if max_odds != min_odds else 1
    
    # Adjust the odds
    adjusted1 = 100 + (abs_odds1 - min_odds) * scale_factor
    adjusted2 = 100 + (abs_odds2 - min_odds) * scale_factor
    
    # Reapply the original signs
    adjusted1 = sign1 * round(adjusted1)
    adjusted2 = sign2 * round(adjusted2)
    
    return adjusted1, adjusted2

def adjust_odds_between_100_120(odds1, odds2):
    # Convert American odds to implied probabilities
    def odds_to_prob(odds):
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return abs(odds) / (abs(odds) + 100)
    
    prob1 = odds_to_prob(odds1)
    prob2 = odds_to_prob(odds2)
    
    # Normalize probabilities
    total_prob = prob1 + prob2
    norm_prob1 = prob1 / total_prob
    norm_prob2 = prob2 / total_prob
    
    # Scale normalized probabilities to 100-120 range
    adjusted1 = 100 + (norm_prob1 * 20)
    adjusted2 = 100 + (norm_prob2 * 20)
    
    # Round to nearest integer
    return round(adjusted1), round(adjusted2)

def calculate_american_odds_2(a_history, b_history):
    a_mean = np.median(a_history)
    b_mean = np.median(b_history)
    spread = round(b_mean - a_mean, 1)
    
    # Calculate probabilities of each team covering the spread
    b_covers = sum(b > a + spread for a, b in zip(a_history, b_history))
    a_covers = len(a_history) - b_covers
    prob_b_covers = b_covers / len(a_history)
    prob_a_covers = a_covers / len(a_history)
    
    # Convert probabilities to American odds
    def prob_to_american_odds(prob):
        # print("what are the odds :-",prob,round(-100 / (prob - 1)),round((100 / prob) - 100))
        if prob > 0.5:
            return round(-100 / (prob - 1))
        else:
            return round((100 / prob) - 100)
    
    b_odds = prob_to_american_odds(prob_b_covers)
    a_odds = prob_to_american_odds(prob_a_covers)
    
    return spread, b_odds, a_odds

import random

# class Team:
#     def __init__(self, name, recent_scores, home_advantage=2):
#         self.name = name
#         self.recent_scores = recent_scores
#         self.home_advantage = home_advantage
        
#     def average_score(self):
#         return sum(self.recent_scores) / len(self.recent_scores)
    
#     def form(self):
#         # Simple form calculation: trend of last 3 games
#         if len(self.recent_scores) >= 3:
#             return sum(self.recent_scores[-3:]) / 3 - self.average_score()
#         return 0

# def calculate_betting_line(home_team, away_team):
#     # Basic point difference
#     point_diff = home_team.average_score() - away_team.average_score()
    
#     # Adjust for home advantage
#     point_diff += home_team.home_advantage
    
#     # Adjust for recent form
#     point_diff += home_team.form() - away_team.form()
    
#     # Add some randomness to simulate other factors (injuries, weather, etc.)
#     point_diff += random.uniform(-3, 3)
    
#     # Round to nearest 0.5
#     return round(point_diff * 2) / 2

# def generate_moneyline(spread):
#     if spread > 0:
#         favorite_odds = -110 - abs(spread) * 10
#         underdog_odds = 100 + abs(spread) * 10
#     else:
#         favorite_odds = -110 - abs(spread) * 10
#         underdog_odds = 100 + abs(spread) * 10
    
#     return round(favorite_odds), round(underdog_odds)

class Team:
    def __init__(self, name, recent_scores, home_advantage=2):
        self.name = name
        self.recent_scores = recent_scores
        self.home_advantage = home_advantage
        
    def average_score(self):
        return sum(self.recent_scores) / len(self.recent_scores)
    
    def form(self):
        if len(self.recent_scores) >= 3:
            return sum(self.recent_scores[-3:]) / 3 - self.average_score()
        return 0

def calculate_betting_line(home_team, away_team):
    point_diff = home_team.average_score() - away_team.average_score()
    point_diff += home_team.home_advantage
    point_diff += home_team.form() - away_team.form()
    point_diff += random.uniform(-3, 3)
    return round(point_diff * 2) / 2

def generate_moneyline(spread):
    if spread > 0:
        favorite_odds = -110 - abs(spread) * 10
        underdog_odds = 100 + abs(spread) * 10
    else:
        favorite_odds = -110 - abs(spread) * 10
        underdog_odds = 100 + abs(spread) * 10
    return round(favorite_odds), round(underdog_odds)

def calculate_totals_line(home_team, away_team):
    predicted_total = home_team.average_score() + away_team.average_score()
    predicted_total += home_team.home_advantage / 2
    predicted_total += (home_team.form() + away_team.form()) / 2
    predicted_total += random.uniform(-5, 5)
    return round(predicted_total * 2) / 2

def generate_totals_odds(total, baseline_total=47):
    # Adjust odds based on difference from baseline
    difference = total - baseline_total
    adjustment = abs(difference) * 5  # 5 points per point difference
    
    if difference > 0:
        over_odds = -100 - adjustment
        under_odds = 100 + adjustment
    elif difference < 0:
        over_odds = 100 + adjustment
        under_odds = -100 - adjustment
    else:
        over_odds = -110
        under_odds = -110
    
    return round(over_odds), round(under_odds)

def sim_super_bowl(df,co_eff,is_custom_sim,team_A='DAL', team_B='NYG', percentile_break=0.2, n_sims=3, year=2024, week=1, excl_vs_before=True):
    # df = get_df(year, week, excl_vs_before=excl_vs_before) # False = df is based on data before some week. True = df is based on all other weeks
    A_minus_B_history = []
    A_plus_B_history = []
    A_history = []
    B_history = []
    A_wins = []
    B_wins = []
    for n_sim in tqdm(range(n_sims)):
        game = Game(team_A, team_B, df,co_eff ,is_custom_sim, print=True, max_effective_time=MAX_EFFECTIVE_TIME)
        for i in range(0, 300):  # second number can be anything big
            is_game_ended = game.simulate_play()
            if is_game_ended:
                final_score = game.scores
                break
        if final_score[team_A]>final_score[team_B]:
            A_wins.append(1)
            B_wins.append(0)
        else:
            A_wins.append(0)
            B_wins.append(1)
        A_history.append(final_score[team_A])
        B_history.append(final_score[team_B])
        A_minus_B_history.append(final_score[team_A] - final_score[team_B])
        A_plus_B_history.append(final_score[team_A] + final_score[team_B])
        print('A history:', A_history)
        print('B history:', B_history)
        print('A minus B history:', A_minus_B_history)
        print()
        print('Team A:', team_A, 'Team B:', team_B)
        # print('Median Home:', team_A, 'minus Away:', team_B, 'score:', stat.median(A_minus_B_history))
        # print_percentiles(A_minus_B_history, percentile_break)
        print('.')
        # print('Median Over under:', stat.median(A_plus_B_history))
        # print_percentiles(A_plus_B_history, percentile_break)
        count_home_wins = sum(i > 0 for i in A_minus_B_history)
        count_home_ties = sum(i == 0 for i in A_minus_B_history)
        count_home_losses = sum(i < 0 for i in A_minus_B_history)
        if count_home_wins + count_home_losses < 1:  # if the first game was a tie
            return None, None

        propo_win = count_home_wins / (count_home_wins + count_home_losses)
        # print("propability win",propo_win)
        
        # print('propo ties:', count_home_ties / (count_home_ties + count_home_wins + count_home_losses))
        se = math.sqrt(propo_win * (1 - propo_win) / (count_home_losses + count_home_wins))
        upper_bound = propo_win + 2*se
        lower_bound = propo_win - 2*se
        # plotting a couple different intervals for fun
        for method in ['normal', 'beta']:  # 'agresti_coull',  'wilson',  ,'jeffreys'
            lower_bound, upper_bound = sm.stats.proportion.proportion_confint(count_home_wins,
                                                                              count_home_wins + count_home_losses,
                                                                              alpha=.05, method=method.lower())
            # print(method[0:6], '\tSim W/L %:', round(propo_win, 2), '[', round(lower_bound, 2), ',',
                #   round(upper_bound, 2), '] n =', count_home_wins + count_home_losses)
    total_simulations = n_sims
    
    balanced_wins_a = 0
    balanced_wins_b = 0 
    for count_1  in  range(len(A_history)):
        if A_history[count_1]>B_history[count_1]:
            balanced_wins_a+=1
        elif A_history[count_1]<B_history[count_1]:
            balanced_wins_b+=1 
        else:
            balanced_wins_a+=1 
    
    if (balanced_wins_a==len(A_history)) or (balanced_wins_b==len(B_history)):
        lst_of_indexes  =   random.sample(range(len(A_history)), 2)
        for index_1 in lst_of_indexes:
            # index_1 = random.randint(0,len(A_history))
            swap_temp =  A_history[index_1]
            swap_temp_2 = B_history[index_1]
            A_history[index_1] = swap_temp_2
            B_history[index_1] = swap_temp
    else:
        pass

    team_a_wins = sum(A_wins)  # Simulated runs where Team A wins
    team_b_wins = sum(B_wins)  # Simulated runs where Team B wins

    # Step 1: Calculate winning probabilities
    team_a_prob = team_a_wins / total_simulations
    team_b_prob = team_b_wins / total_simulations

    # print(f"Team A Winning Probability: {team_a_prob * 100:.2f}%")
    # print(f"Team B Winning Probability: {team_b_prob * 100:.2f}%")

    # Step 2: Calculate moneyline odds based on simulated probabilities
    # team_a_moneyline = calculate_moneyline_odds(team_a_prob)
    # team_b_moneyline = calculate_moneyline_odds(team_b_prob)

    # print(f"Team A Simulated Moneyline: {team_a_moneyline}")
    # print(f"Team B Simulated Moneyline: {team_b_moneyline}")

    team_a_scores = A_history  # New England Patriots' historical scores
    team_b_scores = B_history  # New York Jets' historical scores

    # Step 1: Calculate total points for each simulated game (sum of team scores)
    total_points = [a + b for a, b in zip(team_a_scores, team_b_scores)]
    print(f"Total Points for Each Game: {total_points}")

    # Function to calculate over/under win probability for a given line
    def calculate_over_under_probability(total_points, line):
        over_count = sum(1 for total in total_points if total > line)
        under_count = sum(1 for total in total_points if total < line)
        over_prob = over_count / len(total_points)
        under_prob = under_count / len(total_points)
        return over_prob, under_prob

    # Step 2: Iterate over possible over/under lines to find the optimal one
    def find_optimal_over_under_line(total_points):
        possible_lines = np.arange(20, 180, 0.5)  # Check totals from 20 to 80 in 0.5 increments
        optimal_line = None
        min_diff = float('inf')  # Start with a very high difference

        # Find the line where the probability of going over or under is closest to 50%
        for line in possible_lines:
            over_prob, under_prob = calculate_over_under_probability(total_points, line)
            diff = abs(over_prob - 0.5)  # We want the over probability closest to 50%
            
            if diff < min_diff:
                min_diff = diff
                optimal_line = line

        return optimal_line

    # Step 3: Calculate the optimal over/under line purely from simulations
    # optimal_over_under_line = find_optimal_over_under_line(total_points)
    # print(f"Optimal Over/Under Line: {optimal_over_under_line}")

    # Step 4: Calculate probabilities for over and under based on the optimal line
    # over_prob, under_prob = calculate_over_under_probability(total_points, optimal_over_under_line)

    # Step 5: Calculate the edge based on the simulated probabilities
    def calculate_edge(simulated_prob):
        return (simulated_prob - 0.5) * 100  # Edge compared to a "fair" 50% probability

    # over_edge = calculate_edge(over_prob)
    # under_edge = calculate_edge(under_prob)

    # Step 6: Create the table output for over/under
    # data = {
    #     'Market': ['Over', 'Under'],
    #     'Optimal Line': [f"{optimal_over_under_line:.1f}", f"{optimal_over_under_line:.1f}"],
    #     # 'Simulated Probability': [f"{over_prob:.2f}", f"{under_prob:.2f}"],
    #     'Edge': [f"{over_edge:.2f}%", f"{under_edge:.2f}%"]
    # }

    # Convert the data into a pandas DataFrame
    # df = pd.DataFrame(data)
    # print(df)
    team_a_history = A_history
    team_b_history = B_history

    results = analyze_games(team_a_history, team_b_history)
    adjusted_1 , adjusted_2  = adjust_odds_between_100_120(int(results['Team A Odds']),int(results['Team B Odds']))
    # Print results
    # print("over and under results : ------------------------------------")
    # print(f"Team A Line: {results['Team A Odds']:+d}")
    # print(f"Team B Line: {results['Team B Odds']:+d}")
    # print(f"Over/Under Edge: {results['Over/Under']:.2f}")
    # print("--------------------------------------------------------------")

    # total_A = sum(A_history)
    # total_B = sum(B_history)

    # # Calculate win probabilities (A vs B) for each matchup
    # probabilities_A = [a / (a + b) for a, b in zip(A_history, B_history)]
    # probabilities_B = [b / (a + b) for a, b in zip(A_history, B_history)]

    # # Convert probabilities to American odds
    def to_american_odds(probability):
        if probability > 0.5:
            return -((probability / (1 - probability)) * 100)
        else:
            return ((1 - probability) / probability) * 100

    # # Calculate American odds for both A and B histories
    # american_odds_A = [to_american_odds(prob) for prob in probabilities_A]
    # american_odds_B = [to_american_odds(prob) for prob in probabilities_B]

    # # Calculate the average probability for A and B
    # average_probability_A = sum(probabilities_A) / len(probabilities_A)
    # average_probability_B = sum(probabilities_B) / len(probabilities_B)

    # # Convert the average probabilities to American odds
    # single_odds_A = to_american_odds(average_probability_A)
    # single_odds_B = to_american_odds(average_probability_B)
    A_history_new = A_history
    B_history_new = B_history
    probabilities_A_new = [a / (a + b) if (a + b) != 0 else 0.5 for a, b in zip(A_history_new, B_history_new)]
    probabilities_B_new = [b / (a + b) if (a + b) != 0 else 0.5 for a, b in zip(A_history_new, B_history_new)]

    # Calculate the average probability for A and B
    average_probability_A_new = sum(probabilities_A_new) / len(probabilities_A_new)
    average_probability_B_new = sum(probabilities_B_new) / len(probabilities_B_new)

    # Convert the average probabilities to American odds
    single_odds_A_new = to_american_odds(average_probability_A_new)
    single_odds_B_new = to_american_odds(average_probability_B_new)

    single_odds_A_new, single_odds_B_new
    result_dict_ = {}
    print("----------------------moneyline results :  -----------------------------")

    print("team {} moneyline : {}".format(team_A,single_odds_A_new))
    result_dict_["team_a_moneyline"]=single_odds_A_new
    result_dict_["team_b_moneyline"]=single_odds_B_new

    print("team {} moneyline : {}".format(team_B,single_odds_B_new))
    print("\n")
    # print("---------------------------  -----------------------------")

    def calculate_spread_and_odds(team_a_scores, team_b_scores):
    # Calculate average scores
        team_a_avg = np.mean(team_a_scores)
        team_b_avg = np.mean(team_b_scores)
        
        # Calculate spread
        raw_spread = team_a_avg - team_b_avg
        spread = round(raw_spread * 2) / 2  # Round to nearest half-point
        
        # Determine favorite and underdog
        if spread > 0:
            favorite = "A"
            underdog = "B"
        else:
            favorite = "B"
            underdog = "A"
            spread = abs(spread)
        
        # Calculate win probabilities
        team_a_wins = sum(a >=b for a, b in zip(team_a_scores, team_b_scores))
        total_games = len(team_a_scores)
        prob_a = team_a_wins / total_games
        prob_b = 1 - prob_a
        
        # Convert probabilities to American odds
        def prob_to_american_odds(prob):
            if prob == 0 or prob == 1:
                return None  # Indicate impossibility
            elif prob > 0.5:
                return int(round(-100 / (prob - 1)))
            else:
                return int(round((1 / prob - 1) * 100))
        
        odds_a = prob_to_american_odds(prob_a)
        odds_b = prob_to_american_odds(prob_b)
        
        return {
            "spread": f"favourite team  : {favorite} edge : {spread}",
            "odds_a": f"+{odds_a}" if odds_a and odds_a > 0 else str(odds_a) if odds_a else "N/A",
            "odds_b": f"+{odds_b}" if odds_b and odds_b > 0 else str(odds_b) if odds_b else "N/A",
            "prob_a": prob_a,
            "prob_b": prob_b
        }

    # Example usage
    team_a_history = A_history
    team_b_history = B_history

    result = calculate_spread_and_odds(team_a_history, team_b_history)
    adjusted_3,adjusted_4 = adjust_odds_between_100_120(int(result['odds_a']),int(result['odds_b']))
    # print("spreads results : ---------------")
    # print(f"Spread Edge : {result['spread']}")
    # print(f"Team A Line: {result['odds_a']}")
    # print(f"Team B Line: {result['odds_b']}")

    spreads,odds_b,odds_a=calculate_american_odds_2(A_history,B_history)
    # print("spreads & Over and Under results : ---------------")
    # print(f"Spread Edge : {spreads}")
    # print(f"Team A Line: {odds_b}")
    # print(f"Team B Line: {odds_a}")
    steelers = Team(team_A, A_history)
    colts = Team(team_B, B_history)

    spread = calculate_betting_line(steelers, colts)
    favorite_ml, underdog_ml = generate_moneyline(spread)

    total = calculate_totals_line(steelers, colts)
    over_odds, under_odds = generate_totals_odds(total)
    result_dict_["team_a_spread"]=f"{-1*spread}"
    result_dict_["team_b_spread"]=f"{+1*spread}"
    result_dict_["team_a_spread_line"] = f"{favorite_ml}"
    result_dict_["team_b_spread_line"] = f"{underdog_ml}"
    result_dict_["team_a_totals"] = f"O{total}"
    result_dict_["team_b_totals"] = f"U{total}"
    result_dict_["team_a_totals_line"] = f"{over_odds}"
    result_dict_["team_b_totals_line"] = f"{under_odds}"


    print("------------------------Spreads results --------------------------------")
    print(f"Spread: {steelers.name} {-spread} | {colts.name} +{spread}")
    print(f"line: {steelers.name} {favorite_ml} | {colts.name} +{underdog_ml}")
    print("\n")
    print("------------------------Overs And Under results -----------------------------------------")
    print(f"Totals: O/U {total}")
    print(f"Over and Under Lines {steelers.name}/{colts.name}  :   Over {over_odds} | Under {under_odds}")
    print("\n")
    return result_dict_

    # steelers = Team(team_A, A_history)
    # colts = Team(team_B, B_history)

    # spread = calculate_betting_line(steelers, colts)
    # favorite_ml, underdog_ml = generate_moneyline(spread)

    # print(f"Spread: {steelers.name} {-spread} | {colts.name} +{spread}")
    # print(f"line: {steelers.name} {favorite_ml} | {colts.name} +{underdog_ml}")


    # Step 3: Compare with market odds and calculate edge
    # # Example market odds
    # market_team_a_odds = -150  # Market odds for Team A
    # market_team_b_odds = +130  # Market odds for Team B

    # # Calculate edge for each team
    # team_a_edge = calculate_edge(team_a_prob, market_team_a_odds)
    # team_b_edge = calculate_edge(team_b_prob, market_team_b_odds)

    # print(f"Team A Edge: {team_a_edge}%")
    # print(f"Team B Edge: {team_b_edge}%")

    # res= requests.get("https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=cd73d258cfcbe9d84c638496e13d6cc1&regions=us&markets=h2h,spreads,totals&oddsFormat=american&date=2024-09-20")
    # json_data = json.loads(res.text)
    # count = 0
    # bookmaker = json_data[0]["bookmakers"]
    
    # for market in bookmaker:
    #     print("bookmaker name: ",market["key"])
    #     for odds_type in market["markets"]:
    #         print(odds_type["key"],"odds type")
    #         if odds_type["key"]=="totals":
    #             over = {}
    #             under = {}
    #             for dct in odds_type["outcomes"]:
    #                 if dct["name"]=="Over":
    #                     over["price"]= dct["price"]
    #                     over["point"]=dct["point"]
    #                 elif dct["name"]=="Under":
    #                     under["price"]=dct["price"]
    #                     under["point"]=dct["point"]
                
                
    #             bookmaker_total = over["point"]
    #             bookmaker_odds = (over["price"], under["price"])  # (over, under)
    #             history_a = A_history
    #             history_b = B_history
    #             results = calculate_derived_edge_and_line(history_a, history_b, bookmaker_total, bookmaker_odds)

    #             for key, value in results.items():
    #                 print(f"{key}: {value:.2f}")
    #         if odds_type["key"]=="spreads":
                
    #             spread_lines_team_a = [odds_type["outcomes"][0]["point"]]
    #             odds_team_a = [odds_type["outcomes"][0]["price"]]
    #             spread_lines_team_b = [odds_type["outcomes"][0]["point"]]
    #             odds_team_b = [odds_type["outcomes"][0]["price"]]

    #             simulated_margins_team_a = A_minus_B_history
    #             simulated_margins_team_b = [-1*value for value in A_minus_B_history]
    #             # print(simulated_margins_team_a)
    #             # print(simulated_margins_team_b)
    #             # Calculate spread probabilities and edges
    #             spread_prob_team_a = [calculate_spread_win_probability(simulated_margins_team_a, spread_lines_team_a[0])]
    #             spread_prob_team_b = [calculate_spread_win_probability(simulated_margins_team_b, spread_lines_team_b[0])]

    #             edges_team_a = [calculate_edge(spread_prob_team_a[0], odds_team_a[0]), ]
    #             edges_team_b = [calculate_edge(spread_prob_team_b[0], odds_team_b[0]), ]

    #             data = {
    #                 'Game': [f"{team_A} vs {team_B} "],
    #                 'Spread Team A': [f"{spread_lines_team_a[0]} ({odds_team_a[0]})"],
    #                 'Edge Team A': [f"{edges_team_a[0]:.2f}%"],
    #                 'Spread Team B': [f"{spread_lines_team_b[0]} ({odds_team_b[0]})"],
    #                 'Edge Team B': [f"{edges_team_b[0]:.2f}%"]
    #             }

    #             # Convert to a DataFrame and display
    #             df = pd.DataFrame(data)
    #             print(df)


    

# if __name__ == '__main__':
    # MAX_EFFECTIVE_TIME = 900
    # if True:
    #     is_custom_sim = True
    #     # is_custom_sim = False
    #     co_eff = {}
        # co_eff['run_vs_pass'] = {'pos_team':0.1,'pos_winning*time_left*goal_yd':0.2,'pos_minus_def_score*time_left':0.2,'ydstogo':0.5}
        # co_eff['punt'] = {'pos_winning*ydstogo*goal_yd*time_left*pos_minus_def_score': 0.5, 'pos_team':0.5}
        # co_eff['punt_yds'] = {'goal_yd':1.0}
        # co_eff['FG_attempted']={'time_left*pos_down_three_or_less':0.33 , 'goal_yd*ydstogo': 0.33, 'time_left*pos_minus_def_score':0.33}
        # co_eff['FG_made'] = {'goal_yd':1}
        # co_eff['fumble']= {'def_team':0.25 , 'pos_team':0.25 , 'time_left':0.25, 'run_vs_pass':0.25}
        # co_eff['fumble_lost'] = {'run_vs_pass':1}
        # co_eff['fumble_yds'] ={'def_team':1}
        # co_eff['interception'] = {'time_left':0.333, 'pos_team':0.3333 , 'def_team':0.3333}
        # co_eff['int_yds'] = {'def_team':1}
    #     # sim_super_bowl(df,co_eff,is_custom_sim,team_A='NE', team_B='NYJ')
    # else:
    #     YEAR = 2019
    #     odds_data_df = load_odds_history_df(YEAR)
    #     running_dict = {}
    #     HOME_MOD = 2
    #     for idx, row in odds_data_df.iterrows():
    #         print(row)
    #         simulate_game_and_analyze(row, running_dict, n_sims=228, week=1, excl_vs_before=True, home_mod=None)
            #if len(running_dict) > 0:
                #print(':::RUNNING DICT:::')
                #print(running_dict)

'''
A history: [34, 24, 26, 20, 6, 24, 14, 23, 16, 7, 19, 6, 17, 3, 13, 20, 27, 19, 21, 17, 17, 21, 34, 13, 17, 3, 23, 16, 20, 19, 33, 7, 20, 20, 14, 16, 3, 16, 21, 10, 31, 10, 34, 17, 30, 6, 12, 13, 34, 21, 19, 34, 21, 10, 6, 16, 17, 39, 20, 13, 6, 3, 10, 34, 30, 16, 6, 14, 24, 20, 13, 16, 10, 14, 13, 10, 30, 23, 7, 7, 26, 17, 20, 14, 10, 17, 27, 17, 20, 7, 14, 12, 28, 20, 28, 35, 10, 17, 23, 37, 27, 0, 33, 16, 34, 23, 10, 27, 16, 3, 7, 3, 16, 27, 3, 21, 17, 21, 20, 0, 20, 21, 9, 24, 24, 31, 27, 24, 0, 27, 10, 17, 24, 19, 27, 14, 26, 30, 23, 26, 14, 36, 13, 13, 33, 17, 19, 16, 24, 30, 17, 13, 17, 16, 16, 34, 24, 24, 23, 23, 24, 27, 14, 27, 13, 23, 17, 21, 13, 20, 14, 37, 30, 3, 14, 23, 19, 13, 17, 24, 10, 13, 21, 20, 35, 23, 20, 19, 19, 6, 14, 27, 24, 31, 7, 20, 16, 30, 13, 21, 14, 17, 17, 27, 27, 30, 7, 21, 12, 27, 17, 7, 7, 31, 20, 20, 14, 13, 31, 10, 27, 20, 31, 34, 14, 21, 20, 20, 3, 23, 7, 30, 31, 17, 17, 7, 17, 10, 20, 21, 30, 10, 17, 14, 20, 13, 21, 38, 3, 24, 20, 24, 27, 16, 44, 9, 10, 30, 22, 23, 24, 35, 17, 24, 17, 27, 10, 19, 35, 27, 31, 13, 27, 12, 24, 13, 7, 14, 27, 24, 17, 13, 20, 6, 10, 24, 0, 17, 17, 24, 0, 37, 20, 7, 3, 16, 20, 10, 23, 19, 36, 23, 20, 16, 21, 35, 17, 14, 15, 34, 16, 34, 24, 13, 17, 14, 13, 24, 22, 28, 9, 21, 18, 20, 6, 10, 13, 20, 3, 3, 17, 12, 24, 17, 27, 42, 20, 10, 10, 10, 17, 14, 24, 13, 24, 17, 24, 20, 16, 14, 23, 7, 17, 17, 24, 10, 20, 23, 20, 21, 6, 31, 27, 14, 6, 14, 31, 14, 21, 33, 6, 30, 13, 10, 17, 20, 26, 20, 7, 6, 26, 24, 23, 13, 9, 13, 16, 6, 14, 21, 31, 10, 7, 24, 10, 14, 20, 19, 20, 20, 10, 17, 14, 17, 23, 10, 17, 36, 7, 17, 24, 17, 7, 17, 27, 18, 21, 17, 28, 13, 20, 6, 33, 35, 27, 24, 23, 23, 17, 23, 21, 17, 20, 27, 0, 10, 31, 7, 24, 20, 10, 20, 24, 23, 19, 17, 21, 0, 28, 7, 21, 14, 17, 16, 21, 27, 13, 20, 17, 0, 24, 10, 10, 20, 17, 17, 16, 24, 17, 17, 35, 17, 13, 21, 24, 24, 14, 16, 10, 27, 31, 21, 30, 31, 14, 13, 27, 7, 17, 21, 10, 17, 19, 24, 45, 21, 14, 21, 13, 3, 28, 27, 14, 13, 30, 42, 13, 13, 31, 13, 16, 30, 13, 21, 20, 17, 30, 17, 20, 10, 16, 19, 3, 21, 26, 20, 16, 31, 16, 17, 13, 20, 24, 17, 17, 10, 31, 14, 21, 20, 27, 13, 28, 17, 13, 16, 23, 24, 16, 33, 13, 24, 26, 20, 24, 16, 27, 17, 20, 23, 10, 17, 12, 17, 24, 31, 13, 26, 3, 0, 13, 31, 19, 7, 7, 20, 13, 13, 14, 7, 20, 12, 26, 20, 13, 23, 7, 9, 13, 14, 14, 23, 21, 13, 17, 7, 17, 24, 10, 9, 31, 17, 10, 0, 28, 24, 20, 21, 17, 6, 17, 33, 20, 10, 21, 9, 21, 27, 21, 13, 34, 17, 10, 23, 31, 13, 37, 12, 14, 3, 28, 12, 24, 27, 19, 30, 13, 17, 31, 27, 9, 13, 23, 16, 17, 34, 12, 7, 23, 3, 7, 20, 20, 17, 31, 10, 20, 20, 20, 16, 16, 19, 17, 31, 20, 6, 20, 24, 20, 17, 20, 16, 19, 30, 17, 28, 6, 28, 7, 20, 10, 0, 10, 31, 24, 20, 3, 17, 33, 20, 10, 20, 13, 27, 24, 14, 27, 20, 17, 24, 24, 13, 6, 14, 12, 28, 21, 28, 28, 41, 27, 24, 12, 10, 24, 10, 23, 24, 16, 17, 26, 3, 13, 14, 17, 28, 13, 16, 14, 10, 0, 20, 7, 13, 23, 17, 16, 13, 17, 22, 23, 13, 31, 24, 20, 17, 6, 31, 20, 16, 13, 13, 28, 24, 20, 13, 27, 9, 26, 3, 24, 17, 10, 9, 20, 10, 21, 10, 10, 20, 30, 17, 20, 30, 17, 30, 14, 10, 34, 17, 24, 21, 21, 16, 10, 0, 24, 7, 23, 9, 7, 6, 12, 29, 34, 17, 27, 38, 27, 31, 10, 28, 16, 14, 24, 20, 7, 24, 17, 13, 9, 13, 14, 27, 20, 13, 17, 13, 7, 13, 33, 7, 14, 7, 30, 27, 24, 10, 20, 26, 6, 14, 24, 10, 20, 34, 21, 17, 28, 31, 21, 23, 17, 21, 14, 24, 14, 17, 31, 23, 20, 17, 17, 10, 23, 7, 20, 13, 14, 20, 19, 17, 13, 7, 17, 6, 45, 17, 17, 6, 10, 14, 9, 18, 40, 14, 10, 13, 23, 14, 7, 13, 17, 27, 6, 14, 7, 24, 17, 17, 35, 20, 20, 17, 0, 23, 17, 24, 20, 13, 27, 31, 10, 20, 17, 23, 17, 10, 20, 7, 20, 23, 20, 17, 34, 33, 13, 6, 26, 10, 27, 16, 13, 7, 24, 14, 16, 13, 10, 27, 0, 7, 6, 20, 24, 17, 10, 20, 20, 24, 16, 10, 20, 24, 17, 13, 24, 16, 19, 13, 16, 10, 10, 21, 17, 34, 23, 10, 20, 9, 20, 17, 17, 21, 10, 3, 10, 26, 14, 41, 16, 29, 21, 30, 16, 37, 33, 35, 13, 20, 34, 21, 33, 27, 27, 3, 3, 16, 10, 9, 3, 21, 20, 12, 34, 20, 31, 7, 24, 26, 20, 17, 7, 30, 30, 10, 10, 16, 6, 23, 24, 12, 6, 17, 24, 16, 10, 20, 13, 10, 20, 33, 28, 13, 7, 24, 24, 26, 21, 3, 35, 20, 14, 20, 24, 14, 14, 34, 17, 34, 21, 6, 24, 15, 23, 23, 7, 17, 27, 7, 37, 16, 13, 9, 13, 20, 19, 27, 17, 26, 16, 13, 9, 20, 24, 19, 17, 12, 21, 21, 17, 27, 14, 10, 16, 9, 27, 14, 27, 20, 21, 10, 13, 36, 27, 17, 27, 13, 24, 17, 22, 30, 14, 23, 16, 21, 27, 21, 19, 7, 26, 26, 24, 13, 20, 24, 30, 20, 14, 30, 24, 14, 27, 27, 17, 16, 38, 20, 10, 10, 20, 13, 23, 16, 0, 10, 24, 13, 24, 24, 35, 13, 3, 0, 17, 14, 12, 26, 21, 20, 21, 7, 0, 13, 21, 27, 31, 21, 20, 10, 13, 13, 23, 9, 28, 38, 16, 17, 13, 16, 13, 17, 16, 17, 13, 7, 27, 9, 9, 27, 19, 10, 20, 13, 20, 10, 14, 24, 20, 13, 28, 31, 17, 7, 20, 27, 15, 10, 24, 0, 20, 24, 23, 17, 17, 24, 21, 13, 3, 3, 31, 9, 17, 10, 9, 16, 34, 7, 23, 17, 13, 14, 16, 20, 21, 34, 10, 14, 20, 20, 23, 0, 24, 24, 14, 26, 14, 35, 7, 20, 14, 7, 17, 6, 23, 16, 24, 30, 24, 23, 20, 7, 16, 13, 9, 3, 23, 20, 17, 20, 21, 21, 31, 13, 31, 10, 17, 23, 17, 10, 18, 0, 24, 20, 10, 14, 30, 6, 10, 13, 21, 24, 14, 10, 13, 16, 20, 20, 21, 17, 19, 33, 0, 28, 20, 20, 20, 19, 24, 19, 45, 34, 26, 31, 13, 27, 10, 27, 16, 17, 10, 27, 24, 27, 17, 13, 20, 20, 13, 24, 16, 13, 13, 14, 10, 10, 15, 27, 13, 27, 13, 21, 27, 23, 10, 20, 20, 20, 9, 21, 20, 7, 6, 16, 21, 6, 16, 14, 13, 12, 0, 30, 13, 31, 14, 23, 17, 27, 17, 23, 26, 13, 22, 16, 20, 34, 25, 20, 26, 17, 24, 17, 13, 23, 17, 23, 17, 10, 20, 6, 31, 12, 34, 21, 17, 3, 9, 16, 17, 13, 14, 20, 31, 16, 21, 24, 14, 21, 17, 30, 21, 24, 23, 14, 7, 17, 30, 24, 24, 20, 31, 7, 13, 14, 23, 17, 10, 24, 21, 17, 13, 24, 3, 19, 20, 20, 21, 13, 13, 23, 20, 17, 6, 6, 16, 9, 23, 14, 13, 26, 24, 28, 17, 10, 13, 17, 13, 23, 16, 13, 31, 23, 21, 24, 34, 19, 30, 27, 10, 7, 6, 13, 27, 14, 13, 23, 14, 24, 20, 20, 13, 17, 10, 24, 10, 26, 23, 20, 10, 27, 27, 31, 34, 28, 13, 16, 17, 17, 17, 16, 24, 20, 9, 21, 17, 28, 3, 3, 21, 3, 17, 28, 19, 15, 20, 14, 17, 9, 17, 20, 44, 10, 13, 35, 35, 17, 13, 21, 31, 27, 27, 17, 20, 13, 20, 9, 13, 23, 6, 24, 20, 29, 21, 10, 27, 12, 24, 17, 27, 17, 26, 10, 17, 17, 31, 23, 13, 24, 31, 14, 17, 24, 24, 23, 3, 17, 10, 34, 7, 23, 20, 7, 23, 31, 24, 40, 10, 31, 9, 26, 13, 26, 31, 3, 13, 13, 34, 10, 27, 20, 6, 14, 17, 23, 10, 16, 14, 24, 24, 23, 13, 20, 17, 16, 16, 38, 21, 10, 10, 31, 28, 16, 23, 20, 6, 14, 20, 17, 21, 20, 6, 30, 10, 28, 7, 23, 28, 13, 31, 20, 13, 0, 27, 7, 21, 27, 20, 6, 14, 27, 23, 27, 3, 19, 16, 20, 23, 14, 16, 14, 17, 14, 14, 13, 27, 20, 21, 24, 3, 13, 17, 13, 24, 7, 17, 14, 27, 17, 10, 16, 13, 36, 20, 13, 7, 17, 9, 13, 20, 19, 21, 17, 9, 7, 38, 9, 37, 19, 19, 0, 21, 23, 16, 20, 17, 22, 17, 6, 20, 21, 13, 7, 36, 21, 17, 24, 23, 10, 20, 7, 17, 7, 20, 27, 23, 21, 17, 13, 17, 23, 17, 16, 20, 14, 24, 14, 13, 26, 35, 20, 13, 17, 6, 17, 17, 24, 17, 23, 23, 13, 7, 24, 14, 21, 10, 13, 7, 17, 27, 21, 35, 14, 16, 17, 20, 23, 33, 13, 24, 10, 21, 10, 17, 17, 13, 35, 23, 31, 34, 33, 24, 14, 27, 10, 6, 17, 7, 10, 10, 27, 28, 27, 16, 23, 27, 20, 17, 13, 24, 26, 28, 14, 10, 17, 31, 14, 14, 31, 16, 24, 13, 7, 6, 37, 7, 17, 26, 21, 17, 23, 10, 27, 13, 45, 20, 3, 17, 28, 27, 27, 24, 7, 13, 27, 17, 12, 31, 20, 19, 27, 20, 17, 13, 10, 6, 23, 10, 17, 17, 27, 14, 10, 19, 20, 20, 28, 21, 20, 3, 19, 21, 17, 17, 20, 23, 7, 3, 48, 34, 13, 14, 10, 23, 16, 10, 16, 20, 12, 17, 14, 21, 10, 3, 7, 20, 7, 16, 24, 30, 19, 31, 17, 16, 13, 16, 17, 31, 16, 23, 10, 31, 7, 6, 24, 26, 28, 16, 13, 17, 10, 10, 17, 26, 14, 7, 17, 38, 28, 20, 13, 10, 27, 23, 7, 17, 20, 23, 24, 17, 16, 17, 17, 13, 24, 12, 13, 24, 20, 7, 13, 27, 13, 16, 7, 24, 13, 26, 13, 20, 17, 0, 27, 23, 0, 22, 24, 35, 23, 31, 14, 9, 6, 17, 19, 10, 17, 21, 17, 10, 17, 6, 13, 10, 6, 21, 9, 9, 27, 17, 34, 7, 21, 7, 10, 14, 17, 23, 17, 20, 7, 21, 20, 20, 6, 15, 24, 6, 27, 20, 14, 10, 10, 24, 6, 52, 7, 28, 17, 24, 19, 24, 17, 20, 3, 20, 9, 16, 17, 21, 15, 14, 10, 10, 28, 27, 28, 23, 10, 19, 13, 9, 33, 22, 20, 23, 10, 34, 13, 21, 20, 40, 34, 17, 9, 13, 38, 14, 17, 10, 13, 10, 20, 30, 31]
B history: [31, 27, 17, 9, 10, 28, 19, 10, 34, 23, 21, 17, 31, 27, 20, 17, 17, 20, 16, 14, 19, 35, 21, 9, 6, 17, 27, 20, 10, 23, 35, 38, 17, 13, 34, 31, 24, 17, 16, 13, 14, 9, 27, 23, 14, 22, 17, 23, 20, 37, 21, 24, 31, 23, 27, 33, 20, 14, 7, 12, 28, 22, 14, 20, 27, 12, 16, 34, 17, 10, 9, 16, 30, 20, 37, 23, 24, 27, 13, 6, 17, 27, 17, 31, 10, 19, 31, 31, 37, 28, 31, 16, 16, 17, 20, 21, 13, 9, 14, 21, 31, 27, 38, 23, 37, 16, 20, 17, 13, 17, 21, 27, 17, 17, 13, 34, 38, 22, 29, 34, 24, 37, 17, 13, 10, 23, 21, 24, 16, 27, 34, 24, 28, 21, 13, 24, 30, 14, 37, 13, 26, 30, 20, 13, 14, 23, 28, 20, 27, 6, 21, 27, 20, 3, 24, 41, 21, 13, 20, 23, 28, 20, 38, 17, 17, 22, 14, 13, 20, 14, 24, 27, 24, 7, 28, 24, 13, 31, 24, 24, 31, 16, 34, 23, 30, 27, 17, 14, 9, 10, 16, 35, 20, 20, 41, 13, 9, 31, 29, 33, 17, 7, 10, 27, 24, 17, 38, 14, 17, 20, 20, 13, 27, 21, 23, 20, 31, 24, 28, 13, 20, 33, 20, 23, 17, 24, 27, 16, 33, 10, 24, 14, 24, 13, 13, 32, 19, 14, 23, 31, 16, 21, 21, 21, 3, 19, 24, 19, 20, 28, 24, 20, 21, 24, 41, 3, 10, 24, 24, 10, 30, 10, 21, 26, 10, 6, 30, 28, 17, 17, 21, 30, 3, 38, 24, 10, 20, 27, 17, 17, 24, 14, 26, 20, 30, 21, 23, 26, 20, 12, 35, 10, 14, 34, 20, 38, 19, 31, 23, 24, 34, 28, 27, 24, 24, 20, 17, 34, 20, 3, 17, 27, 20, 17, 24, 20, 23, 10, 7, 27, 7, 14, 14, 20, 13, 24, 17, 28, 24, 25, 17, 19, 17, 17, 10, 35, 27, 14, 27, 17, 30, 24, 9, 24, 34, 17, 13, 16, 17, 6, 13, 24, 28, 35, 27, 20, 22, 20, 24, 30, 21, 21, 28, 10, 17, 7, 24, 26, 19, 10, 7, 10, 31, 10, 21, 26, 13, 24, 28, 0, 13, 17, 37, 17, 38, 10, 19, 17, 20, 10, 34, 13, 13, 14, 0, 26, 30, 31, 23, 3, 20, 20, 30, 20, 20, 26, 24, 26, 48, 31, 16, 14, 16, 7, 27, 16, 33, 13, 3, 14, 10, 17, 14, 21, 14, 13, 13, 28, 16, 13, 24, 7, 31, 31, 26, 19, 17, 41, 7, 16, 16, 28, 38, 31, 3, 38, 33, 28, 13, 30, 28, 12, 24, 20, 24, 35, 10, 28, 31, 22, 24, 28, 24, 38, 21, 34, 17, 30, 28, 26, 31, 10, 24, 17, 34, 17, 13, 20, 34, 23, 20, 17, 23, 24, 28, 31, 31, 27, 20, 17, 34, 21, 20, 23, 14, 20, 24, 34, 20, 20, 14, 21, 37, 13, 20, 24, 17, 3, 20, 21, 17, 23, 28, 20, 24, 34, 19, 17, 20, 24, 14, 6, 34, 31, 23, 37, 17, 3, 20, 24, 31, 26, 10, 17, 21, 23, 26, 20, 16, 24, 23, 20, 24, 24, 20, 24, 31, 26, 24, 20, 17, 34, 23, 14, 23, 13, 19, 13, 7, 23, 17, 23, 10, 24, 20, 34, 28, 21, 30, 13, 23, 14, 16, 16, 24, 27, 30, 16, 35, 28, 14, 13, 12, 10, 20, 10, 20, 12, 38, 38, 34, 31, 26, 20, 16, 31, 38, 14, 16, 14, 14, 16, 20, 20, 21, 16, 6, 23, 17, 30, 16, 10, 17, 23, 27, 36, 28, 14, 19, 20, 17, 28, 24, 20, 21, 24, 27, 13, 30, 16, 24, 28, 34, 6, 21, 21, 13, 6, 23, 17, 21, 24, 38, 17, 35, 17, 10, 27, 20, 24, 33, 20, 14, 20, 24, 24, 23, 9, 34, 7, 20, 14, 16, 34, 10, 17, 24, 26, 21, 13, 35, 9, 27, 17, 23, 20, 24, 27, 24, 37, 24, 17, 13, 20, 13, 28, 16, 20, 34, 23, 17, 10, 13, 6, 38, 13, 10, 31, 27, 17, 20, 17, 14, 38, 21, 16, 17, 31, 14, 29, 10, 20, 10, 30, 24, 13, 27, 24, 23, 20, 21, 16, 31, 17, 20, 17, 10, 13, 24, 30, 20, 20, 23, 20, 13, 17, 20, 23, 7, 17, 17, 27, 17, 19, 31, 7, 21, 20, 10, 23, 16, 23, 31, 10, 23, 14, 27, 31, 13, 31, 17, 23, 17, 7, 16, 20, 33, 13, 16, 17, 20, 24, 13, 27, 27, 27, 21, 14, 31, 37, 7, 37, 31, 31, 27, 13, 13, 20, 17, 10, 23, 30, 26, 24, 31, 23, 16, 23, 24, 41, 13, 27, 17, 27, 35, 23, 31, 38, 19, 36, 13, 30, 17, 30, 23, 20, 17, 10, 44, 20, 21, 10, 44, 9, 17, 21, 14, 19, 17, 21, 20, 20, 31, 15, 35, 31, 34, 27, 33, 24, 20, 24, 30, 17, 10, 13, 17, 13, 26, 17, 24, 26, 27, 30, 9, 20, 27, 16, 20, 35, 20, 24, 20, 27, 20, 10, 17, 7, 24, 23, 10, 31, 28, 33, 13, 28, 24, 27, 26, 24, 20, 30, 27, 24, 13, 24, 24, 31, 17, 24, 27, 16, 28, 30, 16, 17, 19, 24, 44, 17, 10, 24, 12, 31, 20, 28, 24, 27, 14, 20, 13, 6, 10, 21, 27, 13, 20, 20, 7, 27, 21, 3, 26, 38, 17, 24, 23, 17, 20, 34, 20, 31, 20, 10, 19, 30, 24, 21, 14, 7, 34, 20, 16, 30, 24, 41, 17, 17, 27, 26, 10, 20, 14, 27, 21, 36, 6, 6, 23, 16, 31, 27, 20, 21, 20, 31, 31, 23, 31, 13, 23, 17, 31, 21, 16, 10, 30, 31, 19, 20, 20, 37, 20, 17, 17, 23, 27, 10, 10, 33, 20, 17, 10, 17, 24, 24, 35, 6, 44, 24, 13, 19, 12, 24, 27, 20, 24, 19, 24, 17, 27, 23, 21, 24, 10, 17, 28, 17, 30, 20, 21, 34, 17, 16, 21, 28, 37, 34, 24, 24, 41, 10, 19, 17, 7, 13, 40, 17, 9, 16, 10, 28, 14, 13, 17, 6, 17, 28, 20, 10, 13, 23, 24, 20, 20, 27, 17, 21, 34, 21, 16, 10, 12, 20, 14, 6, 30, 10, 20, 24, 13, 10, 26, 27, 13, 16, 10, 28, 21, 17, 14, 17, 28, 13, 20, 13, 31, 13, 27, 23, 24, 41, 24, 17, 20, 17, 34, 21, 13, 10, 10, 14, 20, 13, 16, 26, 21, 7, 13, 41, 10, 27, 21, 10, 30, 19, 34, 23, 19, 34, 17, 30, 7, 34, 30, 20, 27, 37, 24, 24, 24, 13, 23, 20, 24, 23, 17, 20, 10, 17, 24, 14, 20, 27, 23, 17, 14, 19, 3, 17, 27, 27, 30, 12, 28, 21, 9, 16, 27, 13, 23, 24, 21, 51, 13, 37, 17, 3, 10, 29, 20, 31, 28, 24, 21, 9, 10, 27, 16, 17, 40, 42, 21, 26, 20, 20, 31, 3, 21, 19, 7, 13, 20, 13, 28, 24, 13, 28, 13, 26, 7, 30, 30, 23, 28, 20, 31, 21, 27, 13, 16, 31, 16, 10, 23, 28, 21, 29, 20, 14, 21, 17, 17, 23, 28, 10, 21, 20, 31, 14, 9, 17, 55, 7, 27, 21, 20, 23, 30, 13, 14, 20, 24, 21, 17, 20, 20, 23, 17, 24, 17, 24, 16, 20, 31, 27, 35, 21, 17, 13, 24, 38, 24, 24, 24, 28, 30, 19, 13, 15, 24, 27, 20, 12, 20, 17, 34, 10, 35, 42, 27, 14, 20, 26, 36, 23, 10, 21, 24, 24, 28, 34, 27, 30, 20, 14, 23, 13, 21, 13, 30, 28, 16, 24, 34, 12, 20, 27, 20, 23, 24, 21, 13, 27, 17, 17, 12, 13, 27, 30, 20, 12, 33, 28, 28, 24, 23, 31, 17, 10, 19, 20, 16, 30, 24, 10, 7, 21, 17, 27, 17, 41, 17, 31, 17, 24, 17, 31, 20, 17, 27, 27, 20, 14, 29, 27, 10, 21, 16, 16, 27, 27, 51, 27, 31, 13, 27, 13, 38, 24, 14, 10, 17, 23, 14, 33, 14, 32, 24, 13, 13, 13, 17, 24, 23, 20, 22, 20, 24, 34, 6, 10, 10, 24, 13, 23, 17, 17, 20, 0, 44, 23, 24, 20, 20, 27, 17, 19, 28, 21, 19, 24, 9, 21, 16, 20, 30, 15, 20, 0, 30, 27, 16, 21, 21, 17, 17, 24, 24, 31, 28, 13, 17, 13, 17, 17, 17, 16, 17, 33, 20, 9, 24, 20, 34, 24, 20, 21, 20, 27, 14, 28, 24, 15, 34, 23, 34, 27, 3, 24, 26, 28, 16, 7, 34, 3, 23, 29, 30, 21, 16, 20, 34, 37, 20, 3, 23, 21, 9, 30, 40, 34, 31, 10, 35, 35, 17, 20, 24, 6, 13, 24, 16, 19, 24, 22, 17, 27, 10, 16, 16, 37, 6, 17, 34, 31, 17, 27, 38, 21, 17, 23, 13, 34, 20, 13, 14, 19, 42, 27, 10, 21, 17, 17, 27, 6, 22, 20, 17, 28, 10, 21, 16, 14, 24, 10, 28, 16, 27, 10, 27, 34, 20, 17, 30, 31, 7, 17, 41, 17, 17, 24, 10, 17, 27, 28, 13, 21, 27, 17, 33, 31, 24, 14, 21, 27, 21, 16, 24, 31, 17, 23, 10, 20, 20, 24, 34, 29, 23, 28, 10, 31, 14, 7, 10, 31, 40, 24, 23, 27, 24, 21, 17, 30, 37, 30, 17, 20, 20, 13, 17, 20, 17, 13, 27, 28, 27, 15, 35, 41, 10, 24, 27, 37, 34, 7, 19, 33, 27, 21, 30, 7, 17, 20, 36, 21, 17, 31, 17, 31, 23, 24, 17, 17, 24, 23, 10, 27, 21, 10, 20, 35, 17, 13, 16, 26, 20, 26, 23, 13, 17, 23, 24, 16, 26, 27, 7, 14, 14, 24, 27, 28, 33, 21, 27, 7, 21, 23, 17, 10, 24, 21, 24, 21, 10, 21, 24, 17, 34, 23, 7, 37, 13, 10, 20, 20, 28, 30, 13, 26, 26, 21, 10, 17, 17, 28, 24, 20, 20, 37, 13, 12, 23, 28, 6, 12, 0, 27, 24, 26, 13, 24, 6, 17, 21, 31, 24, 20, 24, 27, 16, 27, 13, 16, 20, 33, 23, 29, 13, 30, 27, 6, 44, 21, 20, 0, 24, 17, 17, 17, 17, 33, 27, 32, 17, 23, 14, 20, 13, 34, 27, 24, 16, 13, 21, 14, 34, 24, 37, 31, 13, 20, 7, 16, 20, 30, 37, 23, 24, 24, 27, 31, 31, 24, 38, 31, 24, 6, 24, 20, 17, 27, 31, 27, 23, 34, 37, 28, 19, 20, 21, 24, 13, 24, 16, 23, 27, 30, 23, 21, 24, 17, 23, 24, 7, 10, 31, 20, 17, 17, 6, 16, 10, 30, 6, 20, 20, 21, 27, 17, 19, 16, 17, 27, 17, 34, 19, 27, 6, 13, 30, 23, 35, 31, 10, 40, 16, 24, 27, 27, 20, 20, 17, 34, 27, 17, 17, 7, 16, 7, 20, 20, 24, 23, 24, 34, 30, 34, 27, 17, 20, 13, 17, 24, 28, 3, 14, 27, 25, 10, 45, 34, 16, 7, 20, 27, 38, 17, 24, 20, 10, 13, 33, 24, 24, 10, 34, 7, 23, 13, 24, 16, 19, 38, 17, 27, 13, 37, 14, 23, 24, 10, 21, 26, 13, 13, 20, 13, 17, 31, 27, 14, 23, 17, 37, 27, 17, 44, 24, 28, 9, 28, 26, 26, 27, 19, 27, 26, 38, 16, 44, 17, 10, 24, 20, 19, 26, 3, 28, 20, 7, 28, 13, 9, 27, 29, 13, 24, 13, 31, 13, 31, 20, 17, 24, 10, 24, 20, 24, 16, 24, 16, 19, 14, 24, 19, 24, 21, 23, 13, 13, 13, 34, 22, 24, 31, 21, 24, 24, 10, 27, 17, 30, 20, 28, 23, 21, 37, 26, 6, 21, 17, 23, 17, 24, 20, 17, 13, 17, 21, 7, 31, 21, 24, 13, 20, 14, 28, 31, 17, 14, 17, 24, 23, 23, 24, 27, 27, 20, 14, 23, 16, 30, 21]
A minus B history: [-41, -38, -38, -38, -37, -36, -35, -35, -34, -34, -34, -34, -34, -33, -31, -31, -31, -31, -31, -31, -31, -30, -30, -30, -30, -30, -30, -30, -29, -28, -28, -28, -28, -28, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -27, -26, -26, -26, -26, -26, -25, -25, -25, -25, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -24, -23, -23, -23, -23, -23, -23, -22, -22, -22, -22, -22, -22, -22, -22, -22, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -21, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -19, -19, -19, -19, -19, -19, -19, -19, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 23, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 25, 25, 25, 25, 26, 27, 27, 27, 28, 28, 28, 28, 28, 31, 31, 10]
Team A: KC Team B: SF
Median Home: KC minus Away: SF score: -3.0
n = 2024.  | 0%: = -41 | 0.05%: = -21 | 0.1%: = -17 | 0.15%: = -14 | 0.2%: = -13 | 0.25%: = -10 | 0.3%: = -8 | 0.35%: = -7 | 0.4%: = -6 | 0.45%: = -4 | 0.5%: = -3 | 0.55%: = -2 | 0.6%: = 0 | 0.65%: = 1 | 0.7%: = 3 | 0.75%: = 4 | 0.8%: = 7 | 0.85%: = 9 | 0.9%: = 11 | 0.95%: = 15
propo ties: 0.04891304347826087
normal 	Sim W/L %: 0.39 [ 0.36 , 0.41 ] n = 1925
beta 	Sim W/L %: 0.39 [ 0.36 , 0.41 ] n = 1925
100%|██████████| 2024/2024 [8:06:23<00:00, 12.08s/it]

Team A: SF Team B: BAL
Median Home: SF minus Away: BAL score: 3.0
n = 1944.  | 0%: = -30 | 0.05%: = -15 | 0.1%: = -10 | 0.15%: = -7 | 0.2%: = -6 | 0.25%: = -4 | 0.3%: = -3 | 0.35%: = -1 | 0.4%: = 0 | 0.45%: = 1 | 0.5%: = 3 | 0.55%: = 4 | 0.6%: = 5 | 0.65%: = 7 | 0.7%: = 7 | 0.75%: = 9 | 0.8%: = 11 | 0.85%: = 14 | 0.9%: = 17 | 0.95%: = 20
.
Median Over under: 37.0
n = 1944.  | 0%: = 3 | 0.05%: = 20 | 0.1%: = 23 | 0.15%: = 26 | 0.2%: = 29 | 0.25%: = 30 | 0.3%: = 32 | 0.35%: = 33 | 0.4%: = 35 | 0.45%: = 37 | 0.5%: = 37 | 0.55%: = 40 | 0.6%: = 41 | 0.65%: = 42 | 0.7%: = 44 | 0.75%: = 46 | 0.8%: = 48 | 0.85%: = 51 | 0.9%: = 54 | 0.95%: = 58
propo ties: 0.055041152263374485
normal 	Sim W/L %: 0.61 [ 0.59 , 0.63 ] n = 1837
beta 	Sim W/L %: 0.61 [ 0.59 , 0.63 ] n = 1837

Team A: KC Team B: BAL
Median Home: KC minus Away: BAL score: 1
n = 1887.  | 0%: = -34 | 0.05%: = -18 | 0.1%: = -14 | 0.15%: = -11 | 0.2%: = -8 | 0.25%: = -7 | 0.3%: = -4 | 0.35%: = -3 | 0.4%: = -1 | 0.45%: = 0 | 0.5%: = 1 | 0.55%: = 3 | 0.6%: = 4 | 0.65%: = 6 | 0.7%: = 7 | 0.75%: = 8 | 0.8%: = 10 | 0.85%: = 12 | 0.9%: = 14 | 0.95%: = 18
.
Median Over under: 45
n = 1887.  | 0%: = 10 | 0.05%: = 26 | 0.1%: = 30 | 0.15%: = 33 | 0.2%: = 35 | 0.25%: = 37 | 0.3%: = 40 | 0.35%: = 41 | 0.4%: = 43 | 0.45%: = 44 | 0.5%: = 45 | 0.55%: = 47 | 0.6%: = 48 | 0.65%: = 51 | 0.7%: = 52 | 0.75%: = 55 | 0.8%: = 57 | 0.85%: = 59 | 0.9%: = 63 | 0.95%: = 68
propo ties: 0.06147323794382618
normal 	Sim W/L %: 0.56 [ 0.54 , 0.58 ] n = 1771
beta 	Sim W/L %: 0.56 [ 0.54 , 0.58 ] n = 1771

Team A: KC Team B: SF
Median Home: KC minus Away: SF score: -3
n = 1869.  | 0%: = -41 | 0.05%: = -21 | 0.1%: = -17 | 0.15%: = -14 | 0.2%: = -12 | 0.25%: = -10 | 0.3%: = -9 | 0.35%: = -7 | 0.4%: = -6 | 0.45%: = -4 | 0.5%: = -3 | 0.55%: = -2 | 0.6%: = 0 | 0.65%: = 1 | 0.7%: = 3 | 0.75%: = 4 | 0.8%: = 6 | 0.85%: = 8 | 0.9%: = 11 | 0.95%: = 15
.
Median Over under: 39
n = 1869.  | 0%: = 9 | 0.05%: = 20 | 0.1%: = 24 | 0.15%: = 27 | 0.2%: = 29 | 0.25%: = 30 | 0.3%: = 33 | 0.35%: = 34 | 0.4%: = 36 | 0.45%: = 37 | 0.5%: = 39 | 0.55%: = 40 | 0.6%: = 41 | 0.65%: = 44 | 0.7%: = 45 | 0.75%: = 47 | 0.8%: = 49 | 0.85%: = 51 | 0.9%: = 55 | 0.95%: = 60
propo ties: 0.05457463884430177
normal 	Sim W/L %: 0.38 [ 0.36 , 0.4 ] n = 1767
beta 	Sim W/L %: 0.38 [ 0.36 , 0.4 ] n = 1767

Team A: NE Team B: SF
Median Home: NE minus Away: SF score: -3
n = 1879.  | 0%: = -38 | 0.05%: = -18 | 0.1%: = -14 | 0.15%: = -12 | 0.2%: = -10 | 0.25%: = -8 | 0.3%: = -7 | 0.35%: = -6 | 0.4%: = -4 | 0.45%: = -3 | 0.5%: = -3 | 0.55%: = -1 | 0.6%: = 1 | 0.65%: = 3 | 0.7%: = 3 | 0.75%: = 5 | 0.8%: = 7 | 0.85%: = 9 | 0.9%: = 11 | 0.95%: = 15
.
Median Over under: 30
n = 1879.  | 0%: = 3 | 0.05%: = 13 | 0.1%: = 16 | 0.15%: = 19 | 0.2%: = 20 | 0.25%: = 23 | 0.3%: = 23 | 0.35%: = 26 | 0.4%: = 27 | 0.45%: = 29 | 0.5%: = 30 | 0.55%: = 31 | 0.6%: = 33 | 0.65%: = 34 | 0.7%: = 35 | 0.75%: = 37 | 0.8%: = 39 | 0.85%: = 41 | 0.9%: = 44 | 0.95%: = 48
propo ties: 0.045769026077700906
normal 	Sim W/L %: 0.42 [ 0.4 , 0.44 ] n = 1793
beta 	Sim W/L %: 0.42 [ 0.4 , 0.44 ] n = 1793

Team A: NE Team B: KC
Median Home: NE minus Away: KC score: -3.0
n = 1820.  | 0%: = -35 | 0.05%: = -19 | 0.1%: = -16 | 0.15%: = -13 | 0.2%: = -11 | 0.25%: = -10 | 0.3%: = -7 | 0.35%: = -6 | 0.4%: = -4 | 0.45%: = -3 | 0.5%: = -3 | 0.55%: = -1 | 0.6%: = 1 | 0.65%: = 3 | 0.7%: = 3 | 0.75%: = 5 | 0.8%: = 7 | 0.85%: = 9 | 0.9%: = 11 | 0.95%: = 15
.
Median Over under: 36.0
n = 1820.  | 0%: = 3 | 0.05%: = 19 | 0.1%: = 22 | 0.15%: = 25 | 0.2%: = 27 | 0.25%: = 29 | 0.3%: = 30 | 0.35%: = 31 | 0.4%: = 33 | 0.45%: = 34 | 0.5%: = 36 | 0.55%: = 37 | 0.6%: = 39 | 0.65%: = 40 | 0.7%: = 43 | 0.75%: = 44 | 0.8%: = 47 | 0.85%: = 48 | 0.9%: = 51 | 0.95%: = 56
propo ties: 0.05
normal 	Sim W/L %: 0.42 [ 0.4 , 0.44 ] n = 1729
beta 	Sim W/L %: 0.42 [ 0.4 , 0.44 ] n = 1729
'''
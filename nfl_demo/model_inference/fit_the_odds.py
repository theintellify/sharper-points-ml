def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min

def scale_list(l, to_min, to_max):
    return [scale_number(i, to_min, to_max, min(l), max(l)) for i in l]


# print(scale_list([-300,750],-10 , 110))

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

print(adjust_odds_between_100_120(-230,230))

from pybettor import implied_odds
print(implied_odds(0.99,"all"))

import math

def calculate_scaled_odds(team_a_wins, total_simulations):
    # Avoid division by zero and ensure some uncertainty
    epsilon = 0.0001
    prob_a = (team_a_wins + epsilon) / (total_simulations + 2 * epsilon)
    prob_b = 1 - prob_a
    
    # Calculate log odds to amplify small differences
    log_odds_a = math.log(prob_a / prob_b)
    
    # Scale log odds to 0-1 range
    max_log_odds = math.log((1-epsilon) / epsilon)
    scaled_odds = (log_odds_a + max_log_odds) / (2 * max_log_odds)
    
    # Map to 100-120 range
    odds_a = 100 + scaled_odds * 20
    odds_b = 220 - odds_a  # Ensures odds_a + odds_b = 220
    
    return round(odds_a, 2), round(odds_b, 2)

# print(calculate_scaled_odds(5,5))

import random

class Team:
    def __init__(self, name, recent_scores, home_advantage=2):
        self.name = name
        self.recent_scores = recent_scores
        self.home_advantage = home_advantage
        
    def average_score(self):
        return sum(self.recent_scores) / len(self.recent_scores)
    
    def form(self):
        # Simple form calculation: trend of last 3 games
        if len(self.recent_scores) >= 3:
            return sum(self.recent_scores[-3:]) / 3 - self.average_score()
        return 0

def calculate_betting_line(home_team, away_team):
    # Basic point difference
    point_diff = home_team.average_score() - away_team.average_score()
    
    # Adjust for home advantage
    point_diff += home_team.home_advantage
    
    # Adjust for recent form
    point_diff += home_team.form() - away_team.form()
    
    # Add some randomness to simulate other factors (injuries, weather, etc.)
    point_diff += random.uniform(-3, 3)
    
    # Round to nearest 0.5
    return round(point_diff * 2) / 2

def generate_moneyline(spread):
    if spread > 0:
        favorite_odds = -110 - abs(spread) * 10
        underdog_odds = 100 + abs(spread) * 10
    else:
        favorite_odds = -110 - abs(spread) * 10
        underdog_odds = 100 + abs(spread) * 10
    
    return round(favorite_odds), round(underdog_odds)

# Example usage
steelers = Team("Pittsburgh Steelers", [14, 13, 3, 19])
colts = Team("Indianapolis Colts", [10, 17, 9, 10])

spread = calculate_betting_line(steelers, colts)
favorite_ml, underdog_ml = generate_moneyline(spread)

print(f"Spread: {steelers.name} {-spread} | {colts.name} +{spread}")
print(f"Moneyline: {steelers.name} {favorite_ml} | {colts.name} +{underdog_ml}")
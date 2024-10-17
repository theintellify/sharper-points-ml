import random

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

# Example usage
steelers = Team("Pittsburgh Steelers", [24, 17, 28, 20, 31])
colts = Team("Indianapolis Colts", [21, 14, 24, 27, 17])

spread = calculate_betting_line(steelers, colts)
favorite_ml, underdog_ml = generate_moneyline(spread)

total = calculate_totals_line(steelers, colts)
over_odds, under_odds = generate_totals_odds(total)

print(f"Spread: {steelers.name} {-spread} | {colts.name} +{spread}")
print(f"Moneyline: {steelers.name} {favorite_ml} | {colts.name} +{underdog_ml}")
print(f"Totals: O/U {total}")
print(f"Totals Odds: Over {over_odds} | Under {under_odds}")
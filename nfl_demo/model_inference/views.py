from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
# from model_inference.load_play_by_play import get_data
# from apps import 
# from .tasks import my_task
from model_inference.mass_simulate_compare_odds import sim_super_bowl
from model_inference.models import results_table
import json 
from model_inference.apps import ModelInferenceConfig
import uuid 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):

    co_eff = {}
    co_eff['run_vs_pass'] = {'pos_team':0.1,'pos_winning*time_left*goal_yd':0.2,'pos_minus_def_score*time_left':0.2,'ydstogo':0.5}
    co_eff['punt'] = {'pos_winning*ydstogo*goal_yd*time_left*pos_minus_def_score': 0.5, 'pos_team':0.5}
    co_eff['punt_yds'] = {'goal_yd':1.0}
    co_eff['FG_attempted']={'time_left*pos_down_three_or_less':0.33 , 'goal_yd*ydstogo': 0.33, 'time_left*pos_minus_def_score':0.33}
    co_eff['FG_made'] = {'goal_yd':1}
    co_eff['fumble']= {'def_team':0.25 , 'pos_team':0.25 , 'time_left':0.25, 'run_vs_pass':0.25}
    co_eff['fumble_lost'] = {'run_vs_pass':1}
    co_eff['fumble_yds'] ={'def_team':1}
    co_eff['interception'] = {'time_left':0.333, 'pos_team':0.3333 , 'def_team':0.3333}
    co_eff['int_yds'] = {'def_team':1}
    is_custom_sim = False
    n_sims = 3
    print(request.body)
    input_dict = json.loads(request.body)
    team_A = input_dict["home_team"]
    team_B = input_dict["away_team"]
    run_id = input_dict["id"]
    week  = input_dict["week"]

    df_dict = ModelInferenceConfig.var
    # print(df_dict[1])
    # my_task(df_dict[week],co_eff,)
    uuid_ = uuid.uuid4()

    # my_task.delay(df_dict[week],co_eff,is_custom_sim,team_A,team_B,n_sims,week,run_id,f"{uuid_}")

    result_dict_ = sim_super_bowl(df_dict,co_eff,is_custom_sim,team_A=team_A, team_B=team_B, percentile_break=0.2, n_sims=n_sims, year=2024, week=week, excl_vs_before=True)
    
    obj = results_table(team_a_moneyline = result_dict_["team_a_moneyline"]  , team_b_moneyline = result_dict_["team_b_moneyline"]  , team_a_spread =  result_dict_["team_a_spread"], team_b_spread = result_dict_["team_b_spread"] , team_a_spread_line = result_dict_["team_a_spread_line"]  , team_b_spread_line = result_dict_["team_b_spread_line"] , team_a_totals = result_dict_["team_a_totals"] , team_b_totals = result_dict_["team_b_totals"] , team_a_totals_line = result_dict_["team_a_totals_line"]  , team_b_totals_line = result_dict_["team_b_totals_line"]  , home_team = team_A , away_team = team_B , run_id = run_uuid , uuid = uuid_)
    obj.save()

    return HttpResponse(json.dumps({"home_team":team_A,"away_team":team_B,"uuid":f"{uuid_}","id":f"{run_id}"}))

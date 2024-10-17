from celery import shared_task


@shared_task(serializer="pickle")
def my_task(df,co_eff,is_custom_sim,team_A,team_B,n_sims,week,run_uuid,uuid_):
    from model_inference.mass_simulate_compare_odds import sim_super_bowl
    from model_inference.models import results_table
    # Task logic here
    result_dict_ = sim_super_bowl(df,co_eff,is_custom_sim,team_A=team_A, team_B=team_B, percentile_break=0.2, n_sims=n_sims, year=2024, week=week, excl_vs_before=True)
    
    obj = results_table(team_a_moneyline = result_dict_["team_a_moneyline"]  , team_b_moneyline = result_dict_["team_b_moneyline"]  , team_a_spread =  result_dict_["team_a_spread"], team_b_spread = result_dict_["team_b_spread"] , team_a_spread_line = result_dict_["team_a_spread_line"]  , team_b_spread_line = result_dict_["team_b_spread_line"] , team_a_totals = result_dict_["team_a_totals"] , team_b_totals = result_dict_["team_b_totals"] , team_a_totals_line = result_dict_["team_a_totals_line"]  , team_b_totals_line = result_dict_["team_b_totals_line"]  , home_team = team_A , away_team = team_B , run_id = run_uuid , uuid = uuid_)
    obj.save()
    return result_dict_

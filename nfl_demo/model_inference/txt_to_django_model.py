var = """play_id	Numeric play id that when used with game_id and drive provides the unique identifier for a single play.	numeric
game_id	Ten digit identifier for NFL game.	character
old_game_id	Legacy NFL game ID.	character
home_team	String abbreviation for the home team.	character
away_team	String abbreviation for the away team.	character
season_type	'REG' or 'POST' indicating if the game belongs to regular or post season.	character
week	Season week.	numeric
posteam	String abbreviation for the team with possession.	character
posteam_type	String indicating whether the posteam team is home or away.	character
defteam	String abbreviation for the team on defense.	character
side_of_field	String abbreviation for which team's side of the field the team with possession is currently on.	character
yardline_100	Numeric distance in the number of yards from the opponent's endzone for the posteam.	numeric
game_date	Date of the game.	character
quarter_seconds_remaining	Numeric seconds remaining in the quarter.	numeric
half_seconds_remaining	Numeric seconds remaining in the half.	numeric
game_seconds_remaining	Numeric seconds remaining in the game.	numeric
game_half	String indicating which half the play is in, either Half1, Half2, or Overtime.	character
quarter_end	Binary indicator for whether or not the row of the data is marking the end of a quarter.	numeric
drive	Numeric drive number in the game.	numeric
sp	Binary indicator for whether or not a score occurred on the play.	numeric
qtr	Quarter of the game (5 is overtime).	numeric
down	The down for the given play.	numeric
goal_to_go	Binary indicator for whether or not the posteam is in a goal down situation.	numeric
time	Time at start of play provided in string format as minutes:seconds remaining in the quarter.	character
yrdln	String indicating the current field position for a given play.	character
ydstogo	Numeric yards in distance from either the first down marker or the endzone in goal down situations.	numeric
ydsnet	Numeric value for total yards gained on the given drive.	numeric
desc	Detailed string description for the given play.	character
play_type	String indicating the type of play: pass (includes sacks), run (includes scrambles), punt, field_goal, kickoff, extra_point, qb_kneel, qb_spike, no_play (timeouts and penalties), and missing for rows indicating end of play.	character
yards_gained	Numeric yards gained (or lost) by the possessing team, excluding yards gained via fumble recoveries and laterals.	numeric
shotgun	Binary indicator for whether or not the play was in shotgun formation.	numeric
no_huddle	Binary indicator for whether or not the play was in no_huddle formation.	numeric
qb_dropback	Binary indicator for whether or not the QB dropped back on the play (pass attempt, sack, or scrambled).	numeric
qb_kneel	Binary indicator for whether or not the QB took a knee.	numeric
qb_spike	Binary indicator for whether or not the QB spiked the ball.	numeric
qb_scramble	Binary indicator for whether or not the QB scrambled.	numeric
pass_length	String indicator for pass length: short or deep.	character
pass_location	String indicator for pass location: left, middle, or right.	character
air_yards	Numeric value for distance in yards perpendicular to the line of scrimmage at where the targeted receiver either caught or didn't catch the ball.	numeric
yards_after_catch	Numeric value for distance in yards perpendicular to the yard line where the receiver made the reception to where the play ended.	numeric
run_location	String indicator for location of run: left, middle, or right.	character
run_gap	String indicator for line gap of run: end, guard, or tackle	character
field_goal_result	String indicator for result of field goal attempt: made, missed, or blocked.	character
kick_distance	Numeric distance in yards for kickoffs, field goals, and punts.	numeric
extra_point_result	String indicator for the result of the extra point attempt: good, failed, blocked, safety (touchback in defensive endzone is 1 point apparently), or aborted.	character
two_point_conv_result	String indicator for result of two point conversion attempt: success, failure, safety (touchback in defensive endzone is 1 point apparently), or return.	character
home_timeouts_remaining	Numeric timeouts remaining in the half for the home team.	numeric
away_timeouts_remaining	Numeric timeouts remaining in the half for the away team.	numeric
timeout	Binary indicator for whether or not a timeout was called by either team.	numeric
timeout_team	String abbreviation for which team called the timeout.	character
td_team	String abbreviation for which team scored the touchdown.	character
td_player_name	String name of the player who scored a touchdown.	character
td_player_id	Unique identifier of the player who scored a touchdown.	character
posteam_timeouts_remaining	Number of timeouts remaining for the possession team.	numeric
defteam_timeouts_remaining	Number of timeouts remaining for the team on defense.	numeric
total_home_score	Score for the home team at the start of the play.	numeric
total_away_score	Score for the away team at the start of the play.	numeric
posteam_score	Score the posteam at the start of the play.	numeric
defteam_score	Score the defteam at the start of the play.	numeric
score_differential	Score differential between the posteam and defteam at the start of the play.	numeric
posteam_score_post	Score for the posteam at the end of the play.	numeric
defteam_score_post	Score for the defteam at the end of the play.	numeric
score_differential_post	Score differential between the posteam and defteam at the end of the play.	numeric
no_score_prob	Predicted probability of no score occurring for the rest of the half based on the expected points model.	numeric
opp_fg_prob	Predicted probability of the defteam scoring a FG next.	numeric
opp_safety_prob	Predicted probability of the defteam scoring a safety next.	numeric
opp_td_prob	Predicted probability of the defteam scoring a TD next.	numeric
fg_prob	Predicted probability of the posteam scoring a FG next.	numeric
safety_prob	Predicted probability of the posteam scoring a safety next.	numeric
td_prob	Predicted probability of the posteam scoring a TD next.	numeric
extra_point_prob	Predicted probability of the posteam scoring an extra point.	numeric
two_point_conversion_prob	Predicted probability of the posteam scoring the two point conversion.	numeric
ep	Using the scoring event probabilities, the estimated expected points with respect to the possession team for the given play.	numeric
epa	Expected points added (EPA) by the posteam for the given play.	numeric
total_home_epa	Cumulative total EPA for the home team in the game so far.	numeric
total_away_epa	Cumulative total EPA for the away team in the game so far.	numeric
total_home_rush_epa	Cumulative total rushing EPA for the home team in the game so far.	numeric
total_away_rush_epa	Cumulative total rushing EPA for the away team in the game so far.	numeric
total_home_pass_epa	Cumulative total passing EPA for the home team in the game so far.	numeric
total_away_pass_epa	Cumulative total passing EPA for the away team in the game so far.	numeric
air_epa	EPA from the air yards alone. For completions this represents the actual value provided through the air. For incompletions this represents the hypothetical value that could've been added through the air if the pass was completed.	numeric
yac_epa	EPA from the yards after catch alone. For completions this represents the actual value provided after the catch. For incompletions this represents the difference between the hypothetical air_epa and the play's raw observed EPA (how much the incomplete pass cost the posteam).	numeric
comp_air_epa	EPA from the air yards alone only for completions.	numeric
comp_yac_epa	EPA from the yards after catch alone only for completions.	numeric
total_home_comp_air_epa	Cumulative total completions air EPA for the home team in the game so far.	numeric
total_away_comp_air_epa	Cumulative total completions air EPA for the away team in the game so far.	numeric
total_home_comp_yac_epa	Cumulative total completions yac EPA for the home team in the game so far.	numeric
total_away_comp_yac_epa	Cumulative total completions yac EPA for the away team in the game so far.	numeric
total_home_raw_air_epa	Cumulative total raw air EPA for the home team in the game so far.	numeric
total_away_raw_air_epa	Cumulative total raw air EPA for the away team in the game so far.	numeric
total_home_raw_yac_epa	Cumulative total raw yac EPA for the home team in the game so far.	numeric
total_away_raw_yac_epa	Cumulative total raw yac EPA for the away team in the game so far.	numeric
wp	Estimated win probabiity for the posteam given the current situation at the start of the given play.	numeric
def_wp	Estimated win probability for the defteam.	numeric
home_wp	Estimated win probability for the home team.	numeric
away_wp	Estimated win probability for the away team.	numeric
wpa	Win probability added (WPA) for the posteam.	numeric
vegas_wpa	Win probability added (WPA) for the posteam: spread_adjusted model.	numeric
vegas_home_wpa	Win probability added (WPA) for the home team: spread_adjusted model.	numeric
home_wp_post	Estimated win probability for the home team at the end of the play.	numeric
away_wp_post	Estimated win probability for the away team at the end of the play.	numeric
vegas_wp	Estimated win probabiity for the posteam given the current situation at the start of the given play, incorporating pre-game Vegas line.	numeric
vegas_home_wp	Estimated win probability for the home team incorporating pre-game Vegas line.	numeric
total_home_rush_wpa	Cumulative total rushing WPA for the home team in the game so far.	numeric
total_away_rush_wpa	Cumulative total rushing WPA for the away team in the game so far.	numeric
total_home_pass_wpa	Cumulative total passing WPA for the home team in the game so far.	numeric
total_away_pass_wpa	Cumulative total passing WPA for the away team in the game so far.	numeric
air_wpa	WPA through the air (same logic as air_epa).	numeric
yac_wpa	WPA from yards after the catch (same logic as yac_epa).	numeric
comp_air_wpa	The air_wpa for completions only.	numeric
comp_yac_wpa	The yac_wpa for completions only.	numeric
total_home_comp_air_wpa	Cumulative total completions air WPA for the home team in the game so far.	numeric
total_away_comp_air_wpa	Cumulative total completions air WPA for the away team in the game so far.	numeric
total_home_comp_yac_wpa	Cumulative total completions yac WPA for the home team in the game so far.	numeric
total_away_comp_yac_wpa	Cumulative total completions yac WPA for the away team in the game so far.	numeric
total_home_raw_air_wpa	Cumulative total raw air WPA for the home team in the game so far.	numeric
total_away_raw_air_wpa	Cumulative total raw air WPA for the away team in the game so far.	numeric
total_home_raw_yac_wpa	Cumulative total raw yac WPA for the home team in the game so far.	numeric
total_away_raw_yac_wpa	Cumulative total raw yac WPA for the away team in the game so far.	numeric
punt_blocked	Binary indicator for if the punt was blocked.	numeric
first_down_rush	Binary indicator for if a running play converted the first down.	numeric
first_down_pass	Binary indicator for if a passing play converted the first down.	numeric
first_down_penalty	Binary indicator for if a penalty converted the first down.	numeric
third_down_converted	Binary indicator for if the first down was converted on third down.	numeric
third_down_failed	Binary indicator for if the posteam failed to convert first down on third down.	numeric
fourth_down_converted	Binary indicator for if the first down was converted on fourth down.	numeric
fourth_down_failed	Binary indicator for if the posteam failed to convert first down on fourth down.	numeric
incomplete_pass	Binary indicator for if the pass was incomplete.	numeric
touchback	Binary indicator for if a touchback occurred on the play.	numeric
interception	Binary indicator for if the pass was intercepted.	numeric
punt_inside_twenty	Binary indicator for if the punt ended inside the twenty yard line.	numeric
punt_in_endzone	Binary indicator for if the punt was in the endzone.	numeric
punt_out_of_bounds	Binary indicator for if the punt went out of bounds.	numeric
punt_downed	Binary indicator for if the punt was downed.	numeric
punt_fair_catch	Binary indicator for if the punt was caught with a fair catch.	numeric
kickoff_inside_twenty	Binary indicator for if the kickoff ended inside the twenty yard line.	numeric
kickoff_in_endzone	Binary indicator for if the kickoff was in the endzone.	numeric
kickoff_out_of_bounds	Binary indicator for if the kickoff went out of bounds.	numeric
kickoff_downed	Binary indicator for if the kickoff was downed.	numeric
kickoff_fair_catch	Binary indicator for if the kickoff was caught with a fair catch.	numeric
fumble_forced	Binary indicator for if the fumble was forced.	numeric
fumble_not_forced	Binary indicator for if the fumble was not forced.	numeric
fumble_out_of_bounds	Binary indicator for if the fumble went out of bounds.	numeric
solo_tackle	Binary indicator if the play had a solo tackle (could be multiple due to fumbles).	numeric
safety	Binary indicator for whether or not a safety occurred.	numeric
penalty	Binary indicator for whether or not a penalty occurred.	numeric
tackled_for_loss	Binary indicator for whether or not a tackle for loss on a run play occurred.	numeric
fumble_lost	Binary indicator for if the fumble was lost.	numeric
own_kickoff_recovery	Binary indicator for if the kicking team recovered the kickoff.	numeric
own_kickoff_recovery_td	Binary indicator for if the kicking team recovered the kickoff and scored a TD.	numeric
qb_hit	Binary indicator if the QB was hit on the play.	numeric
rush_attempt	Binary indicator for if the play was a run.	numeric
pass_attempt	Binary indicator for if the play was a pass attempt (includes sacks).	numeric
sack	Binary indicator for if the play ended in a sack.	numeric
touchdown	Binary indicator for if the play resulted in a TD.	numeric
pass_touchdown	Binary indicator for if the play resulted in a passing TD.	numeric
rush_touchdown	Binary indicator for if the play resulted in a rushing TD.	numeric
return_touchdown	Binary indicator for if the play resulted in a return TD. Returns may occur on any of: interception, fumble, kickoff, punt, or blocked kicks.	numeric
extra_point_attempt	Binary indicator for extra point attempt.	numeric
two_point_attempt	Binary indicator for two point conversion attempt.	numeric
field_goal_attempt	Binary indicator for field goal attempt.	numeric
kickoff_attempt	Binary indicator for kickoff.	numeric
punt_attempt	Binary indicator for punts.	numeric
fumble	Binary indicator for if a fumble occurred.	numeric
complete_pass	Binary indicator for if the pass was completed.	numeric
assist_tackle	Binary indicator for if an assist tackle occurred.	numeric
lateral_reception	Binary indicator for if a lateral occurred on the reception.	numeric
lateral_rush	Binary indicator for if a lateral occurred on a run.	numeric
lateral_return	Binary indicator for if a lateral occurred on a return. Returns may occur on any of: interception, fumble, kickoff, punt, or blocked kicks.	numeric
lateral_recovery	Binary indicator for if a lateral occurred on a fumble recovery.	numeric
passer_player_id	Unique identifier for the player that attempted the pass.	character
passer_player_name	String name for the player that attempted the pass.	character
passing_yards	Numeric yards by the passer_player_name, including yards gained in pass plays with laterals. This should equal official passing statistics.	numeric
receiver_player_id	Unique identifier for the receiver that was targeted on the pass.	character
receiver_player_name	String name for the targeted receiver.	character
receiving_yards	Numeric yards by the receiver_player_name, excluding yards gained in pass plays with laterals. This should equal official receiving statistics but could miss yards gained in pass plays with laterals. Please see the description of `lateral_receiver_player_name` for further information.	numeric
rusher_player_id	Unique identifier for the player that attempted the run.	character
rusher_player_name	String name for the player that attempted the run.	character
rushing_yards	Numeric yards by the rusher_player_name, excluding yards gained in rush plays with laterals. This should equal official rushing statistics but could miss yards gained in rush plays with laterals. Please see the description of `lateral_rusher_player_name` for further information.	numeric
lateral_receiver_player_id	Unique identifier for the player that received the last(!) lateral on a pass play.	character
lateral_receiver_player_name	String name for the player that received the last(!) lateral on a pass play. If there were multiple laterals in the same play, this will only be the last player who received a lateral. Please see <https://github.com/mrcaseb/nfl-data/tree/master/data/lateral_yards> for a list of plays where multiple players recorded lateral receiving yards.	character
lateral_receiving_yards	Numeric yards by the `lateral_receiver_player_name` in pass plays with laterals. Please see the description of `lateral_receiver_player_name` for further information.	numeric
lateral_rusher_player_id	Unique identifier for the player that received the last(!) lateral on a run play.	character
lateral_rusher_player_name	String name for the player that received the last(!) lateral on a run play. If there were multiple laterals in the same play, this will only be the last player who received a lateral. Please see <https://github.com/mrcaseb/nfl-data/tree/master/data/lateral_yards> for a list of plays where multiple players recorded lateral rushing yards.	character
lateral_rushing_yards	Numeric yards by the `lateral_rusher_player_name` in run plays with laterals. Please see the description of `lateral_rusher_player_name` for further information.	numeric
lateral_sack_player_id	Unique identifier for the player that received the lateral on a sack.	character
lateral_sack_player_name	String name for the player that received the lateral on a sack.	character
interception_player_id	Unique identifier for the player that intercepted the pass.	character
interception_player_name	String name for the player that intercepted the pass.	character
lateral_interception_player_id	Unique indentifier for the player that received the lateral on an interception.	character
lateral_interception_player_name	String name for the player that received the lateral on an interception.	character
punt_returner_player_id	Unique identifier for the punt returner.	character
punt_returner_player_name	String name for the punt returner.	character
lateral_punt_returner_player_id	Unique identifier for the player that received the lateral on a punt return.	character
lateral_punt_returner_player_name	String name for the player that received the lateral on a punt return.	character
kickoff_returner_player_name	String name for the kickoff returner.	character
kickoff_returner_player_id	Unique identifier for the kickoff returner.	character
lateral_kickoff_returner_player_id	Unique identifier for the player that received the lateral on a kickoff return.	character
lateral_kickoff_returner_player_name	String name for the player that received the lateral on a kickoff return.	character
punter_player_id	Unique identifier for the punter.	character
punter_player_name	String name for the punter.	character
kicker_player_name	String name for the kicker on FG or kickoff.	character
kicker_player_id	Unique identifier for the kicker on FG or kickoff.	character
own_kickoff_recovery_player_id	Unique identifier for the player that recovered their own kickoff.	character
own_kickoff_recovery_player_name	String name for the player that recovered their own kickoff.	character
blocked_player_id	Unique identifier for the player that blocked the punt or FG.	character
blocked_player_name	String name for the player that blocked the punt or FG.	character
tackle_for_loss_1_player_id	Unique identifier for one of the potential players with the tackle for loss.	character
tackle_for_loss_1_player_name	String name for one of the potential players with the tackle for loss.	character
tackle_for_loss_2_player_id	Unique identifier for one of the potential players with the tackle for loss.	character
tackle_for_loss_2_player_name	String name for one of the potential players with the tackle for loss.	character
qb_hit_1_player_id	Unique identifier for one of the potential players that hit the QB. No sack as the QB was not the ball carrier. For sacks please see `sack_player` or `half_sack_*_player`.	character
qb_hit_1_player_name	String name for one of the potential players that hit the QB. No sack as the QB was not the ball carrier. For sacks please see `sack_player` or `half_sack_*_player`.	character
qb_hit_2_player_id	Unique identifier for one of the potential players that hit the QB. No sack as the QB was not the ball carrier. For sacks please see `sack_player` or `half_sack_*_player`.	character
qb_hit_2_player_name	String name for one of the potential players that hit the QB. No sack as the QB was not the ball carrier. For sacks please see `sack_player` or `half_sack_*_player`.	character
forced_fumble_player_1_team	Team of one of the players with a forced fumble.	character
forced_fumble_player_1_player_id	Unique identifier of one of the players with a forced fumble.	character
forced_fumble_player_1_player_name	String name of one of the players with a forced fumble.	character
forced_fumble_player_2_team	Team of one of the players with a forced fumble.	character
forced_fumble_player_2_player_id	Unique identifier of one of the players with a forced fumble.	character
forced_fumble_player_2_player_name	String name of one of the players with a forced fumble.	character
solo_tackle_1_team	Team of one of the players with a solo tackle.	character
solo_tackle_2_team	Team of one of the players with a solo tackle.	character
solo_tackle_1_player_id	Unique identifier of one of the players with a solo tackle.	character
solo_tackle_2_player_id	Unique identifier of one of the players with a solo tackle.	character
solo_tackle_1_player_name	String name of one of the players with a solo tackle.	character
solo_tackle_2_player_name	String name of one of the players with a solo tackle.	character
assist_tackle_1_player_id	Unique identifier of one of the players with a tackle assist.	character
assist_tackle_1_player_name	String name of one of the players with a tackle assist.	character
assist_tackle_1_team	Team of one of the players with a tackle assist.	character
assist_tackle_2_player_id	Unique identifier of one of the players with a tackle assist.	character
assist_tackle_2_player_name	String name of one of the players with a tackle assist.	character
assist_tackle_2_team	Team of one of the players with a tackle assist.	character
assist_tackle_3_player_id	Unique identifier of one of the players with a tackle assist.	character
assist_tackle_3_player_name	String name of one of the players with a tackle assist.	character
assist_tackle_3_team	Team of one of the players with a tackle assist.	character
assist_tackle_4_player_id	Unique identifier of one of the players with a tackle assist.	character
assist_tackle_4_player_name	String name of one of the players with a tackle assist.	character
assist_tackle_4_team	Team of one of the players with a tackle assist.	character
tackle_with_assist	Binary indicator for if there has been a tackle with assist.	numeric
tackle_with_assist_1_player_id	Unique identifier of one of the players with a tackle with assist.	character
tackle_with_assist_1_player_name	String name of one of the players with a tackle with assist.	character
tackle_with_assist_1_team	Team of one of the players with a tackle with assist.	character
tackle_with_assist_2_player_id	Unique identifier of one of the players with a tackle with assist.	character
tackle_with_assist_2_player_name	String name of one of the players with a tackle with assist.	character
tackle_with_assist_2_team	Team of one of the players with a tackle with assist.	character
pass_defense_1_player_id	Unique identifier of one of the players with a pass defense.	character
pass_defense_1_player_name	String name of one of the players with a pass defense.	character
pass_defense_2_player_id	Unique identifier of one of the players with a pass defense.	character
pass_defense_2_player_name	String name of one of the players with a pass defense.	character
fumbled_1_team	Team of one of the first player with a fumble.	character
fumbled_1_player_id	Unique identifier of the first player who fumbled on the play.	character
fumbled_1_player_name	String name of one of the first player who fumbled on the play.	character
fumbled_2_player_id	Unique identifier of the second player who fumbled on the play.	character
fumbled_2_player_name	String name of one of the second player who fumbled on the play.	character
fumbled_2_team	Team of one of the second player with a fumble.	character
fumble_recovery_1_team	Team of one of the players with a fumble recovery.	character
fumble_recovery_1_yards	Yards gained by one of the players with a fumble recovery.	numeric
fumble_recovery_1_player_id	Unique identifier of one of the players with a fumble recovery.	character
fumble_recovery_1_player_name	String name of one of the players with a fumble recovery.	character
fumble_recovery_2_team	Team of one of the players with a fumble recovery.	character
fumble_recovery_2_yards	Yards gained by one of the players with a fumble recovery.	numeric
fumble_recovery_2_player_id	Unique identifier of one of the players with a fumble recovery.	character
fumble_recovery_2_player_name	String name of one of the players with a fumble recovery.	character
sack_player_id	Unique identifier of the player who recorded a solo sack.	character
sack_player_name	String name of the player who recorded a solo sack.	character
half_sack_1_player_id	Unique identifier of the first player who recorded half a sack.	character
half_sack_1_player_name	String name of the first player who recorded half a sack.	character
half_sack_2_player_id	Unique identifier of the second player who recorded half a sack.	character
half_sack_2_player_name	String name of the second player who recorded half a sack.	character
return_team	String abbreviation of the return team. Returns may occur on any of: interception, fumble, kickoff, punt, or blocked kicks.	character
return_yards	Yards gained by the return team. Returns may occur on any of: interception, fumble, kickoff, punt, or blocked kicks.	numeric
penalty_team	String abbreviation of the team with the penalty.	character
penalty_player_id	Unique identifier for the player with the penalty.	character
penalty_player_name	String name for the player with the penalty.	character
penalty_yards	Yards gained (or lost) by the posteam from the penalty.	numeric
replay_or_challenge	Binary indicator for whether or not a replay or challenge.	numeric
replay_or_challenge_result	String indicating the result of the replay or challenge.	character
penalty_type	String indicating the penalty type of the first penalty in the given play. Will be `NA` if `desc` is missing the type.	character
defensive_two_point_attempt	Binary indicator whether or not the defense was able to have an attempt on a two point conversion, this results following a turnover.	numeric
defensive_two_point_conv	Binary indicator whether or not the defense successfully scored on the two point conversion.	numeric
defensive_extra_point_attempt	Binary indicator whether or not the defense was able to have an attempt on an extra point attempt, this results following a blocked attempt that the defense recovers the ball.	numeric
defensive_extra_point_conv	Binary indicator whether or not the defense successfully scored on an extra point attempt.	numeric
safety_player_name	String name for the player who scored a safety.	character
safety_player_id	Unique identifier for the player who scored a safety.	character
season	4 digit number indicating to which season the game belongs to.	numeric
cp	Numeric value indicating the probability for a complete pass based on comparable game situations.	numeric
cpoe	For a single pass play this is 1 - cp when the pass was completed or 0 - cp when the pass was incomplete. Analyzed for a whole game or season an indicator for the passer how much over or under expectation his completion percentage was.	numeric
series	Starts at 1, each new first down increments, numbers shared across both teams NA: kickoffs, extra point/two point conversion attempts, non-plays, no posteam	numeric
series_success	1: scored touchdown, gained enough yards for first down.	numeric
series_result	Possible values: First down, Touchdown, Opp touchdown, Field goal, Missed field goal, Safety, Turnover, Punt, Turnover on downs, QB kneel, End of half	character
order_sequence	Column provided by NFL to fix out-of-order plays. Available 2011 and beyond with source "nfl".	numeric
start_time	Kickoff time in eastern time zone.	character
time_of_day	Time of day of play in UTC "HH:MM:SS" format. Available 2011 and beyond with source "nfl".	character
stadium	Game site name.	character
weather	String describing the weather including temperature, humidity and wind (direction and speed). Doesn't change during the game!	character
nfl_api_id	UUID of the game in the new NFL API.	character
play_clock	Time on the playclock when the ball was snapped.	character
play_deleted	Binary indicator for deleted plays.	numeric
play_type_nfl	Play type as listed in the NFL source. Slightly different to the regular play_type variable.	character
special_teams_play	Binary indicator for whether play is special teams play from NFL source. Available 2011 and beyond with source "nfl".	numeric
st_play_type	Type of special teams play from NFL source. Available 2011 and beyond with source "nfl".	character
end_clock_time	Game time at the end of a given play.	character
end_yard_line	String indicating the yardline at the end of the given play consisting of team half and yard line number.	character
fixed_drive	Manually created drive number in a game.	numeric
fixed_drive_result	Manually created drive result.	character
drive_real_start_time	Local day time when the drive started (currently not used by the NFL and therefore mostly 'NA').	character
drive_play_count	Numeric value of how many regular plays happened in a given drive.	numeric
drive_time_of_possession	Time of possession in a given drive.	character
drive_first_downs	Number of forst downs in a given drive.	numeric
drive_inside20	Binary indicator if the offense was able to get inside the opponents 20 yard line.	numeric
drive_ended_with_score	Binary indicator the drive ended with a score.	numeric
drive_quarter_start	Numeric value indicating in which quarter the given drive has started.	numeric
drive_quarter_end	Numeric value indicating in which quarter the given drive has ended.	numeric
drive_yards_penalized	Numeric value of how many yards the offense gained or lost through penalties in the given drive.	numeric
drive_start_transition	String indicating how the offense got the ball.	character
drive_end_transition	String indicating how the offense lost the ball.	character
drive_game_clock_start	Game time at the beginning of a given drive.	character
drive_game_clock_end	Game time at the end of a given drive.	character
drive_start_yard_line	String indicating where a given drive started consisting of team half and yard line number.	character
drive_end_yard_line	String indicating where a given drive ended consisting of team half and yard line number.	character
drive_play_id_started	Play_id of the first play in the given drive.	numeric
drive_play_id_ended	Play_id of the last play in the given drive.	numeric
away_score	Total points scored by the away team.	numeric
home_score	Total points scored by the home team.	numeric
location	Either 'Home' o 'Neutral' indicating if the home team played at home or at a neutral site.	character
result	Equals home_score - away_score and means the game outcome from the perspective of the home team.	numeric
total	Equals home_score + away_score and means the total points scored in the given game.	numeric
spread_line	The closing spread line for the game. A positive number means the home team was favored by that many points, a negative number means the away team was favored by that many points. (Source: Pro-Football-Reference)	numeric
total_line	The closing total line for the game. (Source: Pro-Football-Reference)	numeric
div_game	Binary indicator for if the given game was a division game.	numeric
roof	One of 'dome', 'outdoors', 'closed', 'open' indicating indicating the roof status of the stadium the game was played in. (Source: Pro-Football-Reference)	character
surface	What type of ground the game was played on. (Source: Pro-Football-Reference)	character
temp	The temperature at the stadium only for 'roof' = 'outdoors' or 'open'.(Source: Pro-Football-Reference)	numeric
wind	The speed of the wind in miles/hour only for 'roof' = 'outdoors' or 'open'. (Source: Pro-Football-Reference)	numeric
home_coach	First and last name of the home team coach. (Source: Pro-Football-Reference)	character
away_coach	First and last name of the away team coach. (Source: Pro-Football-Reference)	character
stadium_id	ID of the stadium the game was played in. (Source: Pro-Football-Reference)	character
game_stadium	Name of the stadium the game was played in. (Source: Pro-Football-Reference)	character
success	Binary indicator wheter epa > 0 in the given play.	numeric
passer	Name of the dropback player (scrambles included) including plays with penalties.	character
passer_jersey_number	Jersey number of the passer.	numeric
rusher	Name of the rusher (no scrambles) including plays with penalties.	character
rusher_jersey_number	Jersey number of the rusher.	numeric
receiver	Name of the receiver including plays with penalties.	character
receiver_jersey_number	Jersey number of the receiver.	numeric
pass	Binary indicator if the play was a pass play (sacks and scrambles included).	numeric
rush	Binary indicator if the play was a rushing play.	numeric
first_down	Binary indicator if the play ended in a first down.	numeric
aborted_play	Binary indicator if the play description indicates "Aborted".	numeric
special	Binary indicator if "play_type" is one of "extra_point", "field_goal", "kickoff", or "punt".	numeric
play	Binary indicator: 1 if the play was a 'normal' play (including penalties), 0 otherwise.	numeric
passer_id	ID of the player in the 'passer' column.	character
rusher_id	ID of the player in the 'rusher' column.	character
receiver_id	ID of the player in the 'receiver' column.	character
name	Name of the 'passer' if it is not 'NA', or name of the 'rusher' otherwise.	character
jersey_number	Jersey number of the player listed in the 'name' column.	numeric
id	ID of the player in the 'name' column.	character
fantasy_player_name	Name of the rusher on rush plays or receiver on pass plays (from official stats).	character
fantasy_player_id	ID of the rusher on rush plays or receiver on pass plays (from official stats).	character
fantasy	Name of the rusher on rush plays or receiver on pass plays.	character
fantasy_id	ID of the rusher on rush plays or receiver on pass plays.	character
out_of_bounds	1 if play description contains ran ob, pushed ob, or sacked ob; 0 otherwise.	numeric
home_opening_kickoff	1 if the home team received the opening kickoff, 0 otherwise.	numeric
qb_epa	Gives QB credit for EPA for up to the point where a receiver lost a fumble after a completed catch and makes EPA work more like passing yards on plays with fumbles.	numeric
xyac_epa	Expected value of EPA gained after the catch, starting from where the catch was made. Zero yards after the catch would be listed as zero EPA.	numeric
xyac_mean_yardage	Average expected yards after the catch based on where the ball was caught.	numeric
xyac_median_yardage	Median expected yards after the catch based on where the ball was caught.	numeric
xyac_success	Probability play earns positive EPA (relative to where play started) based on where ball was caught.	numeric
xyac_fd	Probability play earns a first down based on where the ball was caught.	numeric
xpass	Probability of dropback scaled from 0 to 1.	numeric
pass_oe	Dropback percent over expected on a given play scaled from 0 to 100.	numeric"""

l = "	"

var2="""play_id                                   int64
game_id                                  string
old_game_id                               int64
home_team                                string
away_team                                string
season_type                              string
week                                      int64
posteam                                  string
posteam_type                             string
defteam                                  string
side_of_field                            string
yardline_100                            float64
game_date                                string
quarter_seconds_remaining                 int64
half_seconds_remaining                    int64
game_seconds_remaining                    int64
game_half                                string
quarter_end                               int64
drive                                   float64
sp                                        int64
qtr                                       int64
down                                    float64
goal_to_go                                int64
time                                     string
yrdln                                    string
ydstogo                                   int64
ydsnet                                  float64
desc                                     string
play_type                                string
yards_gained                            float64
shotgun                                   int64
no_huddle                                 int64
qb_dropback                             float64
qb_kneel                                  int64
qb_spike                                  int64
qb_scramble                               int64
pass_length                              string
pass_location                            string
air_yards                               float64
yards_after_catch                       float64
run_location                             string
run_gap                                  string
field_goal_result                        string
kick_distance                           float64
extra_point_result                       string
two_point_conv_result                    string
home_timeouts_remaining                   int64
away_timeouts_remaining                   int64
timeout                                 float64
timeout_team                             string
td_team                                  string
td_player_name                           string
td_player_id                             string
posteam_timeouts_remaining              float64
defteam_timeouts_remaining              float64
total_home_score                          int64
total_away_score                          int64
posteam_score                           float64
defteam_score                           float64
score_differential                      float64
posteam_score_post                      float64
defteam_score_post                      float64
score_differential_post                 float64
no_score_prob                           float64
opp_fg_prob                             float64
opp_safety_prob                         float64
opp_td_prob                             float64
fg_prob                                 float64
safety_prob                             float64
td_prob                                 float64
extra_point_prob                        float64
two_point_conversion_prob               float64
ep                                      float64
epa                                     float64
total_home_epa                          float64
total_away_epa                          float64
total_home_rush_epa                     float64
total_away_rush_epa                     float64
total_home_pass_epa                     float64
total_away_pass_epa                     float64
air_epa                                 float64
yac_epa                                 float64
comp_air_epa                            float64
comp_yac_epa                            float64
total_home_comp_air_epa                 float64
total_away_comp_air_epa                 float64
total_home_comp_yac_epa                 float64
total_away_comp_yac_epa                 float64
total_home_raw_air_epa                  float64
total_away_raw_air_epa                  float64
total_home_raw_yac_epa                  float64
total_away_raw_yac_epa                  float64
wp                                      float64
def_wp                                  float64
home_wp                                 float64
away_wp                                 float64
wpa                                     float64
vegas_wpa                               float64
vegas_home_wpa                          float64
home_wp_post                            float64
away_wp_post                            float64
vegas_wp                                float64
vegas_home_wp                           float64
total_home_rush_wpa                     float64
total_away_rush_wpa                     float64
total_home_pass_wpa                     float64
total_away_pass_wpa                     float64
air_wpa                                 float64
yac_wpa                                 float64
comp_air_wpa                            float64
comp_yac_wpa                            float64
total_home_comp_air_wpa                 float64
total_away_comp_air_wpa                 float64
total_home_comp_yac_wpa                 float64
total_away_comp_yac_wpa                 float64
total_home_raw_air_wpa                  float64
total_away_raw_air_wpa                  float64
total_home_raw_yac_wpa                  float64
total_away_raw_yac_wpa                  float64
punt_blocked                            float64
first_down_rush                         float64
first_down_pass                         float64
first_down_penalty                      float64
third_down_converted                    float64
third_down_failed                       float64
fourth_down_converted                   float64
fourth_down_failed                      float64
incomplete_pass                         float64
touchback                                 int64
interception                            float64
punt_inside_twenty                      float64
punt_in_endzone                         float64
punt_out_of_bounds                      float64
punt_downed                             float64
punt_fair_catch                         float64
kickoff_inside_twenty                   float64
kickoff_in_endzone                      float64
kickoff_out_of_bounds                   float64
kickoff_downed                          float64
kickoff_fair_catch                      float64
fumble_forced                           float64
fumble_not_forced                       float64
fumble_out_of_bounds                    float64
solo_tackle                             float64
safety                                  float64
penalty                                 float64
tackled_for_loss                        float64
fumble_lost                             float64
own_kickoff_recovery                    float64
own_kickoff_recovery_td                 float64
qb_hit                                  float64
rush_attempt                            float64
pass_attempt                            float64
sack                                    float64
touchdown                               float64
pass_touchdown                          float64
rush_touchdown                          float64
return_touchdown                        float64
extra_point_attempt                     float64
two_point_attempt                       float64
field_goal_attempt                      float64
kickoff_attempt                         float64
punt_attempt                            float64
fumble                                  float64
complete_pass                           float64
assist_tackle                           float64
lateral_reception                       float64
lateral_rush                            float64
lateral_return                          float64
lateral_recovery                        float64
passer_player_id                         string
passer_player_name                       string
passing_yards                           float64
receiver_player_id                       string
receiver_player_name                     string
receiving_yards                         float64
rusher_player_id                         string
rusher_player_name                       string
rushing_yards                           float64
lateral_receiver_player_id               string
lateral_receiver_player_name             string
lateral_receiving_yards                 float64
lateral_rusher_player_id                 string
lateral_rusher_player_name               string
lateral_rushing_yards                   float64
lateral_sack_player_id                  float64
lateral_sack_player_name                float64
interception_player_id                   string
interception_player_name                 string
lateral_interception_player_id          float64
lateral_interception_player_name        float64
punt_returner_player_id                  string
punt_returner_player_name                string
lateral_punt_returner_player_id         float64
lateral_punt_returner_player_name       float64
kickoff_returner_player_name             string
kickoff_returner_player_id               string
lateral_kickoff_returner_player_id      float64
lateral_kickoff_returner_player_name    float64
punter_player_id                         string
punter_player_name                       string
kicker_player_name                       string
kicker_player_id                         string
own_kickoff_recovery_player_id          float64
own_kickoff_recovery_player_name        float64
blocked_player_id                        string
blocked_player_name                      string
tackle_for_loss_1_player_id              string
tackle_for_loss_1_player_name            string
tackle_for_loss_2_player_id             float64
tackle_for_loss_2_player_name           float64
qb_hit_1_player_id                       string
qb_hit_1_player_name                     string
qb_hit_2_player_id                       string
qb_hit_2_player_name                     string
forced_fumble_player_1_team              string
forced_fumble_player_1_player_id         string
forced_fumble_player_1_player_name       string
forced_fumble_player_2_team             float64
forced_fumble_player_2_player_id        float64
forced_fumble_player_2_player_name      float64
solo_tackle_1_team                       string
solo_tackle_2_team                       string
solo_tackle_1_player_id                  string
solo_tackle_2_player_id                  string
solo_tackle_1_player_name                string
solo_tackle_2_player_name                string
assist_tackle_1_player_id                string
assist_tackle_1_player_name              string
assist_tackle_1_team                     string
assist_tackle_2_player_id                string
assist_tackle_2_player_name              string
assist_tackle_2_team                     string
assist_tackle_3_player_id               float64
assist_tackle_3_player_name             float64
assist_tackle_3_team                    float64
assist_tackle_4_player_id               float64
assist_tackle_4_player_name             float64
assist_tackle_4_team                    float64
tackle_with_assist                      float64
tackle_with_assist_1_player_id           string
tackle_with_assist_1_player_name         string
tackle_with_assist_1_team                string
tackle_with_assist_2_player_id          float64
tackle_with_assist_2_player_name        float64
tackle_with_assist_2_team               float64
pass_defense_1_player_id                 string
pass_defense_1_player_name               string
pass_defense_2_player_id                 string
pass_defense_2_player_name               string
fumbled_1_team                           string
fumbled_1_player_id                      string
fumbled_1_player_name                    string
fumbled_2_player_id                     float64
fumbled_2_player_name                   float64
fumbled_2_team                          float64
fumble_recovery_1_team                   string
fumble_recovery_1_yards                 float64
fumble_recovery_1_player_id              string
fumble_recovery_1_player_name            string
fumble_recovery_2_team                  float64
fumble_recovery_2_yards                 float64
fumble_recovery_2_player_id             float64
fumble_recovery_2_player_name           float64
sack_player_id                           string
sack_player_name                         string
half_sack_1_player_id                    string
half_sack_1_player_name                  string
half_sack_2_player_id                    string
half_sack_2_player_name                  string
return_team                              string
return_yards                            float64
penalty_team                             string
penalty_player_id                        string
penalty_player_name                      string
penalty_yards                           float64
replay_or_challenge                       int64
replay_or_challenge_result               string
penalty_type                             string
defensive_two_point_attempt             float64
defensive_two_point_conv                float64
defensive_extra_point_attempt           float64
defensive_extra_point_conv              float64
safety_player_name                       string
safety_player_id                         string
season                                    int64
cp                                      float64
cpoe                                    float64
series                                    int64
series_success                            int64
series_result                            string
order_sequence                            int64
start_time                               string
time_of_day                              string
stadium                                  string
weather                                  string
nfl_api_id                               string
play_clock                                int64
play_deleted                              int64
play_type_nfl                            string
special_teams_play                        int64
st_play_type                            float64
end_clock_time                           string
end_yard_line                           float64
fixed_drive                               int64
fixed_drive_result                       string
drive_real_start_time                    string
drive_play_count                        float64
drive_time_of_possession                 string
drive_first_downs                       float64
drive_inside20                          float64
drive_ended_with_score                  float64
drive_quarter_start                     float64
drive_quarter_end                       float64
drive_yards_penalized                   float64
drive_start_transition                   string
drive_end_transition                     string
drive_game_clock_start                   string
drive_game_clock_end                     string
drive_start_yard_line                    string
drive_end_yard_line                      string
drive_play_id_started                   float64
drive_play_id_ended                     float64
away_score                                int64
home_score                                int64
location                                 string
result                                    int64
total                                     int64
spread_line                             float64
total_line                              float64
div_game                                  int64
roof                                     string
surface                                  string
temp                                    float64
wind                                    float64
home_coach                               string
away_coach                               string
stadium_id                               string
game_stadium                             string
aborted_play                              int64
success                                 float64
passer                                   string
passer_jersey_number                    float64
rusher                                   string
rusher_jersey_number                    float64
receiver                                 string
receiver_jersey_number                  float64
pass                                      int64
rush                                      int64
first_down                              float64
special                                   int64
play                                      int64
passer_id                                string
rusher_id                                string
receiver_id                              string
name                                     string
jersey_number                           float64
id                                       string
fantasy_player_name                      string
fantasy_player_id                        string
fantasy                                  string
fantasy_id                               string
out_of_bounds                             int64
home_opening_kickoff                      int64
qb_epa                                  float64
xyac_epa                                float64
xyac_mean_yardage                       float64
xyac_median_yardage                     float64
xyac_success                            float64
xyac_fd                                 float64
xpass                                   float64
pass_oe                                 float64"""
# for line in var.split("\n"):
#     column_name , desc,type_ = line.split(l)
#     print(column_name,type_)
splitter = " "
for line in var2.split("\n"):
    column,type_ = line.split(splitter)[0],line.split(splitter)[-1]
    stxt = ""
    if type_== "string":
        stxt = "model.CharField(max_length=256)"
    elif type_ == "int64":
        stxt = "model.IntegerField()"
    else:
        stxt = "model.FloatField()"
    print(column," = ",stxt)
    
    # try:
        # assert len(line.split(splitter)) == 2
    # except Exception:
        # print(line,len(line.split(splitter)),line.split(splitter),"error")
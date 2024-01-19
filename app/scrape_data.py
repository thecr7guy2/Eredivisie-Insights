import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

stats = ["player","nationality","position","team","age","birth_year","games","games_starts","minutes",
 "goals","assists","pens_made","pens_att","cards_yellow","cards_red","goals_per90","assists_per90",
 "goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg","npxg","xAg","xg_per90",
 "xag_per90","xg_xag_per90","npxg_per90","npxg_xag_per90"]

stats3 = ["players_used","possession","games","games_starts","minutes","goals","assists","pens_made","pens_att","cards_yellow","cards_red","goals_per90","assists_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg","npxg","xa","xg_per90","xa_per90","xg_xa_per90","npxg_per90","npxg_xa_per90"]

shooting2 = ["minutes_90s","goals","pens_made","pens_att","shots_total","shots_on_target",
             "shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90",
             "goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]

shooting3 = ["goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]

passing2 = ["passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance",
 "passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium",
 "passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xa","xa_net",
 "assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes"]

defense2 =["tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","dribble_tackles","dribbles_vs","dribble_tackles_pct","dribbled_past","pressures","pressure_regains",
 "pressure_regain_pct","pressures_def_3rd","pressures_mid_3rd","pressures_att_3rd","blocks","blocked_shots","blocked_shots_saves","blocked_passes","interceptions","clearances","errors"]

possession2 = ["touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","dribbles_completed","dribbles","dribbles_completed_pct",
               "players_dribbled_past","nutmegs","carries","carry_distance","carry_progressive_distance","progressive_carries","carries_into_final_third","carries_into_penalty_area","pass_targets","passes_received"
               ,"passes_received_pct","miscontrols","dispossessed"]


def get_url(category):
    top = "https://fbref.com/en/comps/23/"
    end = "/Eredivisie-Stats"
    return (top + category + end)


def get_tables(url):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    team_vs_table = all_tables[1]
    player_table = all_tables[2]
    return player_table,team_table


def get_frame_players(features,player_table):
    pre_df_player = dict()
    features_wanted_player = features
    rows_player = player_table.find_all('tr')
    for row in rows_player:
         if(row.find('th',{"scope":"row"}) != None):
             for f in features_wanted_player:
                cell = row.find("td",{"data-stat": f})
                if cell is not None:
                    a = cell.text.strip().encode()
                    text=a.decode("utf-8")
                    if(text == ''):
                        text = '0'
                    if((f!='player')&(f!='nationality')&(f!='position')&(f!='team')&(f!='age')&(f!='birth_year')):
                        text = float(text.replace(',',''))
                    if f in pre_df_player:
                        pre_df_player[f].append(text)
                    else:
                        pre_df_player[f] = [text]

    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player

def get_frame_team(features,team_table):
    pre_df_squad = dict()
    #Note: features does not contain squad name, it requires special treatment
    features_wanted_squad = features
    rows_squad = team_table.find_all('tr')
    for row in rows_squad:
        if(row.find('th',{"scope":"row"}) != None):
            name = row.find('th',{"data-stat":"squad"}).text.strip().encode().decode("utf-8")
            if 'squad' in pre_df_squad:
                pre_df_squad['squad'].append(name)
            else:
                pre_df_squad['squad'] = [name]
            for f in features_wanted_squad:
                cell = row.find("td",{"data-stat": f})
                if cell is not None:
                    a = cell.text.strip().encode()
                    text=a.decode("utf-8")
                    if(text == ''):
                        text = '0'
                    if((f!='player')&(f!='nationality')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')):
                        text = float(text.replace(',',''))
                    if f in pre_df_squad:
                        pre_df_squad[f].append(text)
                    else:
                        pre_df_squad[f] = [text]
    df_squad = pd.DataFrame.from_dict(pre_df_squad)
    return df_squad
       
       
def get_player_df(category, features):
    url= get_url(category)
    pt,tt = get_tables(url)
    df = get_frame_players(features,pt)
    return df

def get_team_df(category, features):
    url= get_url(category)
    pt,tt = get_tables(url)
    df = get_frame_players(features,tt)
    return df 

def get_all_player_df():
    a = get_player_df("stats",stats)
    b = get_player_df("shooting",shooting2)
    c = get_player_df("passing",passing2)
    d = get_player_df('defense',defense2)
    e = get_player_df('possession',possession2)

    df = pd.concat([a,b,c,d,e], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df 

def get_all_team_df():
    a = get_team_df("stats",stats3)
    b = get_team_df("shooting",shooting3)
    c = get_team_df("passing",passing2)
    d = get_team_df('defense',defense2)
    e = get_team_df('possession',possession2)

    df = pd.concat([a,b,c,d,e], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df 
    


if __name__ == "__main__":
    players = get_all_player_df()
    json_data = players.to_json(orient='records', lines=True)
    with open('../data/raw_data/player_data.json', 'w') as file:
        file.write(json_data)

    teams = get_all_team_df()
    # print(players.shape)
    # print(teams.shape)
    json_data = teams.to_json(orient='records', lines=True)
    with open('../data/raw_data/team_data.json', 'w') as file:
        file.write(json_data)

    
    
    

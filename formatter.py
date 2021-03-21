with open('rankings/538_elo.csv') as file:
    data = file.read().split('\n')[:-1:]

teams = [team.split(',')[0] for team in data]

with open('mmrankings/teams.txt') as file:
    data = file.read().split('\n')
    short_teams = {team.split(',')[0]: team.split(',')[1] for team in data}

rankings = ['538_elo', 'espn_bpi', 'kenpom', 'rpi']

for system in rankings:
    with open('rankings/{}.csv'.format(system)) as file:
        data = file.read().split('\n')[:-1:]
    old_dict = {team.split(',')[0]: float(team.split(',')[1]) for team in data}
    new_dict = {short_teams[team]: old_dict[team] for team in short_teams}
    with open('mmrankings/{}.csv'.format(system), 'w') as file:
        for team in new_dict:
            file.write("{},{},\n".format(team, new_dict[team]))

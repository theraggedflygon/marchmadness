with open('rankings/538_elo.csv') as file:
    data = file.read().split('\n')[:-1:]

master_teams = [team.split(',')[0] for team in data]

for team in master_teams:
    print(team)

rankings = ['538_elo', 'espn_bpi', 'kenpom', 'rpi']

for system in rankings:
    with open('rankings/{}.csv'.format(system)) as file:
        data = file.read().split('\n')[:-1:]
    sys_teams = [team.split(",")[0] for team in data]
    for team in master_teams:
        if team not in sys_teams:
            print(system, team)
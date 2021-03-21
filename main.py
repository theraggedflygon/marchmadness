import random


def match_sim(t1, t2, rankings, idxs, divs):
    prob = 0.0
    for idx in idxs:
        diff = rankings[idx][t2] - rankings[idx][t1]
        diff *= divs[idx]
        exp_t1 = 1 / (1 + 10 ** (diff / 400))
        prob += exp_t1

    prob /= 4

    result = random.random()
    if result <= prob:
        return t1
    else:
        return t2


random.seed()

with open("matches.txt") as file:
    data = file.read().split("\n")
    matches_master = [[game.split(',')[0], game.split(',')[1]] for game in data]

for i in range(32, 63):
    matches_master[i][0] = int(matches_master[i][0])
    matches_master[i][1] = int(matches_master[i][1])

systems = ["538_elo", "espn_bpi", "kenpom", "rpi"]
divs = {"538_elo": 30.464, "espn_bpi": 25, "kenpom": 20, "rpi": 4000}
rankings_dict = {}

for system in systems:
    with open("mmrankings/{}.csv".format(system)) as file:
        system_data = file.read().split('\n')[:-1:]
        system_dict = {team.split(',')[0]: float(team.split(',')[1]) for team in system_data}
        rankings_dict[system] = system_dict

open("results/results1.csv", 'w').close()

for i in range(100000):
    print(i)
    matches = matches_master.copy()
    winners = ["" for j in range(63)]
    for idx, game in enumerate(matches[:32:]):
        winners[idx] = match_sim(game[0], game[1], rankings_dict, systems, divs)
    for idx, game in enumerate(matches[32:]):
        winners[idx + 32] = match_sim(winners[game[0] - 1], winners[game[1] - 1], rankings_dict, systems, divs)

    with open("results/results1.csv", 'a') as file:
        file.write(','.join(winners))
        file.write('\n')
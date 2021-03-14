import requests
from bs4 import BeautifulSoup


def get_kenpom_rankings():
    kenpom = {}
    r = requests.get("https://kenpom.com/").text
    kp_soup = BeautifulSoup(r, 'lxml')

    kp_table = kp_soup.find('table', id="ratings-table")

    for section in kp_table.find_all("tbody"):
        for team in section.find_all("tr"):
            team_list = []
            for col in team.find_all("td"):
                team_list.append(col.text)
            try:
                kenpom[team_list[1]] = float(team_list[4])
            except IndexError:
                continue

    kenpom_write_file(kenpom)


def kenpom_write_file(ratings):
    with open("rankings/kenpom.csv", 'w') as file:
        for team in ratings:
            file.write("{},{},\n".format(team, ratings[team]))


if __name__ == "__main__":
    get_kenpom_rankings()
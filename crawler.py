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

    write_rankings(kenpom, 'kenpom')


def write_rankings(ratings, source):
    with open("rankings/{}.csv".format(source), 'w') as file:
        for team in ratings:
            file.write("{},{},\n".format(team, ratings[team]))


def espn_get_rankings():
    bpi = {}
    for i in range(1, 8):
        r = requests.get("https://www.espn.com/mens-college-basketball/bpi/_/view/bpi/page/{}".format(i)).text
        espn_soup = BeautifulSoup(r, 'lxml')

        bpi_table = espn_soup.find('table', {"class": "bpi__table"}).find('tbody')

        for team in bpi_table.find_all("tr"):
            team_cols = team.find_all("td")
            name = team_cols[1].find("span", {"class": "team-names"}).text
            bpi_rating = float(team_cols[6].text)
            bpi[name] = bpi_rating

    write_rankings(bpi, 'espn_bpi')

if __name__ == "__main__":
    # get_kenpom_rankings()
    espn_get_rankings()

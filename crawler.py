import requests
from bs4 import BeautifulSoup
import csv


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


def rpi_get_rankings():
    rpi = {}
    r = requests.get("https://www.cbssports.com/college-basketball/rankings/rpi/").text
    rpi_soup = BeautifulSoup(r, 'lxml')

    rpi_table = rpi_soup.find('table', {"class": "TableBase-table"}).find("tbody")

    for team in rpi_table.find_all("tr"):
        team_cols = team.find_all("td")
        team = team_cols[1].text.split("\n")[1]
        rating_str = team_cols[3].text.split("\n")[1].strip()
        if rating_str == "—":
            rating = 0
        else:
            rating = float(rating_str)
        rpi[team] = rating

    write_rankings(rpi, 'rpi')


def elo_538_get_rankings():
    elo = {}
    with open("data/538.csv", 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        gender_idx = headers.index("gender")
        name_idx = headers.index("team_name")
        rating_idx = headers.index("team_rating")
        for team in reader:
            if team[gender_idx] == "mens":
                elo[team[name_idx]] = float(team[rating_idx])

    write_rankings(elo, "538_elo")


def write_rankings(ratings, source):
    with open("rankings/{}.csv".format(source), 'w') as file:
        for team in ratings:
            file.write("{},{},\n".format(team, ratings[team]))


if __name__ == "__main__":
    # get_kenpom_rankings()
    # espn_get_rankings()
    # rpi_get_rankings()
    elo_538_get_rankings()

import re
import curses
import time
import requests
import os
import xml.etree.ElementTree as ET
import urllib
import AdditionalGameInfo
from bs4 import BeautifulSoup
from blessings import Terminal

# sets up blessings terminal for style
t = Terminal()
away_team = " "
home_team = " "
score_line = "R   H   E"
template_innings = "      " + "1   " + "2   " + "3   " + "4   " + "5   " + "6   " + "7   " + "8   " + "9   "
current_month = "month_" + time.strftime("%m") + "/"
current_day = "day_" + time.strftime("%d") + "/"

info = AdditionalGameInfo


def main():
    try:
        team = raw_input("Please select an MLB team: ")
        generator(team)
    except Exception, e:
        print e


def generator(team):  # generates XML page and parser for given team on current day
    url = "http://gd2.mlb.com/components/game/mlb/year_2016/" + current_month + current_day
    game = find_team(grab_links(url), team)
    xml_file = url + game.strip() + "linescore.xml"
    parseXml(xml_file)


def grab_links(url):  # returning all links from given URL
    game_page = requests.get(url)
    soup = BeautifulSoup(game_page.content, "lxml")
    links = soup.find_all("a")  # finds all of the links on Gameday site
    page_links = []

    # adding all of the links to a list
    for link in links:
        page_links.append(link.text)

    return page_links


def find_team(links, team):  # function to find baseball game
    for link in links:
        if re.search(team + 'mlb', link) is not None:
            return str(link)
        else:
            pass

    os.system('clear')
    print t.red("Try a valid MLB team.")
    main()


def setupXmlParser(xml_file):  # sets up XML file to be parsed
    response = urllib.urlopen(xml_file)
    tree = ET.parse(response)
    root = tree.getroot()
    parser(root)


def xmlParser(root):  # parses score, current batter, count, and last play
    global away_team, home_team, score_line, template_innings
    away_team = root.get('away_name_abbrev') + "  "
    home_team = root.get('home_name_abbrev') + "  "

    if root.get('status') == 'In Progress':
        while True:
            away_runs = ""
            home_runs = ""
            for line_score in root.findall('linescore'):
                away_inning = line_score.get('away_inning_runs')
                home_inning = line_score.get('home_inning_runs')
                away_runs = away_runs + away_inning + "   "
                home_runs = home_runs + home_inning + "   "

            print template_innings
            print t.bold(away_team) + " " + away_runs
            print t.bold(home_team) + " " + home_runs

            balls = root.get('balls')
            strikes = root.get('strikes')
            outs = root.get('outs')
            print "B:" + balls + " S:" + strikes + " O:" + outs
            print "At Bat: " + info.current_batter_pitcher(root, 'batter')
            print "Pitching: " + info.current_batter_pitcher(root, 'pitcher')

            last_play = root.get('pbp_last')
            print last_play
            main();

    elif root.get('status') == 'Final':
        os.system('clear')
        print t.bold_underline("FINAL SCORE")
        print "      " + score_line
        print away_team, info.score(root, 'away')
        print home_team, info.score(root, 'home')
        main()

    else:
        os.system('clear')
        game_time = root.get('time') + " " + root.get('time_zone')
        print game_time
        print t.bold(away_team), info.team_win_loss(root, 'away'), info.probable_starters(root, 'away')
        print t.bold(home_team), info.team_win_loss(root, 'home'), info.probable_starters(root, 'home')
        print t.red("This team's game has not yet begun.")
        main()


if __name__ == "__main__":
    main()

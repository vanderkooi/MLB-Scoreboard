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
        url = url_generator(team)
        xml_file = xml_generator(url)
        parseXml(xml_file)
    except Exception, e:
        print e


def url_generator(team): 
    return url = "http://gd2.mlb.com/components/game/mlb/year_2016/" + current_month + current_day

def xml_generator(url):
    game = find_team(grab_links(url), team)
    return url + game.strip() + "linescore.xml"

def grab_links(url):  
    game_page = requests.get(url)
    soup = BeautifulSoup(game_page.content, "lxml")
    links = soup.find_all("a") 
    page_links = []

    for link in links:
        page_links.append(link.text)

    return page_links


def find_team(links, team):  
    for link in links:
        if re.search(team + 'mlb', link) is not None:
            return str(link)
        else:
            pass

    os.system('clear')
    print t.red("Try a valid MLB team.")
    main()


def parseXml(xml_file):  
    response = urllib.urlopen(xml_file)
    tree = ET.parse(response)
    root = tree.getroot()
    parser(root)



def xmlParser(root):  
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

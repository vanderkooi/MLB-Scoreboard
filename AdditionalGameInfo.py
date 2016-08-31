# seperate file to compute additional info about a game

def score(root, team):  # helper function for scores of finished games
    team_runs = root.get(team + '_team_runs') + "  "
    team_hits = root.get(team + '_team_hits') + "  "
    team_errors = root.get(team + '_team_errors') + "  "
    return team_runs + ' ' + team_hits + ' ' + team_errors


def probable_starters(root, team):  # finds probable starters for the game
    for pitcher in root.findall(team + '_probable_pitcher'):
        name = pitcher.get('name_display_roster')
        wins = pitcher.get('wins')
        losses = pitcher.get('losses')
        era = pitcher.get('era')
        return name + " (" + wins + "-" + losses + ", " + era + ")"


def current_batter_pitcher(root, player): # returns the current batter/pitcher in the game
    for at_bat in root.findall('current_' + player):
        first_name = at_bat.get('first_name')
        last_name = at_bat.get('last_name')

    return first_name + " " + last_name


def team_win_loss(root, team):  # finds team's win-loss record
    win = root.get(team + '_win')
    loss = root.get(team + '_loss')
    return "(" + win + "-" + loss + ")"
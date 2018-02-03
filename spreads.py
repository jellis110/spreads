# Load libraries
import pandas
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import csv, math, ast, sys, numpy as np

# Load dataset
dataset = csv.DictReader(open('C:/Users/Josh/Documents/2017NFLStats.csv'))





def homedogbet(wagering_size,starting_bankroll):
    starting_bankroll = 100
    wagering_size = 5
    bankroll = starting_bankroll
    upsets=0
    non_upsets=0
    for game in dataset:
        home_team = game["HomeTeam"]
        away_team = game["VisTeam"]
        home_score = int(game["HomeScore"])
        away_score = int(game["VisScore"])
        home_spread = float(game["HomeSpread"])
        away_spread = float(game["VisSpread"])


        if home_spread > away_spread:
            if home_score > away_score:
                upsets += 1
                bankroll += wagering_size * 1.9091
            else:
                non_upsets += 1
                bankroll -= wagering_size
    ROI = ((bankroll - starting_bankroll) / (wagering_size * (upsets + non_upsets))) * 100
    print ("There were '%s' upsets out of '%s' total matches" % (upsets, upsets + non_upsets))
    print ("Starting bankroll = '%s'" % (starting_bankroll))
    print ("Finishing bankroll = '%s' | ROI = '%s'" % (bankroll, ROI))

def possession(possession):
    game_count = 0
    cover = 0
    no_cover = 0
    push = 0
    
    
    for game in dataset:
       home_team = game["HomeTeam"]
       away_team = game["VisTeam"]
       home_score = int(game["HomeScore"])
       away_score = int(game["VisScore"])
       home_spread = float(game["HomeSpread"])
       away_spread = float(game["VisSpread"])
       home_poss = int(game["TimeofPossessionHome"])
       vis_poss = int(game["TimeofPossessionVis"])
       date = str(game["Date"])

       if home_poss >= possession:
            spread = home_spread
            game_count += 1
            if spread > 0:
                if away_score - home_score == spread:
                    push += 1
                elif home_score - away_score > 0:
                    cover += 1
                elif abs(home_score - away_score) < spread:
                    cover += 1
                elif home_score - away_score < spread:
                    no_cover += 1   
            elif spread < 0:
                if home_score - away_score == spread:
                    push += 1
                elif home_score - away_score > abs(spread):
                    cover += 1
                elif home_score - away_score < abs(spread):
                    no_cover += 1
       elif vis_poss >= possession:
            spread = away_spread
            game_count += 1
            if spread > 0:
                if home_score - away_score == spread:
                    push += 1
                elif away_score - home_score > 0:
                    cover += 1
                elif abs(away_score - home_score) < spread:
                    cover += 1
                elif abs(away_score - home_score) > spread:
                    no_cover += 1 
            elif spread < 0:
                if away_score - home_score == spread:
                    push += 1
                elif away_score - home_score > abs(spread):
                    cover += 1
                elif away_score - home_score < abs(spread):
                    no_cover += 1
       elif possession < home_poss & possession < vis_poss:
            print ("No game found '%s' - '%s' and '%s' '%s' - '%s' " % (date,home_team,away_team, home_poss,vis_poss))
    
    if game_count> 0:
        spread_percent = cover / game_count * 100              
        print("Teams with TOP greater than or equal to '%s' covered the spread '%f' percent of the time" % (possession, spread_percent))
        print ("Covers: '%s' Games: '%s'" % (cover,game_count))
    else:
        print ("No games where one team had '%s' TOP or more." % (possession))
    
def coverspread():
    for game in dataset:
        home_team = game["HomeTeam"]
        away_team = game["VisTeam"]
        home_score = float(game["HomeScore"])
        away_score = float(game["VisScore"])
        home_spread = float(game["HomeSpread"])
        away_spread = float(game["VisSpread"])
        date = str(game["Date"])

        if home_spread < away_spread:
            if (home_score - away_score) < abs(home_spread):
                print ("Date: Away Team '%s' - '%s' covered the spread of '%s'" % (date, away_team, away_spread))
            else:
                print ("Date: Home Team '%s' - '%s' covered the spread of '%s'" % (date, home_team, home_spread))
                
def teamcover(team):
    cover = 0
    no_cover = 0
    push = 0
    
    for game in dataset:
        home_team = game["HomeTeam"]
        away_team = game["VisTeam"]
        home_score = int(game["HomeScore"])
        away_score = int(game["VisScore"])
        home_spread = float(game["HomeSpread"])
        away_spread = float(game["VisSpread"])
        date = str(game["Date"])

        
        if team == home_team:
            spread = home_spread
            if spread > 0:
                if away_score - home_score == spread:
                    print ("Home Push Spread: '%s' '%s'-'%s'" % (spread,home_score,away_score))
                    print (home_score - away_score)
                    push += 1
                elif home_score - away_score > 0:
                    print ("Home Dog '%s' covered '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (home_score - away_score)
                    cover += 1
                elif abs(home_score - away_score) < spread:
                    print ("Home Dog '%s' covered '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (home_score - away_score)
                    cover += 1
                elif home_score - away_score < spread:
                    print ("Home Dog '%s' No Cover '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (home_score - away_score)
                    no_cover += 1   
            elif spread < 0:
                if home_score - away_score == spread:
                    print ("Home Push Spread: '%s' '%s'-'%s'" % (spread,home_score,away_score))
                    print (home_score - away_score)
                    push += 1
                elif home_score - away_score > abs(spread):
                    print ("Home Fav '%s' covered '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (home_score - away_score)
                    cover += 1
                elif home_score - away_score < abs(spread):
                    print ("Home Fav '%s' No Cover '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (home_score - away_score)
                    no_cover += 1   
        if team ==  away_team:
            spread = away_spread
            if spread > 0:
                if home_score - away_score == spread:
                    print ("Away Push Spread: '%s' '%s'-'%s'" % (spread,home_score,away_score))
                    print (home_score - away_score)
                    push += 1
                elif away_score - home_score > 0:
                    print ("Away Dog '%s' covered '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (away_score - home_score)
                    cover += 1
                elif abs(away_score - home_score) < spread:
                    print ("Away Dog '%s' covered '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (away_score - home_score)
                    cover += 1
                elif abs(away_score - home_score) > spread:
                    print ("Away Dog '%s' No Cover '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (away_score - home_score)
                    no_cover += 1 
            elif spread < 0:
                if away_score - home_score == spread:
                    print ("Away Push Spread: '%s' '%s'-'%s'" % (spread,home_score,away_score))
                    print (home_score - away_score)
                    push += 1
                elif away_score - home_score > abs(spread):
                    print ("Away Fav '%s' covered '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (away_score - home_score)
                    cover += 1
                elif away_score - home_score < abs(spread):
                    print ("Away Fav '%s' No Cover '%s' '%s'-'%s'" % (team, spread, home_score, away_score))
                    print (away_score - home_score)
                    no_cover += 1
                
            
    print (" The '%s' went '%s' - '%s' ATS with '%s' pushes." % (team, cover, no_cover,push))

def main():
    print("1. Home Dog Bet")
    print("2. Teams that covered each game")
    print("3. How many times a team covered")
    print("4. Cover by Time of Possession")
    choice = int(input("Select a choice: "))
    if choice == 1:
        starting_bankroll = int(input("Enter starting bankroll: "))
        wagering_size = int(input("Enter size of each wager: "))
        homedogbet(wagering_size,starting_bankroll)
    elif choice == 2:
        coverspread()
    elif choice == 3:
        team = input("Enter team: ")
        teamcover(team)
    elif choice == 4:
        poss = int(input("Time of possession in seconds: "))
        possession(poss)

if __name__ == "__main__":
    main()





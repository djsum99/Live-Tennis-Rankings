import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import re
import urllib.request
from bs4 import BeautifulSoup
from googlesearch import search
from urllib.request import Request, urlopen
import pickle
import time
import os
import glob

australian_open = True
dubai = True
indian_wells = True
miami = True
madrid = True
rome = True
roland_garros = True
wimbledon = True
cincinnati = False
us_open = False
wuhan = False
beijing = False

class Points:
    def __init__(self,level,tournament,number):
        self.level = level
        self.tournament = tournament.split(' - ')[0]
        self.number = number

class Player:
    def __init__(self,name,rank,points_breakdown):
        self.name = name
        self.points_breakdown = points_breakdown
        self.rank = rank
        self.points_possibilities = []
        
        self.points_total = 0
        self.tournaments_used = []
        self.extra_tournaments = 16
        self.mandatories = []
        self.premier_5s = []
        self.others = []
        for i in points_breakdown:
            if i.level=='Grand Slam' or i.level=='Premier Mandatory':
                self.mandatories.append(i)
            elif i.level=='Premier 5':
                self.premier_5s.append(i)
            else:
                self.others.append(i)
        self.premier_5s = sorted(self.premier_5s, key=lambda points: points.number, reverse=True)
        
        if australian_open:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='AUSTRALIAN OPEN':
                    in_there = True
                    break
            if not in_there:
                m = Points('Grand Slam','AUSTRALIAN OPEN',0)
                self.mandatories.append(m)
        if roland_garros:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='ROLAND GARROS':
                    in_there = True
                    break
            if not in_there:
                m = Points('Grand Slam','ROLAND GARROS',0)
                self.mandatories.append(m)
        if wimbledon:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='WIMBLEDON':
                    in_there = True
                    break
            if not in_there:
                m = Points('Grand Slam','WIMBLEDON',0)
                self.mandatories.append(m)
        if us_open:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='US OPEN':
                    in_there = True
                    break
            if not in_there:
                m = Points('Grand Slam','US OPEN',0)
                self.mandatories.append(m)
        if indian_wells:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='INDIAN WELLS':
                    in_there = True
                    break
            if not in_there:
                m = Points('Premier Mandatory','INDIAN WELLS',0)
                self.mandatories.append(m)
        if miami:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='MIAMI':
                    in_there = True
                    break
            if not in_there:
                m = Points('Premier Mandatory','MIAMI',0)
                self.mandatories.append(m)
        if madrid:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='MADRID':
                    in_there = True
                    break
            if not in_there:
                m = Points('Premier Mandatory','MADRID',0)
                self.mandatories.append(m)
        if beijing:
            in_there = False
            for m in self.mandatories:
                if m.tournament=='BEIJING':
                    in_there = True
                    break
            if not in_there:
                m = Points('Premier Mandatory','BEIJING',0)
                self.mandatories.append(m)
        if dubai:
            if len(self.premier_5s)>0:
                self.mandatories.append(self.premier_5s[0])
                self.premier_5s = self.premier_5s[1:]
        if rome:
            if len(self.premier_5s)>0:
                self.mandatories.append(self.premier_5s[0])
                self.premier_5s = self.premier_5s[1:]
        if cincinnati:
            in_there = False
            for m in mandatories:
                if m.level=='Premier 5':
                    in_there = True
                    break
            if not in_there:
                m = Points('Premier 5','-',0)
                self.mandatories.append(m)
        if wuhan:
            in_there = False
            count = 0
            for m in mandatories:
                if m.level=='Premier 5':
                    count+=1
                if count==2:
                    in_there = True
                    break
            if not in_there:
                m = Points('Premier 5','-',0)
                self.mandatories.append(m)
        
        while len(self.premier_5s)>0:
            self.others.append(self.premier_5s[0])
            self.premier_5s = self.premier_5s[1:]
        for i in self.mandatories:
            self.points_total+=i.number
            self.tournaments_used.append(i)
            self.extra_tournaments-=1
        self.others = sorted(self.others, key=lambda points: points.number, reverse=True)
        for i in range(len(self.others)):
            if self.others[i].number==0:
                self.others = self.others[:i]
                break
        count = 0
        while count<self.extra_tournaments and count<len(self.others):
            self.points_total += self.others[count].number
            self.tournaments_used.append(self.others[count])
            count+=1
        self.extra_tournaments-=count
        self.tournaments_used = sorted(self.tournaments_used, key=lambda points: points.number, reverse=True)
        self.current_points = self.points_total

def substringBetween(string,sub1,sub2):
    sub = string.split(sub1,1)[1]
    sub = sub.split(sub2,1)[0]
    return sub.strip()

def get_points_breakdown(link):
    html = urllib.request.urlopen(link)
    soup = BeautifulSoup(html,'lxml')
    points_ytd = []

    singles = soup.find('div',{'class': "matchtype-singles"})
    matches = singles.findAll('div',{'class': "daySeq wta-table-data data-player-matches"})
    for i in range(len(matches)):
        string = matches[i].text
        tournament = string.split(',')[0].strip()
        level = substringBetween(string,'Level:','Prize')
        number = int(substringBetween(string,'+','Prize'))
        points_ytd.append(Points(level,tournament,number))
    
    return points_ytd

def save_players(number):
    r = glob.glob('players/*')
    for i in r:
        os.remove(i)
        
    req = Request('https://www.flashscore.com/tennis/rankings/wta-race/', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage,'lxml')
    
    page = soup.find('div',{'class': 'rankingTable__table'})
    odds = page.findAll('div',{'class': 'rankingTable__row rank-row odd'})
    evens = page.findAll('div',{'class': 'rankingTable__row rank-row even'})

    for i in range(number):
        if i%2==0:
            player = odds[int(i/2)]
        else:
            player = evens[int(i/2)]
        rank = int((player.find('div',{'class': 'rank-column-rank'}).text)[:-1])
        name = player.find('div',{'class': 'rank-column-player'}).text
        points = int(player.find('div',{'class': 'rank-column-points'}).text)
    
        for j in search(name, tld="co.in", num=10, stop=10, pause=2): 
            if j.startswith('https://www.wtatennis.com/players/player/'):
                link = j
                break
        player = Player(name,rank,get_points_breakdown(link))
        player.link = link
        #print(player.name+' '+str(player.rank)+' '+str(points))
        with open('players/'+name,'wb') as f:
            pickle.dump(player,f)

def load_players():
    directory = os.walk('players/')
    files = []
    for r, d, f in os.walk('players/'):
        for file in f:
            files.append(os.path.join(r, file))
    if os.path.isfile('players/.DS_Store'):
        files.remove('players/.DS_Store')

    rankings = []
    for file in files:
        with open(file,'rb') as f:
            player = pickle.load(f)
            rankings.append(player)

    rankings = sorted(rankings, key = lambda player: player.points_total, reverse = True)
    return rankings


grand_slam = [10,70,130,240,430,780,1300,2000]
premier_mandatory_128 = [10,35,65,120,215,390,650,1000]
premier_mandatory_128_bye = [10,65,120,215,390,650,1000]
premier_mandatory_64 = [10,65,120,215,390,650,1000]
premier_mandatory_64_bye = [10,120,215,390,650,1000]
premier_5 = [1,60,105,190,350,585,900]
premier_5_bye = [1,105,190,350,585,900]
premier_64 = [1,30,55,100,185,305,470]
premier_64_bye = [1,55,100,185,305,470]
premier_32 = [1,55,100,185,305,470]
premier_32_bye = [1,100,185,305,470]
international = [1,30,60,110,180,280]



#add a temp points total or something so that when match results come in, ranking table can be updated



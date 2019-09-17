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
from player_data import Points, Player, save_players, load_players
import player_data
from selenium import webdriver
from math import log2

#save_players(50)
rankings = load_players()

winner_loser_combos = []
with open('winner_loser','wb') as f:
            pickle.dump(winner_loser_combos,f)

def to_seven_bits(number):
    array = []
    while number>0:
        array.insert(0,number%2)
        number = int(number/2)
    while len(array)<8:
        array.insert(0,0)
    array = array[:-1]
    return array

class bracket_element:
    def __init__(self,player_name):
        self.opponent = None
        self.bracket_index = []
        self.qualifier = False
        self.lucky_loser = False
        self.bye = False
        self.lost_to = ''
        self.progressed = 0

        on_list = False
        for player in rankings:
            if player.name.startswith(player_name):
                self.player = player
                on_list = True
                break
        if not on_list:
            for player in rankings:
                if player.name.startswith(player_name.split('-')[0]):
                    self.player = player
                    on_list = True
                    break
        if not on_list:
            names = player_name.split(' ')
            for player in rankings:
                in_there = False
                for n in names:
                    if n not in player.name:
                        in_there = False
                        break
                    else:
                        in_there = True
                if in_there:
                    self.player = player
                    on_list = True
                    break
        if not on_list:
            self.player = Player(player_name,0,[])
    
    def lost(self):
        self.lost_to = self.opponent.name
    
    def won(self):
        self.bracket_index = self.bracket_index[:-1]
        self.progressed+=1
        self.player.points_total = self.player.points_possibilities[self.progressed]

class draw:
    def __init__(self,bracket,level):
        self.bracket = bracket
        self.level = level
        for i in self.bracket: #if opponent is BYE then change up the points possibilities
            if level=='Grand Slam':
                i.player.points_possibilities = [x+i.player.points_total for x in player_data.grand_slam]
            elif level=='Premier Mandatory': #r128 or r64
                draw_type = player_data.premier_mandatory_64
                if i.opponent.name=='BYE': ########
                    draw_type = player_data.premier_mandatory_64_bye
                    #i.bracket_index = i.bracket_index[:-1]
                i.player.points_possibilities = [x+i.player.points_total for x in draw_type]
            elif level=='Premier 5':
                draw_type = player_data.premier_5
                if i.opponent.name=='BYE':
                    draw_type = player_data.premier_5_bye
                    #i.bracket_index = i.bracket_index[:-1]
                if i.player.extra_tournaments>0:
                    i.player.points_possibilities = [x+i.player.points_total for x in draw_type]
                else:
                    smallest = i.player.others[0]
                    for j in i.player.tournaments_used:
                        if smallest.number>j.number and not j.level=='Grand Slam'                                                    and not j.level=='Premier Mandatory':
                            smallest = j
                    i.player.points_possibilities = [x+i.player.points_total-smallest.number for x in draw_type]
                    i.player.points_possibilities = [0 if x<0 else x for x in i.player.points_possibilities]
            elif level=='Premier': #r64 or r32
                draw_type = player_data.premier_32
                if i.opponent.name=='BYE':
                    draw_type = player_data.premier_32_bye
                    #i.bracket_index = i.bracket_index[:-1]
                if i.player.extra_tournaments>0:
                    i.player.points_possibilities = [x+i.player.points_total for x in draw_type]
                else:
                    tournies = i.player.tournaments_used
                    p_5s = []
                    for j in tournies:
                        if j.level=='Premier 5':
                            p_5s.append(j)
                    p_5s = sorted(p_5s, key = lambda points: points.number, reverse = True)
                    if len(p_5s)>2:
                        p_5s = p_5s[:2]
                    for j in p_5s:
                        tournies.remove(j)
                    smallest = None
                    for j in tournies:
                        if not j.level=='Grand Slam' and not j.level=='Premier Mandatory':
                            smallest = j
                            break
                    for j in tournies:
                        if smallest.number>j.number and not j.level=='Grand Slam'                                                    and not j.level=='Premier Mandatory':
                            smallest = j
                    i.player.points_possibilities = [x+i.player.points_total-smallest.number 
                                                     if x>smallest.number else i.player.points_total
                                                     for x in draw_type]
                    i.player.points_possibilities = [0 if x<0 else x for x in i.player.points_possibilities]
            elif level=='International':
                if i.player.extra_tournaments>0:
                    i.player.points_possibilities = [x+i.player.points_total for x in player_data.international]
                else:
                    tournies = i.player.tournaments_used
                    p_5s = []
                    for j in tournies:
                        if j.level=='Premier 5':
                            p_5s.append(j)
                    p_5s = sorted(p_5s, key = lambda points: points.number, reverse = True)
                    if len(p_5s)>2:
                        p_5s = p_5s[:2]
                    for j in p_5s:
                        tournies.remove(j)
                    smallest = None
                    for j in tournies:
                        if not j.level=='Grand Slam' and not j.level=='Premier Mandatory':
                            smallest = j
                            break
                    for j in tournies:
                        if smallest.number>j.number and not j.level=='Grand Slam'                                                    and not j.level=='Premier Mandatory':
                            smallest = j
                    i.player.points_possibilities = [x+i.player.points_total-smallest.number
                                                     if x>smallest.number else i.player.points_total
                                                     for x in player_data.international]
                    i.player.points_possibilities = [0 if x<0 else x for x in i.player.points_possibilities]
            if i.player.name=='BYE':
                i.player.points_possibilities = []
            else:
                i.player.current_points = i.player.points_possibilities[0]
        
    def update(self,winner_loser):
        #flashscore will load it as "Williams S." instead of "Williams Serena"
        no_opponent_yet = Player('',0,[])
        
        winner = winner_loser.split(',')[0]
        winner_corrected = ''
        winner_words = winner.split(' ')
        dash_check = winner_words[-1].split('-')[0]
        for i in range(len(winner_words)-1):
            if i==0:
                winner_corrected += winner_words[i]
            else:
                winner_corrected += ' '+winner_words[i]
        winner_corrected += ' '+dash_check
        loser = winner_loser.split(',')[1]
        for element in self.bracket:
            if element.player.name.startswith(winner_corrected):
                for el in self.bracket:
                    if element.opponent.name==el.player.name:
                        el.lost()
                        break
                element.won()
                opponent_there = False
                for el in self.bracket:
                    if element.player.name!=el.player.name and element.bracket_index==el.bracket_index:
                        element.opponent = el.player
                        el.opponent = element.player
                        opponent_there = True
                        break
                if not opponent_there:
                    element.opponent = no_opponent_yet
                break
                
def new_update(bracket,winner):
    no_opponent_yet = Player('',0,[])
    for element in bracket:
        if element.player.name.startswith(winner):
            for el in bracket:
                if element.opponent.name==el.player.name:
                    el.lost()
                    break
            element.won()
            opponent_there = False
            for el in bracket:
                if element.player.name!=el.player.name and element.bracket_index==el.bracket_index:
                    element.opponent = el.player
                    el.opponent = element.player
                    opponent_there = True
                    break
            if not opponent_there:
                element.opponent = no_opponent_yet
            break
        

def create_bracket(player_names,qualifiers,lucky_losers):
    bracket = []
    no_opponent_yet = Player('',0,[])
    for i in range(len(player_names)):
        bracket.append(bracket_element(player_names[i]))
        bracket[i].qualifier = qualifiers[i]
        bracket[i].lucky_loser = lucky_losers[i]
    for i in range(len(bracket)):
        bracket[i].bracket_index = to_seven_bits(i)
    for i in range(int(len(bracket)/2)):
        bracket[2*i].opponent = bracket[2*i+1].player
        bracket[2*i+1].opponent = bracket[2*i].player
    for i in range(len(bracket)):
        if bracket[i].opponent.name=='BYE':
            bracket[i].bracket_index = bracket[i].bracket_index[:-1]
            bracket[i].opponent = no_opponent_yet
    return bracket

def show_bracket(bracket):
    rounds = 7#log2(len(bracket))
    while rounds>=0:
        for i in range(len(bracket)):
            if len(bracket[i].bracket_index)<=rounds:
                print(bracket[i].player.name+': '+str(bracket[i].player.current_points)+' '+bracket[i].lost_to)
        print()
        rounds-=1

def load_draw(url,draw_size):
    browser = webdriver.Safari() #replace with .Firefox(), or with the browser of your choice
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    browser.close()
    innerHTML = innerHTML.split('round first-round')[1]
    innerHTML = innerHTML.split('</div></div></div></div></div></div>')[0]
    html = re.findall(r'width:(.*?)</span>', innerHTML)
    
    players = []
    for h in html:
        if h.split('>')[1]=='':
            players.append('BYE')
        else:
            players.append(h[9:].strip())  
    players = players[:draw_size]

    qualifiers = []
    lucky_losers = []
    for i in range(len(players)):
        qualifier = False
        lucky_loser = False
        if '(Q)' in players[i]:
            qualifier = True
        if '(LL)' in players[i]:
            lucky_loser = True
        qualifiers.append(qualifier)
        lucky_losers.append(lucky_loser)
        players[i] = players[i].split('.')[0]
    
    bracket = create_bracket(players,qualifiers,lucky_losers)
    d_raw = draw(bracket,'Premier 5')
    
    html = innerHTML.split('<span class="participant home')
    for h in range(len(html)):
        html[h] = html[h].split('Click')[0]
        html[h] = html[h].split('playoff')[0]
    html = html[1:]
    for h in html:
        if '179' in h:
            players = re.findall(r'179px;">(.*?)</span>', h)
            for i in range(len(players)):
                players[i] = players[i].split('.')[0]
                for j in range(len(players[i])):
                    index = len(players[i])-1-j
                    if players[i][index]==' ':
                        break
                    if players[i][index]=='-':
                        players[i] = players[i][:index]
                        break
            b1 = None
            b2 = None
            for i in range(len(players)):
                for b in d_raw.bracket:
                    if b.player.name.startswith(players[i]):
                        if i==0:
                            b1 = b.bracket_index
                        else:
                            b2 = b.bracket_index
            if b1==b2:
                if h.startswith(' winner'):
                    new_update(d_raw.bracket,players[0])
                else:
                    new_update(d_raw.bracket,players[1])
        elif '197' in h:
            players = re.findall(r'197px;">(.*?)</span>', h)
            for i in range(len(players)):
                players[i] = players[i].split('.')[0]
                for j in range(len(players[i])):
                    index = len(players[i])-1-j
                    if players[i][index]==' ':
                        break
                    if players[i][index]=='-':
                        players[i] = players[i][:index]
                        break
            if h.startswith(' winner'):
                new_update(d_raw.bracket,players[0])
            elif 'away winner' in h:
                new_update(d_raw.bracket,players[1])    
    '''...
    winners = re.findall(r'participant(.*?)playoff-box-result', innerHTML)
    winners = [element for item in winners for element in item.split('spacer mid nb')]
    winners = [element for item in winners for element in item.split('spacer con nb')]
    winners = [element for item in winners for element in item.split('cleaner')]
    #for i in range(len(winners)):
    #   winners[i] = winners[i].split(';">')[1].split('.')[0]
    with open('winner_loser','rb') as f:
                winner_loser_combos = pickle.load(f)
    for w in winners:
        players = re.findall(r';">(.*?)<', w)
        for i in range(len(players)):
            if players[i]=='':  #fix this, could byes be confused with players that don't have opponents yet?
                players[i]='BYE'
        if 'home winner' in w:
            winner_loser = players[0].split('.')[0]+','+players[1].split('.')[0]
            if winner_loser not in winner_loser_combos:
                winner_loser_combos.append(winner_loser)
                d_raw.update(winner_loser)
        elif 'away winner' in w:
            winner_loser = players[1].split('.')[0]+','+players[0].split('.')[0]
            if winner_loser not in winner_loser_combos:
                winner_loser_combos.append(winner_loser)
                d_raw.update(winner_loser)
        elif 'home' in w or 'away' in w:
            if players[0]=='BYE':
                winner_loser = players[1].split('.')[0]+','+players[0].split('.')[0]
                d_raw.update(winner_loser)
            elif players[1]=='BYE':
                winner_loser = players[0].split('.')[0]+','+players[1].split('.')[0]
                d_raw.update(winner_loser)
            else:
                winner_loser = players[0].split('.')[0]+','+players[1].split('.')[0]
        #print(winner_loser)
    with open('winner_loser','wb') as f:
                pickle.dump(winner_loser_combos,f)...'''and None
    
    return d_raw


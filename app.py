from flask import Flask, jsonify
from bs4 import BeautifulSoup 
import requests

app = Flask(__name__)

def for_outer_div(path):
    url =  "https://www.cricbuzz.com/cricket-match/live-scores" + path
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    outer_div = soup.find_all('div', class_="cb-col cb-col-100 cb-plyr-tbody cb-rank-hdr cb-lv-main")
    return outer_div

@app.route("/")
def live_score():
    outer_div = for_outer_div('/')
    score_dict = {}

    if (len(outer_div) == 0):
        print("There is no live match right now. Check back later.")
    else:
        for div in range(0, len(outer_div)):
            series = (outer_div[div].find('h2').text)
            match_list = outer_div[div].find_all('div', class_= "cb-mtch-lst cb-col cb-col-100 cb-tms-itm")

            for cont in range(0,len(match_list)):
                teams = match_list[cont].div.div.h3.text 
                match_type = match_list[cont].div.div.span.text
                score_card = match_list[cont].find('div', class_="cb-col-100 cb-col cb-schdl")
                link = "https://www.cricbuzz.com" + score_card.a['href']
                score = score_card.div.div.find_all('div', class_="cb-ovr-flo")
                team1, team2 = score[1].text, score[3].text
                score_t1, score_t2 = score[2].text, score[4].text
                status = score_card.find('div', class_="cb-text-live")

                score_dict[series] = {'Teams': teams, 'Match Type': match_type.replace("\xa0"," "), 'Link': link, "Score": {team1: score_t1, team2: score_t2}}
    
    return score_dict

@app.route("/upcoming-matches")
def upcoming_matches():
    outer_div = for_outer_div('/upcoming-matches')
    upcoming_dict = {}

    for div in range(0, len(outer_div)):
        series = (outer_div[div].find('h2').text)
        match_list = outer_div[div].find_all('div', class_= "cb-mtch-lst cb-col cb-col-100 cb-tms-itm")

        for cont in range(0,len(match_list)):
            teams = match_list[cont].div.div.h3.text 
            match_type = match_list[cont].div.div.span.text

            upcoming_dict[series] = {'Teams': teams, 'Match Type': match_type.replace("\xa0"," ")}
    
    return upcoming_dict


if __name__== "__main__":
    app.run(debug=True)

    

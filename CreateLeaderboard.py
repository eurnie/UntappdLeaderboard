#!/usr/bin/python3
print("Content-Type: text/html\n\n")
print("""<html>
<head>
<title>Untappd Leaderboard</title>
<style>
  table, th, td {
  border: 1px solid black;
  text-align: center;
  border-collapse: collapse;
}
</style>
</head>
<body>
""")

import re
import requests
import time

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

###########################
# Functions
###########################

def get_data_from_untappd(url):
    # Setting up and Making the Web Call
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        headers = {'User-Agent': user_agent}
        # Make web request for that URL and don't verify SSL/TLS certs
        response = requests.get(url, headers=headers, verify=False)
        return response.text

    except Exception as e:
        print('[!]   ERROR - Untappd issue: {}'.format(str(e)))
        exit(1)


def get_user_data(passed_user):
    # Parsing user information
    url = 'https://untappd.com/user/{}'.format(passed_user)
    resp = get_data_from_untappd(url)
    html_doc = BeautifulSoup(resp, 'html.parser')
    user1 = html_doc.find_all('span', 'stat')
    if user1:
        return user1

def print_leaderboard(title, user_data_list):
    if (title == 'Total Unique'):
        array_index = 2
    elif (title == 'Total Beers'):
        array_index = 1
    elif (title == 'Total Badges'):
        array_index = 3
    print("<h4>")
    print(title)
    print("""</h4>
        <table>
        <tr>
            <th>Ranking</th>
            <th>Naam</th>
            <th>Aantal</th>
        </tr>
        """)
    counter = 1
    rows = []
    for user_data in user_data_list:
        print("<tr><td>")
        print(str(counter) + ') </td>')
        print("<td>" + find_real_name(user_data[0]) + "</td>")
        print("<td>" + str(user_data[array_index]) + "</td>")
        print("</tr>")
        
        counter += 1
        
    print("</table>")

def find_real_name(nickname):
    if (nickname == 'eurniee'):
        return 'Arne Vermeulen'
    elif (nickname == 'BassieWouters'):
        return 'Sebastiaan Wouters'
    elif (nickname == 'Den_Henry'):
        return 'Hendrik Van Beersel'

###########################
# Start
###########################
def main(): 
    # Suppress HTTPS warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # Get user info
    user_list = ['eurniee', 'BassieWouters', 'Den_Henry']
    user_data_list = []

    for user in user_list:   
        user_data = get_user_data(user)
        user_data_list.append([user, int(format(user_data[0].text)), int(format(user_data[1].text)), int(format(user_data[2].text))])
    
    # Create leaderboard 'Total Unique'
    leaderboard_total_unique = sorted(user_data_list, key = lambda x: x[2], reverse = True)
    print_leaderboard('Total Unique', leaderboard_total_unique)
   
    # Create leaderboard 'Total Beers'
    leaderboard_total_beers = sorted(user_data_list, key = lambda x: x[1], reverse = True)
    print_leaderboard('Total Beers', leaderboard_total_beers)
    
    # Create leaderboard 'Total Badges'
    leaderboard_total_badges = sorted(user_data_list, key = lambda x: x[3], reverse = True)
    print_leaderboard('Total Badges', leaderboard_total_badges)


main()
print("""
</body>
</html>
""")

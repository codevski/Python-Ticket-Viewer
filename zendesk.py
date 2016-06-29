#!/usr/bin/env python3
#
#***********************************************************************
#* Python Ticket Viewer
#* Full Name: Saso Petrovski
#* Date: 27 June 2016
#***********************************************************************
# 

import unittest
import requests
import json
import sys
import datetime

"""
A system that allows to view tickets within the zendesk system via zendesk API calls.
"""

try:
  pyinput = raw_input
except NameError:
  pyinput = input

def pullData(newURL=None):
    if(newURL == None):
        url = 'https://saso.zendesk.com/api/v2/tickets.json?per_page=1'
    else:
        url = newURL
    # Set the request parameters
    #url = 'https://saso.zendesk.com/api/v2/tickets.json?per_page=1'
    user = 's@saso.io'
    pwd = 'ZendeskTest!23'
    
    # Do the HTTP get request
    response = requests.get(url, auth=(user, pwd))

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    
    print("Next Page", data['next_page']) # Testing Purpose
    print("Previous Page", data['previous_page']) # Testing Purpose
    
    
    return data
    

def main_menu():
    """
    This will control the main menu flow including error handling
    """
    
    main_menu = True
    while main_menu == True:
        main_option = pyinput("Type 'menu' to view options or 'quit' to exit\n").lower()
        
        if main_option == "menu":
            main_menu = False
            sub_menu()
            
        elif main_option == "quit":
            break
        
        else:
            print("error")

def sub_menu():
    """
    This will control the sub menu flow including error handling
    """
    # Init Vars
    sub_menu = True
    
    while sub_menu == True:
        print("""
        Select view options:
            * Press 1 to view all tickets
            * Press 2 to view a ticket
            * Type 'quit' to exit
        """)
        
        sub_option = pyinput("Pick option\n").lower()
        if sub_option == "1":
            # Set the request parameters
            listAll()
            
            sub_menu = True
        
        elif sub_option == "2":
            print("test2")
            sub_menu = True
            
        elif sub_option == "quit":
            print("Thanks for using the viewer. Goodbye")
            sub_menu = False
            
        else:
            print("Sorry I did not recognize your option. Please try again")

def listAll():
    # Mite need to make URL Global
    url = url = 'https://saso.zendesk.com/api/v2/tickets.json?per_page=1'
    data = pullData()
    tickets = data['tickets']
    
    while url:
        for all in tickets:
            dateTime = datetime.datetime.strftime(datetime.datetime.strptime( all['created_at'], "%Y-%m-%dT%H:%M:%SZ" ), "%d %b %Y %I:%m:%p")
            print('Ticket with subject', all['subject'], 'opened by', all['submitter_id'], "on", dateTime)
            
        if(data['next_page'] != None):
            if (data['previous_page'] != None):
                answer = input("Press 1 for next page or 2 for previous page\n")
                
                if (answer == "1"):
                    url = data['next_page']
                    #response = requests.get(url, auth=(user, pwd))
                    #data = response.json()
                    data = pullData(url)
                    tickets = data['tickets']
                
                elif (answer == "2"):
                    url = data['previous_page']
                    #response = requests.get(url, auth=(user, pwd))
                    #data = response.json()
                    data = pullData(url)
                    tickets = data['tickets']
                else:
                    break
            else:
                answer = input("Press 1 for next page\n")
                if (answer == "1"):
                    url = data['next_page']
                    #response = requests.get(url, auth=(user, pwd))
                    #data = response.json()
                    data = pullData(url)
                    tickets = data['tickets']
                
                else:
                    break
        else:
            break

def main():
    print("Welcome to the ticket viewer")
    main_menu()

    
main()

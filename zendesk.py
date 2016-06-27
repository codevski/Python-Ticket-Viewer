#!/usr/bin/env python3
#
#***********************************************************************
#* COSC1093_1510  - Scripting Language Programming
#* Semester 2 2016 Assignment #2
#* Full Name        : Saso Petrovski
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
            url = 'https://saso.zendesk.com/api/v2/tickets.json?per_page=1'
            user = 's@saso.io'
            pwd = 'MpsZendesk89!'
            
            # Do the HTTP get request
            response = requests.get(url, auth=(user, pwd))

            # Check for HTTP codes other than 200
            if response.status_code != 200:
                print('Status:', response.status_code, 'Problem with the request. Exiting.')
                exit()
            
            # Decode the JSON response into a dictionary and use the data
            data = response.json()
            
            # Example 1: Print the name of the first group in the list
            tickets = data['tickets']
            #subject = str(data['tickets'][0]['subject'])
            #submitter = str(data['tickets'][0]['submitter_id'])
            #created = str(data['tickets'][0]['created_at'])
            #print( 'id = ', data['tickets'][0]['id'] )
            #d = datetime.datetime.strptime( created, "%Y-%m-%dT%H:%M:%SZ" )
            #d2 = datetime.datetime.strftime(d, "%d %b %Y %I:%m:%p")
            #print('Ticket with subject', "'"+subject+"'", 'opened by', submitter, "on", d)
            #print('Ticket with subject', "'"+subject+"'", 'opened by', submitter, "on", d2)
            #print(data['next_page'])
            
            print("What is the next page", data['next_page'])
            while url:
                for all in tickets:
                    dateTime = datetime.datetime.strftime(datetime.datetime.strptime( all['created_at'], "%Y-%m-%dT%H:%M:%SZ" ), "%d %b %Y %I:%m:%p")
                    print('Ticket with subject', all['subject'], 'opened by', all['submitter_id'], "on", dateTime)
                url = data['next_page']
                print(url)
            
            """
            while url:
                data = response.json()
                for article in data['articles']:
                    print(article['title'])
                url = data['next_page']"""
            
            sub_menu = True
        
        elif sub_option == "2":
            print("test2")
            sub_menu = True
            
        elif sub_option == "quit":
            print("Thanks for using the viewer. Goodbye")
            sub_menu = False
            
        else:
            print("Sorry I did not recognize your option. Please try again")

def main():
    print("Welcome to the ticket viewer")
    main_menu()

    
main()

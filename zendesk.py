#!/usr/bin/env python3
#
#***********************************************************************
#* Python Ticket Viewer
#* Full Name: Saso Petrovski
#* Date: 27 June 2016
#***********************************************************************
# 

import unittest # For Testing
import requests
import json 
import sys
import datetime # Date time

"""
A system that allows to view tickets within the zendesk system via zendesk API calls.
"""

try:
  pyinput = raw_input
except NameError:
  pyinput = input

def findDataLen(tickets):
    big = 0
    for ticket in tickets:
        if(len(ticket['subject']) >= big):
            big = len(ticket['subject'])
    
    return big
    

def pullData(newURL=None, flags=None):
    if(newURL == None and flags == None):
        url = 'https://saso.zendesk.com/api/v2/tickets.json'
    elif (newURL == None):
        url = 'https://saso.zendesk.com/api/v2/tickets.json'+flags
    elif (newURL != None and flags != None):
        url = newURL+flags
    else:
        url = newURL
    # Set the request parameters
    #url = 'https://saso.zendesk.com/api/v2/tickets.json?per_page=1'
    user = 's@saso.io' + '/token'
    pwd = 'RgqBAtndgfzXQaOpwXJVEJmdWqVVN1UMJE3sMqim'

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
            findTicket()
            sub_menu = True
            
        elif sub_option == "quit":
            print("Thanks for using the viewer. Goodbye")
            sub_menu = False
            
        else:
            print("Sorry I did not recognize your option. Please try again")

def listAll():
    # Mite need to make URL Global
    #url = 'https://saso.zendesk.com/api/v2/tickets.json'
    data = pullData('https://saso.zendesk.com/api/v2/tickets.json', '?per_page=25')
    tickets = data['tickets']
    big = findDataLen(tickets)
    while data:
        print("{:<3} | {:<10} | {:<8}".format("ID", "Priority", "Type"), "%-*s" % (big, "| Subject "), " | {:<15} | {:<20} | {:<15}" .format("Opened by", "Created", "Status"))
        print("-"*3, "|", "-"*10, "|", "-"*8, "|", "-"*(big-1), "|", "-"*15, "|", "-"*20, "|", "-"*15)
        for ticket in tickets:
            dateTime = datetime.datetime.strftime(datetime.datetime.strptime( ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ" ), "%d %b %Y %I:%m:%p")
            #print(ticket['id'], ticket['priority'], ticket['type'], ticket['subject'], ticket['submitter_id'], dateTime, ticket['status'])
            print("{:<3} | {:<10} | {:<8}".format(ticket['id'], ticket['priority'], ticket['type']), "%-*s" % (big, "| Subject "), " | {:<15} | {:<15} | {:<15}" .format(ticket['submitter_id'], dateTime, ticket['status']))
            #print("{:<3} | {:<10} | {:<8} | {:<15} | {:<15} | {:<15} | {:<15}".format(ticket['id'], ticket['priority'], ticket['type'], ticket['subject'], ticket['submitter_id'], dateTime, ticket['status']))
            
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

def findTicket():
    aTicket = input('Enter Ticket Number:\n')
    data = pullData('https://saso.zendesk.com/api/v2/search.json?query=', aTicket)
    tickets = data['results']
    if(not tickets):
        print("No Tickets")
    else:
        big = findDataLen(tickets)
        print("{:<3} | {:<10} | {:<8}".format("ID", "Priority", "Type"), "%-*s" % (big, "| Subject "), " | {:<15} | {:<20} | {:<15}" .format("Opened by", "Created", "Status"))
        print("-"*3, "|", "-"*10, "|", "-"*8, "|", "-"*(big-1), "|", "-"*15, "|", "-"*20, "|", "-"*15)
        for ticket in tickets:
            dateTime = datetime.datetime.strftime(datetime.datetime.strptime( ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ" ), "%d %b %Y %I:%m:%p")
            print("{:<3} | {:<10} | {:<8}".format(ticket['id'], ticket['priority'], ticket['type']), "%-*s" % (big, "| Subject "), " | {:<15} | {:<15} | {:<15}" .format(ticket['submitter_id'], dateTime, ticket['status']))


def main():
    print("Welcome to the ticket viewer")
    main_menu()

    
main()

#!/usr/bin/env python3
#
#***********************************************************************
#* Python Ticket Viewer
#* Full Name: Saso Petrovski
#* Date: 4 July 2016
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

class zendesk(object):
    
    
    """
    Used to find total tickets
    """
    def counttotalTickets(self, tickets):
        count = 0
        for ticket in tickets:
            count = count + 1
            
        return count
    
    """
    Used to find longest subject to use for table printing
    """
    def findDataLen(self, tickets):
        big = 0
        for ticket in tickets:
            if(len(ticket['subject']) >= big):
                big = len(ticket['subject'])
        
        return big
        
    
    """
    Function to pull API data with flags provided
    """
    def pullData(self, newURL=None, flags=None):
        if(newURL == None and flags == None):
            url = 'https://saso.zendesk.com/api/v2/tickets.json'
        elif (newURL == None):
            url = 'https://saso.zendesk.com/api/v2/tickets.json'+flags
        elif (newURL != None and flags != None):
            url = newURL+flags
        else:
            url = newURL
        
        """
        Snippet from Zendesk API Docs
        """
        # Set the request parameters
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
        
        return data
    
    """
    Menu Option 1 - Listing all tickets. 25 Tickets per page
    """    
    def listAll(self):
        data = zendesk.pullData(self, 'https://saso.zendesk.com/api/v2/tickets.json', '?per_page=25')
        tickets = data['tickets']
        big = zendesk.findDataLen(self, tickets)
        totalTickets = zendesk.counttotalTickets(self, tickets)
        while data:
            print("{:<3} | {:<10} | {:<8}".format("ID", "Priority", "Type"), "%-*s" % (big+1, "| Subject "), " | {:<15} | {:<20} | {:<15}" .format("Opened by", "Created", "Status"))
            print("-"*3, "|", "-"*10, "|", "-"*8, "|", "-"*(big), "|", "-"*15, "|", "-"*20, "|", "-"*15)
            for ticket in tickets:
                dateTime = datetime.datetime.strftime(datetime.datetime.strptime( ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ" ), "%d %b %Y %I:%m:%p")
                print("{:<3} | {:<10} | {:<8} |".format(ticket['id'], ticket['priority'], ticket['type']), "%-*s" % (big, ticket['subject']), "| {:<15} | {:<15} | {:<15} " .format(ticket['submitter_id'], dateTime, ticket['status']))
    
            if(data['next_page'] != None):
                if (data['previous_page'] != None):
                    answer = input("Press 1 for next page or 2 for previous page\n")
                    
                    if (answer == "1"):
                        url = data['next_page']
                        data = zendesk.pullData(url)
                        tickets = data['tickets']
                    
                    elif (answer == "2"):
                        url = data['previous_page']
                        data = zendesk.pullData(url)
                        tickets = data['tickets']
                    else:
                        break
                else:
                    print("1 of ", totalTickets)
                    answer = input("Press 1 for next page\n")
                    if (answer == "1"):
                        url = data['next_page']
                        data = zendesk.pullData(url)
                        tickets = data['tickets']
                    
                    else:
                        break
            else:
                break
    
    """
    Menu Option 2 - Search for tickets
    """
    def findTicket(self):
        aTicket = input('Enter Ticket Number:\n')
        data = zendesk.pullData(self, 'https://saso.zendesk.com/api/v2/search.json?query=', aTicket)
        tickets = data['results']
        if(not tickets):
            print("No Tickets Found")
        else:
            big = zendesk.findDataLen(self, tickets)
            print("{:<3} | {:<10} | {:<8}".format("ID", "Priority", "Type"), "%-*s" % (big+1, "| Subject "), " | {:<15} | {:<20} | {:<15}" .format("Opened by", "Created", "Status"))
            print("-"*3, "|", "-"*10, "|", "-"*8, "|", "-"*(big), "|", "-"*15, "|", "-"*20, "|", "-"*15)
            for ticket in tickets:
                dateTime = datetime.datetime.strftime(datetime.datetime.strptime( ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ" ), "%d %b %Y %I:%m:%p")
                print("{:<3} | {:<10} | {:<8} |".format(ticket['id'], ticket['priority'], ticket['type']), "%-*s" % (big, ticket['subject']), "| {:<15} | {:<15} | {:<15} " .format(ticket['submitter_id'], dateTime, ticket['status']))
                
    """
    This will control the main menu flow including error handling
    """            
    def main_menu(self):
        main_menu = True
        while main_menu == True:
            main_option = input("Type 'menu' to view options or 'quit' to exit\n").lower()
            
            if main_option == "menu":
                main_menu = False
                zendesk.sub_menu(self)
                
            elif main_option == "quit":
                break
            
            else:
                print("error")
    
    """
    This will control the sub menu flow including error handling
    """
    def sub_menu(self):
        # Init Vars
        sub_menu = True
        
        while sub_menu == True:
            print("""
            Select view options:
                * Press 1 to view all tickets
                * Press 2 to view a ticket
                * Type 'quit' to exit
            """)
            
            sub_option = input("Pick option\n").lower()
            if sub_option == "1":
                # Set the request parameters
                zendesk.listAll(self)
                
                sub_menu = True
            
            elif sub_option == "2":
                zendesk.findTicket(self)
                zendesk.sub_menu = True
                
            elif sub_option == "quit":
                print("Thanks for using the viewer. Goodbye")
                sub_menu = False
                
            else:
                print("Sorry I did not recognize your option. Please try again")
                
"""
Unittesting Section [Not Completed]
"""
class TicketTest(unittest.TestCase):
    def setUp(self):
        # Setup Tickets
        self.test_tickets = []
        self.big = 20
        
        for num in range(10):
            #self.test_tickets = [{'id': num, 'priority': 'normal', 'type': 'problem', 'subject': 'Sample Subject '+ str(num), 'submitter_id': "11111111", 'datetime': '4 Jul 2016 02:06:PM', 'status': 'open'}]
            
            self.test_tickets.append({'id': num, 'priority': 'normal', 'type': 'problem', 'subject': 'Sample Subject '+ str(num), 'submitter_id': "11111111", 'datetime': '4 Jul 2016 02:06:PM', 'status': 'open'})

        pass
            
    def test_print_all(self):
        # print menu option 1
        print("Test Printing All Tickets")
        big = self.big
        tickets = self.test_tickets
        self.assertEquals(zendesk.listAll(self), None) 
        #print("{:<3} | {:<10} | {:<8}".format("ID", "Priority", "Type"), "%-*s" % (big+1, "| Subject "), " | {:<15} | {:<20} | {:<15}" .format("Opened by", "Created", "Status"))
        #print("-"*3, "|", "-"*10, "|", "-"*8, "|", "-"*(self.big), "|", "-"*15, "|", "-"*20, "|", "-"*15)

        #for ticket in tickets:
            #print("{:<3} | {:<10} | {:<8} |".format(ticket['id'], ticket['priority'], ticket['type']), "%-*s" % (big, ticket['subject']), "| {:<15} | {:<15} | {:<15} " .format(ticket['submitter_id'], ticket['datetime'], ticket['status']))
        pass
        
    def test_print_search(self):
        # print menu option 2
        print("Test Printing Searched Ticket 0")
        big = self.big
        tickets = self.test_tickets
        ticket = tickets[0]
        
        #self.assertTrue(zendesk.findTicket(self), None)
        
        pass
    
    
if __name__ == '__main__':
    unittest.main()
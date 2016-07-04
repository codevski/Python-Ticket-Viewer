#!/usr/bin/env python3
#
#***********************************************************************
#* Python Ticket Viewer
#* Full Name: Saso Petrovski
#* Date: 4 July 2016
#***********************************************************************
# 

import zendesk

zendesk = zendesk.zendesk()

def main():
    print("Welcome to the ticket viewer")
    zendesk.main_menu()
    
if __name__ == '__main__':
    main()
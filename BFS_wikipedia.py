# File: BFS_wikipedia.py
# Author: Jesse Pasanen 0545937
# Distributed Systems Final Project
# Sources:
# https://wikipedia.readthedocs.io/en/latest/code.html#api
# https://wikipedia.readthedocs.io/en/latest/quickstart.html


import wikipedia

def page_name_select(page_type):
    while(True):
        page_name = input(f"{page_type} page: ")
        if(len(page_name.strip()) > 0):
            break
        else:
            print(f"Please write the name of the {page_type} page.")
    return page_name

def page_select(page_type):
    while(True):
        page_name = page_name_select(page_type)
        pages = wikipedia.search(page_name, results=10)
        if(len(pages) == 0):
            print(f"No pages found with the search term {page_name}.")
            continue
        else:
            break

    print(f"\nPlease select the {page_type} page from the list: ")
    i = 1
    for page in pages:
        print(f"{i}. {page}")
        i+=1

    while(True):
        selection = input("Selection: ")
        if(not(selection.isdigit())):
            print(f"\nThe selection has to be a number between 1 and {len(pages)}.")
            continue
        if(len(selection.strip()) > 0 and 0 < int(selection) and int(selection) < len(pages)):
            break
        else:
            print(f"\nThe selection has to be a number between 1 and {len(pages)}.")
    return wikipedia.page(pages[int(selection) - 1], auto_suggest=False) #https://github.com/goldsmith/Wikipedia/issues/176


def main():
    print("Welcome!\nThis program finds the shortest path between two Wikipedia pages\nby searching through the links found on each Wikipedia page.")
    print("Start by searching for the Start page and the Goal page.\n")

    start_page = page_select("Start")
    goal_page = page_select("Goal")


    return 0

if __name__ == '__main__':
    main()

# EOF
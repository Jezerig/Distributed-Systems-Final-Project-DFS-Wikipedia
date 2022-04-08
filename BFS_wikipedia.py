# File: BFS_wikipedia.py
# Author: Jesse Pasanen 0545937
# Distributed Systems Final Project
# Sources:
# https://wikipedia.readthedocs.io/en/latest/code.html#api
# https://wikipedia.readthedocs.io/en/latest/quickstart.html
# https://github.com/goldsmith/Wikipedia/issues/176
# https://stackabuse.com/graphs-in-python-breadth-first-search-bfs-algorithm/
# https://stackoverflow.com/questions/44219288/should-i-bother-locking-the-queue-when-i-put-to-or-get-from-it
# https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
# https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution

from ast import Continue
from queue import Queue
import threading
import time
import wikipedia

def search_page_name(page_type): # selecting the search term
    while(True):
        page_name = input(f"\n{page_type} page: ")
        if(len(page_name.strip()) > 0):
            break
        else:
            print(f"Please write the name of the {page_type} page.")
    return page_name

def page_select(page_type): # selecting the spesific page from the list of search results
    while(True):
        page_name = search_page_name(page_type)
        pages = wikipedia.search(page_name, results=5)
        if(len(pages) == 0):
            print(f"No pages found with the search term '{page_name}'.")
            continue
        else:
            break

    print(f"\nPlease select the {page_type} page from the list: ")
    i = 1
    for page in pages:
        print(f"{i}. {page}")
        i+=1

    while(True):
        selection = input("\nSelection: ")
        if(not(selection.isdigit())):
            print(f"\nThe selection has to be a number between 1 and {len(pages)}.")
            continue
        if(len(selection.strip()) > 0 and 0 < int(selection) and int(selection) < len(pages)):
            selected_page = pages[int(selection) - 1]
            break
        else:
            print(f"\nThe selection has to be a number between 1 and {len(pages)}.")
            continue
    while(True):
        try:
            return wikipedia.page(selected_page, auto_suggest=False)
        except(wikipedia.PageError):
            print(f"Error with the page '{selected_page}'. Exiting...")
            exit(-1)
        except wikipedia.DisambiguationError as e:
            print(f"\nThe page '{selected_page}' created a Disambiguation Error due to it not being a spesific page.\nTry with one of the pages listed below.\n")
            print(e)
            selected_page = input(f"\n{page_type} page name: ")
            continue
        except wikipedia.WikipediaException:
            print("Error with the Wikipedia API. Exiting...")
            exit(-1)
            


def bfs(start_page, goal_page):
    visited = set()
    queue = Queue()

    start_node = start_page.title
    goal_node = goal_page.title

    queue.put(start_node)
    visited.add(start_node)

    parent = dict()
    parent[start_node] = None

    path_found = False
    
    while not queue.empty():
        current_node = queue.get()
        # print(current_node)
        if current_node == goal_node:
            path_found = True
            break
        # start_time = time.time()
        try:
            links = wikipedia.page(current_node, auto_suggest=False).links
        except(wikipedia.PageError, wikipedia.DisambiguationError):
            Continue
        # print(f"Wikipedia API response time: {round((time.time() - start_time), 3)} seconds.")
        for link in links:
            if link not in visited:
                queue.put(link)
                parent[link] = current_node
                visited.add(link)  
                if(link == goal_node):
                    path_found = True
        if(path_found):
            break
    path = []
    if path_found:
        path.append(goal_node)
        previous_node = goal_node
        while(parent[previous_node] is not None):
            path.append(parent[previous_node])
            previous_node = parent[previous_node]
        path.reverse()
    
    for node in path:
        if(node != path[-1]):
            print(f"{node} -> ", end="")
        else:
            print(node)
    return path


def main():
    print("\nWelcome!\n\nThis program finds the shortest path between two Wikipedia pages\nby searching through the links found on each Wikipedia page.")
    print("Start by searching for the Start page and the Goal page.")

    start_page = page_select("Start")
    goal_page = page_select("Goal")
    
    if(start_page == goal_page):
        print("The Start page and the Goal page are the same. Path length 0.")
        return 0
    start_time = time.time()
    bfs(start_page, goal_page)
    print(f"Search time: {round((time.time() - start_time), 3)} seconds.")
    return 0

if __name__ == '__main__':
    main()

# EOF
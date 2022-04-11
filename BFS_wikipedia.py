# File: BFS_wikipedia.py
# Author: Jesse Pasanen 0545937
# Distributed Systems Final Project
# Sources:
# https://wikipedia.readthedocs.io/en/latest/code.html#api
# https://wikipedia.readthedocs.io/en/latest/quickstart.html
# https://github.com/goldsmith/Wikipedia/issues/176
# https://stackabuse.com/graphs-in-python-breadth-first-search-bfs-algorithm/
# https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
# https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
# http://pymotw.com/2/threading/
# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
# https://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
# https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Lock_Objects_Acquire_Release.php

import threading
import time
import wikipedia
from queue import Queue # has locking built-in

THREAD_COUNT = 7
STOP_THREADS = False # global variable to tell the threads to stop: https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
EXIT_FLAG = False # global variable to tell the main function to exit

class VisitedPages():   # list for already visited pages with locking: https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Lock_Objects_Acquire_Release.php
    def __init__(self):
        self.lock = threading.Lock()
        self.visited = []

    def add_to_visited(self, page):
        self.lock.acquire()
        try:
          self.visited.append(page)
        finally:
            self.lock.release()

    def notVisited(self, page):
        self.lock.acquire()
        try:
            if page not in self.visited:
                self.visited.append(page)
                return True
            else:
                return False
        finally:
            self.lock.release()


class Parent(): # dictionary for parent-child relationship of nodes
    def __init__(self):
        self.lock = threading.Lock()
        self.parent = dict()

    def add_parent(self, current_page, link):
        self.lock.acquire()
        try:
            self.parent[link] = current_page
        finally:
            self.lock.release()
    
    def get_parent(self, page):
        return self.parent[page]


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

    print(f"\nPlease select the {page_type} page from the list of suggested pages: ")
    i = 1
    for page in pages:
        print(f"{i}. {page}")
        i+=1

    while(True): # selection from the list of pages
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

    while(True): # if the selected page provides an error then the user can type the name of the page freely
        try:
            return_page = wikipedia.page(selected_page, auto_suggest=False)
            print(f"\nSuccess. {page_type} page set as '{return_page.title}'.")
            return return_page
        except(wikipedia.PageError):
            print(f"Error with the page '{selected_page}'. Exiting...")
            exit(-1)
        except wikipedia.DisambiguationError as e: # prints a list of pages due to 'DisambiguationError'
            print(f"\nThe page '{selected_page}' created a Disambiguation Error due to it not being a spesific page.\nTry with one of the pages listed below.\n")
            print(e)
            selected_page = input(f"\n{page_type} page name: ")
            continue
        except wikipedia.WikipediaException:
            print("Error with the Wikipedia API. Exiting...")
            exit(-1)

# BFS search function with help from: https://stackabuse.com/graphs-in-python-breadth-first-search-bfs-algorithm/
# https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
def search(goal_page, visited, queue, parent, path_lock): 
    global STOP_THREADS
    path_found = False
    goal_node = goal_page.title

    while not STOP_THREADS: # loops until one of the threads sets the STOP_STHREADS variable as True
        if(queue.empty()): # Checks if new pages have been added to the queue. Used at the beginning when the first page and it's links have been read
            time.sleep(1)
            continue
        else:
            current_node = queue.get()

        if current_node == goal_node:
            path_found = True
            break

        # start_time = time.time()
        try: # Links within a page; skips pages that cause the errors below
            links = wikipedia.page(current_node, auto_suggest=False).links
        except(wikipedia.PageError, wikipedia.DisambiguationError):
            continue
        # print(f"'{current_node}' Wikipedia API response time: {round((time.time() - start_time), 3)} seconds ({threading.current_thread().name}).")
        
        for link in links: # searched through the links of the page
            if visited.notVisited(link):
                queue.put(link)
                parent.add_parent(current_node, link) 
                if(link == goal_node):
                    path_found = True
        
        if(path_found):
            break
        if(STOP_THREADS):
            break

    if path_found:
        path_lock.acquire()
        try:
            if(STOP_THREADS): # used to stop two threads from printing a path; first one to acquire lock executes the printing
                return
            STOP_THREADS = True
            shortest_path(goal_node, parent)
        finally:
            path_lock.release()
        

def shortest_path(goal_node, parent): # form the path and prints it
    global EXIT_FLAG

    path = []
    path.append(goal_node)
    previous_node = goal_node

    while(parent.get_parent(previous_node) is not None):
        path.append(parent.get_parent(previous_node))
        previous_node = parent.get_parent(previous_node)

    path.reverse()
    print(f"The shortest path with the length of {len(path) - 1} is: ")

    for node in path:
        if(node != path[-1]):
            print(f"{node} -> ", end="")
        else:
            print(node)

    EXIT_FLAG = True # tells the main function to exit


def main():
    print("\nWelcome!\n\nThis program finds the shortest path between two Wikipedia pages\nby searching through the links found on each Wikipedia page.")
    print("Start by searching for the Start page and the Goal page.")

    start_page = page_select("Start")
    goal_page = page_select("Goal")
    
    if(start_page == goal_page):
        print("The Start page and the Goal page are the same. Path length 0.")
        return 0
    
    print("\nSearching...\n")
    visited = VisitedPages()
    queue = Queue()
    parent = Parent()
    path_lock = threading.Lock()

    queue.put(start_page.title)
    visited.add_to_visited(start_page.title)
    parent.add_parent(None, start_page.title)

    start_time = time.time() # timer for search time

    threads_list = []
    for i in range(THREAD_COUNT): # creating threads with help from: http://pymotw.com/2/threading/
        try:
            thread = threading.Thread(target=search, args=(goal_page, visited, queue, parent, path_lock), name=f"Thread-{i}")
            thread.daemon = True
            thread.start()
            threads_list.append(thread)
        except:
            print("Fatal Error with threads")
            exit(-1)

    while(True): # loops until one of threads has printed the path
        try:
            time.sleep(0.1)
            if(EXIT_FLAG):
                print(f"\nSearch time: {round((time.time() - start_time), 3)} seconds")
                break
        except KeyboardInterrupt: # makes it possible to use KeyboardInterrupt while searching: https://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
            print("KeyboardInterrupt")
            exit(-1)
    return 0

if __name__ == '__main__':
    exit(main())

# EOF
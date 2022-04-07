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


from ast import Continue
import wikipedia
import threading
from queue import Queue
from collections import defaultdict

# class Node:
#     def __init__(self, value, neighbors=None):
#         self._value = value
#         if neighbors is None:
#             self._neighbors = []
#         else:
#             self._neighbors = neighbors

#     def has_neighbors(self):
#         if len(self._neighbors) == 0:
#             return False
#         return True
    
#     def add_neighbor(self, neighbor):
#         self._neighbors.append(neighbor)


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, node1, node2):
        self.graph[node1].append(node2)

    def bfs(self, start_page, goal_page):
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
            if current_node == goal_node:
                path_found = True
                break
            try:
                links = wikipedia.page(current_node, auto_suggest=False).links
            except(wikipedia.PageError, wikipedia.DisambiguationError):
                print(f"Skipped {current_node}.")
                Continue
            print(current_node)
            for link in links:
                self.add_edge(current_node, link)
                if link not in visited:
                    queue.put(link)
                    parent[link] = current_node
                    visited.add(link)
            # for next_node in self.graph[current_node]:
                

        path = []
        if path_found:
            path.append(goal_node)
            previous_node = goal_node
            while(parent[previous_node] is not None):
                path.append(parent[previous_node])
                previous_node = parent[previous_node]
            path.reverse()
        print(path)
        return path
        
    


def search_page_name(page_type): # selecting the search term
    while(True):
        page_name = input(f"{page_type} page: ")
        if(len(page_name.strip()) > 0):
            break
        else:
            print(f"Please write the name of the {page_type} page.")
    return page_name

def page_select(page_type): # selecting the spesific page from the list of search results
    while(True):
        page_name = search_page_name(page_type)
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
            print("")
            break
        else:
            print(f"\nThe selection has to be a number between 1 and {len(pages)}.")
    return wikipedia.page(pages[int(selection) - 1], auto_suggest=False)





def main():
    print("Welcome!\nThis program finds the shortest path between two Wikipedia pages\nby searching through the links found on each Wikipedia page.")
    print("Start by searching for the Start page and the Goal page.\n")

    start_page = page_select("Start")
    goal_page = page_select("Goal")
    
    if(start_page == goal_page):
        print("The Start page and the Goal page are the same. Path length 0.")
        return 0
    graph = Graph()
    graph.bfs(start_page, goal_page)


    return 0

if __name__ == '__main__':
    main()

# EOF
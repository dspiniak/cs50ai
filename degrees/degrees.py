import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)]+path
        print(f"new_path: {path}")

        for i in range(degrees):
            print(f"{i}")
            person1 = people[path[i][1]]["name"]
            print(f"person 1: {people[path[i][1]]['name']}")

            person2 = people[path[i+1][1]]["name"]
            print(f"person 2: {people[path[i+1][1]]['name']}")

            print(f"movie: {path[i+1][0]}")
            movie = movies[path[i+1][0]]["title"]

            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """  
    
    # Keep track of number of states explored
    num_explored = 0

    # Initialize frontier to just the starting position
    source = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(source)

    # Initialize an empty explored set
    explored = set()
    
    # Keep looping until solution found
    while True:
        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # If node is the goal, then we have a solution
        if node.state == target:
            movies = []
            people = []
            # path should be a list, in the form of [(1, 2), (3, 4)], where 1,2 is movie 1, person 2
            path = []
            while node.parent is not None:
                movies.append(node.action)
                people.append(node.state)
                node = node.parent
            # print(f"{movies}")
            movies.reverse()
            people.reverse()
            # need to build a list that contains tuple of movie, people
            path = list(zip(movies,people))
            print(f"path: {path}")

            return path

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        # # there's something weird here, action is a movie
        # the pattern is: person A, what movies? then find another person in that movie, then what persons in that movie
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    
    This returns all 
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()





# # Keep track of number
#     # initialize queue
#     queue = QueueFrontier()

#     #path is a dict of movies, person visited
#     path = []

#     # node = Node()
#     # node.parent = source
#     # node.state = source

#     # initialize queue with source
#     queue.add = source
#     explored = []

#     # We visit a node first, add all neighbours of that node, explore if the match target, then add neighbours of those nodes
#     neighbours = neighbors_for_person(source)
#     for i in range(neighbours):
#         queue.add = neighbours[i]
#         explored.append(neighbours[i])
#         if neighbours[i] == target
#             path = []
#     if neighbours == target:
#         return path
#     else: 
    
    


#     # If the frontier is empty, stop. There is no solution to the problem.
#     # Remove a node from the frontier. This is the node that will be considered.

#     # If the node contains the goal state, eturn the solution. Stop.

#     # Else. Expand the node (find all the new nodes that could be reached from this node), and add resulting nodes to the frontier.
#     # Add the current node to the explored set.

#     # explore space
#     # if explored all and no path, then no path

#     #define frontier
#         # frontier is movie, person - how to go around frontier could be within one movie (or not)
#     # starting at source person, find all movies the source starred in, using {stars}
#     # the action is a (movie, person)
#     # need to define a node
#         # state
#         # action, path, previously visited nodes
#     # for movie i, explore all j's
#     # if j = target return
#     # else start next node
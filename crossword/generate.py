import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # print(f"self.domains: {self.domains}")

        # enforce node consistency / remove values thar are inconsistent with word length
            # check each variable and remove words that don't match their length
        # for variable loop
            # for word loop
                # if word doesn't match length, remove
        for variable, words in self.domains.items():
            # print(f"variable: {variable}")
            words_copy = words.copy()
            for word in words_copy:
                # print(f"word: {word}, variable: {variable}, length: {variable.length}")
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
            
        # print(f"new self.domains: {self.domains}")

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # find if x is consistent with y:
            # get position of x and y, where variables cross using crossword.overlaps[x, y] that returns place i, j for overlap
        revised = False
        overlap = self.crossword.overlaps[x, y]
        # remove values from self.domains[x] that don't have value in domain of y
        # print(f"x.domain: {self.domains[x]}")
        domain_x = self.domains[x].copy()
        for word_x in domain_x:
            i = 0
            for word_y in self.domains[y]:
                if word_x[overlap[0]] == word_y[overlap[1]]: i += 1
            if i == 0:
                self.domains[x].remove(word_x)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # what's an arc here?
            # arcs are all variables that are connected between them
            # how to get all intersections between variables?
        if arcs is None:
            list = []
            # for each variable find neighbors and add arc in list
            for variable in self.domains:
                for neighbor in self.crossword.neighbors(variable):
                    list.append((variable, neighbor))
            # print(f"arcs is None, list: {list}")
        else:
            list = arcs
            # print(f"arcs NOT None, list: {list}")
        while list:
            x, y = list.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    list.append((z,x))
        return True
        # intuition
            # make quue with all arcs CHECK
                
            # revise that they are arc-consistent
            # if they are, revise: add some new arcs to be revise, in order to continue to enforce arc-consistency
        # function AC-3(csp):
        # □ queue = all arcs in csp
        # 	® while queue non-empty:
        # 		◊ (X, Y) = Dequeue(queue)
        # 		◊ if Revise(csp, X, Y):
        # 			} if size of X.domain == 0:
        # 				– return false
        # 			} for each Z in X.neighbors - {Y}:
        # 				– Enqueue(queue, (Z,X))
        # □ return true


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # print(f"ASSIGNMENT_COMPLETE, assignment is: {assignment}, domain length: {len(self.domains)}")
        if len(self.domains) == len(assignment):
            return True
        else:
            return False
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # print(f"CONSISTENT, assignment: {assignment}")
        if not assignment:
            # print(f"    returning empty assignment")
            return False
        
        # consistent = all values are distinct, every value is correct length, no conflicts between neighboring variables

        # CHECK VALUE LENGTH
        for variable, word in assignment.items():
            # print(f"variable: {variable}")
            if variable:
                if len(word) != variable.length:
                    return False
        
        # CHECK values are distinct
        seen_values = set()
        for value in assignment.values():
            if value in seen_values:
                return False
            seen_values.add(value)

        # CHECK conflict between neighboring variables
        list = []
        for variable in assignment:
                for neighbor in self.crossword.neighbors(variable):
                    if neighbor in assignment:
                        list.append((variable, neighbor))
        while list:
            x, y = list.pop()
            # print(f"x: {x}, y: {y}")
            overlap = self.crossword.overlaps[x, y]
            word_x = assignment[x]
            word_y = assignment[y]
            if word_x[overlap[0]] != word_y[overlap[1]]:
                return False

        # print(f"    returning consistent variables")
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # print(f"ORDER_DOMAIN_VALUES")
        # print(f"    var: {var}")
        # print(f"    assignment: {assignment}")
        # print(f"    domains: {self.domains}")

        values = list()
        values = self.domains[var]
        # print(f"    values: {values}")
        # what's domain of 'var'
        # how to order by number of values they rule out for neighboring unassigned variables
            # assigning var eliminates n possible choices for neighboring variables
            # how many choices are eliminated for neighboring variables by assigning var
            # if min_choices_eliminated > neighboring variable x: 
            # choosing a value will eliminate that value in how many
        values_to_choices_eliminated = dict()
        for value in values:
            # print(f"    value: {value}")
            values_eliminated = 0
            neighbors = self.crossword.neighbors(var)
            # print(f"    neighbors: {neighbors}")
            for neighbor in neighbors:
                # print(f"    looping neighbor: {neighbor}")
                if neighbor not in assignment:
                    if value in self.domains[neighbor]:
                        values_eliminated += 1
            values_to_choices_eliminated[value] = values_eliminated
        
        # print(f"    values_to_choices_eliminated: {values_to_choices_eliminated}")
        values = sorted(values_to_choices_eliminated, key=lambda item: item[1])
        return values    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        print(f"SELECT_UNASSIGNED_VARIABLE, \n  assignment: {assignment}")
        var_min_len = None
        min_len = float('inf')
        for variable, words in self.domains.items():
            if variable not in assignment:
                print(f"    looping variable: {variable}, words: {words}")
                print(f"    word count: {len(words)}, min_len: {min_len}")
                if len(words) < min_len:
                    var_min_len = variable
                    min_len = len(words)
                    print(f"    var_min_len: {var_min_len}")
                if len(words) == min_len and len(self.crossword.neighbors(variable)) < len (self.crossword.neighbors(var_min_len)):
                    var_min_len = variable
        # print(f"var_min_len: {var_min_len}")
        # what's highest degree? the one with less constraints
        print(f"    returning var_min_len: {var_min_len}")
        return var_min_len
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print(f"**BACKTRACK - assignment: {assignment}")
        # if assignment is complete
        assignment_complete = self.assignment_complete(assignment)
        print(f"    assignment_complete: {assignment_complete}")
        if assignment_complete:
            print(f"ASSIGNMENT IS COMPLETE")
            return assignment
        # var = select unassigned variables
        var = self.select_unassigned_variable(assignment)
        print(f"BACKTRACK    var: {var}")
        # for value in Domain-Values:
        order_domain_values = self.order_domain_values(var, assignment)
        print(f"    order_domain_values: {order_domain_values}")
        for value in order_domain_values:
            print(f"    **ENTERED loop, value: {value}")
            # if value consistent with assignment (doesn't violate constraints of current assignment)
                # what does it mean that the value doesn't violate constraints?
            new_assignment = assignment.copy()
            new_assignment[var] = value
            consistent = self.consistent(new_assignment)
            print(f"    consistent: {consistent}")
            if consistent:
                # add (var = value) to assignment
                assignment[var] = value
                print(f"    assignment[var]: {assignment[var]}")
                # result = backtrack(assignment,csp)
                result = self.backtrack(assignment)
                # if result != None:
                if result != None:
                    # return result
                    return result
                # remove (var = value) from assignment
                assignment.remove(var)
        # return failure
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

import sys
from unittest import result

from crossword import *
import random


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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        need_removal = {}

        for var in self.domains:
            for word in self.domains[var]: # list of possible words
                if len(word) != var.length:
                    if var not in need_removal:
                        need_removal[var] = [word]
                    else:
                        need_removal[var].append(word)
        
        # modify self.domain by removing word that does not satify the length condition
        for var in need_removal: 
            for word in need_removal[var]:
                self.domains[var].remove(word)
        


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        overlap = self.crossword.overlaps[x, y]

        if overlap is None: # no overlap, so no revision
            return False
        
        possible = False

        need_removal = [] # store words that need to be removed here, and remove them from domain later
        for word_x in self.domains[x]:
            for word_y in self.domains[y]:
                if word_x[overlap[0]] == word_y[overlap[1]]: # satisfies constraint
                    possible = True
            if not possible:
                need_removal.append(word_x)
        
        if len(need_removal) != 0:
            for word_x in need_removal:
                self.domains[x].remove(word_x) # only modify domain of x 
            return True

        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # if `arcs` is None, begin with initial list of all arcs
        if arcs is None:
            arcs = []
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
        
        while len(arcs) != 0:
            (x, y) = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                
                x_neighbors = self.crossword.neighbors(x)
                x_neighbors.remove(y)
                for z in x_neighbors:
                    arcs.append((z, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        crossword_var = self.domains

        # Every crossword variable is assigned to a value
        if len(assignment) == len(crossword_var):
            return True

        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = set()
        for var, value in assignment.items():
            # check if all values are distinct
            if value in values:
                return False
            values.add(value)
   
            # check if every value is the correct length
            if var.length != len(value):
                return False

            # check if there are no conflicts between neighboring variables
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if value[i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        cross_out = {}
        neighbors = self.crossword.neighbors(var)
        for value in self.domains[var]:
            cross_out[value] = 0

            for new_var in self.domains:
                if new_var == var or new_var in assignment:
                    continue
                if value in self.domains:
                    cross_out[value] += 1
        
        return sorted(cross_out, key=cross_out.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        potential_value = None

        for var in self.domains:
            # only need to choose variables that are currently not in assignment
            if var in assignment:
                continue
            
            # find variable with the fewest number of remaining values in its domain
            if potential_value is None or len(self.domains[var]) <  len(self.domains[potential_value]):
                potential_value = var
            
            elif len(self.domains[var]) == len(self.domains[potential_value]):
                if len(self.crossword.neighbors(potential_value)) < len(self.crossword.neighbors(var)):
                    potential_value = var
                if len(self.crossword.neighbors(potential_value)) == len(self.crossword.neighbors(var)):
                    potential_value = random.choice([potential_value, var])
            
        return potential_value


    def backtrack(self, assignment: dict):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)

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

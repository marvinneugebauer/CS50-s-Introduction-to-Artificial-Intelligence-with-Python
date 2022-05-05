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

        words = None

        for key in self.domains:
            words = self.domains[key].copy()
            break

        # filter out all words that have not the right length
        for key in self.domains:
            for word in words:
                if len(word) != key.length:
                    self.domains[key].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        if self.crossword.overlaps[x, y] is not None:  # Check if there is an overlapping between x and y
            index_x = self.crossword.overlaps[x, y][0]  # index of overlapping for x
            index_y = self.crossword.overlaps[x, y][1]  # index of overlapping for y

            words = self.domains[x].copy()

            for value_x in words:
                # Check if for all x in X.domain there is no y in Y.domain that satisfies constraint for (X, Y)
                condition = all((value_x[index_x] != value_y[index_y] and value_x != value_y)
                                for value_y in self.domains[y])
                # if there is no y in Y.domain that satisfies constraint for (X, Y) remove y from X.domain
                if condition:
                    self.domains[x].remove(value_x)
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

        queue = []  # Create queue, which is a list of all combinations between to different variables x and y
        if arcs is None:
            for x in self.domains:
                for y in self.domains:
                    if x == y:
                        continue
                    else:
                        queue.append((x, y))
        else:
            queue = arcs

        while len(queue) != 0:  # while list is not empty
            tuple_variables = queue.pop(0)

            if self.revise(tuple_variables[0], tuple_variables[1]):
                if len(self.domains[tuple_variables[0]]) == 0:
                    return False

                neighbor = self.crossword.neighbors(tuple_variables[0]) - {tuple_variables[1]}
                for z in neighbor:
                    queue.append((z, tuple_variables[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(x in assignment for x in self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        assignment_consistent = True

        # Enforcing word uniqueness, by filtering out all the words that are used as values in other variables before

        word_filter = set()

        for word in assignment:
            if assignment[word] in word_filter:
                assignment_consistent = False
            word_filter.add(assignment[word])

        # Check if each word in the values of assignment has the right length

        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                assignment_consistent = False

        # Check if there is a conflicts between neighboring variables

        for variable_x in assignment:
            neighbor_variables = self.crossword.neighbors(
                variable_x)  # Generate a set of all variables that are overlapping with a given x
            for variable_y in neighbor_variables:
                if variable_y in assignment:
                    index_x = self.crossword.overlaps[variable_x, variable_y][0]  # index of overlapping for x
                    index_y = self.crossword.overlaps[variable_x, variable_y][1]  # index of overlapping for y

                    for value_y in self.domains[variable_y]:
                        if assignment[variable_x][index_x] != value_y[index_y]:
                            assignment_consistent = False

        return assignment_consistent

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        words_values = []
        ordered_values = []

        for value_var in self.domains[var]:

            eliminated_choices = 0  # counts the eliminated choices that occurred by choosing a fix value for var
            for var_neighbor in self.crossword.neighbors(var):  # Iterate over the neighbor variables
                index_x = self.crossword.overlaps[var, var_neighbor][0]  # Getting the overlapping first and index of the neighbor variable
                index_y = self.crossword.overlaps[var, var_neighbor][1]

                for value_var_neighbor in self.domains[var_neighbor]:
                    if value_var[index_x] != value_var_neighbor[index_y]:
                        eliminated_choices += 1

            words_values.append((value_var, eliminated_choices))

        words_values = sorted(words_values, key=lambda y: y[1])

        for t in words_values:
            ordered_values.append(t[0])

        return ordered_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        """
        var_values_degrees is dictionary, which maps an unassigned variable to a tuple. The first element in 
        the tuple is the number of the remaining values and the second element is the degree.  
        """
        var_values_degrees = dict()

        for variable in self.domains:
            if variable not in assignment:  # consider all variables that are unassigned
                var_values_degrees[variable] = len(self.domains[variable]), len(self.crossword.neighbors(variable))

        # Sort var_values_degrees by the minimum remaining value heuristic.

        var_values_degrees = {k: var_values_degrees[k] for k in sorted(var_values_degrees, key=var_values_degrees.get)}

        # Sort var_values_degrees by the degree heuristic.

        minimum_values = sorted(var_values_degrees, key=lambda x: (-var_values_degrees[x][0], var_values_degrees[x][1]),
                                reverse=True)

        return minimum_values[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):  # Check if the assignment is complete
            return assignment

        # Get the "best" unassigned variable according to the value heuristic and degree heuristic

        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            new_assignment = assignment.copy()
            new_assignment[variable] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
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

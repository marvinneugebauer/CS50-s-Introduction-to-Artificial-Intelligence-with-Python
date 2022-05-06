import itertools
import random
from copy import deepcopy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines



class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            print("Sentence that was deceted as holding mines: ", self.cells," = ", self.count)
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0 and self.cells:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            print("delete")


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def update_sentence(self, knowledge):
        print("Inside update")
        for sentence in knowledge:
            if sentence.known_mines():
                print("Inside update: add mines")
                copy_set = deepcopy(sentence.known_mines())
                for mine in copy_set:
                    self.mark_mine(mine)
            elif sentence.known_safes():
                print("Inside update: add safes")
                copy_set = deepcopy(sentence.known_safes())
                for safe in copy_set:
                    self.mark_safe(safe)

    def delete (self, knowledge):
        print("inside delete")
        copy_knowledge = knowledge.copy()

        for sentence in copy_knowledge:
            if not sentence.cells:
                knowledge.remove(sentence)


    def create_new_knowledge(self, knowledge):
        print("Inside create new knowledge")
        List = []
        for sentence in knowledge:
            if sentence not in List and sentence.cells:
                if sentence.count <= len(sentence.cells):
                    List.append(sentence)
        knowledge = List
        new_knowledge1 = deepcopy(knowledge)
        knowledge_add = False
        print("Laege von knowledge", len(knowledge))
        print("Laege von new_knowledge1", len(new_knowledge1))
        for i in range(0, len(knowledge)):
            for j in range(0, len(knowledge)):
                if i != j:
                    if knowledge[i].cells.issubset(knowledge[j].cells) and knowledge[j].cells and knowledge[i].cells:
                        new_sentence1 = Sentence(
                            cells=knowledge[j].cells.difference(knowledge[i].cells),
                            count=knowledge[j].count - knowledge[i].count)
                        if new_sentence1 not in new_knowledge1 and new_sentence1.cells:
                            if len(new_sentence1.cells) >= new_sentence1.count:
                                print("add new sentence: ", new_sentence1.cells, new_sentence1.count)
                                new_knowledge1.append(new_sentence1)
                                knowledge_add = True
        if knowledge_add:
            self.update_sentence(new_knowledge1)
            for sentence in new_knowledge1:
                print(sentence.cells, " = ", sentence.count)
            return self.create_new_knowledge(new_knowledge1)
        else:
            print("Knowledge after: ")
            for sentence in new_knowledge1:
                print(sentence.cells, " = ", sentence.count)
            return new_knowledge1

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)  # zu 1)
        self.safes.add(cell)  # zu 2)

        """ 
        In the following, we determine all neighbor cells for a given cell. Then we create a new sentence by creating a  
        tuple that includes a set of all neighbor cells and the corrosponding 
        neighbor cells to a set as well as the corresponding count. 
        """

        if cell == (0, 0):  # above and leftmost
            new_sentence = Sentence(cells={(1, 0), (0, 1), (1, 1)}, count=count)
            self.knowledge.append(new_sentence)
        elif cell == (0, self.width - 1):  # above and rightmost
            new_sentence = Sentence(cells={(0, self.width - 2), (1, self.width - 2), (1, self.width - 1)}, count=count)
            self.knowledge.append(new_sentence)
        elif cell == (self.height - 1, 0):  # down and leftmost
            new_sentence = Sentence(cells={(self.height - 2, 0), (self.height - 2, 1), (self.height - 1, 1)},
                                    count=count)
            self.knowledge.append(new_sentence)
        elif cell == (self.height - 1, self.width - 1):  # down rightmost
            new_sentence = Sentence(cells={(self.height - 1, self.width - 2), (self.height - 2, self.width - 2),
                                           (self.height - 2, self.width - 1)}, count=count)
            self.knowledge.append(new_sentence)
        elif (cell[0] == 0) and (
                0 < cell[1] < self.width - 1):  # first row without the cells on the left and right edges
            new_sentence = Sentence(
                cells={(0, cell[1] - 1), (1, cell[1] - 1), (1, cell[1]), (1, cell[1] + 1), (0, cell[1] + 1)},
                count=count)
            self.knowledge.append(new_sentence)
        elif (cell[0] == self.height - 1) and (0 < cell[1] < self.width - 1):  # last row without the cells on the edge
            new_sentence = Sentence(
                cells={(self.height - 1, cell[1] - 1), (self.height - 2, cell[1] - 1), (self.height - 2, cell[1]),
                       (self.height - 2, cell[1] + 1), (self.height - 1, cell[1] + 1)}, count=count)
            self.knowledge.append(new_sentence)
        elif (0 < cell[0] < self.height - 1) and (cell[1] == 0):  # first column without the cells on the edge
            new_sentence = Sentence(
                cells={(cell[0] - 1, 0), (cell[0] - 1, 1), (cell[0], 1), (cell[0] + 1, 1), (cell[0] + 1, 0)},
                count=count)
            self.knowledge.append(new_sentence)
        elif (0 < cell[0] < self.height - 1) and (
                cell[1] == self.width - 1):  # first column without the cells on the edge
            new_sentence = Sentence(
                cells={(cell[0] - 1, self.width - 1), (cell[0] - 1, self.width - 2), (cell[0], self.width - 2),
                       (cell[0] + 1, self.width - 2), (cell[0] + 1, self.width - 1)}, count=count)
            self.knowledge.append(new_sentence)
        elif (0 < cell[0] < self.height - 1) and (0 < cell[1] < self.width - 1):
            new_sentence = Sentence(cells={(cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1), (cell[0] + 1, cell[1]),
                                           (cell[0] + 1, cell[1] + 1),
                                           (cell[0], cell[1] + 1), (cell[0] - 1, cell[1] + 1), (cell[0] - 1, cell[1]),
                                           (cell[0] - 1, cell[1] - 1)}, count=count)
            self.knowledge.append(new_sentence)
        print("_______________________________________")
        print("Knowlegdge before:", *self.knowledge)

        """
        1. We check if the cardinal number of the set of candidates in Sentence is equal to count. 
           If this is the case, we know that all of the candidates are mines and we add them to self.mines.

        2. We check if count is equal to zero. If this is the case, we know that all of the candidates are safes 
           and we add them to self.safes.
        """
        self.update_sentence(self.knowledge)



        """
        Delete every sentence form the format {}=0 out of the knowledge base.
        """
        print(bool(self.knowledge))
        copy_knowledge = self.knowledge.copy()

        for sentence in copy_knowledge:
            if not sentence.cells:
                self.knowledge.remove(sentence)

        print(bool(self.knowledge))


        for sentence in self.knowledge:
            copy_cells = deepcopy(sentence.cells)
            for cell in copy_cells:
                if cell in self.moves_made:
                    print("Hello")
                    sentence.cells.remove(cell)
                elif cell in self.mines:
                    print("Hello")
                    sentence.cells.remove(cell)
                    sentence.count  -= 1
                elif cell in self.safes:
                    print("Hello")
                    sentence.cells.remove(cell)
        self.delete(self.knowledge)


        self.update_sentence(self.knowledge)
        self.delete(self.knowledge)
        print("_______________________________________")
        #print("Knowlegdge before:")
        for sentence in self.knowledge:
            print (sentence.cells, " = ",sentence.count )
        print("_______________________________________")

        if len(self.knowledge) > 1:
            self.create_new_knowledge(self.knowledge)
        print("Mines that are known: ", self.mines)
        print("Safes that are known: ", self.safes)
        print("Made Moves: ", self.moves_made)
        print("_______________________________________")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                if ((i, j) in self.safes) and not ((i, j) in self.moves_made):
                    return i, j
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if not self.make_safe_move():
            candidates =[]
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if not ((i, j) in self.moves_made) and not ((i, j) in self.mines):
                        candidates.append((i, j))
            return random.choice(candidates)


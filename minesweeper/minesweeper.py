import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines (i row, j column)
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

        if len(self.cells) == self.count and self.count !=0:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check to see if cell is one of the cells included in the sentence. 
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # is the cell present in current sentence?
            # remove cell from sentence
        if cell in self.cells:
            self.cells.remove(cell)

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
    def get_safes(self):
        return self.safes
    
    def get_mines(self):
        return self.mines
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

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made - CHECK
            2) mark the cell as safe - CHECK
            3) add a new sentence to the AI's knowledge base - CHECK
                based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
                if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
                if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        print(f"pressed cell: {cell}")
        self.moves_made.add(cell)
        print(f"moves_made: {self.moves_made}")

        # 2) mark the cell as safe
        if cell not in self.safes:
            self.mark_safe(cell)
            print(f"marked as safe: {cell}")


        # 3) add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`

            # a)if neighbours are not in knowledge base, then neighbours = {count}
                # identify neighbours, ignore if cells are mines or safes       
                # create sentence
        neighbours = self.neighbour_cells(cell)
        neighbour_cells = neighbours[0]
        neighbour_mines = neighbours[1]
        print(f"neighbour cells: {neighbour_cells}")
        neighbour_cells -= self.mines
        neighbour_cells -= self.safes
        # don't add to knowledge if count = 0
        new_sentence = Sentence(neighbour_cells,count - neighbour_mines)
        self.knowledge.append(new_sentence)

        for sentence in self.knowledge:
            print(f"sentence: {sentence}")
        
        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
            # cells that are safe are those that: are known to be safe in sentence
            # cells that are mines are those that: items in sentence == count
        self.update_mines_and_safes()

        # 5) add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        self.infer_sentences()

        for sentence in self.knowledge:
            print(f"new sentences: {sentence}")

        self.update_mines_and_safes()

    def infer_sentences(self):
        # remove_sentences = []
        add_sentences = []
        print(f"entered loop")                                
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1.cells.issubset(sentence2.cells) and sentence1.cells != sentence2.cells and sentence1.count > 0 and sentence2.count > 0:
                    new_sentence = Sentence(sentence2.cells-sentence1.cells,sentence2.count-sentence1.count)
                    print(f"new sentence: {new_sentence}")
                    if new_sentence not in self.knowledge:
                        add_sentences.append(new_sentence)
                    # if sentence2 not in remove_sentences:
                    #     remove_sentences.append(sentence1)     
        
        # for sentence in remove_sentences:
        #     if sentence in self.knowledge:
        #         self.knowledge.remove(sentence)
                        
                # remove any empty sentences
        for sentence in self.knowledge:
            if sentence.cells == set():
                self.knowledge.remove(sentence)

        if add_sentences != []:
            for sentence in add_sentences:
                self.knowledge.append(sentence)
                print(f"appending add_sentences: {sentence}")

        return

    def update_mines_and_safes(self):
        for sentence in self.knowledge:
            # mark as safe
            safe_cells = sentence.known_safes()
            for safe_cell in safe_cells:
                self.mark_safe(safe_cell)
                print(f"marked as safe: {safe_cell}")
            # mark as mine
            mine_cells = sentence.known_mines()
            for mine_cell in mine_cells:
                self.mark_mine(mine_cell)
        print(f"new safes: {self.safes}")
        print(f"new mines: {self.mines}")
        return None

    def neighbour_cells(self, cell):
        neighbours = set()
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Update the cell itself in knowledge base
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i,j))
                    if (i,j) in self.mines:
                        count += 1
        return (neighbours, count)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # first, make moves within cells that are known to be safe
        # making a move is returning (i,j)

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # making a move is returning (i,j)
        # loop over all cells
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    self.moves_made.add((i,j))
                    return (i,j)
    

        
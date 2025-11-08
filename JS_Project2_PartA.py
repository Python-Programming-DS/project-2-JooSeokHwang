# --------------------------------------------------------------------
# Name : Joo Seok Hwang
# Date : 8 Nov 2025
# --------------------------------Note--------------------------------
# This is a program for Game of Tic-Tac-Toe played on 3 by 3 grid by two players.
# Whoever makes 3 marks in a row by row, column, or diagonal wins. 
# Please enjoy the game.
# --------------------------------------------------------------------


# define Board class to building the Game Board:
class Board:
     # this constructor initiates the board with empty cells
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
      
    # this method prints the board. Recall that class methods are functions
    def printBoard(self):
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # using a for-loop, it increments through the rows
        for i in range(3):
            print(f"| {i} |{self.c[i][0]:^3}|{self.c[i][1]:^3}|{self.c[i][2]:^3}|")
            print("-----------------")


# define Game class 
class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'X'

    # this method switches player (self.turn = 'X' or self.turn = 'O').
    def switchPlayer(self):
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
    
    # this method validates the user's entry
    # if valid return True, if invalid error msg and False 
    def validateEntry(self, row, col):
        # if row or column size is bigger than board size, print error msg and return False
        if row > len(self.board.c)-1 or col > len(self.board.c[0])-1:
            print("Invalid entry: try again.")
            print("Row & column numbers must be 0, 1, or 2.")
            return False

        # if the input grid position is not empty, print error msg and return False
        elif self.board.c[row][col] != " ":  
            print("That cell is already taken.")
            return False
    
        # if neither out of the board nor already taken, return True
        else:
            print("Thank you for your selection.")
            return True

    # this method checks if the board is full
    # return True if the board is full, otherwise, retern False 
    def checkFull(self):
        for row in self.board.c:
            if " " in row:
                return False
        return True   
    
    # this method checks for a winner
    # returns True when ‘X’ or ‘O’ becomes a winner, otherwise, returns False.
    def checkWin(self):
        winner = ""
        
        # check win by row by counting marks in each row
        for i in range(len(self.board.c)):
            if self.board.c[i].count(self.turn) == 3:
                winner = self.turn

        # create new lists on each column and check win by counting marks in the lists 
        # I find a simpler way using [row[i] for row in self.board.c], but leaving original code for record
        for i in range(len(self.board.c[0])):  
            col = []
            for j in range(len(self.board.c)):
                col.append(self.board.c[j][i])
            if col.count(self.turn) == 3:
                winner = self.turn
        
        # create new lists by each diagonal and check win by counting marks in the lists
        diag_to_right = []
        for i in range(len(self.board.c)):  # create a diagonal list toward right from [0,0] to [2,2]
            diag_to_right.append(self.board.c[i][i])
            if diag_to_right.count(self.turn) == 3:
                winner = self.turn
        diag_to_left = []
        for i in range(len(self.board.c)):  # create a diagonal list toward left from [0,-1] to [2,-3]
            diag_to_left.append(self.board.c[i][-(i+1)])
            if diag_to_left.count(self.turn) == 3:
                winner = self.turn

        if winner != "":
            return True
        else:
            return False

    # this method checks if the game has met an end condition by calling checkFull() and checkWin()
    # if the game ends, display the result and return True, or return False
    def ifEnd(self):
        # when there is a winner
        if self.checkWin() == True: 
            print(f"\n{self.turn} IS THE WINNER!!!")
            self.board.printBoard()
            return True
        # draw when the board is full but no winner
        elif self.checkFull() == True:  
            print("\nDRAW! NOBODY WINS!")
            self.board.printBoard()
            return True
        else : 
            return False

    # this method runs the tic-tac-toe game
    def playGame(self):      
        valid = False
        while valid == False:
            print(f"\n{self.turn}'s turn.")
            print(f"Where do you want your {self.turn} placed?")
            print("Please enter row number and column number separated by a comma.")
            grid = input()
            print(f"{"\033[F"}{"\033[K"}{"\033[31m"}{grid}{"\033[0m"}")  # highlight user input with red color
            grid = [int(x) for x in grid.split(",")]
            print(f"You have entered row #{grid[0]}\n\t  and column #{grid[1]}")
            valid = self.validateEntry(grid[0], grid[1])
        self.board.c[grid[0]][grid[1]] = self.turn


# main function
def main():
    # first initializes a variable to repeat the game
    game = Game()
    print("\nNew Game: X goes first.")
    game.board.printBoard()
    re = "y"

    # using while-loop that runs until the user says no for another game
    while re.lower() == "y":
        while True:
            game.playGame()
            if game.ifEnd() == True:
                print("\nAnother Game? Enter Y or y for yes.")
                re = input()
                print(f"{"\033[F"}{"\033[K"}{"\033[31m"}{re.upper()}{"\033[0m"}")  # highlight user input with red color
                if re.lower() == "y":
                    game = Game()
                    print("\nNew Game: X goes first.")
                    game.board.printBoard()
                else: break
            else:
                game.board.printBoard()
                game.switchPlayer()

    # goodbye message 
    print("\nThank you for playing!")
    
# call to main() function
if __name__ == "__main__":
    main()

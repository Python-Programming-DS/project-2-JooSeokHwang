# --------------------------------------------------------------------
# Name : Joo Seok Hwang
# Date : 8 Nov 2025
# --------------------------------Note--------------------------------
# This is a program for Game of Tic-Tac-Toe played on 3 by 3 grid by two players. 
# Whoever makes 3 marks in a row by row, column, or diagonal wins. 
# In this game, a human player plays against an AI trained by RandomForest algorithm.
# The computer player takes O and goes second.
# Please enjoy the game.
# --------------------------------------------------------------------

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# define Board class to building the Game Board:
class Board:
     # this constructor initiates the board with empty cells
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
            
    # this method prints the board
    def printBoard(self):
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # using a for-loop, print the board
        for i in range(3):
            print(f"| {i} |{self.c[i][0]:^3}|{self.c[i][1]:^3}|{self.c[i][2]:^3}|")
            print("-----------------")

# define Game class 
class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'X'

    # this method switches players by counting Xs and Os on the board 
    # suppose that X always goes first
    def switchPlayer(self, board):
        x = sum([cell == "X" for row in board for cell in row])
        o = sum([cell == "O" for row in board for cell in row]) 
        if x > o:
            return "O"
        else: return "X"
    
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

    # this method checks whether the board is full
    # return True if the board is full, otherwise, retern False 
    def checkFull(self, board):
        for row in board:
            if " " in row:
                return False
        return True   
    
    # this method checks for a winner
    # if there is a winner, return True and the winner, otherwise, return False and blank as a winner
    def checkWin(self, board):
        winner = ""

        for symbol in ["X", "O"]:
            # check win by row by counting symbol in a row
            for i in range(len(board)):
                if board[i].count(symbol) == 3:
                    winner = symbol

            # create new lists on each column and check win by counting marks in the lists 
            for i in range(len(board[0])):  
                col = [row[i] for row in board]
                if col.count(symbol) == 3:
                    winner = symbol
            
            # create new lists by each diagonal and check win by counting marks in the lists
            diag_to_right = []
            for i in range(len(board)):  # create a diagonal list toward right from [0,0] to [2,2]
                diag_to_right.append(board[i][i])
                if diag_to_right.count(symbol) == 3:
                    winner = symbol
            diag_to_left = []
            for i in range(len(board)):  # create a diagonal list toward left from [0,-1] to [2,-3]
                diag_to_left.append(board[i][-(i+1)])
                if diag_to_left.count(symbol) == 3:
                    winner = symbol

        if winner != "":
            return True, winner
        else:
            return False, winner

    # this method checks if the game has met an end condition by calling checkFull() and checkWin()
    # if the game ends, display the result and return True, or return False
    def ifEnd(self):
        ifwin, winner = self.checkWin(self.board.c)
        # if there is a winner
        if ifwin == True: 
            print(f"\n{winner} IS THE WINNER!!!")
            return True
        # draw when the board is full but no winner
        elif self.checkFull(self.board.c) == True:  
            print("\nDRAW! NOBODY WINS!")
            return True
        else: return False

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


# class for Randomforest model
# I seperate the model from the Game class to avoid retraining it each time the Game is called
class RF:
    def rf_train(self):
        url = r"C:\Users\JOO SEOK HWANG\Documents\Study\EGN5442 programming\Project\tictac_single.txt"
        ttt = pd.read_csv(url, sep=" ", header=None)
        y = ttt.iloc[:,9]
        x = ttt.drop(columns=[9])

        # I found the optimal RandomForest parameters using GridSearchCV
        # all scores were around 0.89
        model_rf = RandomForestClassifier(max_depth=30, max_features="log2", min_samples_leaf=1, n_estimators=400)
        model_rf.fit(x, y)

        return model_rf

    # get the current board status and return the next play
    def nextSoo(self, model, board):
        predict = model.predict([board])
        i = int(predict[0] // 3)
        j = int(predict[0] % 3)

        return (i,j)

    # convert the board of X, O to the list of 1, -1, 0
    def boardconverter(self, board):
        newb = []
        for row in board:
            for kan in row:
                if kan == "X":
                    i = 1
                elif kan == "O":
                    i = -1
                else: i = 0
                newb.append(i)
        return newb

        
def main():
    # initialize the game
    game = Game()
    rf = RF()
    model = rf.rf_train()
    print("\nNew Game: X goes first.")
    game.board.printBoard()
    re = "y"

    # using while-loop that runs until the user says no for another game
    # the computer player takes O and plays second
    while re.lower() == "y":
        while True:
            game.turn = game.switchPlayer(game.board.c)

            if game.turn == "X":
                game.playGame()
                
            else:
                print("\nO's turn.")
                board = rf.boardconverter(game.board.c)
                comCoor = rf.nextSoo(model, board)
                game.board.c[comCoor[0]][comCoor[1]] = "O"

            if game.ifEnd() == True:
                game.board.printBoard()
                print("\nAnother Game? Enter Y or y for yes.")
                re = input()
                print(f"{"\033[F"}{"\033[K"}{"\033[31m"}{re.upper()}{"\033[0m"}")  # highlight user input with red color
                if re.lower() == "y":
                    game = Game()
                    print("\nNew Game: X goes first.")
                else: break
            game.board.printBoard()

if __name__ == "__main__":
    main()
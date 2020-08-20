
import os
import copy
import time
#global variables
SCORE = {
        "Wins" : 0,
        "Loses": 0,
        "Ties" : 0,
        "Total Matches": 0}

########################################
############## Classes #################
########################################
class Player():
    def __init__(self, symbol, num=0):
        self.symbol = symbol
        self.num = num
        self.type = "human"
        self.val = -1

    def move(self, position, Board):
        Board.place(position, self.symbol)
    def getSymbol(self):
        return self.symbol
    def win(self):
        print("Player " + str(self.num) + " wins!")
    def lose(self):
        o = 1 if self.num == 2 else 2
        print("Player " + str(o) + " wins")
        print("Player " + str(self.num) + " loses... :( ")

aiPos = [-1, -1] #used in minimax for tracking best ai move
class AI(Player):
    def __init__(self):
        Player. __init__(self, "o")
        self.symbol = "o"
        self.opponent = None
        self.type = "ai"
        self.val = 1

    def setOpponent(self, Player):
        self.opponent = Player

    def move(self, Board):
        global aiPos
        aiPos = None
        minimax(Board, self, self.opponent)
        time.sleep(1)
        Board.place(aiPos, self.symbol)

################################
### minimax algorithm for AI ###
################################

def minimax(Board, Player, Opponent):
    global aiPos

    s = Player.getSymbol()
    x = Board.state(s) #1 if win, -1 if lose, 0 if tie, 2 if ongoing

    if  x != 2:
        return x * Player.val #1 if benefitting ai, -1 for human, 0 if tie

    #recursive step - check all possible moves
    #and pick move that reduces Player loss (flip side - maximizing gain)
    scores = []
    moves = []

    for i in range(0, 3):
        for j in range(0, 3):
            pos = [i,j]
            if Board.availableSpace(pos):
                #if the move is available, try it and keep score!
                newBoard = Board.copyAndPlace(pos, s)
                score = minimax(newBoard, Opponent, Player)
                scores.append(score)
                moves.append(pos)
    #from the ai's perspective, we want the most gain, the max score.
    #if it's the Player's turn, we want their loss (the min score).
    if Player.type == "ai":
        #max!
        #take the max score, and use it to get move
        i = scores.index(max(scores, default=0)) #index of max score
        aiPos = moves[i]
        return scores[i]
    else:
        #min!
        #Player is human, so we want the score that minimizes loss for the AI
        j = scores.index(min(scores, default=0))
        aiPos = moves[j]
        return scores[j]

class Board():
    def __init__(self):
        row = ["#", "#", "#"]
        self.board = []
        for i in range(0, 3):
            self.board.append(list(row)) #append a clone of row (so no shared memory)

    def getBoard(self):
        return self.board

    def copy(self):
        return copy.deepcopy(self)

    def availableSpace(self, position):
        x = position[0]
        y = position[1]
        if (self.board[x][y] == "#"):
            return True
        return False

    def place(self, position, symbol):
        x = position[0]
        y = position[1]
        if self.availableSpace(position):
            self.board[x][y] = symbol
        else:
            print("That's taken! Please choose a different spot.")
            p = input("Pick a position.")
            newPos = parseInput(p)
            self.place(newPos, symbol)

    def copyAndPlace(self, position, symbol):
        #only to be used in minimax
        b = self.copy() #hardcopy
        b.place(position, symbol)
        return b

    def isFull(self):
        anyHashSymbols = any("#" in row for row in self.board) #find out if there are any # left in board?
        return not anyHashSymbols

    def state(self, winSymbol):
        #tie (0), win (1), or lose (-1)
        s = winSymbol
        l = "x" if s == "o" else "o"
        winState = [s, s, s]
        loseState = [l, l, l]
        row1 = self.board[0]
        row2 = self.board[1]
        row3 = self.board[2]
        col1 = [self.board[0][0], self.board[1][0], self.board[2][0]]
        col2 = [self.board[0][1], self.board[1][1], self.board[2][1]]
        col3 = [self.board[0][2], self.board[1][2], self.board[2][2]]
        diagonal1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
        diagonal2 = [self.board[0][2], self.board[1][1], self.board[2][0]]

        if winState == row1 or winState == row2 or winState == row3 or winState == col1 or winState == col2 or winState == col3 or winState == diagonal1 or winState == diagonal2:
            return 1

        if loseState == row1 or loseState == row2 or loseState == row3 or loseState == col1 or loseState == col2 or loseState == col3 or loseState == diagonal1 or loseState == diagonal2:
            return -1
        if self.isFull():
            return 0 #tie
        return 2

    def checkWin(self, Player):
        global SCORE
        global playing
        s = Player.getSymbol()
        state = board.state(s)

        if state == 0:
            print("it's a tie!")
            playing = playAgain()
            SCORE["Ties"] += 1
            return 0

        elif state == 1:
            if Player.type == "human":
                Player.win()
                SCORE["Wins"] += 1
            if Player.type == "ai":
                print("The AI wins!")
                SCORE["Loses"] += 1
            playing = playAgain()
            return 1

        elif state == -1:
            if Player.type == "human":
                Player.lose()
                SCORE["Loses"] += 1
            if Player.type == "ai":
                print("You beat the AI!")
                SCORE["Wins"] += 1
            playing = playAgain()
            return -1
        else:
            return 2 #do nothing if no win

    def display(self):
        #print the board
        print("")
        print("")
        for i in range(0, 3):
            row = "       "
            for j in range(0, 3):
                row += self.board[i][j]
                if j != 2:
                    row += " | "
            print(row)
            if i != 2:
                print("       -----------")
        print("")
        print("")

########################################
############## Game Setup ##############
########################################
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def playAgain():
    while(True):
        print("")
        print("")
        play_again = input("Would you like to play again? yes or no")
        if play_again.lower() == "yes" or play_again.lower() == "ok" or play_again.lower() == "okay" or play_again.lower() == "y":
            return True
        elif play_again.lower() == 'no' or play_again.lower() == "n":
            return False
        else:
            print("What did you say? Want to play again? I won't judge.")

def parseInput(input):
    #breaks on non ints
    pos = input.split (",")
    pos = [int(i)-1 for i in pos] #subtract 1 for 0-indexing
    return pos

def playerMove(Player):
    p1 = input("Pick a position.")
    p1Pos = parseInput(p1)
    Player.move(p1Pos, board)
    board.display()
    result = board.checkWin(Player)
    return result

def aiMove(AI):
    move = AI.move(board)
    board.display()
    result = board.checkWin(AI)
    return result


tab = "       "
########################################
############## The Game ################
########################################

print("")
print(tab + "Welcome to this humble tic-tac-toe game,")
print(tab + "coded in Python by me, Atreides.")
input(tab + "Ready to begin? (Press Enter)")
print("")

playing = True
while(playing):
    clear()
    print("")

    #pick between ai or 2 player game
    x = input(tab + "One (1) player, or two (2)?")
    #x = 1
    #if 1, then play against the AI
    if int(x) == 1:
        print(tab + "pick a pos by row, col.")
        print(tab + "Begin!")
        SCORE["Total Matches"] +=1
        player1 = Player("x")
        ai = AI()
        ai.setOpponent(player1)
        board = Board()
        board.display()
        inProgress = True
        while(inProgress):
            print(tab + "Player 1, you're up!")
            p1Move = playerMove(player1)
            if p1Move == 1 or p1Move == -1 or p1Move == 0:
                inProgress = False
                continue
            print(tab + "AI's turn!")
            aiMoveResult = aiMove(ai)
            if aiMoveResult == 1 or aiMoveResult == -1 or aiMoveResult == 0:
                inProgress = False
                continue


    #if 2, commence with two-player mode
    else:
        print(tab + "pick a pos by row, col.")
        print(tab + "Begin!")
        SCORE["Total Matches"] +=1

        #create board, player(s)
        board = Board()
        board.display()
        player1 = Player("x", 1)
        player2 = Player("o", 2)
        inProgress = True
        while(inProgress):
            #player 1 move
            print(tab + "Player 1, you're up!")
            p1Move = playerMove(player1)
            if p1Move == 1 or p1Move == -1 or p1Move == 0:
                inProgress = False
                continue

            #player 2 move
            print(tab + "Player 2, it's your turn!")
            p2Move = playerMove(player2)
            if p2Move == 1 or p2Move == -1 or p2Move == 0:
                inProgress = False
                continue

print("Thanks for playing!")
print("Stats:")
print(SCORE)

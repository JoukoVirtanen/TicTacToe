import random

X=0
O=1
BLANK=2

HUMAN=0
COMPUTER=1

X_WIN=0
O_WIN=1
DRAW=2
ON_GOING=3
UNKNOWN=666

def playerNumToStr(num):
    if num==X:
        return "X"
    if num==O:
        return "O"
    return " "

def switchPlayer(player):
    if player==X:
        return O
    return X

def getPlayer(num):
    """
    Both player X and player O can be a human or computer.
    Enter H for human and C for computer.
    """
    player=""
    while (not player=="H") and (not player=="C"):
        player=raw_input("Player "+str(num)+". Enter H for human C for computer: ")
        if (not player=="H") and (not player=="C"):
            print "You did not enter a valid input"
        if player=="H":
            return HUMAN
        elif player=="C":
            return COMPUTER

def isStrInt(num):
    return str(int(num))==num

class BoardClass:
    def __init__(self, size):
        self.board=['?']*size
        self.players=[HUMAN, HUMAN]
        for idx in range(size):
            temp=[BLANK]*size
            self.board[idx]=temp

    def __str__(self):
        size=len(self.board)
        str_out=""
        for row in range(size):
            str_out+=str(size-row)
            for col in range(size):
                str_out+=playerNumToStr(self.board[row][col])
            str_out+="\r\n"

        str_out+=" "
        for row in range(size):
            str_out+=(str(row+1))
        str_out+="\r\n";

        return str_out

    def getPlayers(self):
        self.players[0]=getPlayer(1)
        self.players[1]=getPlayer(2)

    def isValidMove(self, move):
        size=len(self.board)
        row=move[0]
        col=move[1]
        if row<0 or row>=size or col<0 or col>=size:
            return False
            print "Your move is off the board"
        if not self.board[row][col]==BLANK:
            return False
            print "That square is not blank"
        return True
                
    def getMoveHuman(self):
        """
        The move is given as two integers separated by a space.
        The first integer is the column. The second integer is the row.
        """
        invalid=True
        size=len(self.board)
        while invalid:
            invalid=False
            move=raw_input("Enter your move: ")
            parts=move.split(" ")
            if not len(parts)==2:
                invalid=True
                print("Your input is not in two parts")
            if (not invalid) and ((not isStrInt(parts[0])) or (not isStrInt(parts[1]))):
                invalid=True
                print("Your input does not consist of two integers")
            row=size-int(parts[1])
            col=int(parts[0])-1
            if not self.isValidMove([row, col]):
                invalid=True
            if invalid:
                print("You did not input a valid move")
                                 
        return [row, col]
                                
    def updateGame(self, move, player):
        """
        Sets the square selected by the player to an X or an O.
        """
        if self.isValidMove(move):
            self.board[move[0]][move[1]]=player
        else:
            print("That is not a valid move")

    def isRowWin(self):
        """
        Has a player won by controlling a row
        """
        size=len(self.board)
        for row in range(size):
            count=[0]*3
            for col in range(size):
                count[self.board[row][col]]+=1
            if count[X]==size:
                return X_WIN
            if count[O]==size:
                return O_WIN

        return UNKNOWN

    def isColWin(self):
        """
        Has a player won by controlling a column
        """
        size=len(self.board)
        for col in range(size):
            count=[0]*3
            for row in range(size):
                count[self.board[row][col]]+=1
            if count[X]==size:
                return X_WIN
            if count[O]==size:
                return O_WIN

        return UNKNOWN

    def isDiagWin(self):
        """
        Has a player won by controlling a diagonal
        """
        size=len(self.board)
        count=[0]*3
        for i in range(size):
            count[self.board[i][i]]+=1
        if count[X]==size:
            return X_WIN
        if count[O]==size:
            return O_WIN

        count=[0]*3
        for i in range(size):
            count[self.board[i][size-1-i]]+=1
        if count[X]==size:
            return X_WIN
        if count[O]==size:
            return O_WIN

        return UNKNOWN

    def isDraw(self):
        """
        Is the game a draw? If all squares are occupied the game is a draw.
        """
        size=len(self.board)
        for row in range(size):
            for col in range(size):
                if self.board[row][col]==BLANK:
                    return False

        return True

    def getGameState(self):
        """
        Has the game been won by X, won by O, a draw, or still going?
        """
        rowWin=self.isRowWin()
        if rowWin==O_WIN or rowWin==X_WIN:
            return rowWin
        colWin=self.isColWin()
        if colWin==O_WIN or colWin==X_WIN:
            return colWin
        diagWin=self.isDiagWin()
        if diagWin==O_WIN or diagWin==X_WIN:
            return diagWin
        
        if self.isDraw():
            return DRAW
        
        return ON_GOING

        self.board=['?']*size
        self.players=[HUMAN, HUMAN]
        for idx in range(size):
            temp=[BLANK]*size
            self.board[idx]=temp

    def copyBoard(self):
        """
        Duplicates the game
        """
        size=len(self.board)
        copy_board=BoardClass(size)
        size=len(self.board)
        for row in range(size):
            for col in range(size):
                copy_board.board[row][col]=self.board[row][col]
        copy_board.players[X]=self.players[X]
        copy_board.players[0]=self.players[O]

        return copy_board
            

    def getMoveComputer(self, player):
        """
        The AI for the computer. The computer makes a move based on a depth first search.
        """
        game_state=self.getGameState()
        if not game_state==ON_GOING:
            return ([0, 0], game_state)
        draws=[]
        losses=[]
        other_player=switchPlayer(player)
        size=len(self.board)
        for row in range(size):
            for col in range(size):
                if self.board[row][col]==BLANK:
                    self.board[row][col]=player
                    (move, game_state)=self.getMoveComputer(other_player)
                    self.board[row][col]=BLANK
                    if (game_state==X_WIN and player==X) or (game_state==O_WIN and player==O):
                        return ([row, col], game_state)
                    if (game_state==X_WIN and player==O) or (game_state==O_WIN and player==X):
                        losses.append([row, col])
                    if game_state==DRAW:
                        draws.append([row, col])

        if len(draws)>0:
            move=random.choice(draws)
            return (move, DRAW)
        if len(losses)>0:
            move=random.choice(losses)
            if player==X:
                game_state=O_WIN
            else:
                game_state=X_WIN
                
            return (move, game_state)

        return ([UNKNOWN, UNKNOWN], UNKNOWN)

    def playGame(self):
        """
        Get the move from one player. Record the move.
        Get the next move from the next player.
        Repeate until the game is finished.
        """
        print(self)
        game_state=ON_GOING
        current_player=X
        while game_state==ON_GOING:
            if self.players[current_player]==HUMAN:
                move=self.getMoveHuman()
            else:
                (move, game_state)=self.getMoveComputer(current_player)
            self.updateGame(move, current_player)
            current_player=switchPlayer(current_player)
            print(self)
            game_state=self.getGameState()

        printResult(game_state)

def printResult(game_state):
    """
    What is the state of the game?
    """
    if game_state==X_WIN:
        print "X won the game"
    elif game_state==O_WIN:
        print "O won the game"
    elif game_state==DRAW:
        print "The game is a draw"
    elif game_state==ON_GOING:
        print "The game is still ongoing"
    else:
        print "I don't know what is going on"

def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def strToBool(s):
    return s[0]=="Y" or s[0]=="y"

def printIntro():
    intro="""
    **********************************************************
    *This is an ASCII version of TicTacToe.                  *
    *Both X and O can be either a human or a computer.       *
    *To enter your move type the column number of your move, *
    *a space, and the row number of your move.               *
    *                                                        *
    *Created by Jouko Virtanen in 2018                       *
    **********************************************************
    """
    print intro

printIntro()

while True:
    game=BoardClass(3)
    game.getPlayers()
    game.playGame()
    play_again=raw_input("Play again? (Y/N) ")
    if not strToBool(play_again):
        break


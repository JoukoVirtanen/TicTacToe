import random

from Tkinter import *
import tkFont

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

class MainApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container=Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames={}
        page_name=simpleapp_tk.__name__
        frame=simpleapp_tk(parent=container, controller=self)
        self.frames[page_name]=frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("simpleapp_tk")

    def show_frame(self, page_name):
        frame=self.frames[page_name]
        frame.update
        frame.tkraise()

class simpleapp_tk(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller=controller
        self.parent=parent
        self.game=BoardClass(3)

        self.grid()

        helv36=tkFont.Font(family='Helvetica', size=36, weight='bold')
        w=3

        self.player1Label=Label(self, text="Player1: ")
        self.player1Label.grid(column=0,row=0)

        self.var1=StringVar(self)
        self.var1.set("Human")
        options=["Human", "Computer"]
        self.player1DropDown=OptionMenu(self, self.var1, *options)
        self.player1DropDown.grid(column=1,row=0)


        self.player1Labe2=Label(self, text="Player2: ")
        self.player1Labe2.grid(column=0,row=1)

        self.var2=StringVar(self)
        self.var2.set("Human")
        self.player2DropDown=OptionMenu(self, self.var2, *options)
        self.player2DropDown.grid(column=1,row=1)

        action=lambda: self.newGame()
        self.newGameButton=Button(self, text="New Game", command=action)
        self.newGameButton.grid(column=2, row=0, rowspan=2)
        

        self.buttons=['?']*3
        self.btn_text=['?']*3
        for i in range(3):
            self.buttons[i]=['?']*3
            self.btn_text[i]=['?']*3

        for row in range(3):
            for col in range(3):
                self.btn_text[row][col]=StringVar() 
                action=lambda x=row, y=col: self.onButtonClick(x, y)
                self.buttons[row][col]=Button(self, textvariable=self.btn_text[row][col], width=w, font=helv36, command=action)
                self.buttons[row][col].grid(column=col, row=row+2)

        self.gameStateLabelVar=StringVar()
        self.gameStateLabel=Label(self, textvariable=self.gameStateLabelVar, font=helv36, anchor="w")
        self.gameStateLabel.grid(column=0, row=5, columnspan=3, sticky='EW')
        self.gameStateLabelVar.set(u"")

        self.update()

    def makeComputerMove(self):
        (move, temp_game_state)=self.game.getMoveComputer(self.game.current_player)
        self.game.updateGame(move, self.game.current_player)
        self.btn_text[move[0]][move[1]].set(" "+playerNumToStr(self.game.current_player)+" ")
        self.game.current_player=switchPlayer(self.game.current_player)
        game_state=self.game.getGameState()

        return game_state

    def onButtonClick(self, row, col):
        game_state=self.game.getGameState()
        if game_state==ON_GOING and self.game.board[row][col]==BLANK and self.isCurrentPlayerHuman():
            self.game.board[row][col]=self.game.current_player
            self.btn_text[row][col].set(" "+playerNumToStr(self.game.current_player)+" ")
            self.game.current_player=switchPlayer(self.game.current_player)
        game_state=self.game.getGameState()
        if game_state==ON_GOING and self.isCurrentPlayerComputer():
            game_state=self.makeComputerMove()

        if game_state!=ON_GOING:
            self.gameStateLabelVar.set(printResult(game_state))

    def newGame(self):
        self.game.current_player=X
        self.gameStateLabelVar.set("")
        for row in range(3):
            for col in range(3):
                self.btn_text[row][col].set("   ")
                self.game.board[row][col]=BLANK

        if self.var1.get()=="Computer" and self.var2.get()=="Computer":
            self.computerVersusComputer()

        if self.var1.get()=="Computer" and self.var2.get()=="Human":
            self.makeComputerMove()

    def isCurrentPlayerHuman(self):
        return (self.game.current_player==X and self.var1.get()=="Human") or (self.game.current_player==O and self.var2.get()=="Human")

    def isCurrentPlayerComputer(self):
        return not self.isCurrentPlayerHuman()

    def computerVersusComputer(self):
        game_state=self.game.getGameState()
        while game_state==ON_GOING:
            game_state=self.makeComputerMove()

        self.gameStateLabelVar.set(printResult(game_state))

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
        self.current_player=X
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
        return "X WON!"
    elif game_state==O_WIN:
        return "O WON!"
    elif game_state==DRAW:
        return "DRAW"
    elif game_state==ON_GOING:
        return "The game is still ongoing"
    else:
        return "I don't know what is going on"

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
    *Win by getting three in a row.                          *
    *Both X and O can be either a human or a computer.       *
    *                                                        *
    *Created by Jouko Virtanen in 2018                       *
    **********************************************************
    """
    print intro

printIntro()

#while True:
#    game=BoardClass(3)
#    game.getPlayers()
#    game.playGame()
#    play_again=raw_input("Play again? (Y/N) ")
#    if not strToBool(play_again):
#        break

if __name__=="__main__":
    app=MainApp()
    app.title('TicTacToe')
    app.geometry('300x450')
    app.mainloop()

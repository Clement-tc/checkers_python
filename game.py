from piece import Piece
from player import Player
import math


class Game():
    board=[]
    def __init__(self):
        self.player1=Player("player1")
        self.player2=Player("player2")
        self.turn=self.player1
        #add attribute to replace len(self.board)
        self.can_eat={self.player1:0,self.player2:0}
        self.has_move_left={self.player1:True,self.player2:True}
        self.replay_pawn=None
        self.board=[[None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1)],
                    [Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None],
                    [None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1)],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None],
                    [None,Piece(self.player2),None,None,None,Piece(self.player2),None,Piece(self.player2)],
                    [Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None]]

    def has_won(self):
        """ return un boolean pour savoir si un des joueur a gagné"""
        if self.turn==self.player1 and not self.has_move_left[self.player1]:
            return "player2 won"
        if self.turn==self.player2 and not self.has_move_left[self.player2]:
            return "player1 won"
         
        return False
    
    def move(self,starting_x,starting_y,ending_x,ending_y):
        """fonction que permet de deplacer un pion avec les coordonnées du pion et de la destination"""

        if(self.board[ending_x][ending_y]!=None):
            return False

        selected_piece=self.board[starting_x][starting_y]
        self.board[starting_x][starting_y]=None
        self.board[ending_x][ending_y]=selected_piece

    #does it transforme into a queen
        if(ending_x==len(self.board)-1 and self.board[ending_x][ending_y].owner==self.player1):

            self.board[ending_x][ending_y].type="queen"
        if(ending_x==0 and self.board[ending_x][ending_y].owner==self.player2):

            self.board[ending_x][ending_y].type="queen"
        self.change_turn()
        self.compute_moves()
        return True
    
    def eat(self,starting_x,starting_y,ending_x,ending_y):
        """fonction que permet de manger un pion avec les coordonnées du pion et de la destination"""
        self.replay_pawn=self.board[starting_x][starting_y]
        if(self.board[ending_x][ending_y]!=None):
            return False

        selected_piece=self.board[starting_x][starting_y]
        self.board[starting_x][starting_y]=None
        self.board[ending_x][ending_y]=selected_piece

        if(starting_x>ending_x):
            eaten_x=ending_x+1
        else:
            eaten_x=ending_x-1
        if(starting_y>ending_y):
            eaten_y=ending_y+1
        else:
            eaten_y=ending_y-1

        self.board[eaten_x][eaten_y]=None
        self.compute_moves()
        if(self.can_eat[self.turn]==0):
            self.change_turn()
            self.compute_moves()

        if(ending_x==len(self.board)-1 and self.board[ending_x][ending_y].owner==self.player1):

            self.board[ending_x][ending_y].type="queen"
        if(ending_x==0 and self.board[ending_x][ending_y].owner==self.player2):

            self.board[ending_x][ending_y].type="queen"

        self.turn.gainpoint()
        
        return True
    
    def change_turn(self):
        """Change la valeur de self.turn pour alterner les tours des joueurs"""
        if(self.turn==self.player1):
            self.turn=self.player2
        else:
            self.turn=self.player1

    def compute_moves(self):
        """Calcul et attribut aux pions les mouvements possible"""
        self.can_eat={self.player1:0,self.player2:0}
        self.has_move_left={self.player1:False,self.player2:False}
        #parcour the board to look for pieces
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[0])):
                if(self.board[row_index][col_index]==None):
                    continue

                moves_list=[]
                eat_list=[]
                if(self.board[row_index][col_index].owner!=self.turn):
                    self.board[row_index][col_index].moves=(moves_list,eat_list)
                    continue
                if(self.replay_pawn !=None and self.board[row_index][col_index]!=self.replay_pawn):
                    continue
                if(self.board[row_index][col_index].type=="queen"):
                        moves_list,eat_list=self.compute_queen_moves(row_index,col_index)
                else:
                #moves for player 1
                    if(self.board[row_index][col_index].owner==self.player1 and self.board[row_index][col_index].owner==self.turn):
                        #simple pawn move forward
                        if(row_index <len(self.board)-1 and col_index<len(self.board[0])-1 and  self.board[row_index+1][col_index+1]==None):
                            moves_list.append((col_index+1,row_index+1))
                        
                        if(row_index <len(self.board)-1 and col_index>0 and self.board[row_index+1][col_index-1]==None):
                            moves_list.append((col_index-1,row_index+1))
                        
                        #eating pawn move player 1
                        if(row_index <len(self.board)-2 and col_index<len(self.board[0])-2 and self.board[row_index+1][col_index+1]!=None and self.board[row_index+1][col_index+1].owner==self.player2 and self.board[row_index+2][col_index+2]==None):
                            eat_list.append((col_index+2,row_index+2,))
                            self.can_eat[self.player1]=1
                        
                        if(row_index <len(self.board)-2  and col_index>1 and self.board[row_index+2][col_index-2]==None and self.board[row_index+1][col_index-1]!=None and self.board[row_index+1][col_index-1].owner==self.player2):
                            eat_list.append((col_index-2,row_index+2))
                            self.can_eat[self.player1]=1

                    #moves for player 2
                    if(self.board[row_index][col_index].owner==self.player2 and self.board[row_index][col_index].owner==self.turn):
                        #simple pawn move forward
                        if(col_index >0 and  self.board[row_index-1][col_index-1]==None):
                            moves_list.append((col_index-1,row_index-1))
                        
                        if(row_index >0 and col_index<len(self.board)-1 and self.board[row_index-1][col_index+1]==None):
                            moves_list.append((col_index+1,row_index-1))

                        #eating pawn move player 2
                        if(row_index >1 and col_index>1 and self.board[row_index-1][col_index-1]!=None and self.board[row_index-1][col_index-1].owner==self.player1 and self.board[row_index-2][col_index-2]==None):
                            eat_list.append((col_index-2,row_index-2))
                            self.can_eat[self.player2]=1
                        if(row_index >1 and col_index<len(self.board[0])-2 and self.board[row_index-2][col_index+2]==None and self.board[row_index-1][col_index+1]!=None and self.board[row_index-1][col_index+1].owner==self.player1):
                            eat_list.append((col_index+2,row_index-2))
                            self.can_eat[self.player2]=1

                if(eat_list):
                    self.can_eat[self.turn]=1
                
                if(moves_list+eat_list):

                    self.has_move_left[self.turn]=True

                self.board[row_index][col_index].moves=(moves_list,eat_list)
        self.replay_pawn=None

    def compute_queen_moves(self,row_index,col_index):
        """Calcul et attribut aux reines les mouvements possible"""
        in_bound = lambda index_1,index_2: index_1+index_2>=0 and index_1+index_2<8
        moves_list=[]
        eat_list=[]
        directions = [[-1, -1], [-1, 1],[1, -1], [1, 1]]
        while(directions):
            for vector in directions:
                vector_x_sign=math.copysign(1,vector[0])
                vector_y_sign=math.copysign(1,vector[1])
                if(in_bound(vector[0],row_index)and in_bound(vector[1],col_index)):
                    if(self.board[row_index+vector[0]][col_index+vector[1]]==None):

                        moves_list=moves_list+[(col_index+vector[1],row_index+vector[0])]
                        vector_index=directions.index(vector)
                        directions[vector_index]=[int(vector_x_sign+vector[0]),int(vector_y_sign+vector[1])]

                    else:

                        vector_x_index=int(vector[0]+vector_x_sign)
                        vector_y_index=int(vector[1]+vector_y_sign)
                        if(in_bound(vector_x_index,row_index)and in_bound(vector_y_index,col_index)):
                            if(self.board[row_index+vector_x_index][col_index+vector_y_index]==None):
                                if(self.board[row_index+vector[0]][col_index+vector[1]]!=None and self.board[row_index+vector[0]][col_index+vector[1]].owner!=self.turn):

                                    eat_list=eat_list+[(col_index+vector_y_index,row_index+vector_x_index)]
                                    directions.remove(vector)
                                else:
                                    directions.remove(vector)
                            else:
                                directions.remove(vector)
                        else:
                            directions.remove(vector)
                else:
                    directions.remove(vector)
                    


        return (moves_list,eat_list)

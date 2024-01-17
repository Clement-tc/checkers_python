from piece import Piece
from player import Player



class Game():
    board=[]
    def __init__(self):
        #self.board=[0 for i in range(8) for x in range(8)]
        self.lenght=500
        self.width=500
        self.player1=Player("player1")
        self.player2=Player("player2")
        self.turn=self.player1
        #add attribute to replace len(self.board)
        self.can_eat={self.player1:0,self.player2:0}
        self.has_move_left={self.player1:True,self.player2:True}
        self.board=[[None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1)],
                    [Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None],
                    [None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1,"queen"),None,Piece(self.player1)],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [Piece(self.player2),None,Piece(self.player2,"queen"),None,Piece(self.player2),None,Piece(self.player2),None],
                    [None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2)],
                    [Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None]]

    def has_won(self):
        print("into has won has move;",self.has_move_left)
        if self.turn==self.player1 and not self.has_move_left[self.player1]:
            return "player2 won"
        if self.turn==self.player2 and not self.has_move_left[self.player2]:
            return "player1 won"
         
        return False
    
    def move(self,starting_x,starting_y,ending_x,ending_y):


        if(self.board[ending_x][ending_y]!=None):
            return False

        selected_piece=self.board[starting_x][starting_y]
        self.board[starting_x][starting_y]=None
        self.board[ending_x][ending_y]=selected_piece

    #does it transforme into a queen
        if(ending_x==len(self.board)-1 and self.board[ending_x][ending_y].owner==self.player1):
            print("i'm a quee")
            self.board[ending_x][ending_y].type="queen"
        if(ending_x==0 and self.board[ending_x][ending_y].owner==self.player2):
            print("im' a queen")
            self.board[ending_x][ending_y].type="queen"
        self.change_turn()
        self.compute_moves()
        return True
    
    def eat(self,starting_x,starting_y,ending_x,ending_y):
        if(self.board[ending_x][ending_y]!=None):
            return False

        selected_piece=self.board[starting_x][starting_y]
        self.board[starting_x][starting_y]=None
        self.board[ending_x][ending_y]=selected_piece

        if(starting_x>ending_x):
            eaten_x=starting_x-1
        else:
            eaten_x=starting_x+1
        if(starting_y>ending_y):
            eaten_y=starting_y-1
        else:
            eaten_y=starting_y+1

        self.board[eaten_x][eaten_y]=None
        self.compute_moves()
        if(self.can_eat[self.turn]==0):
            self.change_turn()
            self.compute_moves()


        self.turn.gainpoint()
        return True
    
    def change_turn(self):
        if(self.turn==self.player1):
            self.turn=self.player2
        else:
            self.turn=self.player1

    def compute_moves(self):
        self.can_eat={self.player1:0,self.player2:0}
        self.has_move_left={self.player1:False,self.player2:False}
        #parcour the board to look for pieces
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[0])):
                if(self.board[row_index][col_index]==None):
                    continue
                moves_list=[]
                eat_list=[]
                print(self.board[row_index][col_index].owner,self.turn)
                if(self.board[row_index][col_index].owner!=self.turn):
                    self.board[row_index][col_index].moves=(moves_list,eat_list)
                    continue

                
                if(self.board[row_index][col_index].type=="queen"):
                        print("i'am a queen")
                        moves_list,eat_list=self.compute_queen_moves(row_index,col_index)
                        print("\n moves list ",moves_list+eat_list)
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


    def compute_queen_moves(self,row_index,col_index):
        in_bound = lambda index_1,index_2: index_1+index_2>=0 and index_1+index_2<8
        moves_list=[]
        eat_list=[]
        index_count=0
        directions = [[-1, -1], [-1, 1],[1, -1], [1, 1]]
        for vector in directions:
            if(in_bound(vector[0],row_index)and in_bound(vector[0],col_index)):
                print("in bound for moving")
                if(self.board[row_index+vector[0]][col_index+vector[1]]==None):
                    print("into moving")
                    moves_list=moves_list+[(col_index+vector[1],row_index+vector[0])]
                    
                if(in_bound(vector[0]*2,row_index)and in_bound(vector[1]*2,col_index)):
                    print('im in bound for eating',row_index+vector[0]*2,col_index+vector[1]*2)
                    if(self.board[row_index+vector[0]*2][col_index+vector[1]*2]==None):
                        if(self.board[row_index+vector[0]][col_index+vector[1]]!=None and self.board[row_index+vector[0]][col_index+vector[1]].owner!=self.turn):
                            eat_list=eat_list+[(col_index+vector[1]*2,row_index+vector[0]*2)]
        print(moves_list+eat_list)

        return (moves_list,eat_list)

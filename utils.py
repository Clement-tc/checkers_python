import pygame

def draw_board(window_surface,boarder_size):

    boarder_color=(0,0,0)
    width,length=(pygame.display.Info().current_w,pygame.display.Info().current_w)
    boarder_top=pygame.Rect(0,0,width,20)
    pygame.draw.rect(window_surface, boarder_color, boarder_top)
    boarder_left=pygame.Rect(0,0,boarder_size,length)
    pygame.draw.rect(window_surface, boarder_color, boarder_left)
    boarder_right=pygame.Rect(width-boarder_size,0,width,length)
    pygame.draw.rect(window_surface, boarder_color, boarder_right)
    boarder_bot=pygame.Rect(0,length-boarder_size,width,length)
    pygame.draw.rect(window_surface, boarder_color, boarder_bot)

    WHITE=(255,255,255)
    BLACK=(0,0,0)

    squaresize=(width-(boarder_size*2))/8
    
    for x in range(8):
        for y in range(8):
            square=pygame.Rect(boarder_size+x*squaresize,boarder_size+y*squaresize,squaresize,squaresize)
            if(y%2==0 ):
                if(x%2==0):
                    pygame.draw.rect(window_surface, WHITE, square)
                else:
                    pygame.draw.rect(window_surface, BLACK, square)
            else:
                if(x%2!=0):
                    pygame.draw.rect(window_surface, WHITE, square)
                else:
                    pygame.draw.rect(window_surface, BLACK, square)

def is_a_move(turn,pawn_coor,square_coor):
    print(turn)
    if(turn.name=="player1"):
        list_of_moves=[(pawn_coor[0]+1,pawn_coor[1]-1),(pawn_coor[0]+1,pawn_coor[1]+1)]
    else:
        list_of_moves=[(pawn_coor[0]-1,pawn_coor[1]-1),(pawn_coor[0]-1,pawn_coor[1]+1)]

    if square_coor in list_of_moves:
        return True
    return False

def is_a_eat(pawn_coor,square_coor):
    list_of_moves=[(pawn_coor[0]-2,pawn_coor[1]-2),(pawn_coor[0]-2,pawn_coor[1]+2),(pawn_coor[0]+2,pawn_coor[1]-2),(pawn_coor[0]+2,pawn_coor[1]+2)]

    if square_coor in list_of_moves:
        print("true")
        return True
    print("false")
    return False


"""
self.board=[[None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1)],
                    [Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None],
                    [None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1)],
                    [Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None,Piece(self.player1),None],
                    [None,None,None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None,None,None],
                    [None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2)],
                    [Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None],
                    [None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2)],
                    [Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None,Piece(self.player2),None]]
"""

vectors=[[1,1],[-1,1],[1,-1]]

for vector in vectors:
    vectors.remove(vector)
    print(vectors)
    print(vector)
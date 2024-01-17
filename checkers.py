import pygame
import game
import utils
import math

boarder_size=20


    # create a surface object, image is drawn on it.
def moves_visual(game,pos_list,window_surface):
    if(game.can_eat[game.turn]==1):
        pos_list=pos_list[1]
    else:
        pos_list=pos_list[0]+pos_list[1]
        
    print("concataned pos",pos_list)
    width,length=(pygame.display.Info().current_w,pygame.display.Info().current_w)
    squaresize=(width-(boarder_size*2))/8

    for pos in pos_list:
        print("showint square in blue",pos)
        square=pygame.Rect(boarder_size+pos[0]*squaresize,boarder_size+pos[1]*squaresize,squaresize,squaresize)
        pygame.draw.rect(window_surface,(31, 36, 231), square)

def draw_pawn(game):

    width,length=(pygame.display.Info().current_w,pygame.display.Info().current_w)
    squaresize=(width-(boarder_size*2))/8
    pawn_size=(squaresize,squaresize)

    for row_index in range(len(game.board)):
            for col_index in range(len(game.board[0])):
                if(game.board[row_index][col_index]==None):
                     continue
                if(game.board[row_index][col_index].owner.name=="player1"):
                    if(game.board[row_index][col_index].type=="pawn"):
                        pawn = pygame.image.load("pawn_black.png")
                        pawn = pygame.transform.scale(pawn, pawn_size)
                    else:
                        pawn = pygame.image.load("dame_black.png")
                        pawn = pygame.transform.scale(pawn, pawn_size)
        # Using blit to copy content from one surface to other
                    window_surface.blit(pawn, (boarder_size+col_index*squaresize,boarder_size+row_index*squaresize))
                else:
                    if(game.board[row_index][col_index].type=="pawn"):
                        pawn = pygame.image.load("pawn_red.png")
                        pawn = pygame.transform.scale(pawn, pawn_size)
                    else:
                        pawn = pygame.image.load("Dame_red.png")
                        pawn = pygame.transform.scale(pawn, pawn_size)
        
        # Using blit to copy content from one surface to other
                    window_surface.blit(pawn, (boarder_size+col_index*squaresize,boarder_size+row_index*squaresize))
pygame.init()


pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 800))

#background = pygame.Surface((800, 600))
#background.fill(pygame.Color('#000000'))


is_running = True


game_instance=game.Game()
utils.draw_board(window_surface,boarder_size)

width,length=(pygame.display.Info().current_w,pygame.display.Info().current_w)
squaresize=(width-(boarder_size*2))/8

draw_pawn(game_instance)
print(game_instance.board[4][1])
print(game_instance.board[0][3])
#game_instance.move(3,0,4,1)
#window_surface.fill((0,0,0))
#utils.draw_board(window_surface,boarder_size)
print(game_instance.board[0][3])
draw_pawn(game_instance)
game_instance.compute_moves()
selected_pawn=(None,(0,0))
while is_running:

    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            coor=((pos[0]-boarder_size)/squaresize,(pos[1]-boarder_size)/squaresize)
            coor=(math.floor(coor[0]),math.floor(coor[1]))

            if(selected_pawn[0]!=None):
                
                if(selected_pawn[0].owner==game_instance.turn):
                    
                    if(coor in selected_pawn[0].moves[0] and game_instance.can_eat[game_instance.turn]!=1):
                        game_instance.move(selected_pawn[1][1],selected_pawn[1][0],coor[1],coor[0])
                    if(coor in selected_pawn[0].moves[1]):
                        print("eating")
                        game_instance.eat(selected_pawn[1][1],selected_pawn[1][0],coor[1],coor[0])

                    selected_pawn=(None,(0,0))
                    window_surface.fill((0,0,0))
                    utils.draw_board(window_surface,boarder_size)
                    draw_pawn(game_instance)
                else:
                    selected_pawn=(None,(0,0))
            else:
                
                selected_pawn=(game_instance.board[coor[1]][coor[0]],coor)
                if(selected_pawn[0]!=None):
                    moves_visual(game_instance,selected_pawn[0].moves,window_surface)
            if(game_instance.has_won()):
                background_win=pygame.Rect(120,200,6*squaresize,2*squaresize)
                pygame.draw.rect(window_surface, (0,0,0),background_win)
                pygame.font.init()
                my_font=pygame.font.SysFont('arial', 40)
                text_surface = my_font.render(f'le joueur {game_instance.turn.name} a gagné', False, (50, 50, 50))
                window_surface.blit(text_surface, (170,250))
            #is_running=False

             
        if event.type == pygame.QUIT:
            is_running = False

    #window_surface.blit(background, (0, 0))

    pygame.display.update()
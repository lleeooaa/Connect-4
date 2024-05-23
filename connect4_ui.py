import pygame
from pygame.locals import *
import random
import connect4_ai as ai

class Gameboard:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.gameboard = "" #in column order [[col1],[col2],col[3]...]
        for i in range(7):
            for j in range(6):
                self.gameboard+=str(0)
    
    def draw(self):
        for row in range(6):
            for col in range(7):
                cell_rect = pygame.Rect(col * 100+190, row * 100+100, 100, 100)
                pygame.draw.rect(self.parent_screen, (0, 0, 0), cell_rect, 1)
        pygame.display.flip()

class Piece:
    def __init__(self, parent_screen, curr_player):
        self.parent_screen = parent_screen
        self.curr_player=curr_player
    
    def draw(self, pos):
        if self.curr_player==1:
            pygame.draw.circle(self.parent_screen, (242,71,106), pos, 49)
        else:
            pygame.draw.circle(self.parent_screen, (255,244,155), pos, 49)
        pygame.display.flip()

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1080,720))
        self.surface.fill((99,78,52))
        self.font = pygame.font.SysFont("Arial",35)
        self.one_player=self.font.render("1 Player", True, (0,0,0))
        self.one_player_rect=self.one_player.get_rect(center=(850,50))
        self.two_player=self.font.render("2 Player", True, (0,0,0))
        self.two_player_rect=self.two_player.get_rect(center=(1000,50))
        self.start_game()
        self.gamemode=None
        self.player=0
        self.game=None
        self.player1_score=0
        self.player2_score=0

    def start_game(self):
        self.surface.fill((99,78,52))
        pygame.draw.rect(self.surface, (100,100,100), self.one_player_rect)
        pygame.draw.rect(self.surface, (100,100,100), self.two_player_rect)
        self.surface.blit(self.one_player,self.one_player_rect)
        self.surface.blit(self.two_player,self.two_player_rect)
        self.game=Gameboard(self.surface)
        self.game.draw()
        self.player1_score=self.player2_score=0
        self.player=random.choice([1,2])

    def check_draw(self):
        if '0' not in self.game.gameboard:
            return True
        return False

    def add_piece(self, col):
        for i in range(6):
            if self.game.gameboard[col*6+i]=='0':
                self.game.gameboard=list(self.game.gameboard)
                self.game.gameboard[col*6+i]=str(self.player)
                self.game.gameboard=''.join(self.game.gameboard)
                piece=Piece(self.surface, self.player)
                piece.draw((240+100*col,650-100*i))
                if self.check_win((col,i),self.player) or self.check_draw():
                    if self.player==1:
                        text="Red wins"
                    else:
                        text="Yellow wins"
                    if self.check_draw():
                        text='Draw'
                    self.textbox=self.font.render(text, True, (0,0,0))
                    self.textbox_rect=self.two_player.get_rect(center=(540,50))
                    pygame.draw.rect(self.surface, (99,78,52), self.textbox_rect)
                    self.surface.blit(self.textbox,self.textbox_rect)
                    pygame.display.flip()
                    self.gamemode=None
                    return None
                if self.player==1:
                    self.player=2
                else:
                    self.player=1
                return (col,i)

    def check_win(self, pos, player):
        lower_bound_x=max(0,pos[0]-3)
        upper_bound_x=min(3,pos[0])+1
        lower_bound_y=max(0,pos[1]-3)
        upper_bound_y=min(2,pos[1])+1
        for i in range(lower_bound_x,upper_bound_x):
            if self.game.gameboard[i*6+pos[1]]==self.game.gameboard[(i+1)*6+pos[1]]==self.game.gameboard[(i+2)*6+pos[1]]==self.game.gameboard[(i+3)*6+pos[1]]==str(player):
                pygame.draw.line(self.surface, (0,255,255), (240+100*i, 650-100*pos[1]), (240+100*(i+3), 650-100*pos[1]), 10)
                return True
        for j in range(lower_bound_y,upper_bound_y):
            if self.game.gameboard[pos[0]*6+j]==self.game.gameboard[pos[0]*6+j+1]==self.game.gameboard[pos[0]*6+j+2]==self.game.gameboard[pos[0]*6+j+3]==str(player):
                pygame.draw.line(self.surface, (0,255,255), (240+100*pos[0], 650-100*j), (240+100*pos[0], 650-100*(j+3)), 10)
                return True
        for i,j in zip(range(max(max(0,pos[0]-pos[1]),pos[0]-3),upper_bound_x), range(max(max(0,pos[1]-pos[0]),pos[1]-3),upper_bound_y)):
            if self.game.gameboard[i*6+j]==self.game.gameboard[(i+1)*6+j+1]==self.game.gameboard[(i+2)*6+j+2]==self.game.gameboard[(i+3)*6+j+3]==str(player):
                pygame.draw.line(self.surface, (0,255,255), (240+100*i, 650-100*j), (240+100*(i+3), 650-100*(j+3)), 10)
                return True
        for i,j in zip(range(max(max(0,pos[0]+pos[1]-5),pos[0]-3),min(pos[0]+pos[1],upper_bound_x)), range(min(pos[0]+pos[1],min(5,pos[1]+3)),max(max(0,pos[0]+pos[1]-6),pos[1]-3)+2,-1)):
            if self.game.gameboard[i*6+j]==self.game.gameboard[(i+1)*6+j-1]==self.game.gameboard[(i+2)*6+j-2]==self.game.gameboard[(i+3)*6+j-3]==str(player):
                pygame.draw.line(self.surface, (0,255,255), (240+100*i, 650-100*j), (240+100*(i+3), 650-100*(j-3)), 10)
                return True
        
        return False

    def run(self):
        running = True
        pygame.display.flip()
        while running:
            if self.gamemode==1 and self.player==1:
                col=ai.evaluate(self.game.gameboard, 1, 7, self.player1_score, self.player2_score, None)[1]
                pos=self.add_piece(col)
                if not pos:
                    continue    
                self.player1_score,self.player2_score=ai.compute_score(self.game.gameboard, pos, self.player1_score, self.player2_score, 1)
                print(self.player1_score,self.player2_score)
                """
                col=ai.evaluate(self.game.gameboard, 2, 7, self.player1_score, self.player2_score, None)[1]
                pos=self.add_piece(col)
                if not pos:
                    continue    
                self.player1_score,self.player2_score=ai.compute_score(self.game.gameboard, pos, self.player1_score, self.player2_score, 2)
                print(self.player1_score,self.player2_score)
                """

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:   
                        running = False

                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.one_player_rect.collidepoint(event.pos):
                        self.start_game()
                        self.gamemode=1
                    if self.two_player_rect.collidepoint(event.pos):
                        self.start_game()
                        self.gamemode=2
                    if self.gamemode==1 and self.player==2:
                        x, y=pygame.mouse.get_pos()
                        if x>=190 and x<=890 and y>=100 and y<=700:
                            col=(x-190)//100
                            pos=self.add_piece(col)
                            if not pos:
                                continue    
                            self.player1_score,self.player2_score=ai.compute_score(self.game.gameboard, pos, self.player1_score, self.player2_score, 2)
                            print(self.player1_score,self.player2_score)
                                
                    if self.gamemode==2:
                        x, y=pygame.mouse.get_pos()
                        if x>=190 and x<=890 and y>=100 and y<=700:
                            col=(x-190)//100
                            pos=self.add_piece(col)
                            if not pos:
                                continue  
                            self.player1_score,self.player2_score=ai.compute_score(self.game.gameboard, pos, self.player1_score, self.player2_score, 3-self.player)
                            print(self.player1_score,self.player2_score)
                            
if __name__ == "__main__":
    game = Game()
    game.run()

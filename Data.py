import pygame
import random 
import sys

SM_ModellList = []                     #a list of Space Marine models
GS_ModellList = []                     #a list of Genstealer models

pygame.init()
screen = pygame.display.set_mode((700,600))
screen.fill('black')
pygame.display.set_caption('Space Hulk')

#Button class
class Button():
    def __init__(self, x, y, image, scale) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.prev_mouse_state = False

    def draw(self, surface):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()[0] == 1

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            # Check if mouse button is pressed down
            if mouse_state and not self.prev_mouse_state:
                self.clicked = True

         # Check if mouse button is released
        if not mouse_state and self.prev_mouse_state:
            if self.clicked:
                action = True
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

         # Update previous mouse state
        self.prev_mouse_state = mouse_state

        return action
    
class GameStateManager:
    def __init__(self, state) -> None:
        self.state = state
    def changestate(self,newstate):
        self.state = newstate
    def givestate(self):
        return self.state
    
gameStateManager = GameStateManager('main')

class Game:                                         #can variables be exported to individual gamestates?
    def __init__(self) -> None:
        self.Manager = gameStateManager
        self.states = {}                            #a list of gamestates that the game can have
        self.round = 0                              #the current round of the game
        self.player1 = ''                           #name of player 1
        self.player2 = ''                           #name of player 2
        self.selected_Model = None
        self.selected_tile = None                   #saves the selected model for other classes to interact with
        self.clicked_tile = None
        self.CP = random.randint(1,6)               #a random number of CP for the sm player to use
        self.is_playing = self.player1              #the name of the player who is playing

    def changeturn(self):
        if(self.is_playing == self.player1):
            self.round += 1
            for Model in SM_ModellList:
                Model.AP = 4
                self.overwatch = False
                self.guard = False
                self.jam = False
            self.CP = random.randint(1,6)
        if(self.is_playing == self.player2):
            for Model in GS_ModellList:
                Model.AP = 6

    def turnmodel(self):
        self.selected_Model.face = (-1,0) #left

    def redAP(self,Model,amount):
        if(Model in SM_ModellList):
            if(amount > Model.AP):
                Model.AP = 0
                self.CP -= (amount - Model.AP)
            else: Model.AP -= amount
        if(Model in GS_ModellList):
            Model.AP -= amount

    def moveModel(self):
        a = False
        b = False
        if((self.clicked_tile != None) & (self.selected_tile != None) & (self.selected_Model != None)): 
            a = True
            if((self.is_playing == self.player1) & (self.selected_Model in SM_ModellList)):
                match(self.selected_Model.face):
                    case (1,0):
                        if(self.selected_tile.x + 1 == self.clicked_tile.x):
                            if((self.selected_Model.AP != 0) | (self.CP != 0)):
                                self.redAP(self.selected_Model, 1,) 
                                b = True
                        elif(self.selected_tile.x - 1 == self.clicked_tile.x):
                            if(self.selected_Model.AP + self.CP >= 2):
                                self.redAP(self.selected_Model, 2)
                                b = True
                        elif((self.selected_tile.y != self.clicked_tile.y)):
                            b = False
                        if(self.clicked_tile.is_wall == True):
                            b = False
            if((self.is_playing == self.player2) & (self.selected_Model in GS_ModellList)):
                match(self.selected_Model.face):
                    case (1,0):
                        if((self.selected_tile.x + 1 == self.clicked_tile.x) | (self.selected_tile.y != self.clicked_tile.y)):
                            if(self.selected_Model.AP != 0):
                                self.redAP(self.selected_Model, 1,) 
                                b = True
                        elif(self.selected_tile.x - 1 == self.clicked_tile.x):
                            if(self.selected_Model.AP >= 2):
                                self.redAP(self.selected_Model, 2)
                                b = True
                        if(self.clicked_tile.is_wall == True):
                            b = False
        if(a & b):
            game.clicked_tile.occupand = game.selected_tile.occupand
            game.selected_tile.is_occupied = False
            game.clicked_tile.is_occupied = True
            game.selected_tile.occupand = None
            game.selected_tile = game.clicked_tile
            game.clicked_tile = None
        elif(not a):
            print('Bitte wähle ein Model und ein Tile aus!')
        elif(not b):
            print('Dahin kannst du nicht gehen!/ Nicht genügend AP/CP')

    def run(self):
        self.states[self.Manager.givestate()].run()
        pygame.display.update()
        
game = Game()

class gamestateTurn:
    def __init__(self) -> None:
        self.gameStateManager = gameStateManager
    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turnright_button = Button(80, 200, self.move_image, 1)
        self.turnleft_button = Button(160, 200, self.move_image, 1)
        while (True):
            t = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit
            if(self.turnleft_button):
                match(game.selected_Model.face):
                    case(1,0): game.selected_Model.face = (0,1)
                    case(0,1): game.selected_Model.face = (-1,0)
                    case(-1,0): game.selected_Model.face = (0,-1)
                    case(0,-1): game.selected_Model.face = (1,0)

            if(self.turnright_button):
                t
            if(t):
                if(game.is_playing == game.player1):
                    self.gameStateManager.changestate('start')
                else:
                    self.gameStateManager.changestate('run')
            
class gamestateMain:
    def __init__(self) -> None:
        self.gameStateManager = gameStateManager
    def run(self):
        p1 = True
        font = pygame.font.SysFont('CASTELLAR', 20)
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Check if the key is an alphanumeric character or space
                    if event.unicode.isalnum() or event.unicode.isspace() and not (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                        if(p1):
                            game.player1 += event.unicode
                        else:
                            game.player2 += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        if(p1):
                            game.player1 = game.player1[:-1]
                        else:
                            game.player2 = game.player2[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if(p1):p1 = False
                        elif(game.player2 != None):
                            self.gameStateManager.changestate('start')
                            game.run()

            # Clear the screen
            screen.fill((255, 255, 255))

            # Render the input string
            if(p1):
                text_surface = font.render(game.player1, True, (0, 0, 0))
            else:
                text_surface = font.render(game.player2, True, (0,0,0))
            screen.blit(text_surface, (10, 10))
            pygame.display.update()

class Player1Turn:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for row in map:
                for tile in row:
                    tile.render(screen)
                    tile.interact()
            
            SB.display(screen)
            BB.display(screen)
            if(self.move_button.draw(screen)):
                game.moveModel()

            if(self.turn_button.draw(screen)):
                game.is_playing = game.player2
                game.changeturn()
                self.Manager.changestate('run')
                print(self.Manager.givestate())
                game.run()

            pygame.display.update()

class Player2Turn:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for row in map:
                for tile in row:
                    tile.render(screen)
                    tile.interact()
            
            SB.display(screen)
            BB.display(screen)
            if(self.move_button.draw(screen)):
                game.moveModel()

            if(self.turn_button.draw(screen)):
                game.is_playing == game.player1
                game.changeturn()
                self.Manager.changestate('start')
                print(self.Manager.givestate())
                game.run()

            pygame.display.update()

class Tile:
    def __init__(self, x, y, size):
        self.x = x                      # x position on the grid
        self.y = y                      # y position on the grid
        image = pygame.image.load('Pictures/Floor.png')     # image of the floor tiles
        self.image = pygame.transform.scale(image, (int(size), int(size)))
        self.size = size # size of the tile in pixels
        self.is_occupied = False # true if occupied by any miniature
        self.occupand = Model # equals the modell which occupies this tile
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*size,y*size)
        self.clicked = False
        self.is_wall = False

    def render(self, screen):
        if(self.is_wall): 
            image = pygame.image.load('Pictures/Wall.png')
            self.image = pygame.transform.scale(image,(self.size,self.size))
        screen.blit(self.image, (self.x*self.size, self.y*self.size))
        if(self.is_occupied):
            match(self.occupand.face):
                case((1,0)):
                    imaget = pygame.transform.scale(self.occupand.image, (int(self.size), int(self.size)))
                
                case(-1,0):
                    imaget = pygame.transform.scale(self.occupand.image, (int(self.size), int(self.size)))
                    imaget = pygame.transform.rotate(imaget,180)
                
                case((0,1)):
                    imaget = pygame.transform.scale(self.occupand.image, (int(self.size), int(self.size)))
                    imaget = pygame.transform.rotate(imaget,90)

                case((0,-1)):
                    imaget = pygame.transform.scale(self.occupand.image, (int(self.size), int(self.size)))
                    imaget = pygame.transform.rotate(imaget,270)
    
            screen.blit(imaget, (self.x*self.size, self.y*self.size))
    
    def interact(self):
        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos)) and (pygame.mouse.get_pressed()[0] == 1):
            self.clicked = True
        if(pygame.mouse.get_pressed()[0] == 0 and self.clicked):
            if(self.is_occupied):
                game.selected_Model = self.occupand
                print(self.occupand.AP)
                game.selected_tile = self
            else:
                game.clicked_tile = self
                print(game.clicked_tile)
            self.clicked = False

class Model:
    def __init__(self, AP, image):
        self.AP = AP
        self.image = pygame.image.load(image)
        self.face = (1,0)

class SpaceMarine(Model):
    def __init__(self, weapon, rank):
        super().__init__(4,'Pictures/Models/SM.png')
        self.weapon = weapon
        self.rank = rank
        self.overwatch = False
        self.guard = False
        self.jam = False

class Genestealer(Model):
    def __init__(self):
        super().__init__(6, 'Pictures/Models/Gs.png')

class Blip(Model):
    def __init__(self):
        super().__init__(6, 'Pictures/Models/Blip.png')
        self.count = random.randint(1,3)

#generate a Map of tiles
map_width = 20
map_height = 20
tile_size = 25

map = [[Tile(x, y, tile_size, ) for x in range(map_width)] for y in range(map_height)]

class Sidebar():
    def __init__(self):
        self.SM_Modelcount = len(SM_ModellList)
        self.Assault_cannon_Ammo = int
        self.Heavy_flamer_ammo = int
        self.timer = int
        self.pos = (500,0)

    def display(self,screen):
        my_font = pygame.font.SysFont('CASTELLAR', 20)
        image = pygame.image.load('Pictures/Sidebar.png')
        image2 = pygame.transform.scale(image, (int(200), int(500)))
        screen.blit(image2, self.pos)
        CP_Text = my_font.render('CP: '+str(game.CP), False, (0,0,0))
        round_Text = my_font.render('Round: '+str(game.round), False, (0, 0, 0))
        player1_Text = my_font.render('SM: '+game.player1,False,(0,0,0))
        player2_Text = my_font.render('GS: '+game.player2, False, (0,0,0))
        GS_count_Text = my_font.render('GS Models: '+str(len(GS_ModellList)),False,(0,0,0))
        SM_count_Text = my_font.render('SM Models: '+str(len(SM_ModellList)),False,(0,0,0))
        screen.blit(CP_Text, (500,90))
        screen.blit(round_Text, (500,60))
        screen.blit(player1_Text, (500,0))
        screen.blit(player2_Text, (500,30))
        screen.blit(GS_count_Text, (500,120))
        screen.blit(SM_count_Text, (500,150))
SB = Sidebar()  #initiates an Object of Sidebar(singelton)

class Bottombar():
    def __init__(self):
        self.pos = (0,500)
        image = pygame.image.load('Pictures/Bottombar.png')
        self.image = pygame.transform.scale(image, (int(700), int(100)))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.pressed = False
        
        # needed buttons:
            #move
            #turn
            #shoot
            #fight
            #overwatch
            #guard
            #reload/clear_jam
    
    def display(self,screen):
        screen.blit(self.image, self.pos)

    def interact(self,screen):
        pass
        # if(self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1):
        #     self.pressed = True
        # if(self.pressed and pygame.mouse.get_pressed()[0] == 0):
        #     game.moveModel()
        #     self.pressed = False

BB = Bottombar()    #initiates an object of Bottombar(singelton)
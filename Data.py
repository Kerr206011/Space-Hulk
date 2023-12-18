import pygame
import random 
import sys

SM_ModellList = []                     #a list of Space Marine models
GS_ModellList = []                     #a list of Genstealer models
BL_ModellList = []

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
        #get mouse state
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

#ok bro bor
class GameStateManager:
    def __init__(self, state) -> None:
        self.state = state
        self.rev_models = []
        self.save_model = None
        self.save_tile = None
        self.turn = False
    def changestate(self,newstate):
        self.state = newstate
    def givestate(self):
        return self.state
    
gameStateManager = GameStateManager('main')

class Game:                                         #can variables be exported to individual gamestates?
    def __init__(self) -> None:
        self.Manager = gameStateManager
        self.states = {}                            #a list of gamestates that the game can have
        self.is_playing = str                       #the name of the player who is playing
        self.round = 1                              #the current round of the game
        self.player1 = ''                           #name of player 1
        self.player2 = ''                           #name of player 2
        self.selected_Model = None
        self.selected_tile = None                   #saves the selected model for other classes to interact with
        self.clicked_tile = None
        self.clicked_model = None
        self.Assault_cannon_Ammo = 10
        self.Assault_cannon_reload = True
        self.Heavy_flamer_ammo = 6
        self.CP = random.randint(1,6)               #a random number of CP for the sm player to use

    def SM_prep(self):
        self.round += 1
        for Model in SM_ModellList:
            Model.AP = 4
            self.overwatch = False
            self.guard = False
            self.jam = False
        self.CP = random.randint(1,6)

    def GS_prep(self):
        for Model in GS_ModellList:
            Model.AP = 6
        for Model in BL_ModellList:
            Model.AP = 6

    def redAP(self,Model,amount):
        if(Model in SM_ModellList):
            if(amount > Model.AP):
                Model.AP = 0
                self.CP -= (amount - Model.AP)
            else: Model.AP -= amount
        if((Model in GS_ModellList) or (Model in BL_ModellList)):
            Model.AP -= amount

    def vision(self,model,tile):
        ofset_x = 0
        ofset_y = 0
        b = False
        ofs = None
        x = tile.x
        y = tile.y
        is_looking_at_object = False
        i = 1
        seenModels = []
        match(model.face):
            case(1,0):
                ofset_x = 0
                ofset_y = 1
                ofs = (1,0)
            case(0,1):
                ofset_x = 1
                ofset_y = 0
                ofs = (0, -1)
            case(-1,0):
                ofset_x = 0
                ofset_y = 1
                ofs = (-1,0)
            case(0,-1):
                ofset_x = 1
                ofset_y = 0
                ofs = (0,1)
        runS = True
        runL1 = True
        runL2 = True
        runR1 = True
        runR2 = True
        while(runS):
            x += ofs[0]
            y += ofs[1]
            checked_tile = map[y][x]
            if(checked_tile.is_occupied == True):
                seenModels.append(checked_tile)
                x = ((tile.x) + (ofset_x) + (ofs[0]))
                y = ((tile.y) + (ofset_y) + (ofs[1]))
                runS = False
                if(i == 1):
                    is_looking_at_object = True 
                i = 1
            elif(checked_tile.is_wall == True):
                x = ((tile.x) + (ofset_x) + (ofs[0]))
                y = ((tile.y) + (ofset_y) + (ofs[1]))
                runS = False
                if(i == 1):
                    is_looking_at_object = True
                i = 1
            else:
                i += 1
        if(is_looking_at_object):
            match(model.face):
                case((1,0)):
                    if((map[tile.y + 1][tile.x].is_wall) or (map[tile.y + 1][tile.x].is_occupied)):
                        runL1 = False
                        runL2 = False
                    if((map[tile.y -1][tile.x].is_wall) or (map[tile.y -1][tile.x].is_occupied)):
                        runR1 = False
                        runR2 = False
                case((0,1)):
                    if((map[tile.y][tile.x -1].is_wall) or (map[tile.y][tile.x -1].is_occupied)):
                        runL1 = False
                        runL2 = False
                    if((map[tile.y][tile.x +1].is_wall) or (map[tile.y][tile.x +1].is_occupied)):
                        runR1 = False
                        runR2 = False
                case((-1,0)):
                    if((map[tile.y -1][tile.x].is_wall) or (map[tile.y -1][tile.x].is_occupied)):
                        runL1 = False
                        runL2 = False
                    if((map[tile.y +1][tile.x].is_wall) or (map[tile.y +1][tile.x].is_occupied)):
                        runR1 = False
                        runR2 = False
                case((0,-1)):
                    if((map[tile.y][tile.x +1].is_wall) or (map[tile.y][tile.x +1].is_occupied)):
                        runL1 = False
                        runL2 = False
                    if((map[tile.y][tile.x -1].is_wall) or (map[tile.y][tile.x -1].is_occupied)):
                        runR1 = False
                        runR2 = False
        while(runL1):
            checked_tile = map[y][x]
            if(checked_tile.is_occupied):
                seenModels.append(checked_tile)
                if(i == 1):
                    b = True
                    runL2 = False
            elif(checked_tile.is_wall):
                runL1 = False
                if((i == 1) or (b)):
                    runL2 = False
                    x = ((tile.x) - (ofset_x) + (ofs[0]))
                    y = ((tile.y) - (ofset_y) + (ofs[1]))
                else:
                    x = tile.x + (2 * ofset_x) + (2 * ofs[0])
                    y = tile.y + (2 * ofset_y) + (2 * ofs[1])
                i = 1
                b = False
            if((map[(checked_tile.y)+(ofset_y)][(checked_tile.x)+(ofset_x)].is_wall) and (map[(checked_tile.y)-(ofset_y)][(checked_tile.x)-(ofset_x)].is_wall)):
                runL1 = False
                if((i == 1) or (b)):
                    runL2 = False
                    x = ((tile.x) - (ofset_x) + (ofs[0]))
                    y = ((tile.y) - (ofset_y) + (ofs[1]))
                else:
                    x = tile.x + (2 * ofset_x) + (2 * ofs[0])
                    y = tile.y + (2 * ofset_y) + (2 * ofs[1])
                i = 1
                b = False
            if(runL1):
                x += ofs[0]
                y += ofs[1]
                i +=1
            if(is_looking_at_object):
                runL1 = False
                x = ((tile.x) + (2 * ofset_x) + (2 * ofs[0]))
                y = ((tile.y) + (2 * ofset_y) + (2 * ofs[1]))
                if(checked_tile.is_occupied):
                    runL2 = False
                    x = ((tile.x) - (ofset_x) + (ofs[0]))
                    y = ((tile.y) - (ofset_y) + (ofs[1]))
                if(checked_tile.is_wall):
                    runL2 = False
                    x = ((tile.x) - (ofset_x) + (ofs[0]))
                    y = ((tile.y) - (ofset_y) + (ofs[1]))
                i = 1
        while(runL2):
            checked_tile = map[y][x]
            if(checked_tile.is_occupied):
                seenModels.append(checked_tile)
            elif(checked_tile.is_wall):
                runL2 = False
                x = ((tile.x) - (ofset_x) + (ofs[0]))
                y = ((tile.y) - (ofset_y) + (ofs[1]))
            if((map[(checked_tile.y)+(ofset_y)][(checked_tile.x)+(ofset_x)].is_wall) and (map[(checked_tile.y)-(ofset_y)][(checked_tile.x)-(ofset_x)].is_wall)):
                runL2 = False
                x = ((tile.x) - (ofset_x) + (ofs[0]))
                y = ((tile.y) - (ofset_y) + (ofs[1]))
            if(runL2):
                x += ofs[0]
                y += ofs[1]
            if(is_looking_at_object):
                runL2 = False
                x = ((tile.x) - (ofset_x) + (ofs[0]))
                y = ((tile.y) - (ofset_y) + (ofs[1]))
        while(runR1):
            checked_tile = map[y][x]
            if(checked_tile.is_occupied):
                seenModels.append(checked_tile)
                if(i == 1):
                    b = True
            elif(checked_tile.is_wall):
                runR1 = False
                if((i == 1) or (b)):
                    runR2 = False
                else:
                    x = ((tile.x) - (2 * ofset_x) + (2 * ofs[0]))
                    y = ((tile.y) - (2 * ofset_y) + (2 * ofs[1]))
            if((map[(checked_tile.y)+(ofset_y)][(checked_tile.x)+(ofset_x)].is_wall) and (map[(checked_tile.y)-(ofset_y)][(checked_tile.x)-(ofset_x)].is_wall)):
                runR1 = False
                if((i == 1) or (b)):
                    runR2 = False
                else:
                    x = ((tile.x) - (2 * ofset_x) + (2 * ofs[0]))
                    y = ((tile.y) - (2 * ofset_y) + (2 * ofs[1]))
            if(runR1):
                x += ofs[0]
                y += ofs[1]
                i += 1
            if(is_looking_at_object):
                runR1 = False
                x = ((tile.x) - (2 * ofset_x) + (2 * ofs[0]))
                y = ((tile.y) - (2 * ofset_y) + (2 * ofs[1]))
                if(checked_tile.is_occupied):
                    runR2 = False
                if(checked_tile.is_wall):
                    runR2 = False
        while(runR2):
            checked_tile = map[y][x]
            if(checked_tile.is_occupied):
                seenModels.append(checked_tile)
            elif(checked_tile.is_wall):
                runR2 = False
            if((map[(checked_tile.y)+(ofset_y)][(checked_tile.x)+(ofset_x)].is_wall) and (map[(checked_tile.y)-(ofset_y)][(checked_tile.x)-(ofset_x)].is_wall)):
                runR2 = False
            if(runR2):
                x += ofs[0]
                y += ofs[1]
            if(is_looking_at_object):
                runR2 = False
        for tile in seenModels:
            if(tile.occupand in SM_ModellList):
                seenModels.remove(model)
        return(seenModels)

    def shoot(self):
        liste = game.vision(self.selected_Model,self.selected_tile)
        print(liste)
        hit = False
        if(self.clicked_model != None):
            if((self.clicked_tile in liste) and (self.clicked_model in GS_ModellList)):
                match(self.selected_Model.weapon):
                    case('fist'):
                        a = random.randint(1,6)
                        b = random.randint(1,6)
                        c = 0
                        print(a,b,c)
                    case('AssaultCanon'):
                        if(game.Assault_cannon_Ammo != 0):
                            a = random.randint(1,6)
                            b = random.randint(1,6)
                            c = random.randint(1,6)
                            game.Assault_cannon_Ammo -= 1
                            print(a,b,c)
                if((c == 0) and (((a == 6) or (b == 6)) or ((self.selected_Model.susf) and ((a >= 5) or (b >= 5))))):
                    hit = True
                elif((c != 0) and (((a >= 5) or (b >= 5) or (c >=5)) or ((self.selected_Model.susf) and ((a >= 4) or (b >= 4) (c >= 4))))):
                    hit = True
                elif(((a == b) or (a == c) or (c == b)) and (self.is_playing == self.player2)):
                    game.selected_Model.jam = True
                else:
                    game.selected_Model.susf = True

            if(hit):
                GS_ModellList.remove(game.clicked_model)
                game.clicked_model = None
                game.clicked_tile.is_occupied = False
                game.clicked_tile.occupand = None
                game.clicked_tile = None

    def melee(self):
        facing = False
        SM1 = 0
        SM2 = 0
        GS1 = random.randint(1,6)
        GS2 = random.randint(1,6)
        GS3 = random.randint(1,6)
        if((self.selected_tile != None) & (self.clicked_tile != None)):
            if(((self.selected_tile.x + self.selected_Model.face[0]) == self.clicked_tile.x) & ((self.selected_tile.y + self.selected_Model.face[1]) == self.clicked_tile.y)):
                if(self.selected_tile.is_occupied == True):
                    match(self.selected_Model.face):
                        case((1,0)):
                            if(self.clicked_model.face == (-1,0)):
                                facing = True
                        case((-1,0)):
                            if(self.clicked_model.face == (1,0)):
                                facing = True
                        case((0,1)):
                            if(self.clicked_model.face == (0,-1)):
                                facing = True
                        case((0,-1)):
                            if(self.clicked_model.face == (0,1)):
                                facing = True
                    if(self.is_playing == self.player1):
                        game.redAP(game.selected_Model, 1)
                        match(self.selected_Model.weapon):
                            case('fist'):
                                SM1 = random.randint(1,6)
                        if(self.selected_Model.rank == 'sergeant'):
                            SM1 += 1
                        if(((SM1 > GS1) & (SM1 > GS2) & (SM1 > GS3)) or ((SM2 > GS1) & (SM2 > GS2) & (SM2 > GS3))):
                            self.clicked_tile.is_occupied = False
                            self.clicked_tile.occupand = None
                            GS_ModellList.remove(self.clicked_model)
                            self.clicked_model = None
                        elif((facing == True) & (((GS1 > SM1) & (GS1 > SM2)) or ((GS2 > SM1) & (GS2 > SM2)) or ((GS3 > SM1) & (GS3 > SM2)))):
                            self.selected_tile.is_occupied = False
                            self.selected_tile.occupand = None
                            SM_ModellList.remove(self.selected_Model)
                            self.selected_Model = None
                    if(self.is_playing == self.player2):
                        game.redAP(game.selected_Model, 1)
                        match(self.clicked_model.weapon):
                            case('fist'):
                                SM1 = random.randint(1,6)
                        if(self.clicked_model.rank == 'sergeant'):
                            SM1 += 1
                        if(((GS1 > SM1) & (GS1 > SM2)) or ((GS2 > SM1) & (GS2 > SM2)) or ((GS3 > SM1) & (GS3 > SM2))):
                            self.clicked_tile.is_occupied = False
                            self.clicked_tile.occupand = None
                            SM_ModellList.remove(self.clicked_model)
                            self.cicked_model = None
                        elif((facing == True) & (((SM1 > GS1) & (SM1 > GS2) & (SM1 > GS3)) or ((SM2 > GS1) & (SM2 > GS2) & (SM2 > GS3)))):
                            self.selected_tile.is_occupied = False
                            self.selected_tile.occupand = None
                            GS_ModellList.remove(self.selected_Model)
                            self.selected_Model = None
                    print(GS1,GS2,GS3,SM1,SM2)

    def reveal(self, tile):
        self.selected_Model = tile.occupand
        self.selected_tile = tile
        self.Manager.changestate('reveal')
        self.run()
                
    def moveModel(self):
        a = False
        b = False
        match(game.selected_Model.face):
            case(1,0):
                ofset_x = 0
                ofset_y = 1
            case(0,1):
                ofset_x = 1
                ofset_y = 0
            case(-1,0):
                ofset_x = 0
                ofset_y = 1
            case(0,-1):
                ofset_x = 1
                ofset_y = 0
        ofs = game.selected_Model.face
        if((self.clicked_tile != None) & (self.selected_tile != None) & (self.selected_Model != None)): 
            if(self.clicked_tile.is_occupied == False):
                a = True
            if((self.is_playing == self.player1) & (self.selected_Model in SM_ModellList)):
                if(((self.selected_tile.x + ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y + ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                    if((self.selected_Model.AP != 0) | (self.CP != 0)):
                        self.redAP(self.selected_Model, 1,) 
                        b = True
                elif((self.selected_tile.x - ofs[0] == self.clicked_tile.x) or (self.selected_tile.y - ofs[1] == self.clicked_tile.y)):
                    if(self.selected_Model.AP + self.CP >= 2):
                        self.redAP(self.selected_Model, 2)
                        b = True
                if(self.clicked_tile.is_wall == True):
                    b = False
            if((self.is_playing == self.player2) & ((self.selected_Model in GS_ModellList) or (self.selected_Model in BL_ModellList))):
                if(((self.selected_tile.x + ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y + ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                    if(self.selected_Model.AP != 0):
                        self.redAP(self.selected_Model, 1,) 
                        b = True
                elif(((self.selected_tile.x - ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y - ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                    if(self.selected_Model in GS_ModellList):
                        if(self.selected_Model.AP >= 2):
                            self.redAP(self.selected_Model, 2)
                            b = True
                    if(self.selected_Model in BL_ModellList):
                        if(self.selected_Model.AP != 0):
                            self.redAP(self.selected_Model, 1)
                            b = True
                elif((self.selected_tile.x + ofset_x == self.clicked_tile.x) or (self.selected_tile.x - ofset_x == self.clicked_tile.x) or (self.selected_tile.y + ofset_y == self.clicked_tile.y) or (self.clicked_tile.y - ofset_y == self.clicked_tile.y)):
                    if(self.selected_Model.AP != 0):
                        self.redAP(self.selected_Model, 1)
                        b = True
                if(self.clicked_tile.is_wall == True):
                    b = False
        if(a & b):
            self.Manager.save_model = self.selected_Model
            self.Manager.save_tile = self.selected_tile

            game.clicked_tile.occupand = game.selected_tile.occupand
            game.selected_tile.is_occupied = False
            game.clicked_tile.is_occupied = True
            game.selected_tile.occupand = None
            game.selected_tile = game.clicked_tile
            game.clicked_tile = None

            if(self.is_playing == self.player1):
                self.Manager.save_model = None
                self.Manager.save_tile = None
                lis = game.vision(self.selected_Model, self.selected_tile)
                for tile in lis:
                    if(tile.occupand in SM_ModellList):
                        lis.remove(tile)
                    if(tile.occupand in BL_ModellList):
                        self.Manager.rev_models.append(tile)
                        lis.remove(tile)
                self.selected_Model.susf = False
                if(self.Manager.rev_models.__len__() != 0):
                    self.Manager.save_model = self.selected_Model
                    self.Manager.save_tile = self.selected_tile
                    self.reveal(self.Manager.rev_models[0])
                elif(lis != []):
                    self.Manager.changestate('shoot')
                    game.run()
            elif(self.is_playing == self.player2):
                if(self.selected_Model in GS_ModellList):
                    self.clicked_model = self.selected_Model
                    self.clicked_tile = self.selected_tile
                    e = True
                    for row in map: 
                        for tile in row:
                            if(tile.occupand in SM_ModellList):
                                if(tile.occupand.overwatch == True):
                                    checked = self.vision(tile.occupand, tile)
                                    if((tile.occupand.jam == False) & (self.clicked_tile in checked)):
                                        self.selected_Model = tile.occupand
                                        self.selected_tile = tile
                                        self.shoot()
                    # if(e):
                    #     self.clicked_model = None
                    #     self.clicked_tile = None
                    #     self.selected_Model = self.Manager.save_model
                    #     self.Manager.save_model = None
                    #     self.selected_tile = self.Manager.save_tile
                    #     self.Manager.save_tile = None
                                
                if(self.selected_Model in BL_ModellList):
                    c = False
                    for row in map:
                        for tile in row:
                            if(tile.occupand in SM_ModellList):
                                seen = self.vision(tile.occupand, tile)
                                for model in seen:
                                    if(model == self.selected_tile):
                                        c = True
                    if(c):
                        self.selected_tile.is_occupied = False
                        self.Manager.save_tile.occupand = self.Manager.save_model
                        self.selected_tile.occupand = None
                        self.Manager.save_tile.is_occupied = True
                        self.selected_tile = self.Manager.save_tile
                        self.selected_Model = self.Manager.save_model
                        self.Manager.save_model = None
                        self.Manager.save_tile = None
                        c = False

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
        self.turnright_button = Button(320, 200, self.move_image, 1)
        self.turnleft_button = Button(160, 200, self.move_image, 1)
        self.noturn_button = Button(240, 200, self.move_image, 1)
        while(True):
            pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit
            if(self.turnleft_button.draw(screen)):
                match(game.selected_Model.face):
                    case(1,0): game.selected_Model.face = (0,1)
                    case(0,1): game.selected_Model.face = (-1,0)
                    case(-1,0): game.selected_Model.face = (0,-1)
                    case(0,-1): game.selected_Model.face = (1,0)
                game.redAP(game.selected_Model,1)
                pressed = True

            if(self.turnright_button.draw(screen)):
                match(game.selected_Model.face):
                    case(1,0): game.selected_Model.face = (0,-1)
                    case(0,1): game.selected_Model.face = (1,0)
                    case(-1,0): game.selected_Model.face = (0,1)
                    case(0,-1): game.selected_Model.face = (-1,0)
                game.redAP(game.selected_Model,1)
                pressed = True

            if(self.noturn_button.draw(screen)):
                pressed = True
            if(pressed):
                if(game.is_playing == game.player1):
                    self.gameStateManager.changestate('runP1')
                    game.run()
                else:
                    self.gameStateManager.changestate('runP2')
                    game.run()

            pygame.display.update()
            
class gamestateNewGame:
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
                        elif((game.player2 != None) and (game.player2 != game.player1)):
                            game.is_playing = game.player1
                            self.gameStateManager.changestate('runP1')
                            game.run()

            # Clear the screen
            screen.fill((50, 50, 50))

            # Render the input string
            if(p1):
                text_surface = font.render(game.player1, True, (0, 0, 0))
            else:
                text_surface = font.render(game.player2, True, (0,0,0))
            screen.blit(text_surface, (50, 50))
            pygame.display.update()

class Player1Turn:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        self.changeturn_button = Button(120, 500, self.move_image, 1)
        self.shoot_button = Button(180, 500, self.move_image, 1)
        self.melee_button = Button(240, 500, self.move_image, 1)
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
                if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                    game.moveModel()

            if(self.turn_button.draw(screen)):
                if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                    if((game.selected_Model.AP != 0) or ((game.is_playing == game.player1) and (game.CP != 0))):
                        self.Manager.changestate('turn')
                        game.run()
                    else:print('no AP/CP')
                else:print('anderes model wählen')
            
            if(self.changeturn_button.draw(screen)):
                game.is_playing = game.player2
                game.GS_prep()
                print(self.Manager.givestate())
                print(game.is_playing)
                print('0')
                self.Manager.changestate('runP2')
                game.run()
            
            if(self.shoot_button.draw(screen)):
                if((game.selected_Model.AP + game.CP) != 0):
                    game.redAP(game.selected_Model, 1)
                    self.Manager.changestate('shoot')
                    game.run()
                else: print('nicht genug AP')

            if(self.melee_button.draw(screen)):
                if((game.selected_Model.AP + game.CP) != 0):
                    game.melee()
                else: print('nicht genug AP')

            pygame.display.update()

class Player2Turn:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        self.changeturn_button = Button(120, 500, self.move_image, 1)
        self.reveal_button = Button(180, 500, self.move_image, 1)
        self.melee_button = Button(240, 500, self.move_image, 1)
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
                if((game.is_playing == game.player2) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                    game.moveModel()

            if(self.turn_button.draw(screen)):
                if((game.is_playing == game.player2) and (game.selected_Model in GS_ModellList)):
                    if((game.selected_Model.AP != 0) or ((game.is_playing == game.player1) and (game.CP != 0))):
                        self.Manager.changestate('turn')
                        game.run()
                    else: print('no AP/CP')
                else:print('anderes model wählen')

            if(self.changeturn_button.draw(screen)):
                game.is_playing = game.player1
                game.SM_prep()
                print(self.Manager.givestate())
                print(game.is_playing)
                print('1')
                self.Manager.changestate('runP1')
                game.run()

            if(self.reveal_button.draw(screen)):
                if(game.selected_Model in BL_ModellList):
                    self.Manager.rev_models.append(game.selected_tile)
                    game.reveal(game.selected_tile)

            if(self.melee_button.draw(screen)):
                if(game.selected_Model in GS_ModellList):
                    if(game.selected_Model.AP != 0):
                        game.melee()

            pygame.display.update()

class gamestate_shoot:
    def __init__(self) -> None:
        self.manager = gameStateManager
    
    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.shoot_button = Button(60, 500, self.move_image, 1)
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

            if(self.shoot_button.draw(screen)):
                game.shoot()
                if(game.is_playing == game.player1):
                   self.manager.changestate('runP1')
                   game.run()
                else:
                    self.manager.changestate('runP2')
                    game.run()

            pygame.display.update()

class gamestate_Main:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        main_image = pygame.image.load('pictures/Main_Screen.png')
        screen.blit(main_image, (0,0))
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.start_new_button = Button(60, 250, self.move_image, 1)
        self.start_saved_button = Button(120, 250, self.move_image, 1)
        self.options_button = Button(180, 250, self.move_image, 1)
        self.quit_button = Button(240, 250, self.move_image, 1)
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if(self.start_new_button.draw(screen)):
                self.Manager.changestate('start')
                game.run()
            
            if(self.quit_button.draw(screen)):
                pygame.quit()
                sys.exit()
            
            pygame.display.update()

class gamestate_reveal:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.reveal_button = Button(60, 500, self.move_image, 1)

        self.revModel = game.selected_Model
        self.amount = self.revModel.count
        self.tile = game.selected_tile

        self.tile.is_occupied = False
        BL_ModellList.remove(self.tile.occupand)
        self.tile.occupand = Genestealer()
        self.tile.is_occupied = True
        GS_ModellList.append(self.tile.occupand)
        self.amount -= 1
        print(self.amount)
        self.Manager.rev_models.remove(self.tile)

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

            if(self.reveal_button.draw(screen)):
                if(game.clicked_tile != None):
                    if(((game.clicked_tile.x == game.selected_tile.x) or (game.clicked_tile.x == (game.selected_tile.x -1)) or (game.clicked_tile.x == (game.selected_tile.x +1))) and ((game.clicked_tile.y == game.selected_tile.y) or (game.clicked_tile.y == (game.selected_tile.y -1)) or (game.clicked_tile.y == (game.selected_tile.y +1)))):
                        if(game.clicked_tile.is_occupied == False):
                            game.clicked_tile.occupand = Genestealer()
                            GS_ModellList.append(game.clicked_tile.occupand)
                            game.clicked_tile.is_occupied = True
                            self.amount -= 1

            if(self.amount == 0):
                if(self.Manager.rev_models == []):
                    if(game.is_playing == game.player1):
                        game.selected_tile = self.Manager.save_tile
                        game.selected_Model = self.Manager.save_model
                        self.Manager.changestate('shoot')
                        game.run()
                    else: 
                        self.Manager.changestate('runP2')
                        game.run()
                else:
                    game.reveal(self.Manager.rev_models[1])

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
        self.is_entrypoint = False
        self.is_door = False
        self.is_open = False

    def render(self, screen):
        if(self.is_wall): 
            image = pygame.image.load('Pictures/Wall.png')
            self.image = pygame.transform.scale(image,(self.size,self.size))
        if(self.is_door):
            if((map[self.y+1][self.x].is_wall == True) and (map[self.y-1][self.x].is_wall == True)):
                if(self.is_open == False):
                    image = pygame.image.load('Pictures/Door.png')
                    self.image = pygame.transform.scale(image,(self.size,self.size))
                else:
                    image = pygame.image.load('Pictures/Door_open.png')
                    self.image = pygame.transform.scale(image,(self.size,self.size))
            else:
                if(self.is_open == False):
                    image = pygame.image.load('Pictures/Door.png')
                    imagen = pygame.transform.scale(image,(self.size,self.size))
                    self.image = pygame.transform.rotate(imagen,90)
                else:
                    image = pygame.image.load('Pictures/Door_open.png')
                    imagen = pygame.transform.scale(image,(self.size,self.size))
                    self.image = pygame.transform.rotate(imagen,90)
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
            if(((self.is_occupied) and (self.occupand in SM_ModellList) and (game.is_playing == game.player1)) or ((self.is_occupied) and ((self.occupand in GS_ModellList) or (self.occupand in BL_ModellList)) and (game.is_playing == game.player2))):
                game.selected_Model = self.occupand
                game.selected_tile = self
            elif(self.is_occupied):
                    game.clicked_model = self.occupand
                    print(self.occupand)
                    game.clicked_tile = self
            else:
                game.clicked_tile = self
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
        self.susf = False
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
        GS_count_Text = my_font.render('GS Models: '+str((len(GS_ModellList)+len(BL_ModellList))),False,(0,0,0))
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
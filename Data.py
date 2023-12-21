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

class GameStateManager:
    def __init__(self, state) -> None:
        self.state = state
        self.rev_models = []
        self.save_model = None
        self.save_tile = None
        self.rev_count = 0
        self.turn = False
        self.melee_turn = False
        self.gs_moveturn = False
        self.gs_turnaftermove = None
        self.sections = []
        self.ooc = False
        self.ooc_models = []
    def changestate(self, newstate):
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
        self.selected_Model = None
        self.selected_tile = None
        self.clicked_model = None
        self.clicked_tile = None
        self.round += 1
        for Model in SM_ModellList:
            Model.AP = 4
            self.overwatch = False
            self.guard = False
            self.jam = False
        self.CP = random.randint(1,6)
        self.Manager.ooc = False
        self.Manager.ooc_models = []
        for row in map:
            for tile in row:
                tile.is_buring = False
        for row in map: 
            for tile in row:
                if(tile.occupand in SM_ModellList):
                    checked = self.vision(tile.occupand, tile)
                    for tile in checked:
                        if(tile.occupand in BL_ModellList):
                            self.Manager.rev_models.append(tile)
                            checked.remove(tile)
                    if(self.Manager.rev_models.__len__() != 0):
                        self.Manager.save_model = self.selected_Model
                        self.Manager.save_tile = self.selected_tile
                        self.reveal(self.Manager.rev_models[0])

    def GS_prep(self):
        self.selected_Model = None
        self.selected_tile = None
        self.clicked_model = None
        self.clicked_tile = None
        for Model in GS_ModellList:
            Model.AP = 6
        for Model in BL_ModellList:
            Model.AP = 6
        for Model in SM_ModellList:
            Model.AP = 0

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
                ofs = (0, 1)
            case(-1,0):
                ofset_x = 0
                ofset_y = 1
                ofs = (-1,0)
            case(0,-1):
                ofset_x = 1
                ofset_y = 0
                ofs = (0,-1)
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
            elif((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
                x = ((tile.x) + (ofset_x) + (ofs[0]))
                y = ((tile.y) + (ofset_y) + (ofs[1]))
                runS = False
                if(i == 1):
                    is_looking_at_object = True
                i = 1
            else:
                i += 1
                seenModels.append(checked_tile)
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
            if((checked_tile.is_occupied == True) or ((checked_tile.is_entrypoint == False) and (checked_tile.is_wall == False) and (checked_tile.is_buring == False) and ((checked_tile.is_door == False) or (checked_tile.is_open == True)))):
                seenModels.append(checked_tile)
                if((i == 1) and (checked_tile.is_occupied == True)):
                    b = True
                    runL2 = False
            elif((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
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
                if((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
                    runL2 = False
                    x = ((tile.x) - (ofset_x) + (ofs[0]))
                    y = ((tile.y) - (ofset_y) + (ofs[1]))
                i = 1
        while(runL2):
            checked_tile = map[y][x]
            if((checked_tile.is_occupied == True) or ((checked_tile.is_entrypoint == False) and (checked_tile.is_wall == False) and (checked_tile.is_buring == False) and ((checked_tile.is_door == False) or (checked_tile.is_open == True)))):
                seenModels.append(checked_tile)
            elif((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
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
            if((checked_tile.is_occupied == True) or ((checked_tile.is_entrypoint == False) and (checked_tile.is_wall == False) and (checked_tile.is_buring == False) and ((checked_tile.is_door == False) or (checked_tile.is_open == True)))):
                seenModels.append(checked_tile)
                if((i == 1) and (checked_tile.is_occupied == True)):
                    b = True
                    runR2 = False
            elif((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
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
                if((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
                    runR2 = False
        while(runR2):
            checked_tile = map[y][x]
            if((checked_tile.is_occupied == True) or ((checked_tile.is_entrypoint == False) and (checked_tile.is_wall == False) and (checked_tile.is_buring == False) and ((checked_tile.is_door == False) or (checked_tile.is_open == True)))):
                seenModels.append(checked_tile)
            elif((checked_tile.is_buring == True) or (checked_tile.is_wall == True) or ((checked_tile.is_door == True) and (checked_tile.is_open == False)) or (checked_tile.is_entrypoint)):
                runR2 = False
            if((map[(checked_tile.y)+(ofset_y)][(checked_tile.x)+(ofset_x)].is_wall) and (map[(checked_tile.y)-(ofset_y)][(checked_tile.x)-(ofset_x)].is_wall)):
                runR2 = False
            if(runR2):
                x += ofs[0]
                y += ofs[1]
            if(is_looking_at_object):
                runR2 = False
        
        return(seenModels)

    def distance(self,tiles, tilee):
        x = tiles.x - tilee.x
        y = tiles.y - tilee.y
        z = x+y
        distance = abs(z)
        return distance
    
    def shoot(self):
        if(self.selected_Model in SM_ModellList):
            liste = game.vision(self.selected_Model,self.selected_tile)
            print(liste)
            hit = False
            match(self.selected_Model.weapon):
                case('fist'):
                    a = random.randint(1,6)
                    b = random.randint(1,6)
                    c = 0
                    print(a,b,c)
                case('powerSword'):
                    a = random.randint(1,6)
                    b = random.randint(1,6)
                    c = 0
                case('chainFist'):
                    a = random.randint(1,6)
                    b = random.randint(1,6)
                    c = 0
                case('AssaultCanon'):
                    if(game.Assault_cannon_Ammo != 0):
                        a = random.randint(1,6)
                        b = random.randint(1,6)
                        c = random.randint(1,6)
                        game.Assault_cannon_Ammo -= 1
                        print(a,b,c)
                case('claws'):
                    a = 0
                    b = 0
                    c = 0
                case('flamer'):
                    a = 0
                    b = 0
                    c = 0
                    burn = None
                    door = False
                    if(self.Heavy_flamer_ammo != 0):
                        if((self.clicked_tile in liste) and (self.distance(self.selected_tile, self.clicked_tile) < 13)):
                            self.Heavy_flamer_ammo -= 1
                            self.redAP(self.selected_Model, 2)
                            self.selected_Model.guard = False
                            for section in self.Manager.sections:
                                for tile in section:
                                    if(tile == self.clicked_tile):
                                        burn = section
                            if(burn != None):
                                for tile in burn:
                                    if(isinstance(tile,Tile)):
                                        if((tile.is_door) and (tile.is_open == False)):
                                            door = True
                            if(door):
                                for obj in burn:
                                    if(isinstance(obj, list)):
                                        if(self.clicked_tile in obj):
                                            burn = obj
                                            break
                            if(burn != None):
                                for tile in burn:
                                    if(isinstance(tile,Tile)):
                                        roll = random.randint(1,6)
                                        if((roll > 1) and (tile.is_occupied == True)):
                                            tile.is_occupied = False
                                            if(tile.occupand in SM_ModellList):
                                                SM_ModellList.remove(tile.occupand)
                                            elif(tile.occupand in GS_ModellList):
                                                GS_ModellList.remove(tile.occupand)
                                            elif(tile.occupand in BL_ModellList):
                                                BL_ModellList.remove(tile.occupand)
                                        tile.is_buring = True
            if(self.selected_Model.overwatch == True):
                if(((a == b) and not (c != 0)) and (self.is_playing == self.player2)):
                    game.selected_Model.jam = True
            if(self.clicked_model != None) :
                if((self.clicked_tile in liste) and (self.clicked_model in GS_ModellList)):
                    if(self.selected_Model.weapon != 'flamer'):
                        self.redAP(self.selected_Model, 1)
                        self.selected_Model.guard = False
                    if((c == 0) and (((a == 6) or (b == 6)) or ((self.selected_Model.susf) and ((a >= 5) or (b >= 5))))):
                        hit = True
                    elif((c != 0) and (((a >= 5) or (b >= 5) or (c >=5)) or ((self.selected_Model.susf) and ((a >= 4) or (b >= 4) or (c >= 4))))):
                        hit = True
                    elif(((a == b) and not (c != 0)) and (self.is_playing == self.player2)):
                        game.selected_Model.jam = True
                    else:
                        game.selected_Model.susf = True

                if(hit):
                    GS_ModellList.remove(game.clicked_model)
                    game.clicked_model = None
                    game.clicked_tile.is_occupied = False
                    game.clicked_tile.occupand = None
                    game.clicked_tile = None
            if(self.clicked_tile != None):
                if((self.clicked_tile.is_door == True) and (self.clicked_tile.is_open == False)):
                    if((self.selected_Model.weapon == 'fist') or (self.selected_Model.weapon == 'powerSword') or (self.selected_Model.weapon == 'chainFist')):
                        if((a == 6) or (b == 6) or (c == 6)):
                            self.clicked_tile.is_door = False

        for row in map: 
            for tile in row:
                if(tile.occupand in SM_ModellList):
                    checked = self.vision(tile.occupand, tile)
                    for tile in checked:
                        if(tile.occupand in BL_ModellList):
                            self.Manager.rev_models.append(tile)
                            checked.remove(tile)
                    if(self.Manager.rev_models.__len__() != 0):
                        self.Manager.save_model = self.selected_Model
                        self.Manager.save_tile = self.selected_tile
                        self.reveal(self.Manager.rev_models[0])

    def ocDoor(self):
        a = False
        if(self.clicked_tile != None):
            if(self.clicked_tile.is_door == True):
                if((self.selected_Model != None) and (self.clicked_tile.is_occupied == False)):
                    ofs = game.selected_Model.face
                    if(((self.selected_tile.x + ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y + ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                        if(self.is_playing == self.player1):
                            if((self.selected_Model.AP != 0) | (self.CP != 0)):
                                self.redAP(self.selected_Model, 1)
                                self.selected_Model.guard = False
                                a = True
                        if(self.is_playing == self.player2):
                            if(self.selected_Model.AP != 0):
                                self.redAP(self.selected_Model, 1)
                                a = True
                                for row in map: 
                                    for tile in row:
                                        if(tile.occupand in SM_ModellList):
                                            checked = self.vision(tile.occupand, tile)
                                            if(self.selected_tile in checked):
                                                if(self.CP != 0):
                                                    self.Manager.ooc = True
                                                    self.Manager.ooc_models.append(tile.occupand)
                                            # if(tile.occupand.overwatch == True):
                                            #     if((tile.occupand.jam == False) & (self.clicked_tile in checked)):
                                            #         self.selected_Model = tile.occupand
                                            #         self.selected_tile = tile
                                            #         self.shoot()
                                
                if(map[self.clicked_tile.y +1][self.clicked_tile.x].is_buring):
                    a = False
                elif(map[self.clicked_tile.y - 1][self.clicked_tile.x].is_buring):
                    a = False
                elif(map[self.clicked_tile.y][self.clicked_tile.x + 1].is_buring):
                    a = False
                elif(map[self.clicked_tile.y][self.clicked_tile.x - 1].is_buring):
                    a = False

        if(a):
            if(self.clicked_tile.is_open == True):
                self.clicked_tile.is_open = False
            else:
                self.clicked_tile.is_open = True
        for row in map: 
            for tile in row:
                if(tile.occupand in SM_ModellList):
                    checked = self.vision(tile.occupand, tile)
                    for tile in checked:
                        if(tile.occupand in BL_ModellList):
                            self.Manager.rev_models.append(tile)
                            checked.remove(tile)
                    if(self.Manager.rev_models.__len__() != 0):
                        self.Manager.save_model = self.selected_Model
                        self.Manager.save_tile = self.selected_tile
                        self.reveal(self.Manager.rev_models[0])
                
    def melee(self):
        facing = False
        SM1 = 0
        SM2 = 0
        GS1 = random.randint(1,6)
        GS2 = random.randint(1,6)
        GS3 = random.randint(1,6)
        if((self.selected_tile != None) & (self.clicked_tile != None)):
            if((self.clicked_tile.is_door == True) and (self.clicked_tile.is_open == False)):
                self.redAP(self.selected_Model, 1)
                if(self.is_playing == self.player1):
                    match(self.selected_Model.weapon):
                        case('fist'):
                            SM1 = random.randint(1,6)
                        case('powerSword'):
                            SM1 = random.randint(1,6)
                        case('chainFist'):
                            SM1 = 6
                        case('AssaultCanon'):
                            SM1 = random.randint(1,6)
                        case('claws'):
                            SM1 = random.randint(1,6)
                            SM2 = random.randint(1,6)
                            if(SM1 > SM2):
                                SM1 += 1
                            else:
                                SM2 += 1
                        case('flamer'):
                            SM1 = random.randint(1,6)
                    if(self.selected_Model.rank == 'sergeant'):
                        SM1 += 1
                        if(SM2 != 0):
                            SM2 += 1
                    if((SM1 >= 6) or (SM2 >= 6)):
                        self.clicked_tile.is_door = False
                if(self.is_playing == self.player2):
                    if((GS1 >= 6) or (GS2 >= 6) or (GS3 >= 6)):
                        self.clicked_tile.is_door = False
                print(GS1,GS2,GS3,SM1,SM2)
            elif(self.clicked_model != None):
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
                            if(self.clicked_model in GS_ModellList):
                                game.redAP(game.selected_Model, 1)
                                self.selected_Model.guard = False
                                match(self.selected_Model.weapon):
                                    case('fist'):
                                        SM1 = random.randint(1,6)
                                    case('chainFist'):
                                        SM1 = random.randint(1,6)
                                    case('AssaultCanon'):
                                        SM1 = random.randint(1,6)
                                    case('flamer'):
                                        SM1 = random.randint(1,6)
                                    case('powerSword'):
                                        SM1 = random.randint(1,6)
                                        print(GS1,GS2,GS3,SM1,SM2)  
                                        if(((SM1 < GS1) or (SM1 < GS2) or (SM1 < GS3)) or ((SM2 > SM1) and ((SM2 < GS1) or (SM2 < GS2) or (SM2 < GS3)))):
                                            if((GS1 > GS2) and (GS1 > GS3)):
                                                GS1 = random.randint(1,6)
                                            elif((GS2 > GS1) and (GS2 > GS3)):
                                                GS2 = random.randint(1,6)
                                            else:
                                                GS3 = random.randint(1,6)
                                    case('claws'):
                                        SM1 = random.randint(1,6)
                                        SM2 = random.randint(1,6)
                                        if(SM1 > SM2):
                                            SM1 += 1
                                        else:
                                            SM2 += 1
                                if(self.selected_Model.rank == 'sergeant'):
                                    SM1 += 1
                                    if(SM2 != 0):
                                        SM2 += 1
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
                                else:
                                    print(GS1,GS2,GS3,'|',SM1,SM2)  
                                    self.Manager.melee_turn = True
                                    self.Manager.changestate('turn')
                                    self.run()

                        if(self.is_playing == self.player2):
                            if(self.clicked_model in SM_ModellList):
                                game.redAP(game.selected_Model, 1)
                                match(self.clicked_model.weapon):
                                    case('fist'):
                                        SM1 = random.randint(1,6)
                                    case('chainFist'):
                                        SM1 = random.randint(1,6)
                                    case('AssaultCanon'):
                                        SM1 = random.randint(1,6)
                                    case('flamer'):
                                        SM1 = random.randint(1,6)
                                    case('claws'):
                                        SM1 = random.randint(1,6)
                                        if(facing):   
                                            SM2 = random.randint(1,6)
                                            if(SM1 > SM2):
                                                SM1 += 1
                                            else:
                                                SM2 += 1
                                    case('powerSword'):
                                        SM1 = random.randint(1,6)
                                        print(GS1,GS2,GS3,SM1,SM2)  
                                        if(((SM1 < GS1) or (SM1 < GS2) or (SM1 < GS3)) or ((SM2 > SM1) and ((SM2 < GS1) or (SM2 < GS2) or (SM2 < GS3)))):
                                            if((GS1 > GS2) and (GS1 > GS3)):
                                                GS1 = random.randint(1,6)
                                            elif((GS2 > GS1) and (GS2 > GS3)):
                                                GS2 = random.randint(1,6)
                                            else:
                                                GS3 = random.randint(1,6)
                                if(self.clicked_model.rank == 'sergeant'):
                                    SM1 += 1
                                    if(SM2 != 0):
                                        SM2 += 1
                                if(self.clicked_model.guard == True):
                                    if(((SM1 < GS1) or (SM1 < GS2) or (SM1 < GS3)) or ((SM2 != 0) and ((SM2 < GS1) or (SM2 < GS2) or (SM2 < GS3)))):
                                        if((SM2 > SM1) or (SM2 == 0)):
                                            SM1 = random.randint(1,6)
                                        else:
                                            SM2 = random.randint(1,6)
                                        if(self.clicked_model.rank == 'sergeant'):
                                            if((SM1 > SM2) or (SM2 == 0)):
                                                SM1 += 1
                                            else:
                                                SM2 += 1
                                        if((self.clicked_model.weapon == 'claws') and (facing)):
                                            if((SM1 > SM2) or (SM2 == 0)):
                                                SM1 += 1
                                            else:
                                                SM2 += 1
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
                                else:
                                    print(GS1,GS2,GS3,SM1,SM2)  
                                    self.Manager.melee_turn = True
                                    self.Manager.changestate('turn')
                                    self.run()

            print(GS1,GS2,GS3,SM1,SM2)                
        for row in map: 
            for tile in row:
                if(tile.occupand in SM_ModellList):
                    checked = self.vision(tile.occupand, tile)
                    for tile in checked:
                        if(tile.occupand in BL_ModellList):
                            self.Manager.rev_models.append(tile)
                            checked.remove(tile)
                    if(self.Manager.rev_models.__len__() != 0):
                        self.Manager.save_model = self.selected_Model
                        self.Manager.save_tile = self.selected_tile
                        self.reveal(self.Manager.rev_models[0])
                    print(GS1,GS2,GS3,SM1,SM2)

    def reveal(self, tile):
        self.selected_Model = tile.occupand
        self.selected_tile = tile
        self.Manager.changestate('reveal')
        self.run()
                
    def moveModel(self):
        a = False
        b = False
        c = 0
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
                        c = 1
                        b = True
                elif(((self.selected_tile.x - ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y - ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                    if(self.selected_Model.AP + self.CP >= 2):
                        c = 2
                        b = True
                if((self.clicked_tile.is_wall == True) or ((self.clicked_tile.is_door == True) and (self.clicked_tile.is_open == False)) or (self.clicked_tile.is_entrypoint == True)):
                    b = False
                if((((map[self.selected_tile.y+1][self.selected_tile.x].is_wall) or (map[self.selected_tile.y+1][self.selected_tile.x].is_occupied)) and ((map[self.selected_tile.y-1][self.selected_tile.x].is_wall) or (map[self.selected_tile.y-1][self.selected_tile.x].is_occupied))) or (((map[self.selected_tile.y][self.selected_tile.x+1].is_wall) or (map[self.selected_tile.y][self.selected_tile.x+1].is_occupied)) and ((map[self.selected_tile.y][self.selected_tile.x-1].is_wall) or (map[self.selected_tile.y][self.selected_tile.x-1].is_occupied)))):
                    print('ja')
                    if(map[self.selected_tile.y + self.selected_Model.face[1]][self.selected_tile.x + self.selected_Model.face[0]].is_occupied == True):
                        if((self.clicked_tile == map[self.selected_tile.y + ofset_y + ofs[1]][self.selected_tile.x + ofset_x + ofs[0]]) or (self.clicked_tile == map[self.selected_tile.y - ofset_y + ofs[1]][self.selected_tile.x - ofset_x + ofs[0]])):
                            print('ne')
                            b = False
                    elif(map[self.selected_tile.y - self.selected_Model.face[1]][self.selected_tile.x - self.selected_Model.face[0]].is_occupied == True):
                        if((self.clicked_tile == map[self.selected_tile.y + ofset_y - ofs[1]][self.selected_tile.x + ofset_x - ofs[0]]) or (self.clicked_tile == map[self.selected_tile.y - ofset_y - ofs[1]][self.selected_tile.x - ofset_x - ofs[0]])):
                            print('ne')
                            b = False
                if(self.clicked_tile.is_buring):
                    if(self.selected_tile.is_buring):
                        if((random.randint(1,6)) > 1):
                            self.selected_tile.is_occupied = False
                            SM_ModellList.remove(self.selected_Model)
                            self.selected_tile.occupand = None
                            b = False
                    else:
                        b = False
            if((self.is_playing == self.player2) & (self.selected_Model in BL_ModellList)):
                if((self.selected_Model in BL_ModellList) and (self.selected_tile.is_lurkingpoint == True) and (self.clicked_tile.is_entrypoint == True)):
                    if((map[self.clicked_tile.y][self.clicked_tile.x - 1].is_wall == False) and (map[self.clicked_tile.y][self.clicked_tile.x - 1].is_lurkingpoint == False)):
                        self.clicked_tile = map[self.clicked_tile.y][self.clicked_tile.x - 1]
                        if(self.clicked_tile.is_occupied):
                            a = False
                    elif((map[self.clicked_tile.y][self.clicked_tile.x + 1].is_wall == False) and (map[self.clicked_tile.y][self.clicked_tile.x + 1].is_lurkingpoint == False)):
                        self.clicked_tile = map[self.clicked_tile.y][self.clicked_tile.x + 1]
                        if(self.clicked_tile.is_occupied):
                            a = False
                    elif((map[self.clicked_tile.y - 1][self.clicked_tile.x].is_wall == False) and (map[self.clicked_tile.y - 1][self.clicked_tile.x].is_lurkingpoint == False)):
                        self.clicked_tile = map[self.clicked_tile.y - 1][self.clicked_tile.x]
                        if(self.clicked_tile.is_occupied):
                            a = False
                    else:
                        self.clicked_tile = map[self.clicked_tile.y + 1][self.clicked_tile.x]
                        if(self.clicked_tile.is_occupied):
                            a = False
                    b = True
                    if(self.clicked_tile.is_buring):
                        b = False
                    if(b):
                        c = 1

            if((self.is_playing == self.player2) & ((self.selected_Model in GS_ModellList) or (self.selected_Model in BL_ModellList)) and (self.selected_tile.is_lurkingpoint == False)):
                if(((self.selected_tile.x + ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y + ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                    if(self.selected_Model.AP != 0):
                        c = 1
                        b = True
                elif(((self.selected_tile.x - ofs[0] == self.clicked_tile.x) and (ofs[0] != 0)) or ((self.selected_tile.y - ofs[1] == self.clicked_tile.y) and (ofs[1] != 0))):
                    if(self.selected_Model in GS_ModellList):
                        if(self.selected_Model.AP >= 2):
                            c = 2
                            b = True
                    if(self.selected_Model in BL_ModellList):
                        if(self.selected_Model.AP != 0):
                            c = 1
                            b = True
                elif(((self.selected_tile.x + ofset_x == self.clicked_tile.x) and (ofset_x != 0)) or ((self.selected_tile.x - ofset_x == self.clicked_tile.x) and (ofset_x != 0)) or ((self.selected_tile.y + ofset_y == self.clicked_tile.y) and (ofset_y != 0)) or ((self.clicked_tile.y - ofset_y == self.clicked_tile.y) and (ofset_y != 0))):
                    if(self.selected_Model.AP != 0):
                        c = 1
                        b = True
                if((self.clicked_tile.is_wall == True) or ((self.clicked_tile.is_door == True) and (self.clicked_tile.is_open == False)) or (self.clicked_tile.is_entrypoint == True)):
                    b = False
                if((((map[self.selected_tile.y+1][self.selected_tile.x].is_wall) or (map[self.selected_tile.y+1][self.selected_tile.x].is_occupied)) and ((map[self.selected_tile.y-1][self.selected_tile.x].is_wall) or (map[self.selected_tile.y-1][self.selected_tile.x].is_occupied))) or (((map[self.selected_tile.y][self.selected_tile.x+1].is_wall) or (map[self.selected_tile.y][self.selected_tile.x+1].is_occupied)) and ((map[self.selected_tile.y][self.selected_tile.x-1].is_wall) or (map[self.selected_tile.y][self.selected_tile.x-1].is_occupied)))):
                    print('ja')
                    if(map[self.selected_tile.y + self.selected_Model.face[1]][self.selected_tile.x + self.selected_Model.face[0]].is_occupied == True):
                        if((self.clicked_tile == map[self.selected_tile.y + ofset_y + ofs[1]][self.selected_tile.x + ofset_x + ofs[0]]) or (self.clicked_tile == map[self.selected_tile.y - ofset_y + ofs[1]][self.selected_tile.x - ofset_x + ofs[0]])):
                            print('ne')
                            b = False
                    elif(map[self.selected_tile.y - self.selected_Model.face[1]][self.selected_tile.x - self.selected_Model.face[0]].is_occupied == True):
                        if((self.clicked_tile == map[self.selected_tile.y + ofset_y - ofs[1]][self.selected_tile.x + ofset_x - ofs[0]]) or (self.clicked_tile == map[self.selected_tile.y - ofset_y - ofs[1]][self.selected_tile.x - ofset_x - ofs[0]])):
                            print('ne')
                            b = False
                if(self.clicked_tile.is_buring):
                    if(self.selected_tile.is_buring):
                        if((random.randint(1,6)) > 1):
                            self.selected_tile.is_occupied = False
                            SM_ModellList.remove(self.selected_Model)
                            self.selected_tile.occupand = None
                            b = False
                    else:
                        b = False
        print(a,b)
        if(a & b):
            self.redAP(self.selected_Model, c)
            self.selected_Model.guard = False
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
                    if(tile.is_occupied == False):
                        lis.remove(tile)
                    elif(tile.occupand in SM_ModellList):
                        lis.remove(tile)
                    elif(tile.occupand in BL_ModellList):
                        self.Manager.rev_models.append(tile)
                        lis.remove(tile)
                for tile in lis:
                    print(tile.y,tile.x)
                self.selected_Model.susf = False
                if(self.Manager.rev_models.__len__() != 0):
                    self.Manager.save_model = self.selected_Model
                    self.Manager.save_tile = self.selected_tile
                    self.reveal(self.Manager.rev_models[0])
                elif(lis != []):
                    if((self.selected_Model.weapon != 'claws') and (self.selected_Model.weapon != 'flamer')):
                        self.Manager.changestate('shoot')
                        game.run()
            elif(self.is_playing == self.player2):
                if(self.selected_Model in GS_ModellList):
                    self.Manager.gs_turnaftermove = self.selected_Model
                    self.clicked_model = self.selected_Model
                    self.clicked_tile = self.selected_tile
                    for row in map: 
                        for tile in row:
                            if(tile.occupand in SM_ModellList):
                                checked = self.vision(tile.occupand, tile)
                                if(tile.occupand.overwatch == True):
                                    if((tile.occupand.jam == False) & (self.clicked_tile in checked)):
                                        self.selected_Model = tile.occupand
                                        self.selected_tile = tile
                                        self.shoot()
                                for tile in checked:
                                    if(tile.occupand in BL_ModellList):
                                        self.Manager.rev_models.append(tile)
                                        checked.remove(tile)
                                if(self.Manager.rev_models.__len__() != 0):
                                    self.Manager.save_model = self.selected_Model
                                    self.Manager.save_tile = self.selected_tile
                                    self.reveal(self.Manager.rev_models[0])
                                
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
        self.fullturn_button = Button(400, 200, self.move_image, 1)
        self.face_button = Button(320, 200, self.move_image, 1)
        self.move_button = Button(320, 200, self.move_image, 1)
        while(True):
            pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit
            for row in map:
                for tile in row: 
                    tile.render(screen)
            SB.display(screen)
            BB.display(screen)
            
            if(self.gameStateManager.melee_turn == True):
                if(self.face_button.draw(screen)):
                    match(game.selected_Model.face):
                        case(1,0): game.clicked_model.face = (-1,0)
                        case(0,1): game.clicked_model.face = (0,-1)
                        case(-1,0): game.clicked_model.face = (1,0)
                        case(0,-1): game.clicked_model.face = (0,1)
                    pressed = True
                    self.gameStateManager.melee_turn = False

            elif(self.gameStateManager.gs_moveturn == False):
                if(self.turnleft_button.draw(screen)):
                    if((game.is_playing == game.player1) and (game.selected_Model.AP + game.CP != 0)):
                        game.selected_Model.guard = False
                        a = True
                    if((game.is_playing == game.player2) and (game.selected_Model.AP != 0) and (self.gameStateManager.gs_turnaftermove == None) and (self.gameStateManager.turn == False)):
                        self.gameStateManager.gs_moveturn = True
                        a = True
                    if(self.gameStateManager.turn == True):
                        a = True
                    if(self.gameStateManager.gs_turnaftermove != None):
                        a = True
                        pressed = True
                    if(a):
                        match(game.selected_Model.face):
                            case(1,0): game.selected_Model.face = (0,-1)
                            case(0,1): game.selected_Model.face = (1,0)
                            case(-1,0): game.selected_Model.face = (0,1)
                            case(0,-1): game.selected_Model.face = (-1,0)
                        if((self.gameStateManager.turn == False) and (self.gameStateManager.gs_turnaftermove != game.selected_Model)):
                            game.redAP(game.selected_Model,1)
                        else:
                            self.gameStateManager.gs_turnaftermove = None
                        a = False

                if(self.turnright_button.draw(screen)):
                    if((game.is_playing == game.player1) and (game.selected_Model.AP + game.CP != 0)):
                        game.selected_Model.guard = False
                        a = True
                    if((game.is_playing == game.player2) and (game.selected_Model.AP != 0) and (self.gameStateManager.gs_turnaftermove == None) and  (self.gameStateManager.turn == False)):
                        self.gameStateManager.gs_moveturn = True
                        a = True
                    if(self.gameStateManager.turn == True):
                        a = True
                    if(self.gameStateManager.gs_turnaftermove != None):
                        a = True
                        pressed = True
                    if(a):
                        match(game.selected_Model.face):
                            case(1,0): game.selected_Model.face = (0,1)
                            case(0,1): game.selected_Model.face = (-1,0)
                            case(-1,0): game.selected_Model.face = (0,-1)
                            case(0,-1): game.selected_Model.face = (1,0)
                        if((self.gameStateManager.turn == False) and (self.gameStateManager.gs_turnaftermove != game.selected_Model)):
                            game.redAP(game.selected_Model,1)
                        else:
                            self.gameStateManager.gs_turnaftermove = None
                        a = False

                if(((game.is_playing == game.player2) or (self.gameStateManager.turn == True)) and (self.gameStateManager.gs_turnaftermove == None)):
                    if(self.fullturn_button.draw(screen)):
                        if(game.selected_Model.AP != 0):
                            match(game.selected_Model.face):
                                case(1,0): game.selected_Model.face = (-1,0)
                                case(0,1): game.selected_Model.face = (0,-1)
                                case(-1,0): game.selected_Model.face = (1,0)
                                case(0,-1): game.selected_Model.face = (0,1)
                            if(self.gameStateManager.turn == False):
                                game.redAP(game.selected_Model,1)
                                print(game.selected_Model.AP)

            if((self.gameStateManager.gs_moveturn == True) and (self.gameStateManager.turn == False)):
                if(self.move_button.draw(screen)):
                    game.clicked_tile = map[game.selected_tile.y + game.selected_Model.face[1]][game.selected_tile.x + game.selected_Model.face[0]]
                    game.moveModel()
                    self.gameStateManager.gs_turnaftermove = None
                    pressed = True
                    self.gameStateManager.gs_moveturn = False

            if(self.noturn_button.draw(screen)):
                pressed = True
                self.gameStateManager.turn = False
                self.gameStateManager.melee_turn = False
                self.gameStateManager.gs_moveturn = False
                self.gameStateManager.gs_turnaftermove = None
                   
            if(pressed):
                if(self.gameStateManager.rev_count != 0):
                    self.gameStateManager.changestate('reveal')
                    game.run()
                elif(game.is_playing == game.player1):
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
        font = pygame.font.SysFont('Bahnschrift', 20)
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
        self.changeturn_button = Button(120, 500, self.move_image, 1)
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

            if(self.changeturn_button.draw(screen)):
                game.is_playing = game.player2
                game.GS_prep()
                print(self.Manager.givestate())
                print(game.is_playing)
                print('0')
                self.Manager.changestate('gsprep')
                game.run()
                
            if((game.selected_Model in SM_ModellList) and (game.is_playing == game.player1)):
                self.Manager.changestate('actP1')
                game.run()

            pygame.display.update()

class OOC_Activation:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        pressed = False
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        self.changeturn_button = Button(120, 500, self.move_image, 1)
        self.shoot_button = Button(180, 500, self.move_image, 1)
        self.melee_button = Button(240, 500, self.move_image, 1)
        self.ocDoor_button = Button(300, 500, self.move_image, 1)
        self.guard_button = Button(360, 500, self.move_image, 1)

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
                if(game.selected_Model in self.Manager.ooc_models):
                    if(game.CP != 0):
                        game.moveModel()
                        pressed = True

            if(self.turn_button.draw(screen)):
                if((game.selected_Model.AP != 0) or ((game.is_playing == game.player1) and (game.CP != 0))):
                    pressed = True
                    self.Manager.changestate('turn')
                    game.run()
                else:print('no AP/CP')
            
            if((self.changeturn_button.draw(screen)) or (pressed == True)):
                self.Manager.ooc = False
                self.Manager.ooc_models = []
                self.Manager.changestate('runP2')
                game.run()

            if(self.shoot_button.draw(screen)):
                if(game.selected_Model != None):
                    if(game.selected_Model.weapon != 'claws'):
                        if(((game.CP) > 1) and (game.selected_Model.weapon == 'flamer')):
                            pressed = True
                            self.Manager.changestate('shoot')
                            game.run()
                        elif(((game.CP) != 0) and (game.selected_Model.weapon != 'flamer')):
                            pressed = True
                            self.Manager.changestate('shoot')
                            game.run()
                        else: print('nicht genug AP')

            if(self.melee_button.draw(screen)):
                if(game.selected_Model != None):
                    if((game.CP) != 0):
                        pressed = True
                        game.melee()
                    else: print('nicht genug AP')
        
            if(self.ocDoor_button.draw(screen)):
                pressed = True
                game.ocDoor()

            if(self.guard_button.draw(screen)):
                if((game.CP) > 1):
                    pressed = True
                    game.redAP(game.selected_Model, 2)
                    game.selected_Model.overwatch = False
                    game.selected_Model.guard = True

            pygame.display.update()

class Player1Activation:
    def __init__(self) -> None:
        self.Manager = gameStateManager
        self.activated_model = None

    def run(self):
        pressed = False
        if(self.activated_model == None):
            self.activated_model = game.selected_Model
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        self.changeturn_button = Button(120, 500, self.move_image, 1)
        self.shoot_button = Button(180, 500, self.move_image, 1)
        self.melee_button = Button(240, 500, self.move_image, 1)
        self.ocDoor_button = Button(300, 500, self.move_image, 1)
        self.guard_button = Button(360, 500, self.move_image, 1)

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
                    if((self.activated_model != game.selected_Model) and (self.activated_model in SM_ModellList)):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
                    game.moveModel()

            if(self.turn_button.draw(screen)):
                if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                    if((self.activated_model != game.selected_Model) and (self.activated_model in SM_ModellList)):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
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
                self.Manager.changestate('gsprep')
                game.run()

            if(self.shoot_button.draw(screen)):
                if(game.selected_Model != None):
                    if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                        if((self.activated_model != game.selected_Model) and (self.activated_model in SM_ModellList)):
                            self.activated_model.AP = 0
                            self.activated_model = game.selected_Model
                        if(game.selected_Model.weapon != 'claws'):
                            if(((game.selected_Model.AP + game.CP) > 1) and (game.selected_Model.weapon == 'flamer')):
                                self.Manager.changestate('shoot')
                                game.run()
                            elif(((game.selected_Model.AP + game.CP) != 0) and (game.selected_Model.weapon != 'flamer')):
                                self.Manager.changestate('shoot')
                                game.run()
                            else: print('nicht genug AP')

            if(self.melee_button.draw(screen)):
                if(game.selected_Model != None):
                    if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                        if((self.activated_model != game.selected_Model) and (self.activated_model in SM_ModellList)):
                            self.activated_model.AP = 0
                            self.activated_model = game.selected_Model
                        if((game.selected_Model.AP + game.CP) != 0):
                            game.melee()
                        else: print('nicht genug AP')
            
            if(self.ocDoor_button.draw(screen)):
                if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                    if((self.activated_model != game.selected_Model) and (self.activated_model in SM_ModellList)):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
                    game.ocDoor()

            if(self.guard_button.draw(screen)):
                if((game.selected_Model.AP + game.CP) > 1):
                    if((game.is_playing == game.player1) and (game.selected_Model in SM_ModellList)):
                            if((self.activated_model != game.selected_Model) and (self.activated_model in SM_ModellList)):
                                self.activated_model.AP = 0
                                self.activated_model = game.selected_Model
                            game.redAP(game.selected_Model, 2)
                            game.selected_Model.overwatch = False
                            game.selected_Model.guard = True

            pygame.display.update()

class Player2Turn:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.changeturn_button = Button(120, 500, self.move_image, 1)
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

            if(self.Manager.ooc == True):
                self.Manager.changestate('ooc')
                game.run()

            if(self.changeturn_button.draw(screen)):
                game.is_playing = game.player1
                game.SM_prep()
                print(self.Manager.givestate())
                print(game.is_playing)
                print('1')
                self.Manager.changestate('runP1')
                game.run()

            if(((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList)) and (game.is_playing == game.player2)):
                self.Manager.changestate('actP2')
                game.run()

            pygame.display.update()

class Player2Activation:
    def __init__(self) -> None:
        self.Manager = gameStateManager
        self.activated_model = None

    def run(self):
        if(self.activated_model == None):
            self.activated_model = game.selected_Model
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.turn_button = Button(60, 500, self.move_image, 1)
        self.move_button = Button(0, 500, self.move_image, 1)
        self.changeturn_button = Button(120, 500, self.move_image, 1)
        self.reveal_button = Button(180, 500, self.move_image, 1)
        self.melee_button = Button(240, 500, self.move_image, 1)
        self.ocDoor_button = Button(300, 500, self.move_image, 1)
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

            if(self.Manager.ooc == True):
                self.Manager.changestate('ooc')
                game.run()

            if(self.Manager.gs_turnaftermove != None):
                game.selected_Model = self.Manager.gs_turnaftermove
                self.Manager.changestate('turn')
                game.run()

            if(self.move_button.draw(screen)):
                if((game.is_playing == game.player2) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                    if((self.activated_model != game.selected_Model) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
                    game.moveModel()

            if(self.turn_button.draw(screen)):
                if(game.selected_Model != None):
                    if((game.is_playing == game.player2) and (game.selected_Model in GS_ModellList)):
                        if((self.activated_model != game.selected_Model) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                            self.activated_model.AP = 0
                            self.activated_model = game.selected_Model
                        if(game.selected_Model.AP != 0):
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
                    if((self.activated_model != game.selected_Model) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
                    if(game.selected_Model.AP == 6):
                        self.Manager.rev_models.append(game.selected_tile)
                        game.reveal(game.selected_tile)

            if(self.melee_button.draw(screen)):
                if(game.selected_Model in GS_ModellList):
                    if((self.activated_model != game.selected_Model) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
                    if(game.selected_Model.AP != 0):
                        game.melee()

            if(self.ocDoor_button.draw(screen)):
                if((self.activated_model != game.selected_Model) and ((game.selected_Model in GS_ModellList) or (game.selected_Model in BL_ModellList))):
                        self.activated_model.AP = 0
                        self.activated_model = game.selected_Model
                game.ocDoor()

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

class gamestate_reinforcement:
    def __init__(self) -> None:
        self.Manager = gameStateManager

    def run(self):
        amount = 2
        self.move_image = pygame.image.load('Pictures/Wall.png')
        self.place_button = Button(60, 500, self.move_image, 1)
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
            if(self.place_button.draw(screen)):
                if(amount != 0):
                    if((game.clicked_tile != None) and (game.clicked_tile.is_lurkingpoint) and (game.clicked_tile.is_occupied == False)):
                        game.clicked_tile.occupand = Blip()
                        game.clicked_tile.is_occupied = True
                        BL_ModellList.append(game.clicked_tile.occupand)
                        amount -= 1
            lis = []
            for row in map:
                for tile in row:
                    if((tile.is_lurkingpoint) and (tile.is_occupied == False)):
                        lis.append(tile)

            if((amount == 0) or (lis == [])):
                for row in map:
                    for bl in row:
                        if(bl.occupand in BL_ModellList):
                            for row in map:
                                for tile in row:
                                    if(tile.occupand in SM_ModellList):
                                        d = game.distance(bl, tile)
                                        if(d < 7):
                                            bl.occupand.AP = 0
                self.Manager.changestate('runP2')
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
        lis = []

        if(self.Manager.rev_count == 0):

            self.revModel = game.selected_Model
            self.Manager.rev_count = self.revModel.count
            self.tile = game.selected_tile

            self.tile.is_occupied = False
            BL_ModellList.remove(self.tile.occupand)
            self.tile.occupand = Genestealer()
            self.tile.is_occupied = True
            GS_ModellList.append(self.tile.occupand)
            self.Manager.rev_count -= 1
            print(self.Manager.rev_count)
            self.Manager.rev_models.remove(self.tile)
            self.Manager.turn = True
            game.selected_Model = self.tile.occupand
            self.Manager.changestate('turn')
            game.run()

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
                            self.Manager.rev_count -= 1
                            self.Manager.turn = True
                            game.selected_Model = game.clicked_tile.occupand
                            self.Manager.changestate('turn')
                            game.run()

            lis = []

            for row in map:
                for tile in row:
                    if(((tile.x == game.selected_tile.x) or (tile.x == (game.selected_tile.x -1)) or (tile.x == (game.selected_tile.x +1))) and ((tile.y == game.selected_tile.y) or (tile.y == (game.selected_tile.y -1)) or (tile.y == (game.selected_tile.y +1)))):
                        if((tile.is_occupied == False) & (((tile.is_door == True) & (tile.is_open == True)) or (tile.is_door == False)) & (tile.is_wall == False)):
                            lis.append(tile)
        
            if((self.Manager.rev_count == 0) or (lis == [])):
                self.Manager.rev_count = 0
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
                    game.reveal(self.Manager.rev_models[0])

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
        self.rect.topleft = (x*size,y*size) #positions the rect to th right coordinates
        self.clicked = False    #if the tile has been clicked(importnt later)
        self.is_wall = False    #if the tile is a wall-segment thus having a diffrent picture and function
        self.is_entrypoint = False  #if the tile is an entrypoint for reinforcing blips
        self.is_lurkingpoint = False    #if the tile is a lurkingpoint for blips
        self.is_door = False    
        self.is_open = False
        self.is_buring = False

    def render(self, screen):
        if(self.is_wall): 
            image = pygame.image.load('Pictures/Wall.png')
            self.image = pygame.transform.scale(image,(self.size,self.size))
        elif(self.is_door):
            if((map[self.y+1][self.x].is_wall == True) and (map[self.y-1][self.x].is_wall == True)):
                #path = if self.is_open == False "" else ""
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

        elif(self.is_entrypoint):
            image = pygame.image.load('Pictures/entrypoint.PNG')
            if((map[self.y][self.x - 1].is_lurkingpoint == False) and (map[self.y][self.x - 1].is_wall == False)):
                self.image = pygame.transform.scale(image,(self.size,self.size))
            elif((map[self.y + 1][self.x].is_lurkingpoint == False) and (map[self.y + 1][self.x].is_wall == False)):
                imager = pygame.transform.scale(image,(self.size,self.size))
                self.image = pygame.transform.rotate(imager,90)
            elif((map[self.y][self.x + 1].is_lurkingpoint == False) and (map[self.y][self.x + 1].is_wall == False)):
                imager = pygame.transform.scale(image,(self.size,self.size))
                self.image = pygame.transform.rotate(imager,180)
            else:
                imager = pygame.transform.scale(image,(self.size,self.size))
                self.image = pygame.transform.rotate(imager,270)
        elif(self.is_buring):
            image = pygame.image.load('Pictures/Floor_burning.png')
            self.image = pygame.transform.scale(image,(self.size,self.size))
        else:
            image = pygame.image.load('Pictures/Floor.png')
            self.image = pygame.transform.scale(image, (int(self.size), int(self.size)))

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
                    imaget = pygame.transform.rotate(imaget,270)

                case((0,-1)):
                    imaget = pygame.transform.scale(self.occupand.image, (int(self.size), int(self.size)))
                    imaget = pygame.transform.rotate(imaget,90)
    
            screen.blit(imaget, (self.x*self.size, self.y*self.size))
    
    def interact(self):
        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos)) and (pygame.mouse.get_pressed()[0] == 1):
            self.clicked = True
        if(pygame.mouse.get_pressed()[0] == 0 and self.clicked):
            if((gameStateManager.ooc == True) and (self.occupand in gameStateManager.ooc_models)):
                game.selected_Model = self.occupand
                game.selected_tile = self
            elif(gameStateManager.ooc == True):
                game.clicked_model = self.occupand
                print(self.occupand)
                game.clicked_tile = self
            elif(((self.is_occupied) and (self.occupand in SM_ModellList) and (game.is_playing == game.player1)) or ((self.is_occupied) and ((self.occupand in GS_ModellList) or (self.occupand in BL_ModellList)) and (game.is_playing == game.player2))):
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
        super().__init__(6, 'Pictures/Models/Blip_new.PNG')
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
        my_font = pygame.font.SysFont('Bahnschrift', 20)
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
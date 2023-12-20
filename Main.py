from Data import *
from sys import exit

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal()}

gs = Blip()
bl = Genestealer()
cp = SpaceMarine('claws', 'none')
SM_ModellList.append(cp)
GS_ModellList.append(bl)
BL_ModellList.append(gs)

map[5][1].occupand = cp
map[5][1].is_occupied = True

map[5][8].occupand = bl
map[5][8].is_occupied = True

map[6][1].is_wall = True
map[4][1].is_wall = True
map[6][2].is_wall = True
map[4][2].is_wall = True
map[6][3].is_wall = True
map[4][3].is_wall = True
map[5][3].is_door = True
map[15][14].is_wall = True
map[15][16].is_wall = True
map[16][15].is_lurkingpoint = True
map[15][15].is_entrypoint = True

map[17][17].is_door = True
map[17][17].is_open = True 
map[17][16].is_wall = True
map[17][18].is_wall = True

map[5][9].occupand = gs
map[5][9].is_occupied = True
for row in map:
    for tile in row:
        if((tile.x == 0) or (tile.x == 19) or (tile.y == 0) or (tile.y == 19)):
            tile.is_wall = True

game.run()
from Data import *
from sys import exit

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal()}

gs = Blip()
bl = Genestealer()
cp = SpaceMarine('bolter', 'None')
SM_ModellList.append(cp)
GS_ModellList.append(bl)
BL_ModellList.append(gs)
cp.overwatch = True

map[5][1].occupand = cp
map[5][1].is_occupied = True

map[7][8].occupand = bl
map[7][8].is_occupied = True

map[6][1].is_wall = True
map[4][1].is_wall = True
map[6][2].is_wall = True
map[4][2].is_wall = True
map[6][3].is_wall = True
map[4][3].is_wall = True

map[9][9].occupand = gs
map[9][9].is_occupied = True
for row in map:
    for tile in row:
        if((tile.x == 0) or (tile.x == 19) or (tile.y == 0) or (tile.y == 19)):
            tile.is_wall = True

game.run()
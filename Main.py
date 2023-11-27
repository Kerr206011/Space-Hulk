from Data import *
from sys import exit

game.states = {'start':Player1Turn(), 'run':Player2Turn(), 'main':gamestateMain(), 'turn':gamestateTurn()}

gs = Blip()
cp = SpaceMarine('bolter', 'none')
SM_ModellList.append(cp)
GS_ModellList.append(gs)

map[1][1].occupand = cp
map[1][1].is_occupied = True
map[5][5].occupand = gs
map[5][5].is_occupied = True
map[6][5].is_wall = True
for row in map:
    for tile in row:
        if((tile.x == 0) or (tile.x == 19) or (tile.y == 0) or (tile.y == 19)):
            tile.is_wall = True

game.run()
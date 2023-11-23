from Data import *
from sys import exit

game.states = {'start':Player1Turn(), 'run':Player2Turn(), 'main':gamestateMain(), 'turn':gamestateTurn()}

gs = Blip()
cp = SpaceMarine('bolter', 'none')
SM_ModellList.append(cp)
GS_ModellList.append(gs)

map[0][0].occupand = cp
map[0][0].is_occupied = True
map[5][5].occupand = gs
map[5][5].is_occupied = True

game.run()
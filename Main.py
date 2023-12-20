from Data import *
from sys import exit

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal(), 'gsprep':gamestate_reinforcement()}

gs = Blip()
bl = Genestealer()
cp = SpaceMarine('claws', 'none')
SM_ModellList.append(cp)
GS_ModellList.append(bl)
BL_ModellList.append(gs)

gameStateManager.sections = [[map[1][1],map[2][1],map[2][2]],[map[4][4], map[4][8]]]

# for section in gameStateManager.sections:
#     if map[1][1] in section:
#         for tile in section:
#             tile.is_wall = True
#     if map[4][4] in section:
#         for tile in section:
#             tile.is_buring = True

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

map[4][5].is_entrypoint = True
map[4][4].is_wall = True
map[4][6].is_wall = True
map[3][5].is_lurkingpoint = True
map[3][4].is_lurkingpoint = True
map[3][6].is_lurkingpoint = True

map[5][9].occupand = gs
map[5][9].is_occupied = True
for row in map:
    for tile in row:
        if((tile.x == 0) or (tile.x == 19) or (tile.y == 0) or (tile.y == 19)):
            tile.is_wall = True

game.run()
from Data import *
from sys import exit

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal(), 'gsprep':gamestate_reinforcement(), 'actP1':Player1Activation()}

gs = Blip()
bl = Genestealer()
cp = SpaceMarine('flamer', 'none')
sg = SpaceMarine('powerSword', 'sergeant')
SM_ModellList.append(cp)
SM_ModellList.append(sg)
GS_ModellList.append(bl)
BL_ModellList.append(gs)
door1 = [map[5][2]]
door2 = [map[5][4]]
gameStateManager.sections = [[map[5][2],map[5][3],map[5][4],door1,door2],[map[5][5], map[5][6], map[5][7],map[5][8]]]

# for section in gameStateManager.sections:
#     if map[1][1] in section:
#         for tile in section:
#             tile.is_wall = True
#     if map[4][4] in section:
#         for tile in section:
#             tile.is_buring = True

map[5][1].occupand = cp
map[5][1].is_occupied = True
map[5][2].occupand = sg
map[5][2].is_occupied = True

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
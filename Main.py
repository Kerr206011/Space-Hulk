from Data import *
from sys import exit

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal(), 'gsprep':gamestate_reinforcement(), 'actP1':Player1Activation(), 'actP2':Player2Activation(), 'ooc':OOC_Activation(), 'reroll':CP_reroll(), 'smplace':gamestate_SMplace(), 'gsplace':gamestate_gsplace()}

cp = SpaceMarine('flamer', 'none')
sg = SpaceMarine('powerSword', 'sergeant')
SM_ModellList.append(cp)
SM_ModellList.append(sg)

removetiles = []

for tile in map[0]:
    if(tile.x < 19) or (tile.x > 23):
        removetiles.append(tile)
    else:
        tile.is_wall = True

for tile in map[1]:
    if(tile.x < 19) or (tile.x > 23):
        removetiles.append(tile)
    elif(tile.x == 19 or tile.x == 23):
        tile.is_wall = True

for tile in map[2]:
    if(tile.x < 19) or (tile.x > 23):
        removetiles.append(tile)
    elif(tile.x == 19 or tile.x == 23):
        tile.is_wall = True

for tile in map[3]:
    if(tile.x < 19) or (tile.x > 23):
        removetiles.append(tile)
    elif(tile.x == 19 or tile.x == 23):
        tile.is_wall = True

for tile in map[4]:
    if(tile.x < 19) or (tile.x > 23):
        removetiles.append(tile)
    elif(tile.x != 21):
        tile.is_wall = True
    else:
        tile.is_door = True
        
for tile in map[5]:
    if(tile.x < 20) or (tile.x > 22 and tile.x < 25):
        removetiles.append(tile)
    elif(tile.x != 21):
        tile.is_wall = True

for tile in map[6]:
    if(tile.x < 20) or (tile.x > 22 and tile.x < 25):
        removetiles.append(tile)
    elif(tile.x == 20 or tile.x == 22 or tile.x == 25 or tile.x == 29):
        tile.is_wall = True
    elif(tile.x > 25 and tile.x <29):
        tile.is_lurkingpoint = True

for tile in map[7]:
    if(tile.x < 20) or (tile.x > 22 and tile.x < 25):
        removetiles.append(tile)
    elif(tile.x == 20 or tile.x == 22 or (tile.x > 24 and tile.x != 27)):
        tile.is_wall = True
    elif(tile.x == 27):
        tile.is_entrypoint = True

for tile in map[8]:
    if(tile.x < 14) or (tile.x == 29):
        removetiles.append(tile)
    elif(tile.x != 21 and tile.x != 27):
        tile.is_wall = True

for tile in map[9]:
    if(tile.x < 14) or (tile.x == 29):
        removetiles.append(tile)
    elif(tile.x == 14 or tile.x == 28):
        tile.is_wall = True
    elif(tile.x == 16):
        tile.is_door = True
for tile in map[10]:
    if(tile.x < 6 or ( tile.x > 10 and tile.x < 14) or tile.x == 29):
        removetiles.append(tile)
    elif((tile.x > 5 and tile.x < 11) or tile.x == 14 or (tile.x > 15 and tile.x < 21) or (tile.x > 21 and tile.x <27) or tile.x ==28):
        tile.is_wall = True
        
for tile in map[11]:
    if(tile.x == 29):
        removetiles.append(tile)
    elif(tile.x < 7 or (tile.x > 9 and tile.x < 15) or (tile.x > 15 and tile.x < 21) or (tile.x > 21 and tile.x <27) or tile.x ==28):
        tile.is_wall = True

for tile in map[12]:
    if(tile.x == 29):
        removetiles.append(tile)
    elif(tile.x == 0 or tile.x == 28):
        tile.is_wall = True
    elif(tile.x == 6 or tile.x == 10):
        tile.is_door = True

for tile in map[13]:
    if(tile.x == 29):
        removetiles.append(tile)
    elif(tile.x < 7 or (tile.x > 9 and tile.x < 21) or (tile.x > 21 and tile.x <27) or tile.x ==28):
        tile.is_wall = True

for tile in map[14]:
    if(tile.x < 6 or (tile.x > 10 and tile.x < 20) or tile.x == 23 or tile.x == 24):
        removetiles.append(tile)
    elif(tile.x == 6 or tile.x == 7 or tile.x == 9 or tile.x == 10 or tile.x == 20 or tile.x == 22 or tile.x ==25 or tile.x == 26 or tile.x == 28 or tile.x == 29):
        tile.is_wall = True
    elif(tile.x == 8):
        tile.is_door = True
    elif(tile.x == 27):
        tile.is_entrypoint = True

for tile in map[15]:
    if(tile.x < 7 or (tile.x > 9 and tile.x < 20) or tile.x == 23 or tile.x == 24):
        removetiles.append(tile)
    elif(tile.x == 7 or tile.x == 9 or tile.x == 20 or tile.x == 22 or tile.x == 25 or tile.x == 29):
        tile.is_wall = True
    elif(tile.x > 25 and tile.x < 29):
        tile.is_lurkingpoint = True

for tile in map[16]:
    if(tile.x < 7 or (tile.x > 9 and tile.x < 20) or tile.x == 23 or tile.x == 24):
        removetiles.append(tile)
    elif(tile.x == 7 or tile.x == 9 or tile.x == 20 or tile.x == 22 or tile.x >24):
        tile.is_wall = True
    elif(tile.x > 25 and tile.x < 29):
        tile.is_lurkingpoint = True

for tile in map[17]:
    if(tile.x < 7 or (tile.x > 14 and tile.x < 20) or tile.x > 22):
        removetiles.append(tile)
    elif(tile.x == 7 or (tile.x > 8 and tile.x < 15) or tile.x == 20 or tile.x == 22):
        tile.is_wall = True

for tile in map[18]:
    if(tile.x < 7 or tile.x == 15 or tile.x == 16 or tile.x > 25):
        removetiles.append(tile)
    elif(tile.x == 7 or tile.x == 9 or tile.x == 10 or tile.x == 14 or (tile.x > 16 and  tile.x < 21) or (tile.x > 21 and tile.x < 26)):
        tile.is_wall = True
    elif(tile.x > 10 and tile.x < 14):
        tile.is_lurkingpoint = True

for tile in map[19]:
    if(tile.x < 6 or tile.x == 15 or tile.x == 16 or tile.x > 25):
        removetiles.append(tile)
    elif(tile.x == 6 or tile.x == 7 or tile.x == 9 or tile.x == 10 or tile.x == 11 or tile.x == 13 or tile.x == 14 or tile.x == 17 or tile.x == 19 or tile.x == 20 or tile.x == 22 or tile.x == 23 or tile.x == 25):
        tile.is_wall = True
    elif(tile.x == 18 or tile.x == 24):
        tile.is_lurkingpoint = True
    elif(tile.x == 12): 
        tile.is_entrypoint = True
    elif(tile.x == 8): 
        tile.is_door = True

for tile in map[20]:
    if(tile.x < 6 or tile.x == 14 or tile.x == 15 or tile.x == 16 or tile.x > 25):
        removetiles.append(tile)
    elif(tile.x == 6 or tile.x == 10 or tile.x == 11 or tile.x == 13 or tile.x == 17 or tile.x == 25):
        tile.is_wall = True
    elif(tile.x == 18 or tile.x == 24):
        tile.is_lurkingpoint = True
    elif(tile.x == 19 or tile.x == 23): 
        tile.is_entrypoint = True

for tile in map[21]:
    if(tile.x < 6 or tile.x == 14 or tile.x == 15 or tile.x == 16 or tile.x > 25):
        removetiles.append(tile)
    elif(tile.x == 6 or tile.x == 13 or tile.x == 17 or tile.x == 19 or tile.x == 25 or (tile.x > 19 and tile.x < 24)):
        tile.is_wall = True
    elif(tile.x == 18 or tile.x == 24):
        tile.is_lurkingpoint = True
    elif(tile.x == 11):
        tile.is_door = True

for tile in map[22]:
    if(tile.x < 6 or tile.x == 14 or tile.x == 15 or tile.x == 16 or tile.x > 25 or (tile.x > 19 and tile.x < 23)):
        removetiles.append(tile)
    elif(tile.x == 6 or tile.x == 10 or tile.x == 11 or tile.x == 13 or (tile.x > 16 and tile.x < 20) or (tile.x > 22 and tile.x < 28)):
        tile.is_wall = True

for tile in map[23]:
    if(tile.x < 6 or tile.x > 14):
        removetiles.append(tile)
    elif((tile.x > 5 and tile.x < 12) or tile.x == 14 or tile.x == 13):
        tile.is_wall = True
    elif(tile.x == 12):
        tile.is_entrypoint = True

for tile in map[24]:
    if(tile.x < 10 or tile.x > 14):
        removetiles.append(tile)
    elif(tile.x == 10 or tile.x == 14):
        tile.is_wall = True
    elif(tile.x > 10 and tile.x < 14):
        tile.is_lurkingpoint = True

for tile in map[25]:
    if(tile.x < 10 or tile.x > 14):
        removetiles.append(tile)
    elif(tile.x > 9 and tile.x < 15):
        tile.is_wall = True

for ins in removetiles:
    for row in map:
        for tile in row:
            if(tile == ins):
                tile.is_used = False

map[12][1].is_SMentry = True
map[12][2].is_SMentry = True
map[12][3].is_SMentry = True
map[12][4].is_SMentry = True
map[12][5].is_SMentry = True

gameStateManager.sections = [[map[12][1],map[12][2],map[12][3],map[12][4],map[12][5]],[map[12][6],map[12][7],map[12][8],map[12][9],map[12][10],map[11][7],map[11][8],map[11][9],map[13][7],map[13][8],map[13][9],map[14][8]],[map[12][11],map[12][12],map[12][13]],[map[15][8],map[16][8],map[17][8],map[18][8]],[map[19][8],map[20][7],map[20][8],map[20][9],map[21][7],map[21][8],map[21][9],map[21][10],map[22][7],map[22][8],map[22][9]],[map[21][11],map[21][12],map[20][12],map[22][12]],[map[12][14],map[12][15],map[11][15],map[12][16]],[map[10][15],map[9][15],map[9][16]],[map[9][17],map[9][18],map[9][19]]]
print(screen.get_size())

game.run()
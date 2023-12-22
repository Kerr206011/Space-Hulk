from Data import *
from sys import exit

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal(), 'gsprep':gamestate_reinforcement(), 'actP1':Player1Activation(), 'actP2':Player2Activation(), 'ooc':OOC_Activation(), 'reroll':CP_reroll(), 'smplace':gamestate_SMplace(), 'gsplace':gamestate_gsplace()}

cp = SpaceMarine('flamer', 'none')
sg = SpaceMarine('powerSword', 'sergeant')
SM_ModellList.append(cp)
SM_ModellList.append(sg)
door1 = [map[5][2]]
door2 = [map[5][4]]
gameStateManager.sections = []

# removetiles = [map[0][0],map[0][1],map[0][2],map[0][3],map[0][4],map[0][5],map[][],map[1][1],map[1][2],map[2][1],map[2][2]]

# for ins in removetiles:
#     for row in map:
#         for tile in row:
#             if(tile == ins):
#                 row.remove(tile)

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
    elif(tile.x < 7 or (tile.x > 9 and tile.x < 15) or (tile.x > 15 and tile.x < 21) or (tile.x > 21 and tile.x <27) or tile.x ==28):
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

print(screen.get_size())

game.run()
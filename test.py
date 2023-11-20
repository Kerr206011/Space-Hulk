from Data import *
from sys import exit

#names of the players are set through inputs, in the future from in the game
pregame = True
while(pregame):
    print('Wie heißt der Space Marine Spieler?')
    game.player1 = input()
    print('Wie heißt der Genstealer Spieler?')
    game.player2 = input()
    if(game.player1 == game.player2):
        print('Die Namen dürfen nicht gleich sein')
    else:
        pregame = False

game.states = {'start':Player1Turn(), 'run':Player2Turn()}
game.state = 'start'

gs = Blip()
cp = SpaceMarine('bolter', 'none')
SM_ModellList.append(cp)
GS_ModellList.append(gs)

map[0][0].occupand = cp
map[0][0].is_occupied = True
map[5][5].occupand = gs
map[5][5].is_occupied = True

game.run()
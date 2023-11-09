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

game.is_playing = game.player1

#pygame screen is created
pygame.init()
screen = pygame.display.set_mode((700,600))
screen.fill('black')
pygame.display.set_caption('Space Hulk')

gs = Blip()
cp = SpaceMarine('bolter', 'none')
game.SM_ModellList.append(cp)
game.GS_ModellList.append(gs)

map[0][0].occupand = cp
map[0][0].is_occupied = True
map[5][5].occupand = gs
map[5][5].is_occupied = True

run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for row in map:
        for tile in row:
            tile.render(screen)
            tile.interact()
            
    SB.display(screen)
    BB.display(screen)
    BB.interact(screen)

    pygame.display.update()
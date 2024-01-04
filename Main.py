from Data import *
from sys import exit
import pickle
import json

game.states = {'runP1':Player1Turn(), 'runP2':Player2Turn(), 'main': gamestate_Main(), 'start':gamestateNewGame(), 'turn':gamestateTurn(), 'shoot':gamestate_shoot(), 'reveal':gamestate_reveal(), 'gsprep':gamestate_reinforcement(), 'actP1':Player1Activation(), 'actP2':Player2Activation(), 'ooc':OOC_Activation(), 'reroll':CP_reroll(), 'smplace':gamestate_SMplace(), 'gsplace':gamestate_gsplace(), 'smwin':SM_win(), 'gswin':GS_win(), 'level':gamestate_level()}

game.run()
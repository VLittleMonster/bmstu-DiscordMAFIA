from math import floor
from random import choice

def formRoles(rolesList, playersNumb):
    if playersNumb == 1: doctorPlayersCounter = 0
    if playersNumb == 4: doctorPlayersCounter = 1
    if 4 < playersNumb < 14: doctorPlayersCounter = 1
    if 13 < playersNumb < 21: doctorPlayersCounter = 2
    if 20 < playersNumb < 28: doctorPlayersCounter = 3

    mafiaPlayersCounter = floor((playersNumb - 1 - doctorPlayersCounter) / 2)
    commissarPlayersCounter = 1
    friendlyPlayersCounter = playersNumb - doctorPlayersCounter - mafiaPlayersCounter -\
    commissarPlayersCounter

    addedRoles = []

    for i in range(doctorPlayersCounter):
        addedRoles.append("doctor")

    for i in range(mafiaPlayersCounter):
        addedRoles.append("mafia")

    for i in range(friendlyPlayersCounter):
        addedRoles.append("friendly")
        
    addedRoles.append("commissar")

    for i in range(playersNumb):
        randomRole = choice(addedRoles)
        rolesList.append(randomRole)
        addedRoles.remove(randomRole)
    
    return rolesList

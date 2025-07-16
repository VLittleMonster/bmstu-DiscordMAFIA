def numberedList(playersList):

    numberedPlayers = ""
    for i in range(len(playersList)):
        if playersList[i] != "":
            numberedPlayers += str(i + 1)
            numberedPlayers += ") "
            numberedPlayers += str(playersList[i])
            numberedPlayers += "\n"

    return numberedPlayers
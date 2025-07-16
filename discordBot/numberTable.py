def numberedList(playersList):

    numberedPlayers = "\n"
    for i in range(len(playersList)):
        if playersList[i] != "":
            numberedPlayers += str(i + 1) + ") "
            numberedPlayers += str(playersList[i])
            numberedPlayers += "\n"
        else:
            numberedPlayers += str(i + 1) + ") :coffin:"

    return numberedPlayers


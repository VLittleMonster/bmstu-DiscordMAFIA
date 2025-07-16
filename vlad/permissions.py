def defaultProtection(channel, allMembers):
    for member in allMembers:
        return channel.set_permissions(member, read_messages = False, send_messages = False)
        
def day(channel, playersList):
    for player in playersList:
        return channel.set_permissions(player, read_messages = True, send_messages = True)

def night(channel, playersList):
    for player in playersList:
        return channel.set_permissions(player, read_messages = True, send_messages = False)
        
def mafia_day(channel, playersList, rolesList):
    for i in range(len(playersList)):
        player = playersList[i]
        if rolesList[i] == "mafia":
            return channel.set_permissions(player, read_messages = True, send_messages = False)

def mafia_night(channel, playersList, rolesList):
    for i in range(len(playersList)):
        player = playersList[i]
        if rolesList[i] == "mafia":
            return channel.set_permissions(player, read_messages = True, send_messages = True)

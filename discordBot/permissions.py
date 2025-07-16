def defaultProtection(channel, member):
    return channel.set_permissions(member, read_messages = False, send_messages = False)
 
def day(channel, player):
    return channel.set_permissions(player, read_messages = True, send_messages = True)

def night(channel, player):
    return channel.set_permissions(player, read_messages = True, send_messages = False)
        
def mafia_day(channel, player):
    return channel.set_permissions(player, read_messages = True, send_messages = False)

def mafia_night(channel, player):
    return channel.set_permissions(player, read_messages = True, send_messages = True)

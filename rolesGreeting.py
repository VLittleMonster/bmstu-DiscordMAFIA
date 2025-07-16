from numberTable import *

def friendlyGreeting(player):
    return player.send("Итак, сегодня вы Мирный Житель. Будьте готовы вычислить мафию " +\
    "в своем городе, иначе вам не выжить...")

def friendlyGreetingPic(player):
    return player.send_file("https://wmpics.pics/di-5FSUK.jpg)
    
def doctorGreeting(player, playersList):
    return player.send("Итак, сегодня вы Доктор и будете лечить жителей вашего города.\n" +\
    "А вот кто ляжет вам под нож - большой вопрос...\n" + "Началась первая ночь!\n" +\
    "Пришло время вылечить одного из игроков\nДля того, чтобы вылечить игрока " +\
    "пришлите сообщение /heal + 'пробел' + номер игрока из следующего списка!\n" +\
    numberedList(playersList))

def doctorGreetingPic(player, playersList):
    return player.send_file("https://wmpics.pics/di-ZU3W.jpg")

def commissarGreeting(player, playersList):
    return player.send(Итак, сегодня вы Комиссар. Ваша задача вычислить мафию. " +\
    "И кое-кто вам в этом поможет...\nЧтобы вычислить мафию напишите команду " +\
    "/verify + номер игрока из данной таблицы\n" + numberedList(playersList))

def commissarGreetingPic(player, playersList):
    return player.send("https://wmpics.pics/di-Z98I.jpg")
    
def mafiaGreeting(player):
    return player.send("Итак, сегодня вы Мафиози. Прошу вас пройти в комнату 'mafia', " +\
    "чтобы познакомиться с остальным преступным миром...")

def mafiaGreetingPic(player):
    return player.send_file("https://wmpics.pics/di-J3HS.jpg")
    
def mafiaChannelGreeting(channel, playersList):
    return channel.send("Добро пожаловать в клуб мафии!\nПришло время сделать выбор и " +\
    "решить, кого убить первым!\nДля того, чтобы проголосовать, пришлите сообщение " +\
    "/kill + 'пробел' + номер игрока из следующего списка!" + numberedList(playersList))


    

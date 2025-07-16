import discord
import time
import asyncio

from roomCode import *
from permissions import *
from rolesGen import *
from numberTable import *
from rolesGreeting import *
from constants import *

client = discord.Client()

# Реакция на запуск бота
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "HCF Mafia"))
    print("_HCF_")

# Реакция бота на сообщение
@client.event
async def on_message(message):
    # Игнорируем отлик на сообщения ботов
    if message.author.bot:
        return
        
    # Отчистка сервера от лишних каналов
    if message.content.startswith("/clear"):
        for guild in client.guilds:
            for channel in guild.text_channels:
                if str(channel) != "проект" and str(channel) != "мафия":
                    await channel.delete()
                    
    # Оповестить всех на канале о разработке бота
    if message.content.startswith("/sayInfo"):
        for user in message.guild.members:
            try:
                await user.send("Привет, мой друг, я скоро заработаю :3")
            except:
                pass

    # Реакция бота на сообщение о начале игры
    if message.content.startswith("/mafia"):
        #_________________Глобальные переменные_________________________
            
        global hostID # Айди хоста игры
        hostID = message.author
        
        global constPlayersNumb  # Введенное количество игроков
        try:
            constPlayersNumb = int(message.content.split()[1])
            if constPlayersNumb < 1: raise
        
        except:
            await message.channel.send("Зарегистрируйте комнату правильно:" +\
             '\n"/mafia количество игроков"')
            await message.channel.send("Внимание:\nМинимальное количество игроков = 5\n" +\
            "Максимальное количество игроков = 27")
        
        global sms
        sms = message
        global playersNumb # Зарегистрированное количество игроков
        playersNumb = 0
        global allMembers # Список всех участников сервера
        allMembers = message.guild.members
        global playersList # Список мемберов у зарегистрированных игроков
        playersList = []
        global uniqueNumber # Уникальный код для входа в комнату
        uniqueNumber = codeGen()
        global rolesList # Список ролей
        rolesList = []
        global playersStatus
        playersStatus = [[], [], []] # Список статусов игроков [[0,0,0,0],[0,0,0,0],[0,0,0,0]]:
                                     # Первый дочерний список - флаги докторов
                                     # Второй дочерний список - голосование мафии
                                     # Третий дочерний список - флаги повторного голосования
                                     # Нумерация:
                                     # Для первого и третьего дочернего списка
                                     # "0" - нет флага
                                     # "1" - есть флаг
                                     # Для второго
                                     # "0" - никто не проголосовал за убийство игрока
                                     # "1 и больше" - количество проголосовавших за убийство
            
        #_______________________________________________________________

        # Создание комнаты для региcтрации
        await message.channel.send("Комната для игры успешно создана, вот ее уникальный номер: "\
            + '\n"' + uniqueNumber + '"')
        await message.channel.send("Чтобы присоединиться к игре, напишите в чат следующее:" + '\n"/join ' +\
            uniqueNumber + '"\n')
            
    # Регистрация в игре
    if message.content == "/join " + uniqueNumber:
        # Проверка на вход в уже начавшуюся игру
        if playersNumb >= constPlayersNumb:
            await message.channel.send("К сожалению, вы опоздали. Игра уже началась")
            return
            
        # Проверка на зарегистрированность пользователя в игре
        if message.author not in playersList:
            playersNumb += 1
            playersList.append(message.author)
            playersStatus[0].append(0)
            playersStatus[1].append(0)
            playersStatus[2].append(0)
        else:
            await message.channel.send("Вы уже зарегистрированы в игре!")
            return
        
        # Уведомление пользователя о регистрации и количестве оставшихся участников
        if playersNumb != constPlayersNumb:
            await message.channel.send("Вы успешно присоединились к игре!")
            await message.channel.send(str(constPlayersNumb - playersNumb) + " игроков осталось...")
            
        # Создание канала для игры и уведомление участников о конце регистрации
        else:
            await message.channel.send("Игра скоро начнется, прошу всех игроков пройти в комнату " +\
            '"play_room"')
            await message.guild.create_text_channel("play_room")
            await message.guild.create_text_channel("mafia")

    # _____________________Взаимодействие_в_локальном_чате_ночью____________________________________________
    
    if message.content.startswith("/heal") and rolesList[playersList.index(message.author)] == "doctor":
        if playersStatus[2][playersList.index(message.author)] == blocker:
            await message.author.send("Сегодня вы уже сделали свой выбор! Можете ожидать остальных на дневном совете")
        else:
            try:
                if int(message.content.split()[1]) - 1 < 0 or rolesList[int(message.content.split()[1]) - 1] == "":
                    raise
                playersStatus[0][int(message.content.split()[1]) - 1] = voteDoctor
                playersStatus[2][playersList.index(message.author)] = blocker
                await message.author.send(str(playersList[int(message.content.split()[1]) - 1]) +\
                 " успешно вылечен! Можете ожидать остальных на дневном совете")
            except:
                 await message.author.send("Проверьте правильность введенных данных!")
    
    if message.content.startswith("/verify") and rolesList[playersList.index(message.author)] == "commissar":
        if playersStatus[2][playersList.index(message.author)] == blocker:
            await message.author.send("Сегодня вы уже сделали свой выбор! Можете ожидать остальных на дневном совете")
        else:
            try:
                if int(message.content.split()[1]) - 1 < 0 or rolesList[int(message.content.split()[1]) - 1] == "":
                    raise
                if rolesList[int(message.content.split()[1]) - 1] == "mafia":
                    await message.author.send("Вы сделали правильный выбор, данный игрок является мафией.")
                else:
                    await message.author.send("К сожалению, вы ошиблись с выбором, данный игрок не является мафией.")
                playersStatus[2][playersList.index(message.author)] = blocker
            except:
                await message.author.send("Проверьте правильность введенных данных!")

    if message.content.startswith("/kill") and rolesList[playersList.index(message.author)] == "mafia":
        if playersStatus[2][playersList.index(message.author)] == blocker:
            await message.channel.send("Сегодня вы уже сделали свой выбор!")
        else:
            try:
                if int(message.content.split()[1]) - 1 < 0 or rolesList[int(message.content.split()[1]) - 1] == "":
                    raise
                playersStatus[1][int(message.content.split()[1]) - 1] += 1
                playersStatus[2][playersList.index(message.author)] = blocker
                await message.channel.send("Голос за убийство " + str(playersList[int(message.content.split()[1]) - 1]) +\
                 " успешно принят!")
            except:
                await message.author.send("Проверьте правильность введенных данных!")
    # _____________________________________________________________________________________________________
    
    # _____________________Взаимодействие_в_глобальном_чате_ночью____________________________________________
    
    if message.content.startswith("/vote_mafia"):
        try:
            if int(message.content.split()[1]) - 1 < 0 or rolesList[int(message.content.split()[1]) - 1] == "":
                raise
            if playersStatus[2][playersList.index(message.author)] == blocker:
                await message.author.send("Вы уже оставляли голос в дневном голосовании!")
            elif playersStatus[0][int(message.content.split()[1]) - 1] != dead:
                playersStatus[0][int(message.content.split()[1]) - 1] += 1
                playersStatus[2][playersList.index(message.author)] = blocker
                await message.author.send("Ваш голос был успешно принят!")
            else:
                await message.author.send("Вы не можете проголосовать за умершего игрока!")
                raise
        except:
            await message.author.send("Проверьте правильность введенных данных!")
            
    # _____________________________________________________________________________________________________
    
    # Удаление текущей комнаты
    if message.content.startswith("/delete_room"):
        await message.channel.delete()


# Реакция бота на создание канала
@client.event
async def on_guild_channel_create(channel):
    # Глобальные переменные
    global main_channel
    global mafia_channel
    global rolesList
    global playersStatus
    global sms
    
    # Стандартная защита 1 - ой скрытой комнаты
    if channel.name == "privet_mir_1":
        for member in allMembers:
            await defaultProtection(channel, member)
        await channel.delete()
        
    # Стандартная защита 2 - ой скрытой комнаты
    if channel.name == "privet_mir_2":
        for member in allMembers:
            await defaultProtection(channel, member)
        await channel.delete()
        
    elif channel.name == "play_room":
        main_channel = channel # Основной канал игры
        
        # Формирование списка ролей
        rolesList = formRoles(rolesList, playersNumb)
    
        # Стандартная защита от всех участников сервера
        for member in allMembers:
            await defaultProtection(main_channel, member)
            
        # Наступление ночи в игре (блокировка глобального чата)
        for player in playersList:
            await night(main_channel, player)
            
        await channel.send("Добрый вечер, леди и джентельмены, игра началась!")
            
        print(rolesList)

        # Знакомство с ролями в локальном чате
        for member in range(len(playersList)):
            if rolesList[member] == "friendly":
                await friendlyGreeting(playersList[member])
            elif rolesList[member] == "doctor":
                await doctorGreeting(playersList[member], playersList)
            elif rolesList[member] == "commissar":
                await commissarGreeting(playersList[member], playersList)
            else:
                await mafiaGreeting(playersList[member])

    elif channel.name == "mafia":
        mafia_channel = channel # Канал для мафии
        
        # Стандартная защита от всех участников сервера
        for member in allMembers:
            await defaultProtection(mafia_channel, member)
            
        # Наступление ночи в игре (открытие чата для мафии)
        for i in range(len(rolesList)):
            if rolesList[i] == "mafia":
                await mafia_night(mafia_channel, playersList[i])

        # Знакомство мафии в своем текстовом канале
        await mafiaChannelGreeting(mafia_channel, playersList)
   
        # Создание 1 - ой скрытой комнаты
        await sms.guild.create_text_channel("privet_mir_1")
        
# Смена ночи на день
@client.event
async def on_guild_channel_delete(channel):
    # Глобальные переменные
    global main_channel
    global playersList
    global rolesList
    global playersStatus
    global sms

    if channel.name == "privet_mir_1":
                
        await main_channel.send("Город засыпает... Просыпается мафия!")
        
        for i in range(len(rolesList)):
            if rolesList[i] != "" and rolesList[i] != "friendly":
                await playersList[i].send("Наступила ночь, пришло время сделать выбор!")

        # Наступление ночи в игре (открытие чата для мафии)
        for i in range(len(rolesList)):
            if rolesList[i] == "mafia":
                await mafia_night(mafia_channel, playersList[i])
        
        # Задержка для голосования ночью в локальном чате
        await asyncio.sleep(40)
        
        await mafia_channel.send("Время для голосования истекло! Прошу пройти на дневной совет")
        
        # Сообщение в локальный чат для доктора и комиссара о прекращении голосования
        for i in range(len(playersList)):
            if rolesList[i] == "doctor":
                await playersList[i].send("Время для голосования истекло! Прошу пройти на дневной совет")
            if rolesList[i] == "commissar":
                await playersList[i].send("Время для голосования истекло! Прошу пройти на дневной совет")
        
        # Наступление утра в игре (закрытие чата для мафии)
        for i in range(len(rolesList)):
            if rolesList[i] == "mafia":
                await mafia_day(mafia_channel, playersList[i])
        
        # Наступление утра в игре (открытие глобального чата)
        for player in playersList:
            if player != "": await day(main_channel, player)
            
        # Создание 2 - ой скрытой комнаты
        await sms.guild.create_text_channel("privet_mir_2")
        
    elif channel.name == "privet_mir_2":
        mafiaVote = max(playersStatus[1])
        maxCounter = 0
        mafiaChoice = flagIndex
        
        # Подсчет количества максимумов голосов мафии
        for i in range(len(playersList)):
            if playersStatus[1][i] == mafiaVote:
                maxCounter += 1
        
        # Если мафия определилась с выбором
        if maxCounter == 1:
            mafiaChoice = playersStatus[1].index(mafiaVote)

        # Проверка на совпадение с выбором доктора
        if ((playersStatus[0][mafiaChoice] != voteDoctor) and (mafiaChoice != flagIndex)):
            playersStatus[0][mafiaChoice] = voteMafia
            

        print("Итоги ночи: ")
        print(playersStatus)
        
        await main_channel.send("Ночь подошла к концу...Город просыпается.")
        await main_channel.send("Итоги сегодняшней ночи...")
        
        # Результаты ночи
        deadFlag = 0
        for i in range(len(playersStatus)):
            if playersStatus[0][i] == voteMafia:
                await main_channel.send("Сегодня город проснулся без " + str(playersList[i]))
                await die(main_channel, playersList[i])
                rolesList[i] = ""
                playersStatus[0][i] = dead
                playersStatus[1][i] = dead
                playersList[i] = ""
                deadFlag = 1
            elif playersStatus[0][i] == voteDoctor:
                playersStatus[0][i] = 0
                deadFlag = 1
                await main_channel.send("Доктору удалось спасти жизнь " + str(playersList[i]))

        if deadFlag == 0:
            await main_channel.send("В эту ночь не случилось ничего примечательного...")
            
        # ____________________________Определение_конца_игры____________________________
        
        mafiaCounter = 0
        anotherPlayersCounter = 0
        for role in rolesList:
            if role == "mafia": mafiaCounter += 1
            else: anotherPlayersCounter += 1
        if mafiaCounter == 0:
            await main_channel.send("Город одержал победу!")
            exit()
        elif mafiaCounter >= anotherPlayersCounter:
            await main_channel.send("Мафия одержала победу!")
            exit()
            
        # _______________________________________________________________________________
                
        # Обнуление блокаторов для их установки в голосование за мафию
        for i in range(len(playersStatus)):
            playersStatus[2][i] = 0

        await main_channel.send("Итак, Городу предстоит выяснить, кто из жителей - Мафия?")
        await main_channel.send("У вас есть ... минут для обсуждения и выбора мафии. " +\
        "После этого каждый должен написать /vote_mafia + номер игрока, которого вы считаете мафией.")
        await main_channel.send(numberedList(playersList))
        
        await asyncio.sleep(40)

        print("Итоги дневного голосования:")
        print(playersStatus)

        playerVote = max(playersStatus[0])
        maxCounter = 0
        playerChoice = flagIndex
          
        # Подсчет количества максимумов голосов игроков
        for i in range(len(playersList)):
            if playersStatus[0][i] == playerVote:
                maxCounter += 1
                
        # Результаты дневного голосования
        if maxCounter == 1:
            playerChoice = playersStatus[0].index(playerVote)
            rolesList[playerChoice] = ""
            playersStatus[0][playerChoice] = dead
            playersStatus[1][playerChoice] = dead
            await main_channel.send("Город решил, что Мафия - " + str(playersList[playerChoice]))
            await die(main_channel, playersList[i])
            playersList[playerChoice] = ""
        else:
            await main_channel.send("Игроки не смогли договориться...")
            
        # ____________________________Определение_конца_игры____________________________
        
        mafiaCounter = 0
        anotherPlayersCounter = 0
        for role in rolesList:
            if role == "mafia": mafiaCounter += 1
            else: anotherPlayersCounter += 1
        if mafiaCounter == 0:
            await main_channel.send("Город одержал победу!")
            exit()
        elif mafiaCounter >= anotherPlayersCounter:
            await main_channel.send("Мафия одержала победу!")
            exit()
            
        # _______________________________________________________________________________
            
        # Обнуление матрицы голосов и блокаторов
        for list in playersStatus:
            for status in list:
                if status != dead: status = 0
        
        # Наступление ночи в игре (закрытие глобального чата)
        for player in playersList:
            if player != "": await night(main_channel, player)
            
        # Создание скрытой комнаты
        await sms.guild.create_text_channel("privet_mir_1")




















if __name__ == "__main__":
    uniqueNumber = "" # Для избежания ошибки идентификации при присоединении к пустой комнате
    client.run("NzA5ODQ2MzU1MTQ0NjA1ODAy.Xsb9_g.cCa6C5X7cbS_Ops51Vz7N40-WWA")

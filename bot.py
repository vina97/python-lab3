

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

file = open("task_list.txt")
text = file.read()
file.close()
tasks = text.split("\n")

updater = Updater(token)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is the Task_bot: commands supported are\n/showTasks\n/newTask <task to add>\n/removeTask <task to remove>\n/removeAllTasks <substring to use to remove all the tasks that contain it>")

def showTasks(bot, update):
    if tasks.__len__() == 0:
        bot.send_message(chat_id=update.message.chat_id, text="nothing to do here!")
    else:
        message = ''
        for elem in sorted(tasks):
            message = message + elem
        bot.send_message(chat_id=update.message.chat_id, text=message)

def newTask(bot, update, args):
    task = ' '.join(args)
    tasks.append(task)
    bot.send_message(chat_id=update.message.chat_id, text="new task added!")
    savefile()



def removeTask(bot, update, args):
    task = ' '.join(args)
    if tasks.__contains__(task):
        tasks.remove(task)
        bot.send_message(chat_id=update.message.chat_id, text="task correctly deleted!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="task not found!")
    savefile()



def savefile():
    file = open("task_list.txt", 'w')
    for elem in tasks:
        file.write(elem + "\n")
    file.close()


def removeAllTasks(bot, update, args):
    t = ' '.join(args)
    count = 0
    for elem in tasks:
        if elem.__contains__(t):
            count = count + 1
            tasks.remove(elem)
            t = elem + " correctly deleted"
            bot.send_message(chat_id=update.message.chat_id, text=t)
    if count == 0:
        bot.message.reply_text("I did not find any task to delete!\n")
    savefile()

def echo(bot, update):
    receivedText = update.message.text
    textToSend = "I'm sorry, I can't do that"
    bot.sendMessage(chat_id=update.message.chat_id, text=textToSend)

dispatcher.add_handler(CommandHandler('start', start))

showTask_handler = dispatcher.add_handler(CommandHandler('showTasks', showTasks))
dispatcher.add_handler(showTask_handler)

newTask_handler = dispatcher.add_handler(CommandHandler('newTask', newTask, pass_args=True))
dispatcher.add_handler(newTask_handler)

removeTask_handler = dispatcher.add_handler(CommandHandler('removeTask', removeTask, pass_args=True))
dispatcher.add_handler(removeTask_handler)

removeAllTask_handler = dispatcher.add_handler(CommandHandler('removeAllTasks', removeAllTasks, pass_args=True))
dispatcher.add_handler(removeAllTask_handler)

dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
updater.idle()


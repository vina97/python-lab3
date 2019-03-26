

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import messagehandler
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
        bot.message.reply_text("nothing to do here!\n")
    else:
        for elem in sorted(tasks):
            bot.message.reply_text(elem)

def newTask(bot, update, args):
    task = ' '.join(args)
    tasks.append(task)
    file = open("task_list.txt", 'w')
    for elem in tasks:
        file.write(elem + "\n")
    file.close()
    bot.send_message(chat_id=update.message.chat_id, text="new task added!")



def removeTask(bot, update, args):
    task = ' '.join(args)
    if tasks.__contains__(task):
        tasks.remove(task)
        bot.message.reply_text("task correctly deleted!\n")
        file = open("task_list.txt", 'w')
        for elem in tasks:
            file.write(elem + "\n")
        file.close()
    else:
        bot.message.reply_text("task not found!\n")


def removeAllTasks(bot, update, args):
    t = ' '.join(args)
    count = 0
    for elem in tasks:
        if elem.__contains__(t):
            count = count + 1
            tasks.remove(elem)
            bot.message.reply_text(elem + " correctly deleted!\n")
    if count == 0:
        bot.message.reply_text("I did not find any task to delete!\n")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('showTasks', showTasks))
dispatcher.add_handler(CommandHandler('newTask', newTask, pass_args=True))
dispatcher.add_handler(CommandHandler('removeTask', removeTask, pass_args=True))
dispatcher.add_handler(CommandHandler('removeAllTasks', removeAllTasks, pass_args=True))


updater.start_polling()


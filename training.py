from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pickle

chatbot = ChatBot('IGbot')
trainer = ListTrainer(chatbot)


#Loading pickle commments
f = open('./InstagramComments_.p', 'rb')
comments = pickle.load(f)
f.close()

#Training Bot with existing comments
for convo in comments[:10000]:
    trainer.train(convo)

#Testing bot
while True:
    request = input("You: ")
    response = chatbot.get_response(request)
    print('Bot:', response)

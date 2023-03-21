from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import threading
import sys
import time

chatbot = ChatBot(
    'mychatbot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry, I do not understand.',
            'maximum_similarity_threshold': 10,
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
    ]
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
trainer.train("/home/tommy/my_corpus.yml")

conversation_history = []

def print_thinking_message(event):
    message = 'Bot is thinking...'
    for char in message:
        if event.is_set():
            break
        sys.stdout.write(char)
        sys.stdout.flush()

def clear_thinking_message():
    sys.stdout.write('\r')
    sys.stdout.write(' ' * len('Bot is thinking...'))
    sys.stdout.write('\r')
    sys.stdout.flush()

def print_response(response):
    for char in response:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)
    # Add this line
    sys.stdout.write('\n')

while True:
    request = input('You: ')
    if request.lower() == 'quit':
        break
    event = threading.Event()
    t1 = threading.Thread(target=print_thinking_message, args=(event,))
    t1.start()
    response = chatbot.get_response(request)
    event.set()
    t1.join()
    clear_thinking_message()
    conversation_history.append((request, response.text))
    print_response(response.text)
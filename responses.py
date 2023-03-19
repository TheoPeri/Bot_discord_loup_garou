import random

def handle_response(message):
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hello, how are you?'
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    

    if p_message == '!help':
        return 'need help?'
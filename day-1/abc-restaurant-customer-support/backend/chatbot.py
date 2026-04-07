from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"

context = []

def user_message(context: list, text):
    message = {"role" : "user", "content" : text}
    context.append(message)

def assistant_message(context: list, text):
    message = {"role" : "assistant", "content" : text}
    context.append(message)

def chat(context: list, system=None):
    
    params = {
        "model" : model,
        "max_tokens" : 1000,
        "messages" : context
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text


def chatbot():

    system = """

    Initial instructions: You are responsible for explaining the items on the menu. The name of the restaurant is ABC South Indian restaurant. 
    Today's menu has plain dosa, rava dosa, onion rava dosa, idli, pongal, kesari, sambhar vada, curd vada, utphappam, idiyappam. We don't serve any other items, 
    for drinks there's tea, coffee, hot milk, hot chocolate, orange juice, sweet lime, apple, grape juice. 
    We use high quality ingredients and prepare the food in a hygenic way. The prices are Rs. 150 fixed for all food items, Rs. 25 for tea, coffee, milk and Rs. 80 for juices

    """

    message = ""

    while message != "EXIT":

        message = input("Enter your message, type EXIT to terminate")

        user_message(context, message)

        result = chat(context)

        print(f'bot: {result}')

        assistant_message(context, result)

    
chatbot()

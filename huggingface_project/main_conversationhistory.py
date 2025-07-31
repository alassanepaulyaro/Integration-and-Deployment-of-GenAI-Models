# Chatbot with Persistent Chat History
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_core.messages import messages_from_dict, messages_to_dict

load_dotenv()

# Create initial chat history (example) 
history = ChatMessageHistory()
history.add_user_message("hello! let's talk about lion")
history.add_ai_message("hi! I'm down to talk about lion")

# Save/Load chat history 
dicts = messages_to_dict(history.messages)
new_messages = messages_from_dict(dicts)

# Initialize memory with loaded history 
history = ChatMessageHistory(messages=new_messages)
buffer = ConversationBufferMemory(chat_memory=history)

# LLM & ConversationChain 
llm = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0,
)

conversation = ConversationChain(
    llm=llm,
    memory=buffer,
    verbose=True
)

print("Welcome to your AI Chatbot!")
for _ in range(3):
    human_input = input("You: ")
    ai_response = conversation.predict(input=human_input)
    print(f"AI: {ai_response}")

# Save current chat history 
final_dicts = messages_to_dict(history.messages)

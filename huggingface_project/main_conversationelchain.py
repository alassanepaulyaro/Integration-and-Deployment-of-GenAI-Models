# OpenAI and LangChain Conversationelchain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

# On utilise le modèle GPT-4.1-nano via OpenAI API
llm = ChatOpenAI(
    model="gpt-4.1-nano",      # Précise bien ce nom
    temperature=0,
)

conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory(),   # Gestion du contexte conversationnel
    verbose=True
)

print("Welcome to your AI Chatbot! What's on your mind?")
for _ in range(3):
    human_input = input("You: ")
    ai_response = conversation.predict(input=human_input)
    print(f"AI: {ai_response}")

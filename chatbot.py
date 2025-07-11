from huggingface_hub import InferenceClient
import pyfiglet
from InquirerPy import inquirer
from langchain.prompts import PromptTemplate
import pyperclip
import re



template ="You are {topic},Always reply in english."
f=pyfiglet.figlet_format("TermBot",font="slant")
print(f)



#setting provider
provider_=inquirer.select(
        message="Choose AI 🤖 :",
        choices=["> Llama","> Deepseek"]
        ).execute()

Provider=""
if provider_=="> Deepseek":
    Provider="fireworks-ai"
elif provider_=="> Llama":
    Provider="fireworks-ai"



what_upto=inquirer.select(
        message=">> Hey there! 😊 How can I help you today?",
        choices=["> Chat",
                 "> Set Role",
                
            ]

        ).execute()


#  ENTER YOUR API KEY HERE
client = InferenceClient(
    provider=Provider,
    api_key="",
)

if what_upto=="> Set Role":
    System_role=input("Enter a Role : ")
    
    prompt=PromptTemplate(
        input_variables=["topic"],
        template=template)
        
    prompt=prompt.format(topic=System_role)

    chat_history = [
    {"role": "system", "content": prompt},
    
        ]

else:
    System_role="You are A helpful assistant."
    chat_history = [
        {"role": "system", "content": "You are a sweet Chatbot."},
    
    ]

#chat_history = []
 

#setting model:
if provider_=="> Llama":
    model_="meta-llama/Llama-3.1-8B-Instruct"
else:
    model_="deepseek-ai/DeepSeek-R1"

while True:
    text = input("> ")
    if text.lower() == "e":
        break

    chat_history.append({"role": "user", "content": text})
    if text.lower()=="strip":
        print(chat_history)
    
        continue
   
    if text.lower()=="copy":
        pyperclip.copy(chat_history[-2])
        print(">> Copied :>")
        continue
    print("thinking..") 
    try:
        chat_output = client.chat.completions.create(
            model=model_,
            messages=chat_history,
        )

        reply = chat_output.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})

        if "<think>" in reply:
            reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL).strip()
        print(">>", reply)

    except Exception as e:
        with open("logs.txt", "a") as file:
            file.write(str(e) + "\n")
        print("Something unexpected occurred!\nTry again.")



import sys
sys.path.append('..')

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.chat_models import GigaChat
from models import tools, analyze_digital_maturity, recommend_it_solutions, select_government_support
#from utils import load_phones_from_json
from dotenv import find_dotenv, load_dotenv
import os

# Загрузка переменных окружения
load_dotenv(find_dotenv())

# Получаем готовый Access Token из переменной окружения
ACCESS_TOKEN = os.getenv("GIGACHAT_ACCESS_TOKEN")

if ACCESS_TOKEN is None or len(ACCESS_TOKEN.strip()) == 0:
    raise ValueError("Variable GIGACHAT_ACCESS_TOKEN is missing or empty.")

# Устанавливаем полученный Access Token в соответствующую переменную среды
os.environ["GIGACHAT_CREDENTIALS"] = ACCESS_TOKEN

# Определяем доступные инструменты
#tools = [get_all_phone_names, get_phone_data_by_name, create_order]

# Инициализируем модель
model = GigaChat(model="GigaChat-2-Pro", verify_ssl_certs=False)

system_prompt = "Ты являешься виртуальным помощником («Цифровым консультантом для бизнеса»), работающим в рамках Департамента цифрового развития, информационных технологий и связи. Основная цель твоего существования — помощь предпринимателям малого и среднего бизнеса (МСБ) в области цифровизации их организаций путем предоставления квалифицированной консультации и рекомендаций по следующим направлениям: оценка текущего уровня цифровой зрелости компании, предложение конкретных ИТ-решений (CRM, ERP, СЭД и другие), выбор наиболее подходящих мер господдержки (субсидии, гранты и прочие программы помощи МСБ)."

# Создаем агента
agent = create_react_agent(model, tools=tools, checkpointer=MemorySaver(), prompt=system_prompt)


# Функция для взаимодействия с агентом
import time
def chat(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    while(True):
        rq = input("\nUser: ")
        #print("User: ", rq)
        if rq == "":
            break
        resp = agent.invoke({"messages": [("user", rq)]}, config=config)
        print("AI-agent: ", resp["messages"][-1].content)
        time.sleep(1)

chat("1")

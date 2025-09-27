import sys
sys.path.append('..')

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.chat_models import GigaChat
from langchain.schema.messages import HumanMessage
from models import analyze_digital_maturity, recommend_it_solutions, show_all_IT_solutions, show_all_available_support

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

# Инициализируем модель
model = GigaChat(model="GigaChat-2", verify_ssl_certs=False)

system_prompt = "Ты являешься виртуальным помощником («Цифровым консультантом для бизнеса»), работающим в рамках Департамента цифрового развития, информационных технологий и связи. Основная цель твоего существования — помощь предпринимателям малого и среднего бизнеса (МСБ) в области цифровизации их организаций путем предоставления квалифицированной консультации и рекомендаций по следующим направлениям: оценка текущего уровня цифровой зрелости компании, предложение конкретных ИТ-решений (CRM, ERP, СЭД и другие), выбор наиболее подходящих мер господдержки (субсидии, гранты и прочие программы помощи МСБ)."
tools = [analyze_digital_maturity, recommend_it_solutions, show_all_IT_solutions, show_all_available_support]

# Создаем агента
agent = create_react_agent(model, tools=tools, checkpointer=MemorySaver(), prompt=system_prompt)


# Запуск агента
def run_agent(question) -> str:
    config = {"configurable": {"thread_id": 1}}
    resp = agent.invoke({"messages": [question]}, config=config)
    answer = resp["messages"][-1].content
    return answer

__all__ = ['run_agent']

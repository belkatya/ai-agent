from typing import Dict, List
from langchain.tools import Tool
from pydantic import BaseModel, Field
#from typing import Optional

# Модель данных компании
class Company(BaseModel):
    company_name: str = Field(description="Название компании.")
    use_crm: bool = Field(default=False, description="Использует CRM систему?")
    erp_system: bool = Field(default=False, description="Имеется ERP система?")
    cloud_services: bool = Field(default=False, description="Применяются облачные сервисы?")
    big_data_analytics: bool = Field(default=False, description="Используется аналитика больших данных?")
    digital_transformation_level: str = Field(description="Уровень цифровой трансформации.", default="low")
    industry: str = Field(default="", description="Отрасль компании.")

# Список компаний
company_data = {
        "company_name": "Creative Lab",
        "use_crm": True,
        "erp_system": False,
        "cloud_services": True,
        "big_data_analytics": False,
        "digital_transformation_level": "middle"
    }

company = Company(**company_data)

# Функция №1: Анализ цифровой зрелости компании
def analyze_digital_maturity(company_name):
    """
    Оценивает уровень цифровой зрелости компании на основе ее характеристик.

    :param company_name: Название компании
    :type company_name: str
    :return: Уровень цифровой зрелости компании (низкий/средний/высокий)
    :rtype: str
    """
    # дописать поиск компании по названию для извлечения данных из объекта

    # считаем сумму признаков цифровой зрелости
    score = sum([company.use_crm, company.erp_system, company.cloud_services, company.big_data_analytics])

    if score <= 1:
        result = "Низкая цифровая зрелость"
    elif score <= 3:
        result = "Средняя цифровая зрелость"
    else:
        result = "Высокая цифровая зрелость"

    return result


# Функция №2: Рекомендации по внедрению ИТ-решений
def recommend_it_solutions(company: Company):
    """
    Предоставляет рекомендации по внедрению ИТ-решений на основе особенностей компании.

    :param company: Объект компании
    :type company: Company
    :return: Рекомендуемые ИТ-решения
    :rtype: list[str]
    """
    recommendations = []

    if company.use_crm:
        recommendations.append("CRM")
    if company.erp_system:
        recommendations.append("ERP")
    if company.cloud_services:
        recommendations.append("Облачные сервисы")
    if company.big_data_analytics:
        recommendations.append("Система аналитики Big Data")

    return ", ".join(recommendations)


# Функция №3: Выбор мер господдержки
grants_database = {
    "Торговля": ["Государственный грант на развитие торговли", "Программы льготного кредитования"],
    "Производство": ["Поддержка экспортёров", "Компенсация затрат на модернизацию оборудования"],
    "ИТ-компания": ["Программа грантов для разработчиков", "Субсидии на развитие инфраструктуры"],
}

def select_government_support(company: Company):
    """
    Выбирает меры господдержки для компании исходя из её отрасли.

    :param company: Объект компании
    :type company: Company
    :return: Доступные меры господдержки
    :rtype: list[str]
    """
    industry = company.industry
    grants = grants_database.get(industry, [])
    return ', '.join(grants)


# Массив инструментов
tools = [
    Tool.from_function(
        func=analyze_digital_maturity,
        args_schema=Company.schema(),
        return_direct=True,
        name="ANALYZE_DIGITAL_MATURITY",
        description="Анализирует цифровую зрелость компании на основе характеристик."
    ),
    Tool.from_function(
        func=recommend_it_solutions,
        args_schema=Company.schema(),
        return_direct=True,
        name="RECOMMEND_IT_SOLUTIONS",
        description="Рекомендует внедрение ИТ-решений на основе текущих практик компании."
    ),
    Tool.from_function(
        func=select_government_support,
        args_schema=Company.schema(),
        return_direct=True,
        name="SELECT_GOVERNMENT_SUPPORT",
        description="Выбирает доступные меры господдержки на основе отрасли компании."
    )
]
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain.tools.base import tool
from langchain.callbacks.manager import CallbackManagerForToolRun

import json

# Чтение JSON-файла и загрузка данных в словарь
with open('data.json', 'r') as file:
    data = json.load(file)

# Вес каждой категории
weights = {
    "formalization_level": 1,
    "automation_systems": 2,
    "kpi_metrics": 1,
    "data_driven_decisions": 1,
    "it_systems_used": 2,
    "systems_integration": 1,
    "cloud_services_usage": 1,
    "info_security_measures": 1,
    "digital_literacy": 1,
    "training_programs": 1,
    "it_specialists_in_house": 1,
    "employees_automation_perception": 1,
    "it_strategy": 1,
    "state_electronic_services": 1,
    "future_implementation_plans": 1,
}

significance_map = {
    'yes': 1,
    'mostly_yes': 0.8,
    'mostly_no': 0.2,
    'no': 0,
    'unknown': None
}

max_possible_points = sum(weights.values())

# Функция подсчета балла цифровой зрелости
def calculate_digital_maturity_score() -> float:
    total_points = 0
    # Проходим по каждому атрибуту и его весу
    for attr, weight in weights.items():
        # Получаем значение атрибута из словаря data
        value = data.get(attr)

        # Проверяем наличие значения атрибута
        if value is None:
            raise KeyError(f'Атрибут "{attr}" отсутствует в словаре данных')

        # Приводим значение к нижнему регистру и ищем соответствующее число в карте значимости
        mapped_value = significance_map.get(value.lower())

        # Проверяем, существует ли такое значение в карте значимости
        if mapped_value is None:
            break

        # Добавляем взвешенный балл к общей сумме
        total_points += mapped_value * weight

    # Вычисляем процент готовности
    percentage = (total_points / max_possible_points) * 100
    return round(percentage, 2)



# Функция №1:Анализ цифровой зрелости
@tool
def analyze_digital_maturity() -> str:
    """
    Оценивает уровень цифровой зрелости компании на основе ее характеристик.

    """
    print("Вызвана функция: analyze_digital_maturity")
    score = calculate_digital_maturity_score()
    if score <= 40:
        result = "низкий"
    elif score <= 70:
        result = "средний"
    else:
        result = "высокий"
    return f'Цифровая зрелость вашей компании составляет {score}% ({result}).'

#print(analyze_digital_maturity.invoke(""))

# Функция №2: Рекомендации по внедрению ИТ-решений и их применению
@tool
def recommend_it_solutions():
    """
        Делает рекомендации по внедрению ИТ-решений на основе данных о компании (характеристик)

    """
    print("Вызвана функция: recommend_it_solutions")
    # Создаем словарь с условиями и соответствующими решениями
    it_recommendations_map = {
        'formalization_level': ('Нет формализации процессов', ['CRM']),
        'automation_systems': ('Отсутствие автоматизации основных бизнес-процессов', ['СЭД']),
        'kpi_metrics': ('Использование показателей KPI без автоматизированных решений', ['BI-система', 'Big Data Analytics']),
        'data_driven_decisions': ('Решение задач без опоры на цифровые технологии', ['Data-driven система поддержки принятия решений']),
        'it_systems_used': ('Необходимо больше использовать современные ИТ-системы', ['Автоматизированные системы учета и отчетности']),
        'systems_integration': ('Невозможность интеграции существующих систем', ['Средства интеграции приложений']),
        'cloud_services_usage': ('Недостаточное использование облачных сервисов', ['Облачные сервисы']),
        'info_security_measures': ('Проблемы с уровнем информационной безопасности', ['Политика безопасности']),
        'digital_literacy': ('Низкий уровень цифровой грамотности сотрудников', ['Программы повышения квалификации персонала']),
        'training_programs': ('Отсутствуют программы обучения сотрудников', ['Программа подготовки кадров']),
        'it_specialists_in_house': ('Отсутствие внутренних ИТ-специалистов', ['Привлечение сторонних консультантов или создание собственной команды']),
        'employees_automation_perception': ('Негативное отношение сотрудников к автоматизации', ['Мероприятия по повышению осведомленности о преимуществах автоматизации']),
        'it_strategy': ('Отсутствие стратегии внедрения ИТ-технологий', ['Создание ИТ-стратегии компании'])
    }

    # Список возможных рекомендаций
    recommended_solutions = []

    for key in data.keys():
        if key not in it_recommendations_map:
            continue

        condition, solutions = it_recommendations_map[key]
        # Проверяем условие на основании значения параметра
        value = data.get(key)
        if (value != " ") and (value != " "):
            recommended_solutions.extend(solutions)

    return ', '.join(recommended_solutions)


# Функция №2 дополнение: Описание конкретных ИТ-решений

# Чтение JSON-файла и загрузка данных в словарь
with open('IT_solutions_database.json', encoding='utf-8') as file:  # Используйте нужную кодировку
    IT_solutions = json.load(file)

@tool
def show_all_IT_solutions() -> Dict:
    """
    Выводит подробный список всех описаний конкретных ИТ-решений из базы данных.

    Returns: Dict: Словарь с информацией об ИТ-решениях
    """
    print("Вызвана функция: show_all_IT_solutions")
    IT_solutions_list = IT_solutions
    return(IT_solutions_list)

# Функция №3: Подбор мер господдержки

# Чтение JSON-файла и загрузка данных в словарь
with open('grants_database.json', encoding='utf-8') as file:  # Используйте нужную кодировку
    grants = json.load(file)

from datetime import datetime

@tool
def show_all_available_support() -> Dict:
    """
    Просто выводим список всех доступных мер поддержки из базы данных.

    Returns: Dict: Словарь с информацией о мерах поддержки (название и описание)
    """
    print("Вызвана функция: show_all_available_support")
    available_support_list = grants
    return(available_support_list)

"""Марат: «персонаж двадцать пятого уровня крафтит вещи для сотого».

Запустите дважды и сравните:

    python3 check_level.py
    python3 -O check_level.py

Как запускается прод, написано в deploy/run_server.sh.
"""
import random

from valera_craft import craft

random.seed(2)  # чтобы кубик выпадал одинаково при каждом запуске

inventory = [{"name": "звёздная пыль", "quality": 5} for _ in range(3)] + [{"name": "дерево", "quality": 2}]
try:
    result = craft(inventory, "посох архимага", 25)
except AssertionError as error:
    print("проверка уровня сработала:", error)
else:
    print("проверка уровня НЕ сработала. craft вернул:", result)

bot_level = True  # в админке уровень бота-тестировщика выставлен галочкой
torch = craft([{"name": "палка", "quality": 1}, {"name": "смола", "quality": 1}], "факел", bot_level)
print("бот с уровнем", bot_level, "скрафтил:", torch)

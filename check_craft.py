"""Жалобы на крафт Валеры — воспроизведение.

    python3 check_craft.py

random.seed нужен, чтобы настоящий кубик выпадал одинаково при каждом запуске.
"""
import random
from unittest.mock import patch

import valera_craft


def names(inventory):
    return [thing["name"] for thing in inventory]


def sword_kit():
    return [{"name": "сталь", "quality": 3}, {"name": "сталь", "quality": 2},
            {"name": "дерево", "quality": 4}]


print("1. Провал на кубике")
random.seed(1)
inventory = sword_kit()
print("было :", names(inventory))
result = valera_craft.craft(inventory, "меч", 10)
print("стало:", names(inventory))
print("craft вернул", result)

print("\n2. Меч из одной стали")
inventory = [{"name": "сталь", "quality": 3}, {"name": "дерево", "quality": 4}]
print("было :", names(inventory))
try:
    valera_craft.craft(inventory, "меч", 10)
except ValueError as error:
    print("ValueError:", error)
print("стало:", names(inventory))

print("\n3. Подкручиваем кубик: 0.0 меньше любого шанса, крафт обязан провалиться")


def ten_swords():
    made = []
    for _ in range(10):
        result = valera_craft.craft(sword_kit(), "меч", 10)
        made.append(result["name"] if result else None)
    return made


random.seed(2)
with patch("random.random", return_value=0.0):
    print("внутри patch('random.random')      :", ten_swords())
with patch("valera_craft.random", return_value=0.0):
    print("внутри patch('valera_craft.random'):", ten_swords())

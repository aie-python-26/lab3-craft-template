"""Крафт. Старая версия с тестового сервера.

Автор: Валера. Поддержка: никто.

Файл нужен, чтобы воспроизвести жалобы. Чинить его не надо: новый крафт
пишется в craft.py с нуля.
"""
from random import random

from recipes import RECIPES


def _count(inventory, name):
    return sum(item["name"] == name for item in inventory)


def _take(inventory, name):
    for i, item in enumerate(inventory):
        if item["name"] == name:
            return inventory.pop(i)
    raise ValueError(f"нет ингредиента: {name}")


def craft(inventory, recipe_name, player_level):
    if recipe_name not in RECIPES:
        raise ValueError(f"нет такого рецепта: {recipe_name}")
    recipe = RECIPES[recipe_name]
    assert player_level >= recipe["level"], "уровень мал для рецепта"

    # Валера: «проверки собрал списком, так их легко дописывать»
    checks = []
    for name, need in recipe["ingredients"].items():
        checks.append(lambda: _count(inventory, name) >= need)
    if not all(check() for check in checks):
        raise ValueError("не хватает ингредиентов")

    spent = []
    for name, need in recipe["ingredients"].items():
        for _ in range(need):
            spent.append(_take(inventory, name))

    if random() < recipe["fail_chance"]:
        return None  # не повезло

    item = {"name": recipe_name, "quality": min(i["quality"] for i in spent)}
    inventory.append(item)
    return item

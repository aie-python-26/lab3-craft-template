"""Крафт. Здесь вы пишете новую систему.

Рецепты и вместимость инвентаря лежат в recipes.py: их держит остальной
сервер, не трогайте. Правила и контракт — в README.
"""
from recipes import CAPACITY, RECIPES


def craft(inventory, recipe_name, player_level):
    """Скрафтить предмет по рецепту recipe_name.

    Успех: ингредиенты списаны, результат добавлен в конец inventory, craft
    возвращает его. Провал на кубике: craft возвращает None. Крафт невозможен:
    ValueError. При провале и при отказе inventory не меняется совсем.
    """
    raise NotImplementedError

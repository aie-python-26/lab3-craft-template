"""Ваши тесты крафта.

Реализацию берите только из фикстуры impl (она в conftest.py): тогда эти же
тесты можно прогнать на коде Валеры, а автопроверка — на своих реализациях.

    python3 -m pytest -q                        # ваш craft.py
    python3 -m pytest -q --impl valera_craft    # код Валеры

Все тесты и помощники держите в этом файле.
"""
from recipes import CAPACITY, RECIPES


def item(name, quality=3, equipped=False):
    thing = {"name": name, "quality": quality}
    if equipped:
        thing["equipped"] = True
    return thing


def test_torch(impl):
    """Пример. У факела шанс провала 0.0, поэтому кубик можно не трогать."""
    inventory = [item("палка", 2), item("смола", 4), item("кожа")]
    torch = impl.craft(inventory, "факел", 1)
    assert torch == {"name": "факел", "quality": 2}
    assert inventory == [item("кожа"), torch]

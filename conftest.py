"""Общая часть тестов. Не меняйте: автопроверка кладёт рядом с вашими тестами
этот же файл, а не ваш.

Фикстура impl — модуль с функцией craft, который сейчас проверяется. По
умолчанию это ваш craft.py, но реализацию можно подменить:

    python3 -m pytest -q                        # ваш craft.py
    python3 -m pytest -q --impl valera_craft    # те же тесты на коде Валеры
"""
import importlib

import pytest


def pytest_addoption(parser):
    parser.addoption("--impl", default="craft",
                     help="модуль с функцией craft, по умолчанию craft.py")


@pytest.fixture
def impl(request):
    return importlib.import_module(request.config.getoption("--impl"))

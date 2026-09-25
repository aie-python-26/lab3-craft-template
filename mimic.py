"""Мимик: делает из вашего craft.py мутантов и проверяет, заметят ли их ваши тесты.

    python3 mimic.py              # таблица в терминал
    python3 mimic.py > mimic.txt  # она же в файл, для сдачи

Мутант — craft.py с одной маленькой правкой. Если ваши тесты на мутанте
остались зелёными, мутант выжил: тесты не заметили, что код сломан.

Ваша часть — функция mutants(). Всё остальное уже написано.
"""
import ast
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def mutants(source):
    """Все мутанты исходника source. Каждый отличается от оригинала ровно одной правкой:

      1. одно сравнение сдвинуто на границе: < и <=, > и >=, == и != меняются друг на друга;
      2. один and становится or, или один or становится and;
      3. две соседние инструкции одного блока меняются местами;
      4. одна инструкция заменяется на pass.

    Блок — список инструкций в поле body или orelse любого узла, кроме самого
    модуля: верхний уровень файла (импорты, def) не трогаем.

    Возвращает список исходников — строк, которые напечатал ast.unparse.
    Подсказка: каждого мутанта делайте из свежего дерева. Порядок узлов в
    ast.walk для одного и того же исходника всегда один и тот же, поэтому
    нужный узел в свежем дереве можно найти по его номеру.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- дальше уже написано


def run_suite(source):
    """Прогнать test_craft.py, подложив source вместо craft.py. True — тесты зелёные."""
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("recipes.py", "conftest.py", "test_craft.py"):
            shutil.copy(os.path.join(HERE, name), tmp)
        with open(os.path.join(tmp, "craft.py"), "w", encoding="utf-8") as f:
            f.write(source)
        done = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"],
            cwd=tmp, capture_output=True, text=True, timeout=300,
        )
        return done.returncode == 0


def what_changed(original, mutant):
    """Короткое описание правки для таблицы."""
    old, new = original.splitlines(), mutant.splitlines()
    i = next((k for k in range(min(len(old), len(new))) if old[k] != new[k]), min(len(old), len(new)))
    if i >= min(len(old), len(new)):
        return "правка в самом конце файла"
    if sorted(old) == sorted(new):
        return f"строка {i + 1}: переставлены «{old[i].strip()}» и «{new[i].strip()}»"
    if new[i].strip() == "pass":
        return f"строка {i + 1}: «{old[i].strip()}» заменено на pass"
    return f"строка {i + 1}: {old[i].strip()}  ->  {new[i].strip()}"


def without_docstrings(source):
    """Исходник без докстрингов: мутант, который двигает строку-описание, ничего не ломает."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if (isinstance(body, list) and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)):
            del body[0]
            if not body:
                body.append(ast.Pass())
    return ast.unparse(tree)


def main():
    with open(os.path.join(HERE, "craft.py"), encoding="utf-8") as f:
        original = without_docstrings(f.read())
    if not run_suite(original):
        sys.exit("Тесты красные на вашем же craft.py: сначала почините их.")
    print("Строки считаются в craft.py, пересобранном через ast.unparse без докстрингов.\n")
    alive = 0
    for number, mutant in enumerate(mutants(original), 1):
        try:
            compile(mutant, "craft.py", "exec")
        except SyntaxError:
            status = "не компилируется"
        else:
            survived = run_suite(mutant)
            alive += survived
            status = "ВЫЖИЛ" if survived else "убит"
        print(f"{number:3}  {status:17} {what_changed(original, mutant)}")
    print(f"\nвыжило мутантов: {alive}")


if __name__ == "__main__":
    main()

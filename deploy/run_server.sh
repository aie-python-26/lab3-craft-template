#!/bin/sh
# Прод-сервер, Патч 1.8. Запускать только этим скриптом.
# Любые правки — через Марата.

export GAME_ENV=production
export GAME_PORT=7777
export PYTHONOPTIMIZE=1   # Валера: «на проде ассерты не нужны, так быстрее»

exec python3 -m game.server

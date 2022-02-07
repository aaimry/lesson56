Чтобы запустить проект создайте и активируйте виртуальное кружение
```bash
python -m venv venv
.../venv/Scripts/activate
```
Установите фреймвокр из requirements.txt

Примените миграции командой
```bash
./manage.py migrate
```
Загрузите фикстурные статьи командой
```bash
./manage.py loaddata dump.json
```
Чтобы запустить сервер выполните:
```bash
./manage.py runserver
```

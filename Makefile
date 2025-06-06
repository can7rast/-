.PHONY: install run migrate makemigrations shell clean db-reset venv fill

# Переменные
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MANAGE = $(PYTHON) manage.py
PYTHONPATH = PYTHONPATH=.

help:
	@echo "Доступные команды:"
	@echo "  make install    - Установка зависимостей и создание виртуального окружения"
	@echo "  make run        - Запуск сервера разработки"
	@echo "  make migrate    - Применение миграций"
	@echo "  make shell      - Запуск Django shell"
	@echo "  make clean      - Очистка временных файлов"
	@echo "  make db-reset   - Сброс базы данных и применение миграций заново"
	@echo "  make fill       - Заполнение базы данных тестовыми данными (пользователь gege)"

venv:
	@echo "Создание виртуального окружения..."
	python3 -m venv venv
	@echo "Активация виртуального окружения..."
	@echo "Для активации выполните: source venv/bin/activate"

install: venv
	@echo "Установка зависимостей..."
	$(PIP) install -r requirements.txt
	@echo "Применение миграций..."
	$(MANAGE) migrate
	@echo "Установка завершена!"

run:
	@echo "Запуск сервера разработки..."
	$(MANAGE) runserver

migrate:
	@echo "Применение миграций..."
	$(MANAGE) migrate

makemigrations:
	@echo "Создание миграций..."
	$(MANAGE) makemigrations

shell:
	@echo "Запуск Django shell..."
	$(MANAGE) shell

clean:
	@echo "Очистка временных файлов..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

db-reset:
	@echo "Сброс базы данных..."
	rm -f db.sqlite3
	$(MANAGE) migrate
	@echo "База данных сброшена и миграции применены заново"

fill:
	@echo "Заполнение базы данных тестовыми данными..."
	@echo "1. Сброс и базовое заполнение..."
	$(PYTHONPATH) $(PYTHON) scripts/db_population/reset_and_populate.py
	@echo "2. Добавление тестовых данных..."
	$(PYTHONPATH) $(PYTHON) scripts/db_population/populate_test_data.py
	@echo "3. Добавление записей о прогрессе..."
	$(PYTHONPATH) $(PYTHON) scripts/db_population/add_progress_records.py
	@echo "4. Обновление тренировок..."
	$(PYTHONPATH) $(PYTHON) scripts/db_population/update_workouts.py
	@echo "5. Заполнение основных данных..."
	$(PYTHONPATH) $(PYTHON) scripts/db_population/populate_db.py
	@echo "База данных успешно заполнена!"
	@echo "Данные для входа:"
	@echo "  Логин: gege"
	@echo "  Пароль: gege123" 
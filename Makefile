.PHONY: install run migrate makemigrations shell clean db-reset venv

# Переменные
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MANAGE = $(PYTHON) manage.py

help:
	@echo "Доступные команды:"
	@echo "  make install    - Установка зависимостей и создание виртуального окружения"
	@echo "  make run        - Запуск сервера разработки"
	@echo "  make migrate    - Применение миграций"
	@echo "  make shell      - Запуск Django shell"
	@echo "  make clean      - Очистка временных файлов"
	@echo "  make db-reset   - Сброс базы данных и применение миграций заново"

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
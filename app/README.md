# Проект мониторинга станочного оборудования "СтанОК"


## Документация на API
Документация по API [тут](https://documenter.getpostman.com/view/27624378/2s9YRGxpKy#2cbe29a1-c44a-4273-be96-3896f457157c)

## Как настроить и подключить Celery через брокера сообщий Redis

### Требования
Python версии не ниже 3.8.10. Рекомендованная версия python - 3.8.10
Установка всех необъодимых библиотек
```sh
$ python -m pip install -r requirements.txt
```

### Запуск первой программы

Материал по периодическим задачам в [celery](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) 

1. Чтобы запустить сервер Redis Stack с использованием образа redis-stack-server, выполните в терминале следующую команду:
```sh
$ docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```
2. Запускаем фоновый процесс обработки значений
```sh
$ celery -A app worker -B -l INFO
```
3. Полный список параметров `celery`
```sh
$ celery help
```
4. Протестируем работу программы
```sh
$ python ./manage.py shell
```
```python
>>> from device.tasks import test
>>> res = test.delay("Not hello")
>>> res.get()
'Not hello World'
```
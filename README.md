
## Запускаем через Docker

1. Сборка контейнеров
    ```sh
    $ docker-compose -f docker-compose.example.yml build
    ```

2. Запукск контейнера
    ```sh
    $ docker-compose -f docker-compose.example.yml up --detach
    ```

3. Выполнение миграций
    ```sh
    $ docker-compose -f docker-compose.example.yml exec web python manage.py migrate
    ```

4. Заполнение базы данных фиктивными значениями
    ```sh
    $ docker-compose -f docker-compose.example.yml exec web python manage.py loaddata data/fixtures/dev/machine.machine.json
    $ docker-compose -f docker-compose.example.yml exec web python manage.py loaddata data/fixtures/dev/machine.normdetail.json
    ```

5. Открываем url `http://localhost:8000/api/v1/machine/show_test_norm_detail` и молимся, чтобы что-то отображалось
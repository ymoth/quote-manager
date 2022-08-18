**qoute-manager: v1.0.0<br>Разработчик: https://vk.com/ymoth**

### Установка:
`python -m pip install https://github.com/ymoth/quote-manager/archive/main.zip`
# Удобная реализация
****
Создание своей собственной модели, библиотеке нужен путь с зависимостями, файлами, которые будут попадать в тело класса.

```commandline
- folder_name \
-- background.jpg
-- font.ttf
```

Создание своей кастомной модели в которой будет происходить интеграция цитаты:
```py
import quote_manager

quote = quote_manager.QuoteManager(path_to_dependencies="folder_name",
                                   default_font="font.ttf",
                                   background_image="background.jpg",
                                   avatar_image="URL-адресс/Название файла/Image.Image объект",
                                   fullname="Igor Zakatov",
                                   text="Release v1.0.0")
```
Все аргументы, которые можно передать:
```commandline
        # Default arguments
        self._path_to_dependencies = path_to_dependencies - Путь до папки с зависимостями
        self._fullname = fullname - Имя Фамилия пользователя
        self._text = text - Текст, который будет попадать в саму цитату
        self._date = date - Дата, тип: strftime, по умолчанию: "%d.%m.%Y в %H:%M:%S"
        self._by_project = by_project - созданно <кем>, принимает значение None, если не нужен by_project, 

        # Optional arguments
        self._background_image = background_image: ImageType, принимает в себя URL-адресс/Файл/Image.Image | Не опционален
        self._avatar_image = avatar_image: ImageType, принимает в себя URL-адресс/Файл/Image.Image | Не опционален
        self._default_font = default_font: Шрифт, который используется для всего
        self._string_line_limit = string_line_limit: Лимит строки, после N кол-во переносится на новую строку, по умолчанию: 300
        self._string_limit = string_limit: Лимит самой цитаты, по умолчанию - 300

        # Setting sizes options
        self._size_avatar = kwargs.get("size_avatar", (300, 300)) - Срезы аватара
        self._size_background = kwargs.get("size_background", (0, 0, 1280, 720)) - Срезы фона

        self._coordinates_avatar = kwargs.get("coordinates_avatar", (50, 210)) - Координаты аватара
        self._coordinates_fullname = kwargs.get("coordinates_name", (70, 520)) - Координаты имени и фамилии
        self._coordinates_date = kwargs.get("coordinates_date", (70, 545)) - Координаты даты
        self._coordinates_by_project = kwargs.get("coordinates_by_project", (70, 570)) - Координаты by_project

        # Fonts
        Шрифты берутся из %path_to_dependencies% директории. 
        self._fullname_font = kwargs.get("fullname_font", self._default_font) - Шрифт для имени и фамилии
        self._date_font = kwargs.get("date_font", self._default_font) - Шрифт для даты
        self._main_text_font = kwargs.get('main_text_font', "zero_5.ttf") - Шрифт для цитаты
        self._by_project_font = kwargs.get("by_project_font", self._default_font) - шрифт для by_project
```

# Результат, получение данных
****
Возвращается датакласс Quote, в котором есть методы для получения результата.

```py
import quote_manager

quote = quote_manager.QuoteManager(path_to_dependencies="folder_name",
                                   default_font="font.ttf",
                                   background_image="background.jpg",
                                   avatar_image="URL-адресс/Название файла/Image.Image объект",
                                   fullname="Igor Zakatov",
                                   text="Release v1.0.0")

create_quote = quote.sync_create()

create_quote.get_bytes_io - Возвращает io.BytesIO инстанс, в котором созданно само изображение в .png
create_quote.save_image("path", "filename:optional") - создаёт изображение в путь %path%, если filename не указан, библиотека генерирует название в [a-z0-9] значении
create_quote.show_image() - Открывает изображение на вашем компьютере для просмотра.
```
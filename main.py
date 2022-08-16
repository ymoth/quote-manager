from manager import QuoteManager

"""
Между выбором coroutine и sync create методами идёт абсолютно одинаковый код:
Различия в загрузке изображения по URL-адресу, передаваемого в ImageType
- background_image.
- avatar_image.

Если вы не используете загрузку по URL адресу, используйте обычный
sync_create()

Возвращаемый объект - Quote.
"""

test = QuoteManager(fullname="Имя Фамилия",
                    text="Прежде чем осуждать кого-то, возьми его обувь и пройди его путь,"
                         " попробуй его слёзы, почувствуй его боль."
                         " Наткнись на каждый камень, о который он споткнулся."
                         " И только после этого говори, что ты знаешь как правильно жить…",
                    string_line_limit=32,
                    by_project=None,
                    background_image="test/background.jpg")

test.sync_create().save_image("default_dependencies/")

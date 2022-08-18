import dataclasses
import io
import os
import typing

from PIL import ImageDraw
from PIL import Image

type_size = typing.Tuple[typing.Union[int, float], typing.Union[int, float]]


@dataclasses.dataclass
class Quote:
    _content: io.BytesIO

    @property
    def get_bytes_io(self) -> io.BytesIO:
        return self._content

    def save_image(self, path: str, image_name: str = None) -> None:
        Image.open(self._content).save(
            path + f"/quote_{os.urandom(3).hex() if not image_name else image_name}.jpg"
        )
        return None

    def show_image(self) -> None:
        Image.open(self._content).show()
        return None


@dataclasses.dataclass
class GenerateByLength:
    text: str


# Создание готовой макси для аватара, возвращает готовую маску.
def prepare_mask(sizing: type_size, alias_resize: int = 2) -> Image:
    mask = Image.new('L', (sizing[0] * alias_resize, sizing[1] * alias_resize), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(sizing, Image.ANTIALIAS)


# Обрезает и масштабирует изображение под заданный размер.
def prepare_round_the_resulting_image(image: Image, sizing: type_size):
    weight, height = image.size
    result = weight / sizing[0] - height / sizing[1]
    if result > 0:
        image = image.crop(((weight - height) / 2, 0, (weight + height) / 2, height))
    elif result < 0:
        image = image.crop((0, (height - weight) / 2, weight, (height + weight) / 2))
    return image.resize(sizing, Image.ANTIALIAS)


# Данные функция используется исключительно для главного текста, который попадает на середину Image.
def prepare_size_by_text_length(text: str) -> int:
    """Обычная проверка на длину строки, максимальный аргумент = self.limit
    Возвращает size для ImageDraw.truetype"""
    length = len(text)
    if length <= 50:
        return 48
    if length <= 100:
        return 34
    if length <= 150:
        return 23
    return 15


# Данные функция используется исключительно для главного текста, который попадает на середину Image.
def prepare_coordinates_by_text_length(text: str) -> type_size:
    """Обычная проверка на длину строки, максимальный аргумент: 300
    Возвращает координаты для Image.draw"""
    length = len(text[:300])
    if length <= 50:
        return 450, 300
    elif length <= 100:
        return 400, 210
    return 370, 180

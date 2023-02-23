import datetime
import io

import typing

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .generate_utils import (Quote,
                             prepare_round_the_resulting_image,
                             prepare_mask,
                             prepare_size_by_text_length,
                             prepare_coordinates_by_text_length)

from .downloader import coroutine_download
from .downloader import download

ImageType = typing.TypeVar(
    "ImageType",
    bound=typing.Union[Image.Image, bytes, io.BytesIO, str]
)


def open_image_with_bytes(bytes_argument: bytes) -> Image.Image:
    return Image.open(io.BytesIO(bytes_argument))


class QuoteManager:

    def __init__(
            self,
            fullname: str,
            text: str,
            path_to_dependencies: str,
            default_font: str,
            date: str = "%d.%m.%Y в %H:%M:%S",
            by_project: typing.Union[str, bool, None] = "by https://github.com/ymoth",
            background_image: ImageType = "background.jpg",
            avatar_image: ImageType = "default_avatar.jpg",
            string_limit: int = 300,
            string_line_limit: int = 30,
            **kwargs
    ):

        # Default arguments
        self._path_to_dependencies = path_to_dependencies
        self._fullname = fullname
        self._text = text
        self._date = date
        self._by_project = by_project

        # Optional arguments
        self._background_image = background_image
        self._avatar_image = avatar_image
        self._default_font = default_font
        self._string_line_limit = string_line_limit
        self._string_limit = string_limit

        # Setting sizes options
        self._size_avatar = kwargs.get("size_avatar", (300, 300))
        self._size_background = kwargs.get("size_background", (0, 0, 1280, 720))

        self._coordinates_avatar = kwargs.get("coordinates_avatar", (50, 210))
        self._coordinates_fullname = kwargs.get("coordinates_name", (70, 520))
        self._coordinates_date = kwargs.get("coordinates_date", (70, 545))
        self._coordinates_by_project = kwargs.get("coordinates_by_project", (70, 570))

        # Fonts
        self._fullname_font = kwargs.get("fullname_font", self._default_font)
        self._date_font = kwargs.get("date_font", self._default_font)
        self._main_text_font = kwargs.get('main_text_font', "zero_5.ttf")
        self._by_project_font = kwargs.get("by_project_font", self._default_font)

    def _prepare_quote_by_avatar_and_by_background(self, background: Image, avatar: Image) -> Image:
        """Создание самой цитаты, в которую попадают два параметра:
        background: Image, avatar: Image"""

        # Интеграция Image-объекта на аватарку для использования наложения
        avatar = prepare_round_the_resulting_image(avatar, self._size_avatar)
        avatar.putalpha(prepare_mask(self._size_avatar, 4))

        # Обрезка фона до нужно ширины, и наложение маски на аватарку.
        crop_background_image = background.crop(self._size_background)
        image_mask = Image.new("L", avatar.size, 0)

        # Округление аватара и наложение на слой бэкграунда
        draw = ImageDraw.Draw(image_mask)
        draw.ellipse((0, 0, *self._size_avatar), fill=255)
        crop_background_image.paste(avatar, self._coordinates_avatar, image_mask)

        prepare_image_draw = ImageDraw.Draw(crop_background_image)
        prepare_image_draw.text(
            self._coordinates_fullname, self._fullname,
            font=self._generate_font(20)
        )

        # Проверка на дату и добавление данных в цитату
        if self._date is not None:
            prepare_image_draw.text(
                self._coordinates_date,
                self._crop_message(datetime.datetime.now().strftime(self._date)),
                font=self._generate_font(20, font=self._date_font)
            )

        # Проверка на проект и добавление данных в цитату
        if self._by_project is not None:
            prepare_image_draw.text(
                self._coordinates_by_project, self._crop_message(self._by_project, limit=30, ),
                font=self._generate_font(20, font=self._by_project_font)
            )

        # Подставка текста, автоматическая реализация сайзинга и обрезания сообщения
        # За сайзинг отвечает функция generate_utils.prepare_size_by_text_length:55
        # За центрирование(координаты) отвечает функция prepare_coordinates_by_text_length:69
        prepare_image_draw.text(
            prepare_coordinates_by_text_length(self._text),
            self._crop_message(self._text),
            font=ImageFont.truetype(
                self._path_to_dependencies + "//" + self._main_text_font,
                size=prepare_size_by_text_length(self._main_text_font),
                encoding="utf-8"
            )
        )

        # Сохранение в io.Bytes()
        img_byte_arr = io.BytesIO()
        crop_background_image.save(img_byte_arr, format='PNG')

        # Возвращаемый объект, который попадёт в датакласс `Quote`
        return img_byte_arr

    def _generate_font(self, font_size: int = None, font: str = None) -> Image:
        font_size = 40 if font_size is None else font_size
        font = font or self._default_font
        file = open(self._path_to_dependencies + "//" + font, "rb")
        bytes_font = io.BytesIO(file.read())

        return ImageFont.truetype(
            bytes_font,
            size=font_size, encoding="utf-8"
        )

    def _crop_message(self, message: str, limit: int = None) -> str:
        limit = self._string_line_limit if limit is None else limit
        return "\n".join(
            [message[x:x + limit].replace("\n", " ") for x in range(0, len(message), limit)]
        )

    async def coroutine_create(self) -> Quote:
        background = await self._async_getting_image_element(self._background_image)
        avatar = await self._async_getting_image_element(self._avatar_image)
        return Quote(self._prepare_quote_by_avatar_and_by_background(background=background, avatar=avatar))

    def sync_create(self) -> Quote:
        background = self._sync_getting_image_element(self._background_image)
        avatar = self._sync_getting_image_element(self._avatar_image)
        return Quote(self._prepare_quote_by_avatar_and_by_background(background=background, avatar=avatar))

    async def _async_getting_image_element(self, attribute_image: ImageType) -> Image.Image:
        if isinstance(attribute_image, str):
            if "https://" in attribute_image:
                return open_image_with_bytes(await coroutine_download(attribute_image))
            else:
                return Image.open(self._path_to_dependencies + "//" + attribute_image)
        return Image.open(io.BytesIO(attribute_image) if isinstance(attribute_image, bytes) else attribute_image)

    def _sync_getting_image_element(self, attribute_image: ImageType) -> Image.Image:
        if isinstance(attribute_image, str):
            if "https://" in attribute_image:
                return open_image_with_bytes(download(attribute_image))
            else:
                return Image.open(self._path_to_dependencies + "//" + attribute_image)
        return Image.open(io.BytesIO(attribute_image) if isinstance(attribute_image, bytes) else attribute_image)

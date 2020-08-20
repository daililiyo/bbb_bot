# -*- coding:utf-8 -*-

import base64
import io

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from iotbot import GroupMsg, Action, FriendMsg
from iotbot.decorators import not_botself

LEFT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT = 2
LEFT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH = 1 / 4
RIGHT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT = 1
RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH = 1 / 4
RIGHT_PART_RADII = 10
BG_COLOR = '#000000'
BOX_COLOR = '#F7971D'
LEFT_TEXT_COLOR = '#FFFFFF'
RIGHT_TEXT_COLOR = '#000000'
FONT_SIZE = 50

RESOURCES_BASE_PATH = './resources/ph-logo'
FONT_PATH = f'{RESOURCES_BASE_PATH}/font/ArialEnUnicodeBold.ttf'


@not_botself
def receive_friend_msg(ctx: FriendMsg):
    if ctx.Content.startswith('ph '):
        args = [i.strip() for i in ctx.Content.split(' ') if i.strip()]
        if len(args) >= 3:
            left = args[1]
            right = args[2]
            f = combine_img_horizontal
            if len(args) >= 4:
                if args[3] == '1':
                    f = combine_img_vertical
            bot = Action(
                qq_or_bot=ctx.CurrentQQ,
                queue=True,
                queue_delay=0.5
            )

            bot.send_friend_pic_msg(
                ctx.FromUin,
                picBase64Buf=f(left, right),
            )


@not_botself
def receive_group_msg(ctx: GroupMsg):
    if ctx.Content.startswith('ph '):
        args = [i.strip() for i in ctx.Content.split(' ') if i.strip()]
        if len(args) >= 3:
            left = args[1]
            right = args[2]
            f = combine_img_horizontal
            if len(args) >= 4:
                if args[3] == '1':
                    f = combine_img_vertical
            bot = Action(
                qq_or_bot=ctx.CurrentQQ,
                queue=True,
                queue_delay=0.5
            )

            bot.send_group_pic_msg(
                ctx.FromGroupId,
                picBase64Buf=f(left, right),
            )


def create_left_part_img(text: str, font_size: int, type_='h'):
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_width, font_height = font.getsize(text)
    offset_y = font.font.getsize(text)[1][1]
    if type_ == 'h':
        blank_height = font_height * 2
    else:
        blank_height = font_height
    right_blank = int(font_width / len(text) * LEFT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH)
    img_height = font_height + offset_y + blank_height * 2
    if type_ == 'h':
        image_width = font_width + right_blank
    else:
        image_width = font_width + 2 * right_blank
    image_size = image_width, img_height
    image = Image.new('RGBA', image_size, BG_COLOR)
    draw = ImageDraw.Draw(image)
    if type_ == 'h':
        draw.text((0, blank_height), text, fill=LEFT_TEXT_COLOR, font=font)
    else:
        draw.text((right_blank, blank_height), text, fill=LEFT_TEXT_COLOR, font=font)
    return image


def create_right_part_img(text: str, font_size: int):
    radii = RIGHT_PART_RADII
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_width, font_height = font.getsize(text)
    offset_y = font.font.getsize(text)[1][1]
    blank_height = font_height * RIGHT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT
    left_blank = int(font_width / len(text) * RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH)
    image_width = font_width + 2 * left_blank
    image_height = font_height + offset_y + blank_height * 2
    image = Image.new('RGBA', (image_width, image_height), BOX_COLOR)
    draw = ImageDraw.Draw(image)
    draw.text((left_blank, blank_height), text, fill=RIGHT_TEXT_COLOR, font=font)

    # 圆
    magnify_time = 10
    magnified_radii = radii * magnify_time
    circle = Image.new('L', (magnified_radii * 2, magnified_radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, magnified_radii * 2, magnified_radii * 2), fill=255)  # 画白色圆形

    # 画4个角（将整圆分离为4个部分）
    magnified_alpha_width = image_width * magnify_time
    magnified_alpha_height = image_height * magnify_time
    alpha = Image.new('L', (magnified_alpha_width, magnified_alpha_height), 255)
    alpha.paste(circle.crop((0, 0, magnified_radii, magnified_radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((magnified_radii, 0, magnified_radii * 2, magnified_radii)),
                (magnified_alpha_width - magnified_radii, 0))  # 右上角
    alpha.paste(circle.crop((magnified_radii, magnified_radii, magnified_radii * 2, magnified_radii * 2)),
                (magnified_alpha_width - magnified_radii, magnified_alpha_height - magnified_radii))  # 右下角
    alpha.paste(circle.crop((0, magnified_radii, magnified_radii, magnified_radii * 2)),
                (0, magnified_alpha_height - magnified_radii))  # 左下角
    alpha = alpha.resize((image_width, image_height), Image.ANTIALIAS)
    image.putalpha(alpha)
    return image


def combine_img_horizontal(left_text: str, right_text, font_size: int = FONT_SIZE) -> str:
    left_img = create_left_part_img(left_text, font_size)
    right_img = create_right_part_img(right_text, font_size)
    blank = 30
    bg_img_width = left_img.width + right_img.width + blank * 2
    bg_img_height = left_img.height
    bg_img = Image.new('RGBA', (bg_img_width, bg_img_height), BG_COLOR)
    bg_img.paste(left_img, (blank, 0))
    bg_img.paste(right_img, (blank + left_img.width, int((bg_img_height - right_img.height) / 2)), mask=right_img)
    buffer = io.BytesIO()
    bg_img.save(buffer, format='png')
    return base64.b64encode(buffer.getvalue()).decode()


def combine_img_vertical(left_text: str, right_text, font_size: int = FONT_SIZE) -> str:
    left_img = create_left_part_img(left_text, font_size, type_='v')
    right_img = create_right_part_img(right_text, font_size)
    blank = 15
    bg_img_width = max(left_img.width, right_img.width) + blank * 2
    bg_img_height = left_img.height + right_img.height + blank * 2
    bg_img = Image.new('RGBA', (bg_img_width, bg_img_height), BG_COLOR)
    bg_img.paste(left_img, (int((bg_img_width - left_img.width) / 2), blank))
    bg_img.paste(right_img, (int((bg_img_width - right_img.width) / 2), blank + left_img.height), mask=right_img)
    buffer = io.BytesIO()
    bg_img.save(buffer, format='png')
    return base64.b64encode(buffer.getvalue()).decode()

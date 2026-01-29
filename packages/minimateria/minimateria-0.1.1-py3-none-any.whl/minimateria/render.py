import pygame as pg

import os

from .info import ITEM_TILES, DISPLAY, RECIPES


pg.font.init()

window = pg.display.set_mode((1080, 840))

FONT = pg.font.SysFont('Lucida Console', 24)
IMAGES = {}
SPRITES_FOLDER = os.path.normpath(os.path.join(__file__, "../..", "sprites"))
for filename in os.listdir(SPRITES_FOLDER):
    IMAGES[filename.split(".")[0]] = pg.image.load(os.path.join(SPRITES_FOLDER, filename)).convert_alpha()

def rendering(location, tiles, tile_size, extended_view, frame, recipe_number, recipe_machine, inventory, inventory_number):
    if location == 0:
        bg_color = (187, 187, 187)
    else:
        bg_color = (113, 153, 232)
    window.fill(bg_color)
    for tile in tiles[location]:
        if isinstance(tile, tuple):
            current_tile = tiles[location][tile]
            if current_tile["kind"] in IMAGES:
                machine_image = pg.transform.scale(IMAGES[current_tile["kind"]], (tile_size, tile_size))
            else:
                machine_image = pg.transform.scale(IMAGES[f"{current_tile["kind"]}{frame}"], (tile_size, tile_size))
            if current_tile["kind"] in ITEM_TILES:
                machine_image = pg.transform.rotate(machine_image, current_tile["rotation"] * 90)
            window.blit(machine_image, (tile_size * tile[0], tile_size * tile[1]))
            if current_tile["kind"] in DISPLAY and len(current_tile["inventory"]):
                current_tile["item"] = list(current_tile["inventory"])[0]
            if current_tile["kind"] in RECIPES:
                if extended_view:
                    current_tile["item"] = RECIPES[current_tile["kind"]][current_tile["recipe"]][0][0]
                    arrow_image = pg.transform.scale(IMAGES["arrow"], (tile_size, tile_size))
                    arrow_image = pg.transform.rotate(arrow_image, current_tile["rotation"] * 90)
                    window.blit(arrow_image, (tile_size * tile[0], tile_size * tile[1]))
                elif "item" in current_tile:
                    del current_tile["item"]
            if "item" in current_tile:
                display = current_tile["item"]
                display_place = (tile_size * (tile[0] + 1 / 4), tile_size * (tile[1] + 1 / 4))
                if current_tile["item"] in IMAGES:
                    content_image = pg.transform.scale(IMAGES[display], (tile_size // 2, tile_size // 2))
                else:
                    content_image = pg.transform.scale(IMAGES[f"{display}0"], (tile_size // 2, tile_size // 2))
                window.blit(content_image, display_place)
                if current_tile["kind"] in DISPLAY:
                    window.blit(FONT.render(str(current_tile["inventory"][display]), False, (0, 0, 0)), display_place)
    pg.draw.rect(window, (108, 107, 107), pg.Rect(720, 0, 360, 720))
    pg.draw.rect(window, (207, 210, 53), pg.Rect(720, 24 * (recipe_number + 1), 360, 24))
    window.blit(FONT.render(recipe_machine.capitalize(), False, (0, 0, 0)), (720, 0))
    i = 0
    for recipe in RECIPES[recipe_machine]:
        i += 1
        text = ""
        for input in recipe[1]:
            text += f"{input[1]}:{input[0]};  &  "
        text = text[:-3]
        text += f"-> {recipe[0][1]}:{recipe[0][0]}; "
        j = 0
        x = 0
        while j < len(text):
            if text[j] == ":":
                j += 1
                image_text = ""
                while text[j] != ";":
                    image_text += text[j]
                    j += 1
                if image_text in IMAGES:
                    item_image = IMAGES[image_text]
                else:
                    item_image = IMAGES[f"{image_text}0"]
                window.blit(pg.transform.scale(item_image, (24, 24)), (720 + 12 * x, 24 * i))
            else:
                window.blit(FONT.render(text[j], False, (0, 0, 0)), (720 + 12 * x, 24 * i))
            j += 1
            x += 1
    pg.draw.rect(window, (108, 107, 107), pg.Rect(0, 720, 1080, 120))
    pg.draw.rect(window, (207, 210, 53), pg.Rect(48 * inventory_number, 720, 48, 120))
    x = 0
    for item in inventory:
        if item in IMAGES:
            item_image = IMAGES[item]
        else:
            item_image = IMAGES[f"{item}0"]
        window.blit(pg.transform.scale(item_image, (48, 48)), (48 * x, 720))
        window.blit(FONT.render(str(inventory[item]), False, (0, 0, 0)), (48 * x, 768))
        x += 1
    return window
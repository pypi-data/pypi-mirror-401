import pygame as pg

from .info import CRAFTING, DISPLAY, RECIPES


def update_keys(tiles, location, position, inventory, recipe_number, recipe_machine, extended_view):
    key = pg.key.get_pressed()
    if key[pg.K_r] and isinstance(location, int):
        if position in tiles[location]:
            tiles[location][position]["rotation"] = (tiles[location][position]["rotation"] + 1) % 4
    elif key[pg.K_e]:
        if position in tiles[location]:
            if tiles[location][position]["kind"] in DISPLAY:
                if len(tiles[location][position]["inventory"]):
                    inventory_key = list(tiles[location][position]["inventory"])[0]
                    if inventory_key not in inventory:
                        inventory[inventory_key] = tiles[location][position]["inventory"][inventory_key]
                    else:
                        inventory[inventory_key] += tiles[location][position]["inventory"][inventory_key]
                    inventory[inventory_key] = min(inventory[inventory_key], 64)
                    tiles[location][position]["inventory"] = {}
                    if "item" in tiles[location][position]:
                        del tiles[location][position]["item"]
            elif "room" in tiles[location][position]:
                location = tiles[location][position]["room"]
        elif location:
            location = tiles[location]["inside"][0]
    elif key[pg.K_LALT]:
        extended_view = not extended_view
    elif key[pg.K_LEFT]:
        recipe_machine = (recipe_machine - 1) % len(CRAFTING)
        recipe_number = 0
    elif key[pg.K_RIGHT]:
        recipe_machine = (recipe_machine + 1) % len(CRAFTING)
        recipe_number = 0
    elif key[pg.K_UP]:
        recipe_number = (recipe_number - 1) % len(RECIPES[CRAFTING[recipe_machine]])
    elif key[pg.K_DOWN]:
        recipe_number = (recipe_number + 1) % len(RECIPES[CRAFTING[recipe_machine]])
    return tiles, location, inventory, recipe_number, recipe_machine, extended_view
from .info import BUILDINGS, RECIPES, ITEM_TILES, ROOM, CRAFTING
from .craft import crafting


def update_mouse(button, tiles, location, position, inventory, inventory_number, recipe_machine, recipe_number):
    if button == 1:
        if position not in tiles[location]:
            if len(inventory):
                inventory_key = list(inventory)[inventory_number]
                if inventory_key in BUILDINGS:
                    tiles[location][position] = {"kind": inventory_key, "rotation": 0}
                    if inventory_key in RECIPES:
                        tiles[location][position]["recipe"] = 0
                    if inventory_key not in ITEM_TILES and inventory_key not in ROOM:
                        tiles[location][position]["inventory"] = {}
                    elif inventory_key in ROOM:
                        tiles[location][position]["room"] = 0
                        while tiles[location][position]["room"] in tiles:
                            tiles[location][position]["room"] += 1
                        tiles[tiles[location][position]["room"]] = {"inside": (location, position)}
                    inventory[inventory_key] -= 1
                    if inventory[inventory_key] == 0:
                        del inventory[inventory_key]
                if inventory_number >= len(inventory):
                    inventory_number = len(inventory) - 1
        elif "recipe" in tiles[location][position]:
            current_tile = tiles[location][position]
            current_tile["recipe"] = (current_tile["recipe"] + 1) % len(RECIPES[current_tile["kind"]])
    elif button == 3:
        if position in tiles[location]:
            if "room" in tiles[location][position] and len(tiles[tiles[location][position]["room"]]) == 0:
                del tiles[tiles[location][position]["room"]]
            del tiles[location][position]
        else:
            current_recipe = RECIPES[CRAFTING[recipe_machine]][recipe_number]
            inventory = crafting(current_recipe, inventory)
            for item in inventory:
                inventory[item] = min(inventory[item], 64)
    elif len(inventory):
        if button == 4:
            inventory_number = (inventory_number - 1) % len(inventory)
        elif button == 5:
            inventory_number = (inventory_number + 1) % len(inventory)
    return tiles, inventory_number, inventory
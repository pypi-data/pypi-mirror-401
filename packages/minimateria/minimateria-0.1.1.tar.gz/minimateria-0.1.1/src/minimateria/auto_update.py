from .info import ADJACENT, ITEM_TILES, RECIPES, DISPLAY, ROOM
from .craft import crafting


def update_auto(tiles):
    new_tiles = {}
    for room in tiles:
        new_tiles[room] = {}
        for tile in tiles[room]:
            if isinstance(tile, tuple):
                new_tiles[room][tile] = {}
                for content in tiles[room][tile]:
                    new_tiles[room][tile][content] = tiles[room][tile][content]
            else:
                new_tiles[room][tile] = tiles[room][tile]
    for room in tiles:
        for tile in tiles[room]:
            if isinstance(tile, tuple):
                current_tile = tiles[room][tile]
                next_tile = (tile[0] + ADJACENT[current_tile["rotation"]][0], tile[1] + ADJACENT[current_tile["rotation"]][1])
                next_room = room
                while tiles[next_room].get(next_tile, {"kind": None})["kind"] in ROOM:
                    room_size = ROOM[tiles[next_room][next_tile]["kind"]]
                    next_room = tiles[next_room][next_tile]["room"]
                    if ADJACENT[current_tile["rotation"]][0] == 0:
                        next_tile = (room_size // 2, (ADJACENT[current_tile["rotation"]][1] // 2) % room_size)
                    else:
                        next_tile = ((ADJACENT[current_tile["rotation"]][0] // 2) % room_size, room_size // 2)
                while next_room > 0 and (next_tile[0] >= room_size or next_tile[0] < 0 or next_tile[1] >= room_size or next_tile[1] < 0):
                    next_tile = (tiles[next_room]["inside"][1][0] + ADJACENT[current_tile["rotation"]][0], tiles[next_room]["inside"][1][1] + ADJACENT[current_tile["rotation"]][1])
                    next_room = tiles[next_room]["inside"][0]
                if next_tile in tiles[next_room]:
                    if current_tile["kind"] in ITEM_TILES and "item" in current_tile:
                        if tiles[next_room][next_tile]["kind"] in ITEM_TILES:
                            if "item" not in new_tiles[next_room][next_tile]:
                                new_tiles[next_room][next_tile]["item"] = current_tile["item"]
                            else:
                                new_tiles[next_room][next_tile]["buffer_item"] = current_tile["item"]
                            del new_tiles[room][tile]["item"]
                        elif "inventory" in tiles[next_room][next_tile]:
                            moveable = True
                            if tiles[next_room][next_tile]["kind"] in RECIPES:
                                for item in RECIPES[tiles[next_room][next_tile]["kind"]][tiles[next_room][next_tile]["recipe"]][1]:
                                    if item[0] == current_tile["item"]:
                                        break
                                else:
                                    moveable = False
                            elif tiles[next_room][next_tile]["kind"] in DISPLAY and len(tiles[next_room][next_tile]["inventory"]):
                                if list(tiles[next_room][next_tile]["inventory"])[0] != current_tile["item"]:
                                    moveable = False
                            if moveable:
                                if current_tile["item"] not in tiles[next_room][next_tile]["inventory"]:
                                    new_tiles[next_room][next_tile]["inventory"][current_tile["item"]] = 1
                                else:
                                    new_tiles[next_room][next_tile]["inventory"][current_tile["item"]] += 1
                                del new_tiles[room][tile]["item"]
                    elif current_tile["kind"] in RECIPES:
                        current_recipe = RECIPES[current_tile["kind"]][current_tile["recipe"]]
                        current_tile["inventory"] = crafting(current_recipe, current_tile["inventory"])
                        if current_recipe[0][0] in current_tile["inventory"]:
                            if tiles[next_room][next_tile]["kind"] in ITEM_TILES:
                                if "item" not in new_tiles[next_room][next_tile]:
                                    new_tiles[next_room][next_tile]["item"] = current_recipe[0][0]
                                else:
                                    new_tiles[next_room][next_tile]["buffer_item"] = current_recipe[0][0]
                                current_tile["inventory"][current_recipe[0][0]] -= 1
                            elif "inventory" in tiles[next_room][next_tile]:
                                moveable = True
                                if tiles[next_room][next_tile]["kind"] in RECIPES:
                                    for item in RECIPES[tiles[next_room][next_tile]["kind"]][tiles[next_room][next_tile]["recipe"]][1]:
                                        if item[0] == current_recipe[0][0]:
                                            break
                                    else:
                                        moveable = False
                                elif tiles[next_room][next_tile]["kind"] in DISPLAY and len(tiles[next_room][next_tile]["inventory"]):
                                    if list(tiles[next_room][next_tile]["inventory"])[0] != current_recipe[0][0]:
                                        moveable = False
                                if moveable:
                                    if current_recipe[0][0] not in tiles[next_room][next_tile]["inventory"]:
                                        new_tiles[next_room][next_tile]["inventory"][current_recipe[0][0]] = 1
                                    else:
                                        new_tiles[next_room][next_tile]["inventory"][current_recipe[0][0]] += 1
                                    current_tile["inventory"][current_recipe[0][0]] -= 1
                            if current_tile["inventory"][current_recipe[0][0]] == 0:
                                del current_tile["inventory"][current_recipe[0][0]]
                if "inventory" in new_tiles[room][tile]:
                    for item in new_tiles[room][tile]["inventory"]:
                        new_tiles[room][tile]["inventory"][item] = min(new_tiles[room][tile]["inventory"][item], 64)
    for room in tiles:
        for tile in new_tiles[room]:
            if "buffer_item" in new_tiles[room][tile] and "item" not in new_tiles[room][tile]:
                new_tiles[room][tile]["item"] = new_tiles[room][tile]["buffer_item"]
                del new_tiles[room][tile]["buffer_item"]
    return new_tiles
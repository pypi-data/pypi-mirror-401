import pygame as pg

from .info import FPS, CRAFTING
from .auto_update import update_auto
from .render import rendering
from .key_input import update_keys
from .mouse_input import update_mouse


def main() -> str:
    pg.init()
    pg.display.set_caption("Minimateria")
    
    clock = pg.time.Clock()
    run = True
    tick = 0
    tiles = {0: {}}
    location = 0
    tile_number = 3
    extended_view = False
    inventory = {}
    inventory_number = 0
    recipe_number = 0
    recipe_machine = 0
    
    while run:
        clock.tick(FPS)

        tick += 1
        tile_size = 720 // tile_number
        position = (pg.mouse.get_pos()[0] // tile_size, pg.mouse.get_pos()[1] // tile_size)
        frame = (tick // 2) % 6

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN and isinstance(location, int) and position[0] < 720:
                tiles, inventory_number, inventory = update_mouse(event.button, tiles, location, position, inventory, inventory_number, recipe_machine, recipe_number)
            elif event.type == pg.KEYDOWN:
                tiles, location, inventory, recipe_number, recipe_machine, extended_view = update_keys(tiles, location, position, inventory, recipe_number, recipe_machine, extended_view)
        
        if tick % FPS == 0:
            tiles = update_auto(tiles)
        rendering(location, tiles, tile_size, extended_view, frame, recipe_number, CRAFTING[recipe_machine], inventory, inventory_number)

        pg.display.update()
    pg.quit()

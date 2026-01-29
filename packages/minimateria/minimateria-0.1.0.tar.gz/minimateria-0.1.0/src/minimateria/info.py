FPS = 24
ADJACENT = ((1, 0), (0, -1), (-1, 0), (0, 1))
ITEM_TILES = {"belt"}
DISPLAY = {"vault"}
BUILDINGS = ("belt", "compactor", "smelter", "vault", "crafter", "tiny room")
CRAFTING = ("compactor", "smelter", "crafter")
ROOM = {"tiny room": 3}
RECIPES = {
    "compactor": (
        (("compactium", 1), ()),
        (("compactium machine casing", 1), (("compactium gear", 1), ("dried compactium", 2))),
        (("tiny room", 1), (("compactor", 1), ("smelter", 1))),
    ),
    "crafter": (
        (("compactium gear", 1), (("compactium", 2),)),
        (("dried compactium gear", 1), (("dried compactium", 2),)),
        (("belt", 1), (("compactium machine casing", 1), ("compactium", 1), ("dried compactium", 1))),
        (("compactor", 1), (("compactium machine casing", 1), ("compactium gear", 1))),
        (("smelter", 1), (("compactium machine casing", 1), ("dried compactium gear", 1))),
        (("vault", 1), (("belt", 1), ("compactium gear", 1))),
        (("crafter", 1), (("belt", 1), ("dried compactium gear", 1))),
    ),
    "smelter": (
        (("dried compactium", 1), (("compactium", 1),)),
    ),
}
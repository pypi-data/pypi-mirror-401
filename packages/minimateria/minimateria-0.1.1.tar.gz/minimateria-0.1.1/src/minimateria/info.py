FPS = 24
ADJACENT = ((1, 0), (0, -1), (-1, 0), (0, 1))
ITEM_TILES = {"belt"}
DISPLAY = {"vault"}
BUILDINGS = ("belt", "compactor", "smelter", "vault", "crafter", "tiny room", "pure compactor")
CRAFTING = ("compactor", "smelter", "crafter", "pure compactor")
ROOM = {"tiny room": 3}
RECIPES = {
    "compactor": (
        (("compactium", 1), ()),
        (("compactium machine casing", 1), (("compactium gear", 1), ("dried compactium", 2))),
        (("tiny room", 1), (("compactor", 1), ("smelter", 1))),
        (("compactium crystal", 1), (("compactium gear", 1), ("dried compactium gear", 1), ("belt", 1), ("compactium machine casing", 1))),
        (("pure compactium machine casing", 1), (("tiny room", 1), ("pure compactium gear", 1))),
    ),
    "smelter": (
        (("dried compactium", 1), (("compactium", 1),)),
        (("pure compactium", 1), (("compactium crystal", 1),)),
    ),
    "crafter": (
        (("compactium gear", 1), (("compactium", 2),)),
        (("dried compactium gear", 1), (("dried compactium", 2),)),
        (("belt", 1), (("compactium machine casing", 1), ("compactium", 1), ("dried compactium", 1))),
        (("compactor", 1), (("compactium machine casing", 1), ("compactium gear", 1))),
        (("smelter", 1), (("compactium machine casing", 1), ("dried compactium gear", 1))),
        (("vault", 1), (("belt", 1), ("compactium gear", 1))),
        (("crafter", 1), (("belt", 1), ("dried compactium gear", 1))),
        (("pure compactium gear", 1), (("pure compactium", 2), ("compactium gear", 1))),
        (("pure compactor", 1), (("pure compactium machine casing", 1), ("compactor", 2))),
    ),
    "pure compactor": (
        (("compactium gear", 1), ()),
    ),
}
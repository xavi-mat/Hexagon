inventory = None
MANY_NAMES = []
ITEM_NAMES = []
renpy = None
config = None
Fixed = None
Solid = None
Image = None
hexmap = None
Null = None

"""renpy
init python:
"""

################################################################################
# Variables
log_list = []

################################################################################
# Classes
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.row = y % 2
        self.known = False
        self.npc = None
        self.item = None
        self.terrain = renpy.random.choice(["prado", "bosque", "colinas", "montes", "lago"])
        # self.hexagon = "hex_" + self.terrain

        self.pos = (x * 146 + 73 * self.row, y * 42)

    @property
    def adjacents(self):
        if self.row:
            return [
                (self.x, self.y - 2),
                (self.x + 1, self.y - 1),
                (self.x + 1, self.y + 1),
                (self.x, self.y + 2),
                (self.x, self.y + 1),
                (self.x, self.y - 1),
            ]
        return [
            (self.x, self.y - 2),
            (self.x, self.y - 1),
            (self.x, self.y + 1),
            (self.x, self.y + 2),
            (self.x - 1, self.y + 1),
            (self.x - 1, self.y - 1),
        ]

    @property
    def hexagon(self):
        if self.known:
            return "hex_" + self.terrain
        return Null()

    @property
    def event(self):
        if not self.known:
            return None
        if self.npc:
            return self.npc.image
        if self.item:
            return self.item.image

    def reveal(self):
        self.known = True

    @property
    def desc(self):
        desc = ""
        desc += f"Terreno: {self.terrain}\n"
        if self.npc:
            desc += "{b}" + self.npc.name + "{/b}\n"
            desc += self.npc.desc
        if self.item:
            desc += self.item.desc
        return desc


class HexagonGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        for y in range(height):
            for x in range(width):
                self.cells.append(Cell(x, y))

    def get_cell(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.cells[y * self.width + x]

    def get_adjacents(self, cell):
        adj_coords = cell.adjacents
        adj_cells = [self.get_cell(*coords) for coords in adj_coords]
        adj_cells = [c for c in adj_cells if c]
        return adj_cells

    def get_distance(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if (dx >= 0) == (dy >= 0):
            return max(abs(dx), abs(dy))
        else:
            return abs(dx) + abs(dy)

    def get_path(self, x1, y1, x2, y2):
        path = []
        while x1 != x2 or y1 != y2:
            min_distance = self.get_distance(x1, y1, x2, y2)
            min_cell = None
            for cell in self.get_adjacent_cells(x1, y1):
                distance = self.get_distance(cell.x, cell.y, x2, y2)
                if distance < min_distance:
                    min_distance = distance
                    min_cell = cell
            if min_cell:
                path.append(min_cell)
                x1, y1 = min_cell.x, min_cell.y
            else:
                break
        return path


class NPC:
    def __init__(self, ide, name, image):
        self.ide = str(ide)
        self.name = name
        self.image = image
        self.visit = 0
        self.wants = None
        self.has = None
        self.label = "visit_npc_" + self.ide
        self.dismiss = True

    @property
    def desc(self):
        desc = ""
        if self.wants:
            wanted = self.wants.name
            if inventory.has_item(self.wants):
                wanted = "{color=#44ff44}" + wanted + "{/color}"
            else:
                wanted = "{color=#ff4444}" + wanted + "{/color}"
            desc += f"Quiere: {wanted}\n"
        if self.has:
            desc += f"Tiene: {self.has.name}\n"
        desc += f"Visitas: {self.visit}\n"
        return desc

class Item:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def has_item(self, item):
        return item in self.items



################################################################################
# Functions
def select_cell(c):
    global cell, adjacents, npc
    c.reveal()
    cell = c
    npc = cell.npc
    adjacents = hexmap.get_adjacents(cell)
    for c in adjacents:
        c.reveal()

def create_npcs(items):
    renpy.random.shuffle(MANY_NAMES)
    num = (len(items) - 1) * 3
    npcs = []
    for i in range(num):
        name = MANY_NAMES[i]
        image = "npc_" + str(renpy.random.randint(1, 12))
        npc = NPC(i, name, image)
        npcs.append(npc)
    renpy.random.shuffle(npcs)
    for i in range(num):
        item_index = i // 3
        npcs[i].wants = items[item_index]
        npcs[i].has = items[item_index+1]
    return npcs

def create_items(num):
    renpy.random.shuffle(ITEM_NAMES)
    items = []
    for i in range(num):
        name = ITEM_NAMES[i]
        image = "item_" + str(renpy.random.randint(1, 6))
        item = Item(name, image)
        items.append(item)
    renpy.random.shuffle(items)
    return items

def get_available_cells(num):
    """
    Return a list of cells that are not water and not the starting cell.
    So the charas can be placed on them.
    """
    available = [c for c in hexmap.cells if c.terrain != "lago" and not (c.x==0 and c.y==12)]
    return renpy.random.sample(available, num)

def place_npcs_on_map(npcs):
    cells = get_available_cells(len(npcs))
    for npc, cell in zip(npcs, cells):
        cell.npc = npc


################################################################################
# Helpers
def logit(txt):
    log_list.append(txt)

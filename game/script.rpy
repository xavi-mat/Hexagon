
define e = Character("Eileen")


label start:

    $ _confirm_quit = False

    scene expression Solid("#000000")

    # Initialize
    $ items = create_items(21)
    $ inventory = Inventory()
    $ inventory.add_item(items[0])
    $ inventory.add_item(renpy.random.choice(items))
    $ inventory.add_item(renpy.random.choice(items))
    $ inventory.add_item(renpy.random.choice(items))
    $ hexmap = HexagonGrid(10,25)
    $ npcs = create_npcs(items)
    $ place_npcs_on_map(npcs)

    $ cell = hexmap.get_cell(0, 12)
    $ cell.terrain = renpy.random.choice(["prado", "bosque", "colinas", "montes"])
    $ adjacents = hexmap.get_adjacents(cell)
    $ select_cell(cell)

    show screen main_map


    jump main_loop


label main_loop:

    call screen over_map
    hide screen main_map
    show screen main_map

    $ new_cell = _return
    $ select_cell(new_cell)

    if npc:
        $ npc.visit += 1
        if npc.wants:
            "[npc.name] quiere «[npc.wants.name]» y tiene «[npc.has.name]».\n{nw}"
            if inventory.has_item(npc.wants):
                extend "Has dado a [npc.name] lo que quería."
                $ inventory.remove_item(npc.wants)
                $ inventory.add_item(npc.has)
                $ npc.wants = None
                $ npc.has = None
            else:
                extend "No tienes lo que quiere."
        else:
            pass # Another visit

    jump main_loop
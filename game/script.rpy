
define e = Character("Eileen")


label start:

    if config.developer:
        $ _confirm_quit = False

    scene black

    # Initialize
    $ items = create_items(21)
    $ inventory = Inventory()
    $ inventory.add_item(items[0])
    $ inventory.add_item(renpy.random.choice(items))
    $ inventory.add_item(renpy.random.choice(items))
    $ inventory.add_item(renpy.random.choice(items))
    $ hexmap = HexagonGrid(10, 24)
    $ npcs = create_npcs(items)
    $ place_npcs_on_map(npcs)

    # Starting point
    $ cell = hexmap.get_cell(0, 12)
    $ cell.terrain = renpy.random.choice(["prado", "bosque", "colinas", "montes"])
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

        if renpy.has_label(npc.label):
            call expression npc.label

        if npc.wants:
            if inventory.has_item(npc.wants):
                menu:
                    "Darle a [npc.name] «[npc.wants.name]» a cambio de «[npc.has.name]».":
                        # "Has dado a [npc.name] lo que quería."
                        $ inventory.remove_item(npc.wants)
                        $ inventory.add_item(npc.has)
                        $ npc.wants = None
                        $ npc.has = None
                        if npc.dismiss:
                            $ cell.npc = None  # Delete npc from map
                    "No darle nada.":
                        pass
            # else:
            #     "[npc.name] quiere «[npc.wants.name]» y tiene «[npc.has.name]».\n{nw}"
            #     extend "No tienes lo que quiere."
        # else:
        #     pass # Another visit

    jump main_loop

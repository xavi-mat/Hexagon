screen main_map():

    default innpc = None

    for c in hexmap.cells:
        fixed:
            xysize(100, 86)
            pos c.pos
            add c.hexagon
            if c.event and c.npc and inventory.has_item(c.npc.wants):
                add "wanted_marker" align (0.5, 0.5)
            if c.event:
                imagebutton idle c.event:
                    align (0.5, 0.5)
                    action SetScreenVariable("innpc", c.npc)

            if cell == c:
                add "hexagon_selected"

    frame:
        xpos 1485
        xsize 435 yfill True
        has vbox
        label "Cell"
        text "[cell.desc]" size 24

        if innpc:
            add Solid("#0000CC", ysize = 5)
            label "[innpc.name]"
            text "[innpc.desc]" size 24

        if inventory.items:
            add Solid("#0000CC", ysize = 5)
            label "Inventario"
            for item in inventory.items:
                text "[item.name]" size 24

        add Solid("#0000CC", ysize = 5)
        for line in log_list:
            text line size 18


screen over_map():

    for c in adjacents:
        if c and not c.terrain == "lago":
            fixed:
                xysize(100, 86)
                pos c.pos
                imagebutton idle Text("🟠", size=22) hover Text("🟡", size=22):
                    align (0.5, 1.0)
                    action Return(c)

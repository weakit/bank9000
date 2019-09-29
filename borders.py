# border characters
vrt = "│"
hor = "─"
rgt = "┐"
lft = "┌"
rgb = "┘"
lfb = "└"
rgh = "┤"
lfh = "├"
uph = "┴"
bth = "┬"
blk = "█"


def line_border(width, height):
    top = lft + (hor * (width - 2)) + rgt
    mid = vrt + (' ' * (width - 2)) + vrt
    bot = lfb + (hor * (width - 2)) + rgb
    scr = top + (('\n' + mid) * (height - 2)) + '\n' + bot
    return scr


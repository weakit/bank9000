width, height = 80, 24  # common terminal size

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


def size(w, h):
    global width, height
    width, height = w, h


def line_border(w=None, h=None):
    if not w or not h:
        w, h = width, height
    top = lft + (hor * (w - 2)) + rgt
    mid = vrt + (' ' * (w - 2)) + vrt
    bot = lfb + (hor * (w - 2)) + rgb
    scr = top + (('\n' + mid) * (h - 2)) + '\n' + bot
    return scr


def overlay_line(base, line):
    if len(line) > len(base):  # if overlay line exceeds base line, cut excess
        line = line[:len(base)]
    for n, char in enumerate(line):
        if not char.isspace():
            base = base[:n] + char + base[n + 1:]
    return base


def overlay(base, *layers):
    if not layers:
        return base
    base_lines = base.split('\n')
    layer_lines = [layer.split('\n') for layer in layers]
    for layer in layer_lines:
        if len(layer) > len(base_lines):  # if number of lines exceed base lines, ignore excess
            layer = layer[:len(base_lines)]
        for n, line in enumerate(layer):
            base_lines[n] = overlay_line(base_lines[n], line)
    return "".join(base_lines)


def centre_text(text, w=None):
    if not w:
        w = width
    text = text.split('\n')
    sl = len(max(text, key=len))
    spaces = ' ' * (width // 2 - sl // 2)
    text = [spaces + x + '\n' for x in text]
    return "".join(text)[:-1]  # remove last \n


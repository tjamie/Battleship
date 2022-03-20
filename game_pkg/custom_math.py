import re


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


def convert_coords(coords):
    try:
        # eg, A4 => [0,3]
        # ABC# => [i,j]
        # allows some flexibility in user inputs, so A1, A-1, A 1 etc should work
        alpha = "".join(re.findall("[a-zA-Z]+", coords))
        # This assumes a maximum grid height of 26
        i = ord(alpha.lower()) - 96 - 1
        j = int("".join(re.findall("[0-9]+", coords))) - 1
        #print([i, j])
        return True, [i, j]
    except:
        return False, [0, 0]


def validate_coords(coords, grid):
    try:
        i = coords[0]
        j = coords[1]

        if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]):
            return True
        else:
            return False
    except:
        return False


def direction_handler(direction):
    dir = direction.lower()
    e = 0
    s = 0
    if dir == "s" or dir == "south":
        s = 1
    elif dir == "e" or dir == "east":
        e = 1
    elif dir == "n" or dir == "north":
        s = -1
    elif dir == "w" or dir == "west":
        e = -1
    else:
        # print("<DEBUG> Invalid direction argument")
        None

    return e, s

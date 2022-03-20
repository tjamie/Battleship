import game_pkg.custom_math as cmath
import time
import copy
import random

delay = 0.5


class Battlefield():
    def __init__(self, height, width):
        # build i x j playfields with this variable
        grid = self.define_grid(cmath.clamp(
            height, 1, 26), cmath.clamp(width, 1, 99))

        # this is where the player will place his/her ships
        self.defense_grid = list(grid)
        # this is where the player will record hits/misses -- will simultaneously mark opponent's defense_grid
        self.attack_grid = copy.deepcopy(grid)

    def define_grid(self, height, width):
        cell = "   "

        # first_row = list([cell])*width
        # grid = list([first_row])*height
        first_row = []
        grid = []
        for i in range(0, width):
            first_row.append(cell)
        for i in range(0, height):
            grid.append(list(first_row))

        return grid

    def display_grid(self, grid):
        cell_wall = "|"
        # len(grid[0]) gets number of columns -- important if field isn't a square
        cell_floor = "   " + "----"*len(grid[0]) + "-"
        col_labels = "   "

        # Generate column labels
        for j in range(0, len(grid[0])):
            if len(str(j+1)) < 2:
                col_labels += "  {} ".format(str(j+1))
            elif len(str(j+1)) < 3:
                col_labels += " {} ".format(str(j+1))
        temp_row = ""
        result = str(col_labels) + "\n"
        result += cell_floor + "\n"

        # Generate row labels and finish building string to display grid
        for i in range(0, len(grid)):
            temp_row = " {} ".format(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]) + cell_wall
            for j in grid[i]:
                temp_row += j + cell_wall
            result += temp_row + "\n"
            result += cell_floor + "\n"
        print(result)

    def display_defense(self):
        print("Your battlefield:")
        self.display_grid(self.defense_grid)

    def display_offense(self):
        print("Your opponent's battlefield and known ship locations:")
        self.display_grid(self.attack_grid)


class Ship():
    def __init__(self, type, hp, owner):
        self.hp = hp
        self.type = type
        self.owner = owner
        self.span = set()

    def spawn(self, grid, coords, direction):
        i = coords[0]
        j = coords[1]
        ship_symbol = " S "

        d = cmath.direction_handler(direction)
        e = d[0]
        s = d[1]

        for k in range(0, self.hp):
            # print("Populating {0}, {1}".format(i+k*s, j+k*e))
            grid[i+k*s][j+k*e] = ship_symbol
            self.span.add((i+k*s, j+k*e))

    def validate_spawn_location(self, grid, coords, direction):
        # First checks if ship being placed extends beyond the play area and then checks if
        # any entities are already located within the ship's footprint

        i = coords[0]
        j = coords[1]

        imax = len(grid)-1
        jmax = len(grid[0])-1

        d = cmath.direction_handler(direction)
        e = d[0]
        s = d[1]

        if i+s*(self.hp-1) <= imax and i+s*(self.hp-1) >= 0 and j+e*(self.hp-1) <= jmax and j+e*(self.hp-1) >= 0 and not d == (0, 0):
            for k in range(0, self.hp):
                if not grid[i+k*s][j+k*e].isspace():
                    return False
            return True
        else:
            return False

    def take_damage(self, coords):
        i = coords[0]
        j = coords[1]

        # print("{0} taking damage at ({1},{2})".format(self.type, i, j))
        self.span.remove((i, j))

    def isalive(self):
        if len(self.span) > 0:
            return True
        else:
            print("The attack sank {0}'s {1}!".format(
                self.owner.capitalize(), self.type))
            time.sleep(delay)
            return False


class Player():
    # create a Human(Player) and Comp(Player) with differing methods for ship placement and attacking
    def __init__(self, name, navy, height, width):
        self.name = name
        self.bf = Battlefield(height, width)
        print("Battlefield initialized")
        self.ships = self.create_navy(navy)
        print("Navy initialized")

    def create_navy(self, navy_template):
        ships = []
        # print("Creating navy for {}!".format(self.name))
        # print("Template: {}".format(navy_template))
        for ship_type, ship_hp in navy_template.items():
            # print("Creating {}".format(ship_type))
            ships.append(Ship(ship_type, ship_hp, self.name))
        return ships


class Human(Player):
    def __init__(self, name, navy, height, width):
        super().__init__(name, navy, height, width)
        self.ishuman = True

    def spawn_ships(self):
        print("--- Ship Placement for {} ---".format(self.name.capitalize()))
        for ship in self.ships:
            while True:
                print("Currently placing: {0} (size: {1})".format(
                    ship.type, ship.hp))
                time.sleep(delay)
                print(
                    "Input ship spawn location. Format must be alpha-number, e.g. \'A-5\'")

                user_coords = cmath.convert_coords(input("Grid coordinates: "))
                if user_coords[0]:
                    coords = user_coords[1]
                    print(
                        "Input ship direction relative to the spawn point. Valid inputs are N, E, S, and W.")
                    dir = input("Direction: ").lower()
                    if ship.validate_spawn_location(self.bf.defense_grid, coords, dir):
                        ship.spawn(self.bf.defense_grid, coords, dir)
                        self.bf.display_defense()
                        break
                    else:
                        print(
                            "Invalid input. Ships can not extend beyond the play area.")
                        time.sleep(delay)
                else:
                    print("Invalid coordinate input.")

    def attack(self, other):
        # print("{}'s turn!".format(self.name.capitalize()))
        while True:
            self.bf.display_offense()
            user_coords = cmath.convert_coords(
                input("Input attack coordinates: "))
            if user_coords[0] and cmath.validate_coords(user_coords[1], self.bf.attack_grid):
                i = user_coords[1][0]
                j = user_coords[1][1]
                if self.bf.attack_grid[i][j].isspace():
                    # check enemy's defense grid, then update enemydef and useroff accordingly
                    if other.bf.defense_grid[i][j] == " S ":
                        self.bf.attack_grid[i][j] = " H "
                        other.bf.defense_grid[i][j] = " H "
                        print("The attack hit one of {}'s ships!".format(
                            other.name.capitalize()))
                        for ship in other.ships:
                            if (i, j) in ship.span:
                                ship.take_damage([i, j])
                                if not ship.isalive():
                                    other.ships.remove(ship)

                                    print("{0}'s ships remaining: {1}".format(other.name,
                                                                              len(other.ships)))
                                break
                    else:
                        self.bf.attack_grid[i][j] = " - "
                        other.bf.defense_grid[i][j] = " - "
                        print("The attack missed!")
                    self.bf.display_offense()
                    break
                else:
                    print("Invalid input. Location has already been attacked.")
                    time.sleep(delay)
            else:
                print(
                    "Invalid coordinate input. Format must be alpha-number, e.g. \'A-5\'")
                time.sleep(delay)


class Comp(Player):
    def __init__(self, name, navy, height, width):
        super().__init__(name, navy, height, width)
        self.height = height
        self.width = width
        self.ishuman = False
        self.difficulty = self.set_difficulty()
        self.hit_history = {}
        self.attack_history = set()

    def set_difficulty(self):
        while True:
            print("Difficulty selection for {}\n1. Easy\n2. Hard".format(
                self.name.capitalize()))
            choice = input("Select difficulty:").lower()
            if choice == "1" or choice == "easy":
                return "easy"
            elif choice == "2" or "hard":
                return "hard"
            else:
                print("Invalid input.")

    def spawn_ships(self):
        # Make this less of a bodge if time allows. Which it may not because of my garbo job.
        for ship in self.ships:
            while True:
                i = random.randint(0, self.height-1)
                j = random.randint(0, self.width-1)
                dir = random.choice(["n", "e", "s", "w"])
                if ship.validate_spawn_location(self.bf.defense_grid, [i, j], dir):
                    ship.spawn(self.bf.defense_grid, [i, j], dir)
                    break
                else:
                    continue

    def attack(self, other):
        # print("{}'s turn!".format(self.name.capitalize()))
        if self.difficulty == "easy":
            self.attack_easy(other)
        elif self.difficulty == "hard":
            self.attack_hard(other)

    def attack_easy(self, other):
        while True:
            # brute forcing this again unless I have time to make it better
            i = random.randint(0, self.height-1)
            j = random.randint(0, self.width-1)
            if self.bf.attack_grid[i][j].isspace():
                # check enemy's defense grid, then update enemydef and useroff accordingly
                if other.bf.defense_grid[i][j] == " S ":
                    self.bf.attack_grid[i][j] = " H "
                    other.bf.defense_grid[i][j] = " H "
                    for ship in other.ships:
                        if (i, j) in ship.span:
                            print("The attack struck {0}'s {1}!".format(
                                other.name.capitalize(), ship.type))
                            ship.take_damage([i, j])
                            if not ship.isalive():
                                other.ships.remove(ship)
                                print("{0}'s ships remaining: {1}".format(other.name,
                                                                          len(other.ships)))
                            break
                else:
                    self.bf.attack_grid[i][j] = " - "
                    other.bf.defense_grid[i][j] = " - "
                    print("The attack missed!")
                time.sleep(delay)
                break

    def attack_hard(self, other):

        while True:
            if len(self.attack_history) < 1 or len(self.hit_history) < 1:
                # randomly fire first move of the game or if no living ships have been hit
                # note: remove ships from self.hit_history once they sink
                i = random.randint(0, self.height-1)
                j = random.randint(0, self.width-1)
            else:
                # check nearby spaces for H belonging to the current target ship
                # target ship will be first item in dictionary
                # proceed with i+n or j+n until TARGET ship sinks

                target_positions = list(self.hit_history.items())[0][1]
                i = target_positions[0][0]
                j = target_positions[0][1]
                if len(target_positions) == 1:
                    # attack adjacent coordinates if target ship has only been hit once
                    if (i+1, j) not in self.attack_history and i+1 < self.height:
                        i += 1

                    elif (i-1, j) not in self.attack_history and i-1 >= 0:
                        i -= 1

                    elif (i, j+1) not in self.attack_history and j+1 < self.width:
                        j += 1

                    else:
                        j -= 1

                else:
                    # If target ship has been hit more than once, target coordinates in line with ship and adjacent to previous hit(s)
                    dir_i = 0
                    dir_j = 0
                    # determine target ship orientation
                    if (target_positions[0][0] + target_positions[1][0])/2 == target_positions[0][0]:
                        dir_j = 1
                    else:
                        dir_i = 1

                    # scan either side of hits on target ship for an empty cell
                    # go to other side if scan finds a cell with a missed attack
                    # want [i,j] not in target_positions and (i,j) not in self.attack_history
                    i_scan = i
                    j_scan = j
                    dir_scan = 1
                    delta = 1
                    legal_coords = True
                    block_positive = False
                    block_negative = False

                    # scan adjacent coordinate until empty location found
                    while True:
                        # already know ship's orientation at this point
                        if (i_scan, j_scan) not in self.attack_history and legal_coords:
                            # proceed with target coordinates
                            i = i_scan
                            j = j_scan
                            break
                        else:
                            # check positive side first, then negative side
                            # when checking negative side, delta++
                            if dir_scan == 1:
                                i_scan = i + delta*dir_i*dir_scan
                                j_scan = j + delta*dir_j*dir_scan

                                dir_scan = -1

                                if i_scan < self.height and j_scan < self.width and not block_positive:
                                    # attack history already being check at start of loop
                                    if self.bf.attack_grid[i_scan][j_scan] == " - ":
                                        block_positive = True
                                        legal_coords = False
                                    else:
                                        legal_coords = True
                                else:
                                    legal_coords = False
                            else:
                                # negative side
                                i_scan = i + delta*dir_i*dir_scan
                                j_scan = j + delta*dir_j*dir_scan

                                dir_scan = 1
                                delta += 1

                                if i_scan >= 0 and j_scan >= 0 and not block_negative:
                                    if self.bf.attack_grid[i_scan][j_scan] == " - ":
                                        block_negative = True
                                        legal_coords = False
                                    else:
                                        legal_coords = True
                                else:
                                    legal_coords = False

            if self.bf.attack_grid[i][j].isspace():
                self.attack_history.add((i, j))
                # check enemy's defense grid, then update enemydef and useroff accordingly
                if other.bf.defense_grid[i][j] == " S ":
                    self.bf.attack_grid[i][j] = " H "
                    other.bf.defense_grid[i][j] = " H "
                    for ship in other.ships:
                        if (i, j) in ship.span:
                            print("The attack struck {0}'s {1}!".format(
                                other.name.capitalize(), ship.type))
                            ship.take_damage([i, j])
                            if ship.type in self.hit_history:
                                self.hit_history[ship.type] += [(i, j)]
                            else:
                                self.hit_history[ship.type] = [(i, j)]

                            if not ship.isalive():
                                other.ships.remove(ship)
                                del self.hit_history[ship.type]
                                print("{0}'s ships remaining: {1}".format(other.name,
                                                                          len(other.ships)))
                            time.sleep(delay)
                            break
                else:
                    self.bf.attack_grid[i][j] = " - "
                    other.bf.defense_grid[i][j] = " - "
                    print("The attack missed!")
                    time.sleep(delay)
                break

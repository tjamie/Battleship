from game_pkg import entities as entity
from game_pkg import battle


default_navy = {
    "carrier": 5,
    "battleship": 4,
    "destroyer": 3,
    "submarine": 3,
    "patrol boat": 2
}

# test_navy = {
#     "pontoon": 4,
#     "airboat": 4
# }

main_menu = """\
    1. Play standard
    2. Play with custom arena
    3. Quit"""

while True:
    print("Welcome to Battleship!")
    print(main_menu)

    choice = input("Select option: ").lower()

    if choice == "1" or choice == "play":
        name = input("Input your name: ")
        h = w = 10

        bot = entity.Comp("Marvin the friendly bot", default_navy, h, w)
        bot.spawn_ships()

        player = entity.Human(name, default_navy, h, w)
        player.bf.display_defense()
        player.spawn_ships()

        battle.conflict(player, bot)

    elif choice == "2" or choice == "custom":
        name = input("Input your name: ")
        while True:
            try:
                h = int(input("Input battlefield height: "))
                break
            except:
                print("Invalid input.")
        while True:
            try:
                w = int(input("Input battlefield width: "))
                break
            except:
                print("Invalid input")

        bot = entity.Comp("Marvin the friendly bot", default_navy, h, w)
        bot.spawn_ships()

        player = entity.Human(name, default_navy, h, w)
        player.bf.display_defense()
        player.spawn_ships()

        battle.conflict(player, bot)

    elif choice == "3" or choice == "quit":
        break

    # elif choice == "4":
    #     name = "test human"

    #     h = w = 5

    #     bot = entity.Comp("Marvin the friendly bot", test_navy, h, w)
    #     bot.spawn_ships()

    #     player = entity.Human(name, test_navy, h, w)
    #     player.bf.display_defense()
    #     player.spawn_ships()

    #     battle.conflict(player, bot)

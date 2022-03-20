import random


def conflict(player1, player2):
    dice_roll = random.randint(0, 1)
    print("Battle commenced!")
    if dice_roll == 0:
        attacker = player1
        defender = player2
    else:
        attacker = player2
        defender = player1

    print("{} has the first turn.".format(attacker.name.capitalize()))

    while True:
        turn(attacker, defender)
        if len(defender.ships) < 1:
            print("{0} has no more ships remaining. {1} wins the game!".format(
                defender.name.capitalize(), attacker.name.capitalize()))
            input("Press enter to continue.")
            break
        else:
            attacker, defender = defender, attacker


def turn(attacker, defender):
    print("{}'s turn!".format(attacker.name.capitalize()))
    if attacker.ishuman:
        while True:
            print(
                "(1) Attack\n(2) Show your side of the battlefield\n(3) Show your radar")
            choice = input("Select an option: ")
            if choice == "1" or choice.lower() == "attack":
                attacker.attack(defender)
                break
            elif choice == "2" or choice.lower() == "battlefield" or choice.lower() == "defense":
                attacker.bf.display_defense()
                # input("Press enter to continue.")
            elif choice == "3" or choice.lower() == "radar":
                attacker.bf.display_offense()
                # input("Press enter to continue.")
            else:
                print("Invalid input.")
    else:
        attacker.attack(defender)

def print_grid(val):
    print("---------")
    print_row(val[0:3])
    print_row(val[3:6])
    print_row(val[6:9])
    print("---------")


def print_row(val):
    print(f"| {val[0]} {val[1]} {val[2]} |")


def check(val, symbol):
    return all([symbol == x for x in val])


def check_win(val, symbol):
    combinations = [val[0:3], val[3:6], val[6:9], val[0:9:3], val[1:9:3], val[2:9:3], val[0:9:4], val[2:7:2]]
    return any([check(i, symbol) for i in combinations])


# get grid
# values = list(input("Enter cells:"))
values = list("         ")
x_turn = True
current_symbol = "X"

# print grid
print_grid(values)
turns = 9

# action
while True:
    if turns == 0:
        print("Draw")
        break
    else:
        print("Enter the coordinates:")
        user_input = input().split()
        # check if quit
        if any([i == "q" for i in user_input]):
            break
        # proper number of inputs
        if len(user_input) == 2:
            # ensure inputs are numbers
            if user_input[0].isdigit() and user_input[1].isdigit():
                x = int(user_input[0])
                y = int(user_input[1])
                # ensure inputs are in correct range
                if 4 > x > 0 and 4 > y > 0:
                    position = (x - 1) * 3 + (y - 1)
                    # ensure position entered is empty
                    if values[position] == '_' or values[position] == " ":
                        values[position] = current_symbol
                        print_grid(values)
                        # check if winner
                        if check_win(values, current_symbol):
                            print(current_symbol, "wins")
                            break
                        # flip player and decrement turns
                        else:
                            x_turn = not x_turn
                            current_symbol = "X" if x_turn else "O"
                            turns -= 1
                    else:
                        print("This cell is occupied! Choose another one!")
                else:
                    print("Coordinates should be from 1 to 3!")
            else:
                print("You should enter numbers!")
        else:
            print("You need to enter only 2 inputs!")

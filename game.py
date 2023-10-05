import sys
import random
import hashlib
import hmac
from tabulate import tabulate

def winner(u_ch, comp_ch,num):
    matrix = game_logic(num)
    u_ind = num.index(u_ch)
    comp_ind = num.index(comp_ch)
    result = matrix[u_ind][comp_ind]
    if result == "Win":
        return "You Win!"
    elif result == "Lose":
        return "Computer Win!"
    else:
        return "Draw"
      
def game_logic(num):
    matrix = [["" for _ in range(len(num))] for _ in range(len(num))]
    for i in range(len(num)):
        for j in range(len(num)):
            if i == j:
                matrix[i][j] = "Draw"
            else:
                diff = (j - i) % len(num)
                if diff <= len(num) // 2:
                    matrix[i][j] = "Win"
                else:
                    matrix[i][j] = "Lose"
    return matrix

def view_table(matrix, moves):
        head = ["v PC\\User >"] + moves
        rows = [[moves[i]] + row for i, row in enumerate(matrix)]
        return tabulate(rows, headers=head, tablefmt="grid")
def key():
    return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()

def hmac_gen(key_ran, data):
    hmac_ob = hmac.new(key_ran.encode(), data.encode(), hashlib.sha256)
    return hmac_ob.hexdigest()

def main():
    if len(sys.argv) < 4 or (len(sys.argv) - 1) % 2 == 0 or len(set(sys.argv[1:])) != len(sys.argv) - 1:
        print("Invalid input. Please provide an odd number (>=3) of unique choices.")
        print("Example: python game.py 1 2 3....")
        sys.exit(1)
    
    choice = sys.argv[1:]
    while True:
        random_key = key()
        comp_ch = random.choice(choice)
        hmac = hmac_gen(random_key,comp_ch)
        print("HMAC:", hmac)

        print("Available moves:")
        for index, move in enumerate(choice, 1):
            print(f"{index} - {move}")

        print("0 - exit")
        print("? - help")

        u_ch = input("Enter your move: ")
        if u_ch == '0':
            print("Exiting the game. Goodbye!")
            break
        elif u_ch == '?':
            print("Game logic:")
            table = view_table(game_logic(choice), choice)
            print(table)
            print()
            continue

        if u_ch not in choice:
            print("Invalid move. Try again.")
            print()
            continue

        print("Your move:", u_ch)
        print("Computer move:", comp_ch)

        win = winner(u_ch, comp_ch,choice)
        print(win)

        print("HMAC key:", random_key)
        print()
        break

main()
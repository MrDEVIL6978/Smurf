# Areas for Improvement:
#
# Error Handling: The code could benefit from more robust error handling for invalid user inputs or unexpected conditions.
# Security: Real-world casino games would have strong security measures to prevent cheating and fraud. This code is for entertainment purposes only and should not be used for real money gambling.
# Balance Management: There's no limit on how much a user can bet, and some games (Russian Roulette) offer potentially risky bets.
# Limited User Interface: The UI is text-based, which can be less engaging than a graphical interface.
# Enhancing User Interface and Interaction:
#
# Visual Enhancements: Consider incorporating a graphical user interface (GUI) using libraries like Pygame or Tkinter. This would make the games more visually appealing and interactive.
# Sound Effects: Adding sound effects for actions like card dealing, coin flips, and winning/losing can enhance the user experience.
# Animations: Simple animations for dealing cards, spinning a roulette wheel, etc., can add to the immersive feel of the games.
# Progress Tracking: Implement features to track a user's wins, losses, and overall statistics. Leaderboards for high scores can add a competitive element.
# Customization: Allow users to personalize their experience by choosing avatars, themes, or sound preferences.
# Testing and Evaluation:
#
# Thorough Testing: Test the game logic extensively to ensure fair gameplay, accurate win/loss calculations, and proper handling of edge cases.
# User Feedback: Playtesting with real users allows you to identify areas for improvement in terms of usability, clarity, and overall user experience.
# Overall, the code provides a good foundation for a casino game arcade. By addressing the areas for improvement and incorporating the suggestions for UI/UX enhancement, you can create a more engaging and user-friendly experience.
#
# Disclaimer:  Remember that gambling can be addictive and risky.  Always gamble responsibly and be aware of the potential consequences.


import time
import os
import random

def initialize_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def deal_cards(deck, num_cards):
    return [deck.pop() for _ in range(num_cards)]

def print_hand(hand, player_name):
    print(f"{player_name}'s hand:")
    rank_symbol=""
    for card in hand:
        rank, suit = card
        if rank.isdigit():
            rank_symbol = rank
        elif rank == 'A':
            rank_symbol = '🂡'
        elif rank == 'J':
            rank_symbol = '🂣'
        elif rank == 'Q':
            rank_symbol = '🂥'
        elif rank == 'K':
            rank_symbol = '🂦'
        if suit == 'Hearts':
            suit_symbol = '♥'
        elif suit == 'Diamonds':
            suit_symbol = '♦'
        elif suit == 'Clubs':
            suit_symbol = '♣'
        else:
            suit_symbol = '♠'
        print(f"{rank_symbol}{suit_symbol}", end=" ")
    print()

def evaluate_poker_hand(hand):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    hand_ranks = [ranks.index(card[0]) for card in hand]
    hand_ranks.sort(reverse=True)

    # Check for straight flush
    straight_flush = False
    if len(set([card[1] for card in hand])) == 1:
        straight_flush = check_straight(hand_ranks)
    if straight_flush:
        return 9, hand_ranks

    # Check for four of a kind
    four_of_a_kind = False
    for rank in set([card[0] for card in hand]):
        if [card[0] for card in hand].count(rank) == 4:
            four_of_a_kind = True
            break
    if four_of_a_kind:
        return 8, hand_ranks

    # Check for full house
    full_house = False
    three_of_a_kind = False
    pair = False
    for rank in set([card[0] for card in hand]):
        if [card[0] for card in hand].count(rank) == 3:
            three_of_a_kind = True
        elif [card[0] for card in hand].count(rank) == 2:
            pair = True
    if three_of_a_kind and pair:
        full_house = True
    if full_house:
        return 7, hand_ranks

    # Check for flush
    flush = False
    if len(set([card[1] for card in hand])) == 1:
        flush = True
    if flush:
        return 6, hand_ranks

    # Check for straight
    straight = check_straight(hand_ranks)
    if straight:
        return 5, hand_ranks

    # Check for three of a kind
    three_of_a_kind = False
    for rank in set([card[0] for card in hand]):
        if [card[0] for card in hand].count(rank) == 3:
            three_of_a_kind = True
            break
    if three_of_a_kind:
        return 4, hand_ranks

    # Check for two pairs
    pairs = []
    for rank in set([card[0] for card in hand]):
        if [card[0] for card in hand].count(rank) == 2:
            pairs.append(rank)
    if len(pairs) == 2:
        return 3, hand_ranks

    # Check for one pair
    pair = False
    for rank in set([card[0] for card in hand]):
        if [card[0] for card in hand].count(rank) == 2:
            pair = True
            break
    if pair:
        return 2, hand_ranks

    # High card
    return 1, hand_ranks

def check_straight(hand_ranks):
    straight = True
    for i in range(len(hand_ranks) - 1):
        if hand_ranks[i] - hand_ranks[i + 1] != 1:
            straight = False
            break
    return straight

def calculate_hand_value(hand):
    value = 0
    num_aces = 0
    for rank, suit in hand:
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            num_aces += 1
            value += 11
        else:
            value += int(rank)
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def play_poker(concurrent):
    print("Welcome to Poker!")
    deck = initialize_deck()
    player_hand = deal_cards(deck, 5)
    bot_hand = deal_cards(deck, 5)
    print_hand(player_hand, "Your")
    print_hand(bot_hand, "Bot's")

    user_discard = input("Enter the positions (1-5) of cards to discard, separated by spaces: ").strip().split()
    try:
        discard_positions = list(map(int, user_discard))
        discard_positions.sort(reverse=True)
        for pos in discard_positions:
            player_hand.pop(pos - 1)
        player_hand.extend(deal_cards(deck, len(user_discard)))
        print_hand(player_hand, "Your")

        while calculate_hand_value(bot_hand) < 17:
            bot_hand.append(deck.pop())
            print_hand(bot_hand, "Bot")

        user_score, user_hand_ranks = evaluate_poker_hand(player_hand)
        bot_score, bot_hand_ranks = evaluate_poker_hand(bot_hand)

        if user_score > bot_score:
            print("Congratulations! You won the Poker game.")
            return concurrent * 2
        elif user_score == bot_score:
            if user_hand_ranks > bot_hand_ranks:
                print("Congratulations! You won the Poker game.")
                return concurrent * 2
            else:
                print("Bot won the game. Better luck next time.")
                return 0
        else:
            print("Bot won the game. Better luck next time.")
            return 0

    except ValueError:
        print("Invalid input. Please enter card positions as numbers separated by spaces.")

def calculate_score(hand):
    score = 0
    num_aces = 0
    for card in hand:
        rank = card[0]
        if rank.isdigit():
            score += int(rank)
        elif rank in ['J', 'Q', 'K']:
            score += 10
        elif rank == 'A':
            num_aces += 1
            score += 11
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def play_blackjack(concurrent):
    print("Welcome to Blackjack!")
    deck = initialize_deck()
    player_hand = deal_cards(deck, 2)
    bot_hand = deal_cards(deck, 2)
    print_hand(player_hand, "Your")
    print_hand([bot_hand[0], ('?', '?')], "Bot's")

    risk_factor = 0.5  # Initial risk factor

    while calculate_score(player_hand) < 21:
        action = input("Do you want to 'hit' or 'stand'? ").strip().lower()
        if action == 'hit':
            player_hand.append(deck.pop())
            print_hand(player_hand, "Your")
            if calculate_score(player_hand) > 21:
                print("You busted! Better luck next time.")
                return 0
        elif action == 'stand':
            break
        else:
            print("Invalid action. Please enter 'hit' or 'stand'.")

    print_hand(bot_hand, "Bot's")

    # Adjust risk factor based on bot's score and dealer's showing card
    bot_score = calculate_score(bot_hand)
    dealer_showing_card = bot_hand[0][0]
    if dealer_showing_card in ['J', 'Q', 'K', '10']:
        risk_factor = 0.3  # Lower risk for high dealer card
    elif dealer_showing_card in ['9', '8', '7']:
        risk_factor = 0.7  # Higher risk for medium dealer card
    else:
        risk_factor = 0.5  # Default risk factor

    while calculate_score(bot_hand) < 17 or (calculate_score(bot_hand) < 21 and random.random() < risk_factor):
        bot_hand.append(deck.pop())
        print_hand(bot_hand, "Bot's")
        if calculate_score(bot_hand) > 21:
            print("Bot busted! You win!")
            return concurrent * 2

    user_score = calculate_score(player_hand)
    bot_score = calculate_score(bot_hand)

    if user_score > bot_score:
        print("Congratulations! You won the Blackjack game.")
        return concurrent * 2
    else:
        print("Bot won the game. Better luck next time.")
        return 0

def print_board(board):
    print("┌───┬───┬───┐")
    for row in range(3):
        print("│", end="")
        for col in range(3):
            print(f" {board[row][col]} │", end="")
        print("\n├───┼───┼───┤")
    print("└───┴───┴───┘")

def check_win(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def bot_move(board):
    # Check for winning moves for the bot
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O"
                if check_win(board, "O"):
                    return
                board[row][col] = " "

    # Check for blocking moves for the user
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "X"
                if check_win(board, "X"):
                    board[row][col] = "O"
                    return
                board[row][col] = " "

    # Take the center square if available
    if board[1][1] == " ":
        board[1][1] = "O"
        return

    # Make a random move
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == " ":
            board[row][col] = "O"
            break

def play_tic_tac_toe(concurrent):
    print("Welcome to Tic-Tac-Toe!")
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player = random.choice(players)
    print(f"The game will start with player '{current_player}'.")

    player_points = 0
    bot_points = 0

    while True:
        print_board(board)
        if current_player == 'X':
            while True:
                try:
                    move = int(input("Enter your move (1-9): ")) - 1
                    row = move // 3
                    col = move % 3
                    if 0 <= move <= 8 and board[row][col] == " ":
                        board[row][col] = 'X'
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number (1-9).")
        else:  # Bot's move
            print("Bot is making its move...")
            bot_move(board)

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player '{current_player}' wins!")
            if current_player == 'X':
                player_points += 1
            else:
                bot_points += 1

            if player_points == 3:
                print("Congratulations! You won the Tic-Tac-Toe game!")
                return concurrent * 2
            else:
                print(f"Player Points: {player_points}, Bot Points: {bot_points}")
                print("Starting a new round...")
                board = [[" " for _ in range(3)] for _ in range(3)]
                current_player = random.choice(players)
                print(f"The next round will start with player '{current_player}'.")
                continue

        # Check for tie
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            print(f"Player Points: {player_points}, Bot Points: {bot_points}")
            print("Starting a new round...")
            board = [[" " for _ in range(3)] for _ in range(3)]
            current_player = random.choice(players)
            print(f"The next round will start with player '{current_player}'.")
            continue

        # Switch turns
        current_player = 'X' if current_player == 'O' else 'O'

    # If game ends without a winner (though it shouldn't reach here)
    return 0
def play_coinflip(concurrent):
    print("Welcome to Coinflip!")
    while True:
        bet_amount = input("Enter the amount you want to bet (or type 'exit' to leave): ").strip().lower()
        if bet_amount == 'exit':
            return 0
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if bet_amount > concurrent:
            print("Insufficient funds.")
        else:
            break

    bet_type = input("Choose your bet type: 'heads/tails', 'streak', or 'odd/even': ").lower()

    user_choice = input("Choose 'heads' or 'tails': ").lower()
    outcomes = ['heads', 'tails']
    coinflip_result = random.choices(outcomes, weights=[0.4, 0.6])[0]

    print("The coin is spinning in the air...")
    time.sleep(1)
    print(f"And it is {coinflip_result.capitalize()}!")

    if bet_type == 'heads/tails':
        if user_choice == coinflip_result:
            print(f"You won! You doubled your bet amount. {bet_amount} + {bet_amount} = {bet_amount * 2}")
            return bet_amount * 2
        else:
            print("You lost. Better luck next time.")
            return 0
    elif bet_type == 'streak':
        previous_results = []
        streak_count = 0
        for _ in range(3):
            coinflip_result = random.choices(outcomes, weights=[0.4, 0.6])[0]
            previous_results.append(coinflip_result)
            if len(previous_results) > 1 and previous_results[-1] == previous_results[-2]:
                streak_count += 1
            else:
                streak_count = 0
        if streak_count >= 2:
            print(f"You won! You doubled your bet amount. {bet_amount} + {bet_amount} = {bet_amount * 2}")
            return bet_amount * 2
        else:
            print("You lost. Better luck next time.")
            return 0
    elif bet_type == 'odd/even':
        if coinflip_result == 'heads':
            result = 'odd'
        else:
            result = 'even'
        if user_choice == result:
            print(f"You won! You doubled your bet amount. {bet_amount} + {bet_amount} = {bet_amount * 2}")
            return bet_amount * 2
        else:
            print("You lost. Better luck next time.")
            return 0
    else:
        print("Invalid bet type. Please try again.")
        return 0

def play_rock_paper_scissor(concurrent):
    print("Welcome to Rock Paper Scissors!")
    while True:
        bet_amount = input("Enter the amount you want to bet (or type 'exit' to leave): ").strip().lower()
        if bet_amount == 'exit':
            return 0
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if bet_amount > concurrent:
            print("Insufficient funds.")
        else:
            break

    user_choice = input("Choose 'rock', 'paper', or 'scissors': ").lower()
    outcomes = ['rock', 'paper', 'scissors']

    # Track user's past choices
    user_history = []

    if user_choice == 'rock':
        computer_choice = random.choices(outcomes, weights=[0.2, 0.6, 0.2])[0]
    elif user_choice == 'paper':
        computer_choice = random.choices(outcomes, weights=[0.2, 0.2, 0.6])[0]
    else:
        computer_choice = random.choices(outcomes, weights=[0.6, 0.2, 0.2])[0]

    # Update user's history
    user_history.append(user_choice)

    # Predict user's next move based on history
    if len(user_history) >= 3:
        last_three_choices = user_history[-3:]
        if last_three_choices.count(last_three_choices[0]) == 3:
            predicted_choice = outcomes[(outcomes.index(last_three_choices[0]) + 1) % 3]
            computer_choice = outcomes[(outcomes.index(predicted_choice) + 1) % 3]

    print("You are throwing your choice...")
    time.sleep(1)
    print(f"The computer chooses {computer_choice.capitalize()}!")

    if user_choice == computer_choice:
        print("It's a tie!")
        return 0
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        print(f"You won! You doubled your bet amount. {bet_amount} + {bet_amount} = {bet_amount * 2}")
        return bet_amount * 2
    else:
        print("You lost. Better luck next time.")
        return 0

def play_russian_roulette(concurrent):
    print("Welcome to Russian Roulette!")
    print("Warning: If you choose to play, your entire current balance will be placed as a bet.")
    input("Press Enter to continue...")

    def initialize_chamber():
        total_bullets = random.randint(5, 10)  # Increased range for live rounds
        num_blanks = random.randint(1, min(total_bullets - 1, 3))  # Decreased range for blanks
        revolver_chamber = [0] * num_blanks + [1] * (total_bullets - num_blanks)
        random.shuffle(revolver_chamber)
        print(f"The revolver chamber is loaded with {num_blanks} blanks and {total_bullets - num_blanks} live rounds.")
        return revolver_chamber

    revolver_chamber = initialize_chamber()
    prize_pool = concurrent * 2
    user_lives = 3  # Decreased user lives
    dealer_lives = 3
    current_turn = 'user'

    while user_lives > 0 and dealer_lives > 0:
        if not revolver_chamber:
            print("\nThe chamber is empty. Reinitializing...")
            revolver_chamber = initialize_chamber()

        if current_turn == 'user':
            print("\nIt's your turn to shoot.")
            choice = input("Do you want to shoot yourself (y) or the dealer (n)? ").strip().lower()

            if choice == 'y':
                print("You chose to shoot yourself.")
                input("Press Enter to spin the chamber and pull the trigger...")
                chamber_result = revolver_chamber.pop(0)

                if chamber_result == 1:
                    print("You hit a live round! You lost a life.")
                    user_lives -= 1
                else:
                    print("The chamber was empty. You survived this round!")
                    prize_pool += 0.1 * prize_pool
                    print(f"Prize pool increased by 10%. Current prize pool: ${prize_pool}")

            elif choice == 'n':
                print("You chose to shoot the dealer.")
                input("Press Enter to spin the chamber and pull the trigger...")
                chamber_result = revolver_chamber.pop(0)

                if chamber_result == 1:
                    print("Dealer hit a live round! Dealer lost a life.")
                    dealer_lives -= 1
                else:
                    print("The chamber was empty. Dealer survived this round!")

            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

            current_turn = 'dealer'

        elif current_turn == 'dealer':
            print("\nIt's the dealer's turn to shoot.")
            if random.random() < 0.8:  # Increased probability of shooting the user
                print("The dealer chose to shoot you.")
                input("Press Enter to spin the chamber and pull the trigger...")
                chamber_result = revolver_chamber.pop(0)

                if chamber_result == 1:
                    print("Dealer hit a live round! You lost a life.")
                    user_lives -= 1
                else:
                    print("The chamber was empty. You survived this round!")

            else:
                print("The dealer chose to shoot himself.")
                input("Press Enter to spin the chamber and pull the trigger...")
                chamber_result = revolver_chamber.pop(0)

                if chamber_result == 1:
                    print("Dealer hit a live round! Dealer lost a life.")
                    dealer_lives -= 1
                else:
                    print("The chamber was empty. Dealer survived this round!")
                    prize_pool -= 0.2 * prize_pool
                    print(f"Prize pool decreased by 20%. Current prize pool: ${prize_pool}")

            current_turn = 'user'

        print(f"\nYou have {user_lives} lives left.")
        print(f"The dealer has {dealer_lives} lives left.")
        input("Press Enter to continue...")

    if user_lives > 0 and dealer_lives <= 0:
        print(f"\nCongratulations! You survived Russian Roulette and won ${prize_pool}.")
        deposit_to_bank(prize_pool)
        print("Your winning prize has been deposited into your bank account.")
        concurrent = 0
        return concurrent
    elif dealer_lives > 0 and user_lives <= 0:
        print("\nGame over. The dealer survived, and you lost all lives.")
        return 0

# Define the folder and file name for the bank
folder2_name = "bank"
file2_name = "bank_amount.txt"
file2_path = os.path.join(folder2_name, file2_name)

# Define the folder and file name for personal cash
folder_name = "data"
file_name = "activity_number.txt"
file_path = os.path.join(folder_name, file_name)

# Function to ensure the folder and file exist
def setup_bank():
    if not os.path.exists(folder2_name):
        os.makedirs(folder2_name)
    if not os.path.exists(file2_path):
        with open(file2_path, 'w') as file2:
            file2.write("0")

# Function to ensure the folder and file exist for personal cash
def setup_cash():
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("0")

# Function to get the current balance
def get_bank_balance():
    with open(file2_path, 'r') as file2:
        return float(file2.read().strip())

# Function to update the bank balance
def update_bank_balance(amount):
    with open(file2_path, 'w') as file2:
        file2.write(str(amount))

# Function to get the current cash balance
def get_cash_balance():
    with open(file_path, 'r') as file:
        return float(file.read().strip())

# Function to update the cash balance
def update_cash_balance(amount):
    with open(file_path, 'w') as file:
        file.write(str(amount))

# Function to deposit an amount to the bank
def deposit_to_bank(amount):
    current_balance = get_bank_balance()
    new_balance = current_balance + amount
    update_bank_balance(new_balance)
    print(f"Deposited {amount}. New bank balance is {new_balance}.")

# Function to withdraw an amount from the bank
def withdraw_from_bank(amount):
    current_balance = get_bank_balance()
    if amount > current_balance:
        print("Insufficient funds in the bank.")
    else:
        new_balance = current_balance - amount
        update_bank_balance(new_balance)
        print(f"Withdrew {amount}. New bank balance is {new_balance}.")
        return amount

# Main function to handle user commands
def main():
    setup_bank()
    setup_cash()
    concurrent = get_cash_balance()
    print("Welcome to the Arcade Unit!")
    print("The following commands are available:")
    print("For saving your current amount: 'Asave'")
    print("For menu: 'Amenu'")
    print("For current balance: 'Abalance'")
    print("For exiting the game: 'Aexit'")
    print("For help: 'Ahelp'")
    print("For Bank commands: 'Abank'")

    while True:
        user_command = input("Enter your command: ").strip()
        if user_command == "Amenu":
            print("Here we have games like:")
            print("1. The Dealer (code-108)")
            print("2. The Grinder (code-102)")
            print("3. The Mastermind (code-106)")
        elif user_command == "Abalance":
            print(f"Your current balance: {get_cash_balance()}")
        elif user_command == "Ahelp":
            print("Here are the main commands:")
            print("For saving your current amount- Asave")
            print("For menu- Amenu")
            print("For Current balance- Abalance")
            print("For exiting the game- Aexit")
            print("For the commands- Ahelp")
            print("For Bank commands- Abank")
        elif user_command == "Asave":
            update_cash_balance(concurrent)
            print(f"Your amount has been saved: {get_cash_balance()}")
        elif user_command == "102":
            print("SO YOU HAVE CHOSEN THE GRINDER GAME")
            concurrent += 500
            update_cash_balance(concurrent)
            print("Choose a game to play:")
            print("1. Poker")
            print("2. Blackjack")
            print("3. Tic-Tac-Toe")
            game_choice = input("Enter your choice (1-3): ")
            if game_choice == "1":
                print("Poker (Simplified):")
                print("Goal: Make the best five-card hand using your two cards and three community cards dealt face-up.")
                print("Hand Rankings (highest to lowest): Royal Flush, Straight Flush, Four of a Kind, Full House (three of a kind and a pair), Flush (five cards of the same suit), Straight (five consecutive ranks), Three of a Kind, Two Pair, One Pair, High Card.")
                print("Gameplay:")
                print("You are dealt two cards face down. Three cards are dealt face-up in the center (flop).")
                print("You can choose to Fold (discard your hand and lose your bet), Call (match the current bet), or Raise (increase the bet).")
                print("After the flop, one more card is dealt face-up (turn). Betting happens again.")
                print("Finally, one last card is dealt face-up (river). Betting happens again.")
                print("You reveal your cards, and the winner is determined based on the best five-card hand.")
                print("Outcomes:")
                print("Win: You win the pot (total bets) if you have the best hand.")
                print("Lose: You lose your bet if you fold or have a weaker hand than the bot.")
                poker_winnings = play_poker(concurrent)
                if poker_winnings > 0:
                    concurrent += poker_winnings
                    update_cash_balance(concurrent)
            elif game_choice == "2":
                print("Blackjack:")
                print("Goal: Get a hand value closer to 21 than the dealer without going over (busting).")
                print("Gameplay:")
                print("You and the dealer are each dealt two cards.")
                print("Card values: 2-10 = face value, Face cards (Jack, Queen, King) = 10, Ace = 1 or 11 (depending on your advantage).")
                print("You can choose to Hit (receive another card), stand (stay with your current hand), or Double Down (double your bet and receive one more card).")
                print("After you finish playing your hand, the dealer plays theirs according to preset rules (hitting until reaching 17 or higher).")
                print("You win if your hand value is closer to 21 than the dealer's without busting.")
                print("Outcomes:")
                print("Win: You get paid according to the payout table (usually 1:1 for a regular win, higher for Blackjack - two cards totaling 21).")
                print("Lose: You lose your bet if you bust or the dealer has a closer hand value to 21.")
                print("Push (Tie): If your hand value equals the dealer's, you get your bet back.")
                blackjack_winnings = play_blackjack(concurrent)
                if blackjack_winnings > 0:
                    concurrent += blackjack_winnings
                    update_cash_balance(concurrent)
            elif game_choice == "3":
                print("OH!, cmon dude u dont want me to explain you, how to play tic-tac-toe right?")
                tic_tac_toe_winnings = play_tic_tac_toe(concurrent)
                if tic_tac_toe_winnings > 0:
                    concurrent += tic_tac_toe_winnings
                    update_cash_balance(concurrent)
            else:
                print("Invalid choice.")
        elif user_command == "108":
            print("SO YOU HAVE CHOSEN THE DEALER GAME")
            print("Choose a game to play:")
            print("1. Coinflip")
            print("2. Rock Paper Scissors")
            print("3. Russian Roulette")
            game_choice = input("Enter your choice (1-3): ")
            if game_choice == "1":
                print("Coin Flip:")
                print("Goal: Guess whether the coin will land on Heads or Tails.")
                print("Gameplay:")
                print("You can choose to bet an amount of money.")
                print("The coin is flipped virtually.")
                print("You guess Heads or Tails.")
                print("Outcomes:")
                print("Win: If your guess matches the outcome, you win double your bet.")
                print("Lose: If your guess doesn't match the outcome, you lose your bet.")

                concurrent += play_coinflip(concurrent)
                update_cash_balance(concurrent)
            elif game_choice == "2":
                print("Rock-Paper-Scissors:")
                print("Goal: Choose the hand that beats the bot's choice (Rock beats Scissors, Scissors beat Paper, Paper beats Rock).")
                print("Gameplay:")
                print("You choose Rock, Paper, or Scissors.")
                print("The bot randomly chooses Rock, Paper, or Scissors.")
                print("Outcomes:")
                print("Win: If your choice beats the bot's choice, you win double your bet. (There's a function that tracks your choices to try and predict the bot's next move, but it's not guaranteed).")
                print("Lose: If the bot's choice beats yours, you lose your bet.")
                print("Tie: If both choose the same hand, it's a tie and you get your bet back.")

                concurrent += play_rock_paper_scissor(concurrent)
                update_cash_balance(concurrent)
            elif game_choice == "3":
                documents=input("THE RUSSIAN ROULETTE IS A VERY SERIOUS GAME AND IT IS A LITTLE BIT TRICKY, SO IF YOU WANT TO KNOW THE RULES OF THIS GAME THEN ENTER 'info' OTHERWISE ENTER 'pass'.")
                if (documents=="info"):
                    print("Russian Roulette is a high-risk game where players take turns putting a revolver containing a random number of live rounds against their heads and pulling the trigger. The game continues until one player is eliminated or a winner emerges.")

                    print("Here are the basic rules and gameplay according to the code:")

                    print("Game Start: When you choose to play Russian Roulette, the entire current balance in your personal cash will be placed as a bet. The game will warn you about this before proceeding.")

                    print("Loading the Chamber: The game initializes the revolver chamber by randomly selecting a number of bullets (between 3 and 8) and blanks (between 2 and the minimum of 4 or one less than the total bullets). These bullets and blanks are shuffled and loaded into the chamber.")

                    print("Prize Pool: The initial prize pool is set to twice your current balance.")

                    print("Player and Dealer Lives: Both you (the player) and the dealer start with 3 lives each.")

                    print("Turn-based Gameplay: The game is played in turns, alternating between you and the dealer.")

                    print("Player's Turn:")

                    print("You will be prompted to choose whether to shoot yourself or the dealer.")
                    print("If you choose to shoot yourself, the chamber will be spun, and a round will be fired.")
                    print("If it's a live round, you lose a life.")
                    print("If it's a blank, you survive the round, and the prize pool increases by 10%.")
                    print("If you choose to shoot the dealer, the chamber will be spun, and a round will be fired at the dealer.")
                    print("If it's a live round, the dealer loses a life.")
                    print("If it's a blank, the dealer survives the round.")
                    print("Dealer's Turn:")

                    print("The dealer has a 80% chance of choosing to shoot you.")
                    print("If the dealer shoots you and it's a live round, you lose a life.")
                    print("If it's a blank, you survive the round.")
                    print("If the dealer chooses to shoot themselves and it's a live round, the dealer loses a life.")
                    print("If the dealer shoots themselves and it's a blank, the dealer survives the round, but the prize pool decreases by 20%.")
                    print("Game End:")

                    print("If you lose all your lives, the game ends, and you lose your entire bet.")
                    print("If the dealer loses all their lives, you win the game and the current prize pool amount.")
                    print("If the chamber becomes empty during the game, it will be reinitialized with a new set of bullets and blanks.")
                    print("Winning and Losing:")

                    print("If you win, the winning prize from the prize pool will be deposited into your bank account.")
                    print("If you lose, you lose your entire bet amount.")
                    print("It's important to note that Russian Roulette is an extremely dangerous game, and this implementation is purely for entertainment purposes and should not be attempted in real life.")
                    input("Enter to start the Dance of the  Death !!!")
                    concurrent += play_russian_roulette(concurrent)
                    update_cash_balance(concurrent)
                else:
                    concurrent += play_russian_roulette(concurrent)
                    update_cash_balance(concurrent)
            else:
                print("Invalid choice.")
        elif user_command == "106":
            print("SO YOU HAVE CHOSEN THE MASTERMIND GAME")
            print("Currently underdevelopment")
        elif user_command == "Abank":
            print("Bank commands:")
            print("For checking bank balance: 'Acheckbalance'")
            print("For depositing to bank: 'Adeposit'")
            print("For withdrawing from bank: 'Awithdraw'")
        elif user_command == "Acheckbalance":
            print(f"Your current bank balance: {get_bank_balance()}")
        elif user_command == "Adeposit":
            deposit_amount = int(input("Enter the amount to deposit: "))
            if concurrent >= deposit_amount:
                concurrent -= deposit_amount
                deposit_to_bank(deposit_amount)
                update_cash_balance(concurrent)
            else:
                print("Insufficient funds in your cash balance.")
        elif user_command == "Awithdraw":
            withdraw_amount = int(input("Enter the amount to withdraw: "))
            if get_bank_balance() >= withdraw_amount:
                withdrawn_amount = withdraw_from_bank(withdraw_amount)
                concurrent += withdrawn_amount
                update_cash_balance(concurrent)
            else:
                print("Invalid command. Please try again.")

        if __name__ == "__main__":
            main()
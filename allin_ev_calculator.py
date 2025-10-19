from treys import Card, Evaluator, Deck
import random
import os
from scipy.stats import binom
import matplotlib.pyplot as plt
import numpy as np
directory = './spin025per250729'
def process_all_txt_files_in_directory(directory):
    
    evaluator = Evaluator()
    total_ev = 0
    total_profit_chip = 0
    count_txt = 0
    allin_game_count = 0
    all_pot_size_sum = 0
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            full_path = os.path.join(directory, filename)
            print(f"Processing file: {full_path}")
            print("done : ", count_txt)
            count_txt += 1
            ev = 0
            profit_chip = 0
            iterations = 10000
            wins1 = 0
            wins2 = 0
            ties = 0

            with open(full_path, 'r') as file:
                lines = file.readlines()

            all_in_situations = []
            allin = 0
            player_count = 0
            calculate_done = 0 
            wins1 = 0
            wins2 = 0
            ties = 0

            for i, line in enumerate(lines):
                if "*** HOLE CARDS ***" in line:
                    allin = 0

                if "shows" in line :

                    allin = 1
                    if line.split(":")[0] == "Hero":
                        hero_hand = line.split("[")[1].split("]")[0].split(" ")
                    else:
                        other_hand = line.split("[")[1].split("]")[0].split(" ")
                        
                    player_count += 1
                    if player_count == 3 :
                        allin = 0
                        player_count = 0
                
                if "*** FLOP ***" in line:
                    
                    if allin == 1 and hero_hand != []:

                        evaluator = Evaluator()
                        iterations = 10000

                        wins1 = 0
                        wins2 = 0
                        ties = 0

                        for _ in range(iterations):
                            deck = Deck()

                            hand1 = [Card.new(hero_hand[0]), Card.new(hero_hand[1])]
                            hand2 = [Card.new(other_hand[0]), Card.new(other_hand[1])]
                            remaining_deck = [card for card in deck.cards if card not in hand1 and card not in hand2]

                            board = random.sample(remaining_deck, 5)

                            score1 = evaluator.evaluate(hand1, board)
                            score2 = evaluator.evaluate(hand2, board)

                            if score1 < score2:
                                wins1 += 1
                            elif score2 < score1:
                                wins2 += 1
                            else:
                                ties += 1

                        win_rate1 = (wins1 / iterations) * 100
                        win_rate2 = (wins2 / iterations) * 100
                        tie_rate = (ties / iterations) * 100
                        print("hero_hand : ", hero_hand)
                        print("other_hand : ", other_hand)
                        print(f"Hero Win Rate: {win_rate1:.2f}%")
                        print(f"Player 2 Win Rate: {win_rate2:.2f}%")
                        print(f"Tie Rate: {tie_rate:.2f}%")
                        calculate_done = 1
                        
                    allin = 0
                    player_count = 0
                    
                if "and won" in line and calculate_done == 1:
                    
                    calculate_done = 0
                    hero_hand = []
                    if("," in line.split("and won")[1].split("(")[1].split(")")[0]):
                        pot = int(line.split("and won")[1].split("(")[1].split(")")[0].split(",")[0] + line.split("and won")[1].split("(")[1].split(")")[0].split(",")[1])
                    else:
                        pot = int(line.split("and won")[1].split("(")[1].split(")")[0])
                    print("pot : ", pot)
                    print("current ev : ", win_rate1/100 * pot - pot / 2)
                    ev += (win_rate1/100 * pot - pot / 2)

                    if i < len(lines) - 1:
                        next_line = lines[i + 1]
                        next_next_line = lines[i + 2]
                        if "and won" in next_line or "and won" in next_next_line:
                            print("tie")
                        else:
                            if "Hero" in line:
                                profit_chip += (pot/2)
                                print("profit chips", profit_chip)
                                all_pot_size_sum += (pot/2)
                                allin_game_count += 1
                            else :
                                profit_chip -= pot/2
                                print("profit chips", profit_chip)
                                all_pot_size_sum += (pot/2)
                                allin_game_count += 1
                    calculate_done = 0
                    hero_hand = []

            print("----------------------------------------")
            print("ev : ", ev)
            print("profit chips", profit_chip)
            print("current allin_game_count : ", allin_game_count)
            print("----------------------------------------")
            total_ev += ev
            total_profit_chip += profit_chip
            
    return total_ev, total_profit_chip, allin_game_count, all_pot_size_sum


total_ev, total_profit_chip, total_allin_game_count, all_pot_size_sum = process_all_txt_files_in_directory(directory)
print("total_ev : ", total_ev)
print("total_profit_chip : ", total_profit_chip)
print("total_allin_game_count : ", total_allin_game_count)
print("all_pot_size_sum : ", all_pot_size_sum)
print("total_all_in_winrate : ", (all_pot_size_sum + total_ev) / (all_pot_size_sum * 2))
print("all_in_winrate result: ", (all_pot_size_sum + total_profit_chip) / (all_pot_size_sum * 2))
print("AVG pot size : ", all_pot_size_sum / total_allin_game_count)
print("reality win game count : ", total_profit_chip / (all_pot_size_sum / total_allin_game_count))
print("ev win game count : ", total_ev / (all_pot_size_sum / total_allin_game_count))
avg_pot_size = all_pot_size_sum / total_allin_game_count

n = total_allin_game_count
p = (all_pot_size_sum + total_ev) / (all_pot_size_sum * 2)
target_win = int((total_allin_game_count - (total_profit_chip // avg_pot_size)) // 2 + (total_profit_chip // avg_pot_size))
print("target_win : ", target_win)

x = np.arange(0, n + 1)
probs = binom.pmf(x, n, p)

target_prob = probs[target_win]
print(f"Probability of exactly {target_win} wins: {target_prob:.6f}")

mean = n * p
std_dev = np.sqrt(n * p * (1 - p))
print(f"Mean : {mean:.4f}")
print(f"Standard Deviation : {std_dev:.4f}")

z_score = (target_win - mean) / std_dev
print(f"{target_win} wins is {z_score:.4f} standard deviations away from the mean.")

plt.figure(figsize=(10, 6))
bars = plt.bar(x, probs, color='skyblue', edgecolor='black')
bars[target_win].set_color('red')

plt.title(f'Reality Probability Distribution of Wins in {n} Games (Win Rate = {p*100:.0f}%)', fontsize=14)
plt.xlabel('Number of Wins', fontsize=12)
plt.ylabel('Probability', fontsize=12)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()



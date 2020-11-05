import bot
import pongsim
import random
from tqdm.gui import tqdm
import tqdm


def do_generation(current_bots, num_rounds = 2, show_last = False):
    print("ROUNDS:")
    for round_num in range(num_rounds):
        if round_num == num_rounds - 1 and show_last:
            losers = do_round(current_bots, show_last)
        else:
            losers = do_round(current_bots)
        for loser in losers:
            current_bots.remove(loser)
    return current_bots


def do_round(current_bots, show_last = False):
    losers = []
    for i in tqdm.tqdm(range(len(current_bots) // 2)):

        player_one = current_bots[i]
        player_two = current_bots[len(current_bots) - i - 1]
        match = pongsim.Pong(False, False)
        if (i == len(current_bots) // 2 - 1 and show_last) or (i+1) % 10 == 0:
            winner = match.run(bot_one=player_one, bot_two=player_two, with_ui=True, max_score=5)
        else:
            winner = match.run(bot_one=player_one, bot_two=player_two, with_ui=False, max_score=3)
        if winner == 1:
            losers.append(player_one)
        elif winner == 0:
            losers.append(player_two)
    return losers


def run(num_generations=3):
    current_bots = [bot.PongBot() for _ in range(100)]
    for gen in range(num_generations):
        print("Generation: {}".format(gen+1))
        current_bots = do_generation(current_bots)
        new_bots = []
        for current in current_bots:
            new_bots.append(bot.PongBot(current.model))
            new_bots.append(bot.PongBot(current.model))
            if random.random() > ((gen+1)/num_generations):
                new_bots.append(bot.PongBot())
            else:
                new_bots.append(bot.PongBot(current.model))
        current_bots += new_bots
        random.shuffle(current_bots)
    best_bots = current_bots

    print("STARTING FINALS")
    with tqdm.tqdm(total=250) as pbar:
        while len(best_bots) > 1:
            first = random.choice(best_bots)
            second = random.choice(best_bots)
            while first == second:
                second = random.choice(best_bots)
            match = pongsim.Pong(False, False)
            winner = match.run(first, second, True)
            if winner == 1:
                loser = first
            elif winner == 0:
                loser = second
            if len(best_bots) < 5:
                loser.model.save("finalists/{}".format(len(best_bots)))
            best_bots.remove(loser)
            pbar.update(10)
        first.model.save("finalists/1")


run(10)
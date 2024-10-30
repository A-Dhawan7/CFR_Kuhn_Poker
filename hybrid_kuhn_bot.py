from cfr_kuhn_bot import KuhnPokerCFR
import numpy as np
from random import shuffle

class HybridKuhnPokerBot:
    """
    Hybrid Kuhn Poker bot that uses Counterfactual Regret Minimization (CFR) for decision-making
    and adapts dynamically based on opponent behavior. It classifies opponents as 'aggressive',
    'passive', or 'balanced' and adjusts its strategy accordingly.
    """

    ACTION_PASS = "p"  # Represents a "pass" action
    ACTION_BET = "b"   # Represents a "bet" action
    ADJUSTMENT_VALUE = 0.3  # Value by which the bot's strategy is adjusted based on opponent type

    def __init__(self):
        # Initialize the CFR-based bot with tracking for opponent behavior
        self.cfr_bot = KuhnPokerCFR()
        # Tracking opponent's actions to classify their playstyle
        self.opponent_model = {"pass_count": 0, "bet_count": 0}
        # Tracks the total number of rounds played to calculate action percentages
        self.total_rounds = 0
        # Thresholds for identifying if an opponent is aggressive or passive
        self.aggressiveness_threshold = 0.7
        self.passivity_threshold = 0.7
        # Results storage for recording win rates against each opponent type
        self.results = {"aggressive": [], "passive": [], "balanced": []}

    def update_opponent_model(self, opponent_action):
        """
        Updates the opponent model based on observed actions to understand their playstyle.

        Parameters:
            - opponent_action: Action taken by the opponent, either "p" (pass) or "b" (bet)
        """
        if opponent_action == self.ACTION_PASS:
            self.opponent_model["pass_count"] += 1
        elif opponent_action == self.ACTION_BET:
            self.opponent_model["bet_count"] += 1
        self.total_rounds += 1  # Increment total rounds to calculate probabilities

    def detect_opponent_type(self):
        """
        Determines the opponent's type based on their betting patterns.

        Returns:
            - A string representing the opponent type: 'aggressive', 'passive', or 'balanced'
        """
        if self.total_rounds == 0:
            return 'balanced'  # Default to balanced if no rounds have been played
        pass_rate = self.opponent_model["pass_count"] / self.total_rounds
        bet_rate = self.opponent_model["bet_count"] / self.total_rounds
        # Classify as 'aggressive' if betting rate is above aggressiveness threshold
        if bet_rate > self.aggressiveness_threshold:
            return 'aggressive'
        # Classify as 'passive' if passing rate is above passivity threshold
        elif pass_rate > self.passivity_threshold:
            return 'passive'
        else:
            return 'balanced'  # If neither threshold is met, classify as 'balanced'

    def play_round(self, history, player_card, is_player_1=True):
        """
        Determines the bot's action based on the opponent type and CFR strategy.

        Parameters:
            - history: A string representing the actions taken so far in the round
            - player_card: The bot's private card for the round
            - is_player_1: Boolean indicating if the bot is Player 1 (default is True)

        Returns:
            - The chosen action ('p' for pass or 'b' for bet)
        """
        opponent_type = self.detect_opponent_type()  # Identify opponent type for strategy adjustment
        node = self.cfr_bot.get_or_create_node(player_card, history)
        cfr_strategy = node.get_average_strategy()

        # Adjust strategy based on opponent type
        if opponent_type == 'aggressive':
            adjusted_strategy = [
                min(1, cfr_strategy[0] + self.ADJUSTMENT_VALUE),  # Increase probability of pass
                max(0, cfr_strategy[1] - self.ADJUSTMENT_VALUE)   # Decrease probability of bet
            ]
        elif opponent_type == 'passive':
            adjusted_strategy = [
                max(0, cfr_strategy[0] - self.ADJUSTMENT_VALUE),  # Decrease probability of pass
                min(1, cfr_strategy[1] + self.ADJUSTMENT_VALUE)   # Increase probability of bet
            ]
        else:  # For balanced opponents, use the CFR-derived strategy directly
            adjusted_strategy = cfr_strategy

        # Normalize adjusted strategy and select action based on the adjusted probabilities
        adjusted_strategy = np.array(adjusted_strategy) / sum(adjusted_strategy)
        action = np.random.choice([self.ACTION_PASS, self.ACTION_BET], p=adjusted_strategy)
        return action

    def simulate_game(self, opponent_bot, n_games=1000):
        """
        Simulates multiple games against a specified opponent bot and records the win rate.

        Parameters:
            - opponent_bot: Function representing the opponent bot's strategy
            - n_games: Number of games to simulate against the opponent

        Output:
            - Prints the win rate, loss rate, and net wins for each opponent type
        """
        win_count, loss_count = 0, 0

        for _ in range(n_games):
            shuffle(self.cfr_bot.deck)  # Randomize the deck for each game
            player_cards = [self.cfr_bot.deck[0], self.cfr_bot.deck[1]]
            history = ""  # Reset action history for each game

            # Play until the game reaches a terminal state
            while not self.cfr_bot.is_terminal_state(history):
                if len(history) % 2 == 0:  # Bot's turn to act
                    action = self.play_round(history, player_cards[0])
                    history += action
                else:  # Opponent's turn to act
                    opponent_action = opponent_bot(player_cards[1], history)
                    history += opponent_action
                    self.update_opponent_model(opponent_action)

            # Evaluate the game's outcome and update win/loss counts
            game_result = self.cfr_bot.compute_terminal_reward(history, player_cards)
            if game_result > 0:
                win_count += 1
            elif game_result < 0:
                loss_count += 1

        # Calculate win and loss rates
        win_rate = win_count / n_games
        loss_rate = loss_count / n_games
        opponent_type = opponent_bot.__name__.replace("_bot", "")  # Identify opponent type from function name
        self.results[opponent_type].append(win_rate)  # Track win rate per opponent type

        # Print summary of results for the current opponent type
        print(f"Results against {opponent_type.capitalize()} Bot:")
        print(f"  Win Rate: {win_rate:.2%}")
        print(f"  Loss Rate: {loss_rate:.2%}")
        print(f"  Net Wins: {win_count - loss_count}\n")

# Opponent Bot Definitions
def passive_bot(card, history):
    """
    A conservative opponent bot that bets only if holding 'K' and if the action history indicates
    a favorable sequence (e.g., opponent has passed).
    """
    return "b" if card == "K" and "p" in history else "p"

def aggressive_bot(card, history):
    """
    An aggressive opponent bot that bets frequently, especially when sensing a weak move from
    the opponent (e.g., pass) or if holding a high card like 'K' or 'Q'.
    """
    return "b" if "p" in history or card in ["K", "Q"] else "p"

def balanced_bot(card, history):
    """
    A balanced opponent bot with a mixed strategy: it bets when holding 'K' and tends to bet
    after a pass from the opponent, but is more cautious with lower cards.
    """
    if card == "K":
        return "b"
    elif "p" in history:
        return "b" if card == "Q" else "p"
    else:
        return "p"

if __name__ == "__main__":
    # Initialize the hybrid bot and simulate games against each opponent type
    hybrid_bot = HybridKuhnPokerBot()
    hybrid_bot.simulate_game(passive_bot, n_games=1000)
    hybrid_bot.simulate_game(aggressive_bot, n_games=1000)
    hybrid_bot.simulate_game(balanced_bot, n_games=1000)

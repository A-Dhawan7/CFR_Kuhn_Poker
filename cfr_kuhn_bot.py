import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from tabulate import tabulate
import logging

# Set up logging for iteration progress
logging.basicConfig(level=logging.INFO, format='%(message)s')

class KuhnPokerCFR:
    """
    Counterfactual Regret Minimization (CFR) for Kuhn Poker using a three-card deck ('K', 'Q', 'J').
    CFR is applied to approximate Nash equilibrium strategies over many iterations, minimizing regret.
    """

    def __init__(self):
        # Represents the game deck: King, Queen, Jack
        self.deck = ["K", "Q", "J"]
        # Dictionary of nodes representing each information set (state)
        self.node_map = {}
        # Number of actions available (0 = pass, 1 = bet)
        self.n_actions = 2
        # List to track cumulative gain over iterations for convergence visualization
        self.cumulative_gains = []

    def train(self, n_iterations=50000):
        """
        Trains the CFR model over a defined number of iterations to approximate Nash equilibrium strategies.
        
        Parameters:
            - n_iterations: Total number of training iterations for CFR algorithm.
        """
        # Dynamically set plot interval based on total iterations
        plot_interval = max(1, n_iterations // 100)  # Plot about every 1% of the iterations
        total_gain = 0  # Accumulated gain to observe progress

        for i in range(n_iterations):
            shuffle(self.deck)  # Randomize deck for each iteration
            # Deal two cards to players for each round of CFR
            player_cards = [self.deck[0], self.deck[1]]

            # Run CFR from an empty game history
            total_gain += self.counterfactual_regret_minimization('', 1, 1, player_cards)

            # Update the strategy of all nodes based on accumulated regrets
            for _, node in self.node_map.items():
                node.update_strategy()

            # Record and log the cumulative gain periodically
            if i % plot_interval == 0:
                cumulative_gain = abs(total_gain / (i + 1))  # Taking absolute to track magnitude of learning
                self.cumulative_gains.append(cumulative_gain)
                logging.info(f"Iteration {i + 1}, Cumulative Gain (Absolute): {cumulative_gain:.4f}")

        # Display final results and strategy convergence plot
        self.display_results(abs(total_gain / n_iterations))
        self.plot_convergence()

    def counterfactual_regret_minimization(self, history, prob_p1, prob_p2, player_cards):
        """
        Recursive function implementing CFR for regret minimization at each decision point.
        
        Parameters:
            - history: String representing sequence of actions taken so far.
            - prob_p1, prob_p2: Probability of each player reaching the current state.
            - player_cards: Array with Player 1's and Player 2's private cards.
        
        Returns:
            - The expected utility of the current game state.
        """
        # Determine whose turn it is
        is_p1_turn = len(history) % 2 == 0
        current_player_card = player_cards[0] if is_p1_turn else player_cards[1]

        # Check if this is a terminal state
        if self.is_terminal_state(history):
            return self.compute_terminal_reward(history, player_cards)

        # Access or create a new node for the current state
        node = self.get_or_create_node(current_player_card, history)
        strategy = node.strategy
        action_utilities = np.zeros(self.n_actions)

        # Calculate counterfactual utility for each action
        for action in range(self.n_actions):
            next_history = history + node.action_map[action]
            if is_p1_turn:
                action_utilities[action] = -self.counterfactual_regret_minimization(
                    next_history, prob_p1 * strategy[action], prob_p2, player_cards)
            else:
                action_utilities[action] = -self.counterfactual_regret_minimization(
                    next_history, prob_p1, prob_p2 * strategy[action], player_cards)

        # Calculate total utility and update regrets
        util = np.sum(action_utilities * strategy)
        regrets = action_utilities - util
        if is_p1_turn:
            node.regret_sum += prob_p2 * regrets
        else:
            node.regret_sum += prob_p1 * regrets

        return util

    def get_or_create_node(self, card, history):
        """
        Retrieve or create a decision node for the current game state (card and action history).
        
        Parameters:
            - card: Current player's private card.
            - history: String of actions taken so far.
        
        Returns:
            - Node representing the current state.
        """
        key = f"{card} {history}"
        if key not in self.node_map:
            self.node_map[key] = Node(key)
        return self.node_map[key]

    @staticmethod
    def is_terminal_state(history):
        """Determines if the game state is terminal based on the action history."""
        return history[-2:] in {'pp', 'bb', 'bp'}

    @staticmethod
    def compute_terminal_reward(history, player_cards):
        """
        Calculates the reward at terminal states based on the final hands and actions.
        
        Parameters:
            - history: Sequence of actions in the game.
            - player_cards: Array with Player 1's and Player 2's cards.
        
        Returns:
            - Reward value based on the game outcome.
        """
        rank = {'K': 3, 'Q': 2, 'J': 1}  # Card ranks for comparison
        p1_card, p2_card = player_cards

        if history[-1] == 'p':
            if history[-2:] == 'pp':
                return 1 if rank[p1_card] > rank[p2_card] else -1
            return 1  # Player who bet last wins
        return 2 if rank[p1_card] > rank[p2_card] else -2

    def display_results(self, expected_game_value):
        """Displays final strategies and the overall expected value for Player 1."""
        print(f"Expected Game Value (Player 1): {expected_game_value:.4f}")
        print("\nPlayer 1 Strategies:")
        self.print_strategy_table(is_player_1=True)
        print("\nPlayer 2 Strategies:")
        self.print_strategy_table(is_player_1=False)

    def print_strategy_table(self, is_player_1):
        """
        Prints the strategy table for each player showing probabilities for each action.
        
        Parameters:
            - is_player_1: Boolean indicating if the table is for Player 1 (True) or Player 2 (False).
        """
        rows = []
        for key, node in sorted(self.node_map.items()):
            if (len(key) % 2 == 0) == is_player_1:
                rows.append([key] + [f"{p:.2f}" for p in node.get_average_strategy()])
        headers = ["InfoSet", "Pass", "Bet"]
        print(tabulate(rows, headers=headers, tablefmt="pretty"))

    def plot_convergence(self):
        """Plots the convergence of absolute cumulative gains to assess strategy stability."""
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(self.cumulative_gains)), self.cumulative_gains, marker='o', linestyle='-')
        plt.xlabel("Iterations (in intervals)", fontsize=12)
        plt.ylabel("Absolute Cumulative Gain", fontsize=12)
        plt.title("Convergence of CFR Strategy for Kuhn Poker", fontsize=14, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()

    def test_against_bots(self):
        """
        Evaluates CFR bot's performance against basic strategies: passive, aggressive, and balanced.
        """
        # Define strategies for basic bots
        bots = {
            "Passive": lambda card, history: "p",
            "Aggressive": lambda card, history: "b",
            "Normal": lambda card, history: "b" if card == "K" else "p"
        }
        
        n_games = 1000  # Number of games per opponent
        results = {bot_name: 0 for bot_name in bots}

        for bot_name, bot_strategy in bots.items():
            for _ in range(n_games):
                shuffle(self.deck)
                player_cards = [self.deck[0], self.deck[1]]
                history = ""
                while not self.is_terminal_state(history):
                    if len(history) % 2 == 0:
                        # CFR bot's turn
                        node = self.get_or_create_node(player_cards[0], history)
                        action = np.random.choice(["p", "b"], p=node.get_average_strategy())
                        history += action
                    else:
                        # Opponent bot's turn
                        action = bot_strategy(player_cards[1], history)
                        history += action

                # Record result of each game
                results[bot_name] += self.compute_terminal_reward(history, player_cards)

            results[bot_name] /= n_games  # Average result per game

        # Display testing results
        print("\nCFR Bot Performance Against Different Strategies:")
        for bot_name, result in results.items():
            print(f"Against {bot_name} Bot: Average Gain per Game = {result:.4f}")

class Node:
    """
    Represents a decision node in the game, tracking regrets and strategy updates over CFR iterations.
    """

    def __init__(self, key):
        self.key = key
        self.n_actions = 2  # Actions: pass, bet
        self.regret_sum = np.zeros(self.n_actions)  # Regret for each action
        self.strategy_sum = np.zeros(self.n_actions)  # Cumulative strategy for averaging
        self.action_map = {0: 'p', 1: 'b'}  # Maps action index to action label
        self.strategy = np.repeat(1 / self.n_actions, self.n_actions)  # Initial strategy is uniform

    def update_strategy(self):
        """Updates strategy based on regret-matching; positive regrets contribute to future strategies."""
        positive_regrets = np.maximum(0, self.regret_sum)
        normalizing_sum = positive_regrets.sum()
        self.strategy = positive_regrets / normalizing_sum if normalizing_sum > 0 else np.repeat(1 / self.n_actions, self.n_actions)
        self.strategy_sum += self.strategy  # Aggregate strategies over iterations

    def get_average_strategy(self):
        """Calculates average strategy across all iterations, with uniform distribution as fallback."""
        if self.strategy_sum.sum() > 0:
            avg_strategy = self.strategy_sum / self.strategy_sum.sum()
        else:
            avg_strategy = np.repeat(1 / self.n_actions, self.n_actions)
        return avg_strategy

if __name__ == "__main__":
    # Request user input for training iterations only
    n_iterations = int(input("Enter the number of training iterations: "))

    trainer = KuhnPokerCFR()
    trainer.train(n_iterations=n_iterations)
    trainer.test_against_bots()

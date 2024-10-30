# Kuhn Poker CFR Bot

## Table of Contents
- [Project Description](#project-description)
- [What is Kuhn Poker?](#what-is-kuhn-poker)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Opponent Bot Strategies](#opponent-bot-strategies)
- [Results and Performance](#results-and-performance)
- [Visualizations](#visualizations)
- [To Do](#to-do)
- [Contributing](#contributing)
- [License](#license)

## Project Description
This project implements a Kuhn Poker bot using **Counterfactual Regret Minimization (CFR)**. The bot dynamically adapts its strategy based on the behavior of its opponents, classifying them as **aggressive**, **passive**, or **balanced**. The goal is to approximate Nash equilibrium strategies in the game of Kuhn Poker.

## What is Kuhn Poker?
Kuhn Poker is a simple two-player game played with a three-card deck consisting of a King (K), a Queen (Q), and a Jack (J). Each player is dealt one card face down, and they take turns betting or passing. The game has a fixed betting structure, and the player with the highest-ranking card wins at showdown, or the player who bets last wins if both players choose to pass. The simplicity of Kuhn Poker makes it an excellent platform for studying game theory and strategy optimization techniques like CFR.

## Features
- **CFR Algorithm**: Implements the CFR algorithm for strategy optimization.
- **Dynamic Adaptation**: Adjusts the bot's strategy based on detected opponent behavior.
- **Opponent Bot Types**: Includes different opponent bots with varying strategies.
- **Performance Tracking**: Tracks and displays win/loss rates against each opponent type.
- **Visualizations**: Provides graphs to visualize bot performance over time.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
1. Run the bot:
   python main.py
2. Input training parameters when prompted (e.g., number of training iterations).
3. View the results of the bot's performance against various opponent strategies.

## Opponent Bot Strategies
1. Passive Bot: Always passes unless holding a King and in a favorable position.
2. Aggressive Bot: Bets often, utilizing a more aggressive strategy.
3. Balanced Bot: Mixes strategies, betting with Kings, and varying actions based on history.

## Results and Performance
1. After running simulations against different opponents, the bot will print win/loss rates and net wins for each opponent type.

## Example output:

Results against Passive Bot:
  Win Rate: 75.00%
  Loss Rate: 25.00%
  Net Wins: 50

Results against Aggressive Bot:
  Win Rate: 60.00%
  Loss Rate: 40.00%
  Net Wins: 20

Results against Balanced Bot:
  Win Rate: 65.00%
  Loss Rate: 35.00%
  Net Wins: 30

## Visualizations
1. Images showcasing the game tree and how CFR works and a graph showcasing the bot's convergence towards Nash equilibrium can be found in the images/ directory. These visualizations help illustrate the strategy optimization process in Kuhn Poker.

## To Do / Improving The Project
1. Implement Leduc Poker and test out Monte Carlo Sampling with CFR --> MCCFR for more complex strategies
2. Explore additional sampling techniques such as Importance Sampling and Regret Matching+ (CFR+)

**Why?:**
CFR+ and MCCFR are crucial because they sample iterations more efficiently, allowing for quicker convergence toward Nash equilibrium by focusing on the most relevant parts of the strategy space. Instead of iterating through each node and the entire probability space, you take a sample of all paths or only use positive regret to minimize
the amount of computation. Based on these samples, you would estimate the rest of the values. This is proven to help models reach the Nash equilibrium faster than regular
CFR methods. However, due to Kuhn Poker's simplicity, it isn't needed but may be needed for Leduc Poker and Texas Hold'Em.

## Contributing
1. Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

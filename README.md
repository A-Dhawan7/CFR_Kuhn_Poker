# Kuhn Poker CFR Bot

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Opponent Bot Strategies](#opponent-bot-strategies)
- [Results and Performance](#results-and-performance)
- [Visualizations](#visualizations)
- [Contributing](#contributing)
- [License](#license)

## Project Description
This project implements a Kuhn Poker bot using **Counterfactual Regret Minimization (CFR)**. The bot dynamically adapts its strategy based on the behavior of its opponents, classifying them as **aggressive**, **passive**, or **balanced**. The goal is to approximate Nash equilibrium strategies in the game of Kuhn Poker.

## Features
- **CFR Algorithm**: Implements the CFR algorithm for strategy optimization.
- **Dynamic Adaptation**: Adjusts the bot's strategy based on detected opponent behavior.
- **Opponent Bot Types**: Includes different types of opponent bots with varying strategies.
- **Performance Tracking**: Tracks and displays win/loss rates against each opponent type.
- **Visualizations**: Provides graphs to visualize bot performance over time.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/kuhn_poker_cfr_bot.git
   cd kuhn_poker_cfr_bot

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
1. Run the bot:
   python main.py
2. Input training parameters when prompted (e.g., number of training iterations).
3. View results of the bot's performance against various opponent strategies.

## Opponent Bot Strategies
1. Passive Bot: Always passes unless holding a King and in a favorable position.
2. Aggressive Bot: Bets often, utilizing a more aggressive strategy.
3. Balanced Bot: Mixes strategies, betting with Kings and varying actions based on history.

## Results and Performance
1. After running simulations against different opponents, the bot will print win/loss rates and net wins for each opponent type.

## Example output:

yaml
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
1. Images showcasing the game tree and CFR workings can be found in the images/ directory. These visualizations help illustrate the strategy optimization process in Kuhn Poker.


## Contributing
1. Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

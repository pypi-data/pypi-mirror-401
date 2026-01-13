📦 minigamesbyvedcodes – A Simple Python Games Library
🎮 Overview

minigamesbyvedcodes is a beginner-friendly Python library that lets users play classic games by calling simple functions — no complex setup, no boilerplate code.

This is my first Python module, built to understand:

Python packages & modules

Clean API design

Code reuse

Real-world library structure

✨ Features

✅ Tic Tac Toe (2-player)

✅ Rock Paper Scissors (Player vs Computer)

✅ Maths Quiz (Score-based)

✅ Shared player name system

✅ Single-function game execution

✅ Clean and extendable structure

📁 Project Structure
minigamesbyvedcodes/
│
├── minigamesbyvedcodes/
│   ├── __init__.py
│   ├── users.py
│   ├── tictactoe.py
│   ├── rps.py
│   └── maths_quiz.py
│
├── README.md
└── setup.py


Each file has a single responsibility, following professional Python library practices.

🚀 Installation

After publishing on PyPI:

pip install minigamesbyvedcodes

▶️ Usage
import minigamesbyvedcodes as mnigames 

minigames.tic_tac_toe()
minigames.rock_paper_scissors()
minigames.maths_quiz()


That’s it — the game starts instantly 🎉

🧠 Module Explanation
__init__.py

Acts as the public API

Controls what users can import

Keeps internal files hidden

users.py

Handles player name input

Reused across all games

Prevents code duplication (DRY principle)

tictactoe.py

Implements board logic

Player switching

Win & draw conditions

Fully terminal-based

rps.py

Rock Paper Scissors logic

Player vs Computer

Randomized computer moves

maths_quiz.py

Generates random math questions

Tracks score

Interactive quiz format

🎯 Why This Project?

This project helped me learn:

How real Python libraries are structured

How to expose clean functions

How to reuse logic across modules

How PyPI publishing works

📄 License

MIT License — free to use and modify.
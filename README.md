# NeuralChess 
### Designed and Built by Austin Shouli

## Overview 

NeauralChess is an ongoing personal project to train an machine learning (ML) algorithm to play the Los Alamos Chess variant using reinforcement learning (RL). Los Alamos Chess is played on a 6x6 board without bishops, and is notable for being the first chess-like game to be played by a computer, in 1956. AlphaZero style modelling of the observation space, action space, action mask and rewards are used with a Gymnasium/PettingZoo enviroment constructed around these rules. Los Alamos chess was chosen partly to simplify the enviroment cosntruction, but also to demonstrate an understaing of how the observation/action space modeling works by modifying it from the AlphaZeo format and similar enviroments. 

   *Note that this is in active development, and is intended as an educational exploration of machine learning techniques and tools. The focus has not been on efficiency, but rather on agile development to complete a working model in pursuit of learning. Therefore, the code is likely not as robust, efficient or organized as would be expected in a commercial or academic setting.

This project consists of three main components. Parts 1 and 2 are essentially functioning, and Part 3 is being developed:

 1. Part 1 is a python package called board, which consists of a set of classes defining a chess board, teams, pieces and the move set for each piece. This can be used to play a game of chess by alternating the play_turn() call until the game is over, with an ascii style board being printed to the terminal. Capture-the-king rules are implimented, as well as Los Alamos rules, which eliminates the need for checking if a king is in check/checkmate. Kings can move into check, and a player must formally capture an opponent's king to end the game. (An 8x8 variant exisits in another branch).  

 2. Part 2 consists of a custom Gymnasium / PettingZoo enviroment (Gymnasium, formely by OpenAI, is an API for reinforcement learning containing various enviroments for training machine learning algorithms. PettingZoo is  variant of Gymnasium deidated to MARL - Multi-Agent Reinforcement Learning). The custom Los Alamos Chess enviroment uses the Agent Enviroment Cycle (AEC) API, is constructed based on the PettingZoo tutorials and documentation, and passes all of the relevent PettingZoo enviroment tests. This API allows for a portable enviroment that can easily be adapted to varios ML/RL librares and algorithms.  
    

3. Part 3 is ongoing and consists of an effort to construct and traing a machine learning algorithm to play Los Alamos chess, using the PettingZoo enviroment. The current plan is to use the PyTorch TorchRL library, which consists of a PettingZooWrapper for usinging PettingZoo enviroments with TorchRL. The plan for the initial model is to use a Multi-Layer Perceptron (MLP) to impliment a Deep-Q Network (DQN), with plans to add other styles of RL algorithms, such as PPO, to play against each other and compare results.


## Running the program

Running engine.py from the command line will run a random game of chess, with each move selected based on the observation space, and selected from the action space with the action mask applied. This results in no invalid moves being chosen. If an invalid move is chosen, the game will terminate and -1 reward is applied to the offending player. Each move the board is output as an ascii diagram, to the terminal and the /data/game.txt file. The game.txt file will be overwritten each time the program is run. 

    Windows: 
    
        $ python3 .\neuralchess\engine.py


## Future Developments 

- Add requirements.txt
- Add captured pieces tracking to each team 
- Add pawn upgrading as a valid move
- Build a menu system for training algorithms, playing the against each other, and playing against a human player

## Links 
Los Alamos Chess: https://en.wikipedia.org/wiki/Los_Alamos_chess
AlphaZero Chess Paper: https://arxiv.org/abs/1712.01815
Gymnasium: https://gymnasium.farama.org/
PettingZoo: https://pettingzoo.farama.org/
PettingZooWrapper: https://pytorch.org/rl/reference/generated/torchrl.envs.PettingZooWrapper.html



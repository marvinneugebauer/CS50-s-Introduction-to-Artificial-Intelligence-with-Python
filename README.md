# CS50's Introduction to Artificial Intelligence with Python
Topics that are covering by that course
- **graph search algorithms** 
- **adversarial search**
- **knowledge representation**
- **logical inference** 
- **probability theory** 
- **Bayesian networks**
- **Markov models**
- **machine learning**
- **reinforcement learning**
- **neural networks**
- **natural language processing**
  


# Description of the Projects

- **Project: Degrees**
    +  For two sets of CSV data files, where each file contains the same names, and the same structure, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. Therefore we are using the **breadth-first search algorithm** in ``degrees.py ``.
- **Project: Tictactoe**
    + Using the **Minimax algorithm**, implement an AI in ``tictactoe.py`` to play Tic-Tac-Toe optimally.
- **Project: Knights**
    + Determine how to represent "Knights and Knaves" puzzles using **propositional logic**, such that an AI running a **model-checking algorithm** could solve these puzzles for us. An implemenation of that problem can be found in ``logic.py`` together with ``puzzle.py``.
- **Project: Minesweeper**
    + The goal in this project is to build an AI that can play Minesweeper. In doing so we use knowledge-based agents that make decisions by considering their knowledge base, and making inferences based on that knowledge. An implemenation of that problem can be found in ``minesweeper.py`` together with ``runner.py``.
- **Project: PageRank**
    + In this project, we implementing the **PageRank’s algorithm**. In order to calculate PageRank we are using a combination of two approaches in ``pagerank.py``: First by sampling pages from a Markov Chain random surfer. Second by iteratively applying the PageRank formula.
- **Project: Heredity**
    + In this project we use a **Bayesian Network** in ``heredity.py`` to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, our AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.
- **Project: Crossword**
    + In this project we write an AI to generate and solve crossword puzzles. Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. Therefore we model this sort of problem as a **constraint satisfaction problem** and use the **AC3 algorithm** in order to solve that problem. An implemenation of that problem can be found in ``generate.py`` together with ``crossword.py``. 
- **Project: Shopping**
    + In this project we write an AI to generate and solve crossword puzzles. An implemenation of that problem can be found in ``generate.py`` together with ``crossword.py``. 
 

#  References
https://cs50.harvard.edu/ai/2020/

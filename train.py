import copy
import random
from tetris import *
import pickle

q = {}
a = 0.5
g = 0.85
explore = 0.3
actions = [-1, 0, 1]

def run_games(iterations):
  hi_score = 0
  hi_reward = 0

  print('iteration,score,hiscore,hireward')

  for i in range(iterations):
    game = Game()
    last_score = 0
    while not game.game_over:
      st = game.numerical_representation()
      random.shuffle(actions)
      at = actions[0] if random.random() < explore else max(actions, key=lambda a: q.get((st, a), 0))
      game.step(at)
      st1 = game.numerical_representation()
      reward = game.score - last_score
      last_score = game.score

      q[(st, at)] = q.get((st, at), 0) + \
        a * (
          reward + \
            g * max([q.get((st1, a), 0) for a in actions]) - \
            q.get((st, at), 0)
        )
      if q[(st, at)] > hi_reward:
        hi_reward = q[(st, at)]

    configure_turtle()
    game.draw()

    if hi_score < game.score:
      hi_score = game.score

    print(str(i) + ',' + str(game.score) + ',' + str(hi_score) + ',' + str(hi_reward))

run_games(100000)
with open('q.pickle', 'wb') as file:
  pickle.dump(q, file)

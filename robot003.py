import rg
import random

class Robot:
    def find_enemy(self, game):
        enemy = None
        for loc, bot in game.robots.iteritems():

            if enemy is None or bot.hp < enemy.hp:
                enemy = bot
        return enemy

    def act(self, game):
        # if there are enemies around, attack them
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        #else, move towards weakest enemy
        enemy = self.find_enemy(game)

        # move toward the center
        next_move = rg.toward(self.location,enemy.location)
        return ['move', next_move]

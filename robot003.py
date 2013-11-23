import rg
import random

## Always move towards the weakest enemy
## If the next step towards the enemy is occupied with
## a friendly bot or is unsafe, move randomly

class Robot:
    def find_weakest_enemy(self, game):
        enemy = None
        for loc, bot in game.robots.iteritems():

            if enemy is None or bot.hp < enemy.hp:
                enemy = bot
        return enemy

    def next_move(self, destination, game):
        print "next_move!"
        def is_valid_and_safe(step):
            for unsafe_type in  ['invalid', 'spawn', 'obstacle']:
                if unsafe_type in rg.loc_types(step):
                    print "unsafe_type:", unsafe_type
                    return False
            return True
        def is_friendly(step, game):
            for loc, robot in game.robots.items():
                if robot.player_id == self.player_id:
                    if loc == step:
                        print "is_friendly:", True
                        return True
            return False


        test_step = rg.toward(self.location, destination)
        if is_valid_and_safe(test_step) and not is_friendly(test_step,game):
            return test_step
        print "not OK test_step: %s"%(test_step,)
        mask = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        next_step = (self.location[0]+mask[0], self.location[1]+mask[1])
        print "mask: %s, next_step: %s"%(mask, next_step)
        return next_step


    def act(self, game):
        # if there are enemies around, attack them
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        #else, move towards weakest enemy
        enemy = self.find_weakest_enemy(game)

        destination = enemy.location
        move = self.next_move(destination, game)
        if move is None:
            return ['guard']
        return ['move', move]

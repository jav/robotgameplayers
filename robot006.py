import rg
import random

## Always move towards the weakest frendly bot
## If the next step towards the enemy is occupied with
## a friendly bot or is unsafe, move randomly
## If self.hp <20, just move towards center

class Robot:
    def friendly_list(self, game):
        return [(loc, bot) for (loc, bot) in game.robots.iteritems() if bot.player_id == self.player_id]

    def enemy_list(self, game):
        return [(loc, bot) for (loc, bot) in game.robots.iteritems() if bot.player_id != self.player_id]

    def find_weakest_bot(self, lst, game):
        weak_bot = None
        for loc, bot in lst:
            print "find_weakest_bot(): loc: %s, bot: %s"%(loc, bot)
            if weak_bot is None or bot.hp < weak_bot.hp:
                weak_bot = bot
        return weak_bot

    def next_move(self, destination, game):
        print "next_move!"
        def is_valid_and_safe(step):
            for unsafe_type in  ['invalid', 'spawn', 'obstacle']:
                if unsafe_type in rg.loc_types(step):
                    print "unsafe_type:", unsafe_type
                    return False
            return True
        def is_friendly(step, game):
            for loc, robot in self.friendly_list(game):
                if loc == step:
                    print "is_friendly:", True
                    return True
            return False


        test_step = rg.toward(self.location, destination)
        if is_valid_and_safe(test_step) and not is_friendly(test_step,game):
            return test_step
        print "not OK from: %s to test_step: %s"%(self.location, test_step)
        #move clockwize
        move_mask = (test_step[1]-self.location[1], test_step[0]-self.location[0])
        next_step = (self.location[0]+move_mask[0], self.location[1]+move_mask[1])
        print "mask: %s, next_step: %s"%(move_mask, next_step)
        return next_step


    def act(self, game):
        # if health < 20, just move to the centre
        if self.hp < 20:
            if self.location == rg.CENTER_POINT:
                return ['guard']
            # if there are enemies around, attack them
            for loc, bot in self.enemy_list(game):
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]
            # move toward the center
            return self.next_move(rg.CENTER_POINT, game)

        # if there are enemies around, attack them
        for loc, bot in self.enemy_list(game):
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        #else, move towards weakest enemy
        target_bot = self.find_weakest_bot(self.friendly_list(game),game)
        destination = target_bot.location
        move = self.next_move(destination, game)

        if move is None:
            return ['guard']
        return ['move', move]

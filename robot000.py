import rg
import random

#This robot just moves out of the spawn area (towards centre)

class Robot:
    def act(self, game):

        if 'spawn' in rg.loc_types(self.location):
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        else:
            return ['guard']

import pygame
from bullet import Bullet
class LevelState():
    def __init__(self):
        self.level = 0
        self.achieve_score_for_l1 = 2
        self.achieve_score_for_l2 = 5
        self.achieve_score_for_l3 = 7
        self.achieve_score_for_l4 = 9
        self.window=False

    def level_change(self):
        if self.achieve_score_for_l1==Bullet.score:
            self.level=1
            pygame.display.update()

    def level_change2(self):
        if self.achieve_score_for_l2==Bullet.score:
            self.level=2
            pygame.display.update()
    
    def level_change3(self):
        if self.level==3:
            pygame.display.update()

    def level_change4(self):
        if self.achieve_score_for_l4==Bullet.score:
            self.level=4
            pygame.display.update()

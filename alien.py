import pygame as pg
from pygame.sprite import Sprite

import sounds
from eBullet import EBullet


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, setting, screen, hitPoint=3, isboss = False):
        """Initialize the alien and set its starting point"""
        super(Alien, self).__init__()
        self.screen = screen
        self.setting = setting
        self.isboss = isboss
        # load the alien image and set its rect attribute
        self.image = pg.image.load('gfx/spaceship4.png')
        self.image = pg.transform.rotate(self.image, 180)
        if self.isboss == True:
            self.image = pg.transform.scale(self.image,(setting.screenWidth // 8, setting.screenWidth // 8))
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the aliens exact position
        self.x = float(self.rect.x)

        # timer for shooting
        self.timer = 0

        # hitpoint for a basic alien (default : 3)
        if setting.gameLevel == 'normal':
            self.hitPoint = hitPoint
        elif setting.gameLevel == 'hard':
            self.hitPoint = 5

    def checkEdges(self):
        """Returns True if alien is at the edge of screen"""
        screenRect = self.screen.get_rect()
        if self.rect.right >= screenRect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def checkBottom(self):
        """Returns True if alien is at the bottom of screen"""
        screenRect = self.screen.get_rect()
        if self.rect.bottom >= screenRect.bottom:
            return True

    def update(self, setting, screen, ship, aliens, eBullets):
        """Move the alien right or left"""
        self.ship = ship
        self.aliens = aliens
        self.eBullets = eBullets
        self.x += (self.setting.alienSpeed * self.setting.fleetDir)
        self.rect.x = self.x
        self.shoot(setting, screen, self.ship, self.aliens, self.eBullets)

    def shoot(self, setting, screen, ship, aliens, eBullets):
        if setting.gameLevel == 'hard':
            setting.shootTimer = 10     # default = 50

        if self.isboss == False:
            if self.rect.centerx >= self.ship.rect.centerx and len(eBullets) <= 4:
                if self.timer >= setting.shootTimer:
                    sounds.enemy_shoot_sound.play()
                    self.timer = 0
                    newBullet = EBullet(setting, screen, self)
                    eBullets.add(newBullet)
                self.timer += 1
        else:
            if self.rect.centerx >= self.ship.rect.centerx and len(eBullets) <= 45:
                if self.timer >= setting.shootTimer:
                    sounds.enemy_shoot_sound.play()
                    self.timer = 0
                    newBullet1 = EBullet(setting, screen, self)
                    eBullets.add(newBullet1)
                    newBullet2 = EBullet(setting, screen, self, 1)
                    eBullets.add(newBullet2)
                    newBullet3 = EBullet(setting, screen, self, 2)
                    eBullets.add(newBullet3)
                self.timer += 1

    def blitme(self):
        """draw hte alien"""
        self.screen.blit(self.image, self.rect)



import pygame

from shared import constants


class Game(object):
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Initialize screen
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)

        # Initialize background
        self.background_image = self.init_background()
        self.background_rect = self.background_image.get_rect()

    def init_background(self):
        back_image = pygame.image.load(constants.BACKGROUND_IMAGE_PATH)
        back_image = pygame.transform.scale(back_image, constants.SCREEN_SIZE)
        return back_image

    def start(self):
        while True:
            self.handle_events()
            self.update_logic()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def update_logic(self):
        pass

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)
        # self.screen.fill(self.setting.background_color)
        pygame.display.flip()



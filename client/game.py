import pygame

from client.game_session import GameSession
from shared import constants
from shared.constants import FPS, BLACK, LOG_BORDER_RECT, HAND_BORDER_RECT, SHARED_HAND_BORDER_RECT, LOG_BACK_COLOR


class Context(object):
    """ Everyone deserves a bit of context """

    def __init__(self, screen, game_session, log_view, hand_view, shared_hand_view, game):
        self.screen = screen
        self.game_session = game_session
        self.log_view = log_view
        self.hand_view = hand_view
        self.shared_hand_view = shared_hand_view
        self.game = game


class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):  # RECTANGLE (X,Y,100,130)
        """ Loads image from x, y, x + offset, y + offset """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class RectView(object):
    def __init__(self, screen, game_session, rect_points, border_color, border_width=5):
        self._screen = screen
        self._game_session = game_session
        self._rect_points = rect_points
        self._border_color = border_color
        self._border_width = border_width
        self._context: Context = None

    def set_context(self, context):
        self._context = context

    def draw(self):
        # Draw rectangle border
        pygame.draw.rect(self._screen, self._border_color, self._rect_points, self._border_width)


class LogView(RectView):
    def __init__(self, screen, game_session, rect_points, font_size=16):
        super().__init__(screen, game_session, rect_points, BLACK)
        self._font_size = font_size
        self._font = pygame.font.SysFont('Comic Sans MS', font_size)

        self._text_surfaces = []  # list of rendered logs

        self._background_surface = pygame.Surface((rect_points[2], rect_points[3]))
        self._background_surface.set_alpha(128)
        self._background_surface.fill(LOG_BACK_COLOR)

    def print_log(self, log_text):
        text_surface = self._font.render(log_text, False, (255, 255, 255))
        self._text_surfaces.append(text_surface)
        if len(self._text_surfaces) >= 25:  # Sorry, this is a magic number. don't mess with the font size...
            self._text_surfaces.pop(0)

    def draw(self):
        super().draw()
        # draw transparent background
        self._screen.blit(self._background_surface, (0, 0))
        y = self._font_size * 1.15
        for i in range(len(self._text_surfaces)):
            text_surface = self._text_surfaces[i]
            self._screen.blit(text_surface, (5, i * y))


class Button(object):
    def __init__(self, screen, game_session, text, rect_points, non_active_color, hover_color, on_click_handler):
        self._screen = screen
        self._game_session = game_session
        self._text = text
        self._rect_points = rect_points
        self._non_active_color = non_active_color
        self._hover_color = hover_color
        self._on_click_handler = on_click_handler

        self._font = pygame.font.SysFont(None, 16)

        # button stuff
        self.start_click = False

    def change_text(self, text):
        self._text = text

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()

        x, y, w, h = self._rect_points

        is_mouse_in_btn = self.is_mouse_inside_button(mouse_pos)
        btn_color = self._hover_color if is_mouse_in_btn else self._non_active_color

        if is_mouse_in_btn and is_mouse_pressed[0] and not self.start_click:
            self.start_click = True
        if not is_mouse_in_btn and not is_mouse_pressed[0] and self.start_click:
            self.start_click = False

        pygame.draw.rect(self._screen, btn_color, self._rect_points)
        # You need to depress the mouse inside the button for stuff to work
        if self.start_click and is_mouse_in_btn and not is_mouse_pressed[0]:
            self._on_click_handler()
            self.start_click = False

        text_surface: pygame.Surface = self._font.render(self._text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + (w / 2), y + (h / 2))
        self._screen.blit(text_surface, text_rect)

    def is_mouse_inside_button(self, mouse_pos):
        x, y, w, h = self._rect_points
        return x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h


class HandView(RectView):
    def __init__(self, screen, game_session, rect_points):
        super().__init__(screen, game_session, rect_points, BLACK)
        x, y, w, h = rect_points
        center_x, center_y = (x + w * 0.4, y + h * 0.65)
        self.center_x, self.center_y = center_x, center_y
        btn_width = 60
        btn_height = 40
        self.bet_btn = Button(screen, game_session, 'Bet',
                              (center_x - btn_width * 1.1, center_y, btn_width, btn_height), constants.BLUE,
                              constants.LIGHT_BLUE, self.on_bet)
        self.call_btn = Button(screen, game_session, 'Call',
                               (center_x + btn_width * 2.3, center_y, btn_width, btn_height), constants.BLUE,
                               constants.LIGHT_BLUE, self.on_call)
        self.check_btn = Button(screen, game_session, 'Check',
                                (center_x - btn_width * 2.3, center_y, btn_width, btn_height), constants.BLUE,
                                constants.LIGHT_BLUE, self.on_check)
        self.fold_btn = Button(screen, game_session, 'Fold',
                               (center_x + btn_width * 1.1, center_y, btn_width, btn_height), constants.BLUE,
                               constants.LIGHT_BLUE, self.on_fold)
        self.up_arrow_btn = Button(screen, game_session, 'Raise Bet',
                                   (center_x, center_y - btn_height * 1.1, btn_width, btn_height), constants.BLUE,
                                   constants.LIGHT_BLUE, self.on_raise_bet)
        self.down_arrow_btn = Button(screen, game_session, 'Lower Bet',
                                     (center_x, center_y + btn_height * 1.1, btn_width, btn_height), constants.BLUE,
                                     constants.LIGHT_BLUE, self.on_lower_bet)

        self.spritesheet = SpriteSheet(constants.CARD_DECK_IMAGE_PATH)

    def on_bet(self):
        if self._game_session.is_my_turn():
            self._game_session.execute_bet()

    def on_fold(self):
        if self._game_session.is_my_turn():
            self._game_session.execute_fold()

    def on_raise_bet(self):
        if self._game_session.is_my_turn():
            self._game_session.raise_bet(20)
            self._context.log_view.print_log('bets {}, if u r sure press \"bet\" button'.format(self._game_session.bet))

    def on_lower_bet(self):
        if self._game_session.is_my_turn():
            self._game_session.lower_bet(20)
            self._context.log_view.print_log('bets {}, if u r sure press \"bet\" button'.format(self._game_session.bet))

    def on_check(self):
        if self._game_session.is_my_turn():
            self._game_session.execute_check()

    def on_call(self):
        if self._game_session.is_my_turn():
            self._game_session.execute_call()

    def draw(self):
        super().draw()
        self.bet_btn.draw()
        self.fold_btn.draw()
        self.call_btn.draw()
        self.check_btn.draw()
        self.up_arrow_btn.draw()
        self.down_arrow_btn.draw()

        cards = list(self._game_session.hand.values())
        for i in range(len(cards)):
            card = cards[i]
            x, y = card[0], card[1]
            card_image = self.spritesheet.image_at((x, y, 100, 130))
            self._screen.blit(card_image, (self.center_x - 50 + i * 100, self.center_y - 100 * 3))


class SharedHandView(RectView):
    def __init__(self, screen, game_session: GameSession, rect_points):
        super().__init__(screen, game_session, rect_points, BLACK)
        self.spritesheet = SpriteSheet(constants.CARD_DECK_IMAGE_PATH)

    def draw(self):
        super().draw()

        for i in range(len(self._game_session.shared_hand)):
            card = self._game_session.shared_hand[i]
            x, y = card[1][0], card[1][1]
            card_image = self.spritesheet.image_at((x, y, 100, 130))
            self._screen.blit(card_image, (i * 100 + 100, self._rect_points[1] + 10))


class Game(object):
    def __init__(self, game_session: GameSession):
        self._game_session = game_session
        self._game_state = None

        # Initialize pygame
        pygame.init()

        # Initialize screen
        self._screen = pygame.display.set_mode(constants.SCREEN_SIZE)

        # Initialize background
        back_image = pygame.image.load(constants.BACKGROUND_IMAGE_PATH)
        back_image = pygame.transform.scale(back_image, constants.SCREEN_SIZE)
        self._background_image = back_image
        self._background_rect = self._background_image.get_rect()

        # Initialize Views
        self._log_view = LogView(self._screen, self._game_session, LOG_BORDER_RECT)
        self._hand_view = HandView(self._screen, self._game_session, HAND_BORDER_RECT)
        self._shared_hand_view = SharedHandView(self._screen, self._game_session, SHARED_HAND_BORDER_RECT)
        # Game Context
        self._game_context = Context(self._screen, self._game_session, self._log_view, self._hand_view,
                                     self._shared_hand_view, self)

        self._log_view.set_context(self._game_context)
        self._hand_view.set_context(self._game_context)
        self._shared_hand_view.set_context(self._game_context)
        self._game_session.set_context(self._game_context)

        # Game clock - for FPS accuracy
        self._clock = pygame.time.Clock()

    def start(self):
        """ Game loop """
        while True:
            self.handle_events()
            self.update_logic()
            self.draw()

    def handle_events(self):
        """ Handles window events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def update_logic(self):
        """ Update game logic """
        # dx = dv * dt
        # delta_time: time passed since last tick
        delta_time = self._clock.tick(FPS)

        # Check if we have data to recv and handle it
        self._game_session.try_recv_game_state()

        # TODO check whatever

    def draw(self):
        """ Draw game to screen """
        self._screen.blit(self._background_image, self._background_rect)
        self._log_view.draw()
        self._hand_view.draw()
        self._shared_hand_view.draw()

        pygame.display.flip()

import pygame
import time
import entity_manager
import asset_manager
import score


# Initialize Pygame
pygame.init()


# Turn on cProfile
ENABLE_PROFILING = False


class Application:
    def __init__(self):
        # Set up display
        screen_dimensions = (800, 600)
        self.screen = pygame.display.set_mode(screen_dimensions, pygame.DOUBLEBUF)
        pygame.display.set_caption('Tower VI')

        # Initialize images
        asset_manager.init_images(self.screen)

        # Create a font
        self.font = pygame.font.SysFont('Helvetica Neue', 12)

        # Initialize frame rate clock
        self.frame_rate = 70
        self.clock = pygame.time.Clock()

        # Set up game
        self.player = None
        self.initialize_game()

    def initialize_game(self, difficulty=4):
        score.reset()
        entity_manager.reset()
        self.player = entity_manager.spawn('ship', 300, 300)
        entity_manager.spawn('asteroid', 100, 100)
        entity_manager.spawn('asteroid', 200, 100)
        entity_manager.spawn('asteroid', 300, 100)
        entity_manager.spawn('asteroid', 400, 100)

    def training_mode(self):
        score.reset()
        entity_manager.reset()
        self.player = entity_manager.spawn('ship', 300, 300)

    def main(self):
        prev_time = time.time() - (1 / self.frame_rate)
        running = True

        while running:
            # calculate time delta (dt = seconds / frame)
            dt = time.time() - prev_time
            prev_time = time.time()

            # handle user input and other events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.initialize_game()
                    elif event.key == pygame.K_t:
                        self.training_mode()

            keys = pygame.key.get_pressed()
            self.player.set_controls(
                left=keys[pygame.K_LEFT],
                right=keys[pygame.K_RIGHT],
                thrust=keys[pygame.K_UP],
                shoot=keys[pygame.K_SPACE],
            )

            entity_manager.update(dt)

            self.screen.fill((0, 0, 0))

            entity_manager.draw(self.screen)

            # frame rate display
            self.screen.blit(self.font.render(f'{1 / dt}', True, (255, 255, 255)), (5, 5))

            # score display
            if not self.player.alive:
                msg = self.font.render(f'You lose...    remaining: {score.get_remaining()}', True, (255, 255, 255))
                offset_x = msg.get_width() // 2
                offset_y = msg.get_height() // 2
                self.screen.blit(msg, (400 - offset_x, 300 - offset_y))
                reset_msg = self.font.render('press [esc] to reset', True, (255, 255, 255))
                offset_x = reset_msg.get_width() // 2
                offset_y = reset_msg.get_height() // 2 - 20
                self.screen.blit(reset_msg, (400 - offset_x, 300 - offset_y))
            elif score.get_remaining() <= 0:
                msg = self.font.render(f'You win!    score: {score.get_score()}', True, (255, 255, 255))
                offset_x = msg.get_width() // 2
                offset_y = msg.get_height() // 2
                self.screen.blit(msg, (400 - offset_x, 300 - offset_y))
                reset_msg = self.font.render('press [esc] to reset', True, (255, 255, 255))
                offset_x = reset_msg.get_width() // 2
                offset_y = reset_msg.get_height() // 2 - 20
                self.screen.blit(reset_msg, (400 - offset_x, 300 - offset_y))

            pygame.display.update()

            # Control main loop rate
            self.clock.tick(self.frame_rate)


app = Application()

if ENABLE_PROFILING:
    import cProfile
    cProfile.run('app.main()', sort=1)
else:
    app.main()
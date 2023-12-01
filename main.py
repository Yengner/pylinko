import pygame
import pymunk
import random
import sys

from ball import Ball
from board import Board
from settings import *

# Import 'get_donor_profile_picture' function from 'utils.py'
from utils import get_donor_profile_picture
from tiktok_live_client import TikTokLiveClient

# Create a TikTokLive client instance with the correct stream ID
stream_id = "@yengner.png"
tiktok_client = TikTokLiveClient(stream_id)

class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 1800)

        # Plinko setup
        self.ball_group = pygame.sprite.Group()
        self.board = Board(self.space)

        # Debugging
        self.balls_played = 0

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the mouse click position collides with the image rectangle
                    if self.board.play_rect.collidepoint(mouse_pos):
                        self.board.pressing_play = True
                    else:
                        self.board.pressing_play = False
                # Spawn ball on left mouse button release
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_play:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.play_rect.collidepoint(mouse_pos):
                        random_x = WIDTH//2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                        click.play()
                        self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
                        self.ball_group.add(self.ball)
                        self.board.pressing_play = False
                    else:
                        self.board.pressing_play = False

            # Receive data from TikTok Live API
            try:
                data = tiktok_client.receive_data()
            except Exception as e:
                print("Error receiving data:", e)
                

            # Check if the user is live
            if data is None or data.get("live_status") != 1:
                print("User is not live or no data received")
                

            try:
                # Process gift or follower events
                if "gift" in data or "follower" in data:
                    # Extract donor's unique identifier
                    donor_id = data["gift"]["user_id"] if "gift" in data else data["follower"]["id"]

                    # Fetch the donor's profile picture
                    donor_profile_picture = get_donor_profile_picture(donor_id)

                    # Spawn a new ball with the donor's profile picture
                    random_x = WIDTH // 2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                    new_ball = Ball((random_x, 20), self.space, self.board, self.delta_time, donor_profile_picture)
                    self.ball_group.add(new_ball)
            except Exception as e:
                # Handle any error during event processing
                print("Error processing event:", e)
            self.screen.fill(BG_COLOR)

            # Time variables
            self.delta_time = self.clock.tick(FPS) / 1000.0

            # Pymunk
            self.space.step(self.delta_time)
            self.board.update()
            self.ball_group.update()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()

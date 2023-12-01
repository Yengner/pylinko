import requests
import pygame
import tiktok_live_client

# Import the global client instance in utils.py
from tiktok_live_client import TikTokLiveClient

# Create a TikTokLive client instance
tiktok_client = TikTokLiveClient(stream_id="@yengner.png")

def get_donor_profile_picture(donor_id):
    # Use TikTok User API to get the donor's profile picture URL
    user_info = tiktok_client.client.__get_client_params(donor_id)
    profile_picture_url = user_info["user"]["avatar_url"]

    # Download the profile picture
    response = requests.get(profile_picture_url)
    image_data = response.content

    # Convert image data to Pygame Surface
    profile_picture = pygame.image.frombuffer(image_data, size=(40, 40))

    return profile_picture


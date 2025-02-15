
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

import os
import time
import spotipy
import keyboard

load_dotenv()


auth_manager = SpotifyOAuth(
    client_id= os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET"),
    redirect_uri= os.getenv("REDIRECT_URI"),
    scope='user-read-playback-state user-modify-playback-state',
    cache_path=".cache"
)
sp = spotipy.Spotify(auth_manager=auth_manager)



def wait_for_active_device():
    """Wait until an active Spotify device is detected."""
    for _ in range(10):  # Check for up to 10 times (50 seconds)
        devices = sp.devices()
        if devices['devices']:
            return devices['devices'][0]['id']  # Return the first active device ID
        print("Waiting for active device...")
        time.sleep(5)
    print("No active device found. Playback may not resume.")
    return None



def restart_spotify():
    # Kill Spotify process
    os.system("taskkill /F /IM Spotify.exe")  
    time.sleep(2)  # Give time to fully close

    # Restart Spotify properly in the user session
    print("Restarting Spotify...")
    os.startfile("spotify")  # This ensures Spotify launches for the logged-in user
    
    time.sleep(10)  # Wait for Spotify to fully start

    print("Sending play command to resume playback...")
    keyboard.press_and_release("play/pause media")  # Simulate pressing play

def refresh_token():
    global sp
    if not sp.auth_manager.validate_token(sp.auth_manager.cache_handler.get_cached_token()):
        print("Refreshing Spotify token...")
        sp.auth_manager.get_access_token(as_dict=False)



def get_currently_playing():
    while True:
        try:
            refresh_token()
            current_playback = sp.current_playback()
            
            if current_playback and 'currently_playing_type' in current_playback:
                playing_type = current_playback.get('currently_playing_type', 'unknown')
                
                if playing_type not in ['track', 'episode']:
                    print(f"Unexpected content playing ({playing_type}). Restarting Spotify...")
                    restart_spotify()
                    continue  # Continue loop after restarting Spotify
            else:
                print("No active playback found.")
        except Exception as e:
            print(f"Error occurred: {e}")
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    get_currently_playing()

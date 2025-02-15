# SpotAdSkipper

Skip Spotify ads! Immediately closes the spotify client upon detecting a non-track/episode being played and reopens it, playing the next track on the most recent completed track.

# Usage

A Client ID and Client Secret is needed from a [Spotify Developer Account](https://developer.spotify.com/)  
  
Navigate to the project directory and run the script using 'python spotadskipper.py'. This will run the script indefinitely and must be cancelled manually during the user's session.  
  
It will detect the current playback and restarts the Spotify client if it is not a song/track or an episode and immediately play the next track after the most recent track before restarting
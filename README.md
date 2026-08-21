# LED-Spotify-Matrix
Using a 64x64 LED dot matrix, this code connects to your Spotify account and will display the album cover of the song you are currently listening in real time to as a rotating CD image.

# Hardware
- Raspberry Pi
- Adafruit RGB Matrix Bonnet
- 64x64 LED panel
- 5V Power supply
- Ribbon Cable
- MicroSD Card

# Setup
Follow these steps to generate the tokens your Raspberry Pi needs to access your Spotify account.

1. Create a Spotify Developer App
- Go to: https://developer.spotify.com

- Log in and open the Dashboard

- Click Create App

- Copy your Client ID and Client Secret

- Add this Redirect URL
http://127.0.0.1:8888/callback


2. Authorize Your App
- Open this URL replacing YOUR_CLIENT_ID with the one from your Spotify dashboard

https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://127.0.0.1:8888/callback&scope=user-read-private%20user-read-email


- After logging in, Spotify will redirect you to a URL containing:  
?code=YOUR_AUTHORIZATION_CODE  
Copy everything after code=.

3. Get Tokens
- Run this command in your terminal replacing the placeholders with the codes gathered from the previous steps:

bash
curl -X POST https://accounts.spotify.com/api/token \
  -u "YOUR_CLIENT_ID:YOUR_CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_AUTHORIZATION_CODE" \
  -d "redirect_uri=http://127.0.0.1:8888/callback"  
  
Spotify will respond with JSON containing an access_token and a refresh_token  

4. Save Your Tokens
Create a .env file containing:  
 
SPOTIFY_CLIENT_ID=your_id  
SPOTIFY_CLIENT_SECRET=your_secret  
SPOTIFY_REFRESH_TOKEN=your_refresh_token  
SPOTIFY_ACCESS_TOKEN=your_access_token

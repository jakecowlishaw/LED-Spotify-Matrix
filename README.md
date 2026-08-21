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

# Additional
For this project I 3D modeled a stand for the LED Matrix, along with a case for the Pi to rest on the back. The exact matrix I used was a 64x64 2mm pitch waveform Led Matrix ([Link](https://www.amazon.com/2048-Matrix-Adjustable-Brightness-Compatible/dp/B0BRBG71WS?crid=3U2IPXXK42OK2&dib=eyJ2IjoiMSJ9.4RL-284Rdnl7T7Dne0CUtnTT70pTEpl5SuwPy2Wp800KdTCPqk-B-sWpXiSWoGiyBmSv7VuJLc9sZOiFsp0_3JvdnbX--jNRQujoT3EKn9T621MIRBih6MoR0eLUD9967pnQGPrKv14fvFLiu5mCMsYh3zulY3JBCBzfMxDFBB_ziuVzzvQgPmVQrmVDXC-7.aNrDB8yv9l9W7kduIfUMEgWqiX8mcodHhvMwlxKFMaM&dib_tag=se&keywords=%E2%80%9CWaveshare%2B64x64%2BRGB%2BMatrix%2BP2.5&qid=1783545847&sprefix=%2Caps%2C302&sr=8-1&th=1)) and I used a Raspberry Pi 3 Model B+



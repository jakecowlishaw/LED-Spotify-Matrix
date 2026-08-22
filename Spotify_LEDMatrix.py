import os
import requests
import time
import threading
from requests.auth import HTTPBasicAuth
from PIL import Image, ImageDraw
from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from dotenv import load_dotenv

load_dotenv()

spotifyRefreshToken = os.getenv("spotifyRefreshToken")
spotifyAccessToken = os.getenv("spotifyAccessToken")
clientID = os.getenv("clientID")
clientSecret = os.getenv("clientSecret")

spotifyTokenURL = "https://accounts.spotify.com/api/token"
spotifyGetCurrentTrackURL = "https://api.spotify.com/v1/me/player/currently-playing"

updateTrackInfo = None


def get_JSON_response(inputURL, accessToken):
        response = requests.get(
        inputURL,
        headers = {"Authorization": f"Bearer {accessToken}"}
        )
        return response

def get_current_track(accessToken):
    trackResponce = get_JSON_response(spotifyGetCurrentTrackURL, accessToken)

    if len(trackResponce.content) == 0:
        return None
    
    trackResponseJSON = trackResponce.json()
    
    #the token as expired
    if "error" in trackResponseJSON:
        if refresh_access_token():
            return get_current_track(spotifyAccessToken)
        else:
            print("Failed to refresh token.")
            return None
    
    if(trackResponseJSON['item'] == None):
        return None
    
    isPlaying = trackResponseJSON["is_playing"]
    albumArt = trackResponseJSON['item']['album']['images'][0]['url']
    trackName = trackResponseJSON['item']['name']

    currentTrackInfo = {
        "name": trackName,
        "albumArt": albumArt,
        "isPlaying": isPlaying,

    }
    return currentTrackInfo


def getUpdates():
    global updateTrackInfo
    while True:
        updateTrackInfo = get_current_track(spotifyAccessToken)
        time.sleep(2)


def refresh_access_token():
    global spotifyAccessToken
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": spotifyRefreshToken
    }
    response = requests.post(
        spotifyTokenURL, 
        data = payload, 
        auth = HTTPBasicAuth(clientID, clientSecret)
    )
    
    responseJSON = response.json()    
    if "access_token" in responseJSON:
        spotifyAccessToken = responseJSON.get("access_token")
        print("Token Refreshed")
        return True
    
    return False



def draw_cd(currentAlbumArt):
    #download the and process the image URL  
    downloadImage = requests.get(currentAlbumArt)
    downloadImage = Image.open(BytesIO(downloadImage.content))
    downloadImage = downloadImage.resize((64, 64), Image.LANCZOS)
    downloadImage = downloadImage.convert("RGB")

    #make near black pixels totally black
    pixels = downloadImage.load()
    for x in range(64):
        for y in range(64):
            r, g, b = pixels[x,y]
            if(r < 20 and g < 20 and b < 20):
                pixels[x,y] = (0,0,0)
    
    imageMask = Image.new("L", (64, 64), 0)
    drawMask = ImageDraw.Draw(imageMask)
    #draw the outer CD shape
    drawMask.ellipse((0, 0, 63, 63), fill=255)
    #draw inside CD hole
    center = 32
    innerRadius = 4
    x0 = center - innerRadius
    y0 = x0
    x1 = center + innerRadius
    y1 = x1
    drawMask.ellipse((x0, y0, x1, y1), fill = 0)

    #anywhere there is white the image is visible, black is invisable
    downloadImage.putalpha(imageMask)
    
    outline = ImageDraw.Draw(downloadImage)
    outline.ellipse((0,0,63,63), outline = (30,30,30), width = 1)
    outline.ellipse((x0, y0, x1, y1), outline = (30,30,30), width = 1)

    return downloadImage


def build_matrix():
    matrixOptions = RGBMatrixOptions()
    matrixOptions.rows = 64
    matrixOptions.cols = 64
    matrixOptions.hardware_mapping = "adafruit-hat"
    #improve image quality/flickering
    matrixOptions.gpio_slowdown = 4  
    matrixOptions.pwm_bits = 11    
    matrixOptions.brightness = 80

    return RGBMatrix(options= matrixOptions)



def main():
    prevSong = ""
    rotateDegrees = 0
    cdImage = None
    matrix = build_matrix()
    matrixCanvas = matrix.CreateFrameCanvas()

    threading.Thread(target=getUpdates, daemon = True).start() 

    while True: 
        currentTrackInfo = updateTrackInfo

        if currentTrackInfo != None:
            currentSong = currentTrackInfo['name']
            currentAlbumArt = currentTrackInfo['albumArt']
            

            if(currentSong != prevSong):
                rotateDegrees = 0            
                cdImage = draw_cd(currentAlbumArt)
                prevSong = currentSong

            if(cdImage != None):
                newImage = Image.new("RGB", (64, 64), (0, 0, 0))
                rotatedImage = cdImage.rotate(rotateDegrees)
                newImage.paste(rotatedImage, mask=rotatedImage)
                
                #push the image to the matrix
                matrixCanvas.SetImage(newImage)
                matrixCanvas = matrix.SwapOnVSync(matrixCanvas)

                if(rotateDegrees + 0.75 >= 360):
                    rotateDegrees = 0
                else:
                    rotateDegrees += 0.75


        else:
            blackScreen = Image.new("RGB", (64, 64), (0, 0, 0))
            matrixCanvas.SetImage(blackScreen)
            matrixCanvas = matrix.SwapOnVSync(matrixCanvas)

        time.sleep(0.05)

if __name__ == '__main__':
    main()

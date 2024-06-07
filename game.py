import random
import os
import time
import keyboard
import speech_recognition as sr
import re
import queue 
from os import path
from queue import Queue
q = Queue() 
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "lefte.wav")
# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
# recognize speech using Microsoft Azure Speech
AZURE_SPEECH_KEY = "ce75478025d34093a355ee8889881815"  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
AZURELOCATION = "eastasia"
try:
    text = r.recognize_azure(audio, key=AZURE_SPEECH_KEY, location=AZURELOCATION)
    print("Microsoft Azure Speech thinks you said " + str(text))
except sr.UnknownValueError:
    print("Microsoft Azure Speech could not understand")
except sr.RequestError as e:
    print("Could not request results from Microsoft Azure Speech service; {0}".format(e))
#print(re.findall(r'\b\w+\b', str(text)))
it = re.finditer(r"[\ba-zA-Z]+",str(text)) 
for match in it: 
    print (match.group() )
    if match.group() == 'left'or match.group() == 'Left' or match.group() == 'Neft' or match.group() == 'neft' :
        print("0")
        q.put(0)
    elif match.group() == 'right'or match.group() == 'Right' :
        print("1")
        q.put(1)
print(q.queue)
os.system('pause')

# Game settings
WIDTH = 30
HEIGHT = 20
PLAYER = 'O'
OBSTACLE = 'X'
EMPTY = ' '
LOVE = 'H'
start_time = time.time()
# Initialize player and obstacles
player_pos = WIDTH // 2
obstacles = []
hp = 99
love_pos = [HEIGHT-2, random.randint(0, WIDTH-1)]
# Game loop
while True:
    # Move obstacles
    for j in range(WIDTH-20):
        if random.random() < 0.1:
            obstacles.append([0, random.randint(0, WIDTH-1)])
    for obstacle in obstacles:
        obstacle[0] += 1
        
    # Move love item
    love_pos[0] += 1
    if love_pos[0] == HEIGHT:
        love_pos = [0, random.randint(0, WIDTH-1)]

    # Check for collision with love item
    if love_pos[0] == HEIGHT-1 and love_pos[1] == player_pos:
        hp += 1
        love_pos = [0, random.randint(0, WIDTH-1)]

    # Check for collision with obstacles
    for obstacle in obstacles:
        if obstacle[0] == HEIGHT and obstacle[1] == player_pos:
            hp -= 1
            print("You hit an obstacle! HP:", hp)
            end_time = time.time()
            print("Elapsed time:", gametime, "seconds.")

            if hp == 0:
                print("Game Over! ")
                exit(0)
            response = input("Do you want to continue? (y/n)")
            if response.lower() == 'n':
                print("Game Over!")
                print("Elapsed time:", gametime, "seconds.")

                exit(0)
           
    obstacles = [obstacle for obstacle in obstacles if obstacle[0] < HEIGHT]
    for match in it: 
        print (match.group() )
        if match.group() == 'left'or match.group() == 'Left' :
            player_pos = max(0, player_pos - 1)
        elif match.group() == 'right'or match.group() == 'Right' :
            player_pos = max(0, player_pos - 1)
    # Draw game
    os.system('cls')  # Use 'cls' instead of 'clear' on Windows
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if [i, j] in obstacles:
                print(OBSTACLE, end='')
            elif i == HEIGHT-1 and j == player_pos:
                print(PLAYER, end='')
            elif i == love_pos[0] and j == love_pos[1]:
                print(LOVE, end='')
            else:
                print(EMPTY, end='')
        if i == 0:
            end_time = time.time()
            gametime=round(end_time - start_time, 2)
            print(" TIME: ",gametime)
            print(" HP: " + "H" * hp)
            print("voice:"+str(text))
        print()
    time.sleep(0.1)

    # Move player
    a=-1
    if not q.empty():
        a=q.get_nowait()
    if keyboard.is_pressed('left') or a==0:
        player_pos = max(0, player_pos - 1)
    elif keyboard.is_pressed('right') or a==1:
        player_pos = min(WIDTH - 1, player_pos + 1)


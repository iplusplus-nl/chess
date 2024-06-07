import numpy as np
import Chessboard
import Camera
import Game
import pygame
import Fen as fen
from pygame import mixer

screenSize = (1280, 720)
theta = np.pi * 1.5
phi = np.pi / 6.0
distance = 10.0






def getScreenCoord(camera, point):
    temp = camera.getCoordOnScreen(point)
    return pygame.Vector2(temp[0], temp[1]), temp[2]


# pygame setup
pygame.init()
mixer.init()
mixer.music.load('audio/switch.mp3')
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = np.array([0.0, 0.0, 0.0])
player_rot = np.array([0.0, 0.0, 0.0])

rmbDown = False
lastMousePos = (0, 0)

game = Game.Game(pygame, screen, screenSize)
changed = True

animation = None



def updateCamera(chessboard=None):
        camera = Camera.Camera(
            distance, 
            theta, 
            phi, 
            np.pi / 4.0, 
            screenSize[0] / screenSize[1],
            0.5, 50, 
            screenSize
        )
        if chessboard is None:
            chessboard = Chessboard.Chessboard(8, pygame, screen, camera, getScreenCoord, screenSize)
        else:
            chessboard.camera = camera
            chessboard.screenSize = screenSize
        game.camera = camera
        game.chessboard = chessboard
        return camera, chessboard

camera, chessboard = updateCamera()
hoverPiece = None

detectHover = True


timeout = 303000
timeoutOpponent = 303000

timeSinceLastClock = 0

lastFen = None

while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

         # Handle mouse button events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if animation is None:
                    (detectHover, animation) = game.click(event.pos)
                    changed = True
            if event.button == 3:  # Right mouse button
                rmbDown = True
                lastMousePos = event.pos
            elif event.button == 4:  # Mouse wheel up
                if distance > 8.0:
                    distance -= distance * 0.1
                    camera, chessboard = updateCamera(chessboard)
                    if animation is not None:
                        animation.camera = camera
                    changed = True
            elif event.button == 5:  # Mouse wheel down
                if distance < 24.0:
                    distance += distance * 0.1
                    camera, chessboard = updateCamera(chessboard)
                    if animation is not None:
                        animation.camera = camera
                    changed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                rmbDown = False

        # Handle mouse motion
        elif event.type == pygame.MOUSEMOTION:
            if rmbDown:
                dx, dy = event.rel
                theta -= dx * 0.005 * np.cos(phi*0.8)
                phi += dy * 0.005
                phi = max(np.pi/2 * 0.1, min(np.pi/2 * 0.7, phi))  # Limit pitch to -90 to +90 degrees
                camera, chessboard = updateCamera(chessboard)
                if animation is not None:
                        animation.camera = camera
                changed = True

            if detectHover and animation is None:
                hoverVert = np.array(event.pos)
                hoverPiece = chessboard.getHoverCell(hoverVert)

        elif event.type == pygame.VIDEORESIZE:
            screenSize = event.size
            game.screenSize = screenSize
            camera, chessboard = updateCamera(chessboard)
            if animation is not None:
                animation.camera = camera
            changed = True
            surface = pygame.display.set_mode(screenSize,pygame.RESIZABLE)

    if detectHover:
        if game.computeHeight(hoverPiece):
            changed = True
    
    if animation is not None:
        changed = True

    if timeSinceLastClock > 0.1:

        if chessboard.yourTurn:
            timeout -= 100
        else:
            timeoutOpponent -= 100
        clockTime = int(np.floor(timeout / 1000+0.99))
        chessboard.timeout = clockTime
        clockTime = int(np.floor(timeoutOpponent / 1000+0.99))
        chessboard.timeoutOpponent = clockTime
        changed = True

        timeSinceLastClock = 0

    if changed:
        screen.fill("black")
        chessboard.draw()
        game.draw()
        changed = False



        if animation is not None:
            terminate = animation.draw()
            if terminate:
                game.board = animation.endBoard
                a = fen.getFen(game)
                print(a)
                
                mixer.music.play()
                chessboard.yourTurn = not chessboard.yourTurn
                if chessboard.yourTurn == False:
                    timeout += 3000
                else:
                    timeoutOpponent += 3000

                animation = None
                changed = True

        



    pygame.display.flip()
    dt = clock.tick(60) / 1000
    timeSinceLastClock+=dt

    

pygame.quit()
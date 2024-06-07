import numpy as np



class Animation:
    def __init__(self, screenSize, pygame, screen, camera, sprite, size, startPos, endPos, duration, endBoard):
        self.screenSize = screenSize
        self.pygame = pygame
        self.screen = screen
        self.camera = camera
        self.sprite = sprite
        self.size = size
        self.startPos = startPos
        self.endPos = endPos
        self.duration = duration
        self.startTime = pygame.time.get_ticks()
        self.endBoard = endBoard

    def smoothStep(self, pos1, pos2, x):
        if x < 0:
            x = 0
        if x > 1:
            x = 1

        x = x / 2 + 0.5

        y = x * x * (3.0 - 2.0 * x)

        y = 2 * y - 1

        return np.array([
            pos1[0] + (pos2[0] - pos1[0]) * y,
            pos2[1] + (pos1[1] - pos2[1]) * (1-y),
            pos1[2] + (pos2[2] - pos1[2]) * y
        ])
    
    def getScreenCoord(self, point):
        temp = self.camera.getCoordOnScreen(point)
        return self.pygame.Vector2(temp[0], temp[1]), temp[2]

    def draw(self):
        class Piece:
            def __init__(self, sprite, point, vert, size, angle, depth):
                self.sprite = sprite
                self.point = point
                self.vert = vert
                self.size = size
                self.angle = angle
                self.depth = depth


        pointBottom = self.smoothStep(
            self.startPos,
            self.endPos,
            (self.pygame.time.get_ticks() - self.startTime) / self.duration
        )

        altitude = pointBottom[1]
        pointBottom[1] = 0

        height = self.size / 8
        pointTop = pointBottom + np.array([0, height, 0])
        vertBottom, depthBottom = self.getScreenCoord(pointBottom)
        vertTop, depthTop =self.getScreenCoord(pointTop)
        vertVec = np.array([
            vertTop[0] - vertBottom[0],
            - vertTop[1] + vertBottom[1]
        ])

        piece =Piece(
            self.sprite, 
            pointBottom,
            vertBottom + vertVec.dot(np.array([[1,0],[0,-1]]))*(altitude), 
            1.2*self.screenSize[0]*height/np.linalg.norm(pointBottom-self.camera.position), 
            (np.arctan2(vertVec[1], vertVec[0]) - np.pi/2) % (2*np.pi), 
            (depthBottom + depthTop) / 2)
                    

        sprite = self.pygame.transform.rotate(piece.sprite, piece.angle/np.pi*180)
        sprite = self.pygame.transform.scale(sprite, (int(piece.size), int(piece.size)))
        rect = sprite.get_rect()
        rect.center = piece.vert
        self.screen.blit(sprite, rect)

        #self.pygame.draw.circle(self.screen, self.pygame.Color(255, 0, 0), piece.vert, 3)
        #self.pygame.draw.line(self.screen, self.pygame.Color(255, 0, 0), piece.vert, piece.vert + 50*np.array([np.cos(-piece.angle - np.pi / 2), np.sin(-piece.angle - np.pi / 2)]), 2)
        

        if (self.pygame.time.get_ticks() - self.startTime) > self.duration:
            return True
        return False

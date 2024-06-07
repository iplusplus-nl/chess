import os
import numpy as np
import Animation


class Game:
    altStandard = 0.35
    altElevated = 0.4
    kingMoved = False
    castleKingMoved = False
    castleQueenMoved = False
    enPassant = '-'
    fullMove = 1
    halfMove = 0
    blackCastle = 'kq'



    def __init__(self, pygame, screen, screenSize, size=8):
        self.pygame = pygame
        self.screen = screen
        self.chessboard = None
        self.camera = None
        self.size = size
        self.screenSize = screenSize
        self.origin = np.array([-self.size*3.5/8, 0, -self.size*3.5/8])

        spritesDir = os.getcwd() + '/sprites/'
        filenames = next(os.walk(spritesDir), (None, None, []))[2]

        sprites = {}
        for filename in filenames:
            sprites[filename[:-4]] = pygame.image.load(spritesDir+filename).convert_alpha()
        self.sprites = sprites
    
    board = [
        "RNBQKBNR",
        "PPPPPPPP",
        "        ",
        "        ",
        "        ",
        "        ",
        "pppppppp",
        "rnbqkbnr"
    ]
    angles = [ #0 for looking +x, 1 for 45 degress ccw...
        [6] * 8,
        [6] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [2] * 8,
        [2] * 8
    ]
    heights = [ #from 0 to 20 for animation
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8
    ]

    clickedPiece = None

    altitudeTable = []
    for i in range(21):
        if i > 10:
            altitudeTable.append(altElevated)
        else:
            altitudeTable.append(altElevated*np.sin(i/10*np.pi/2))

    def getPossiblePositions(self, x, z):
        possiblePositions = []
        if self.board[z][x] == 'P':#pawn
            if x > 0 and z < 7:
                if self.board[z+1][x-1].islower():
                    possiblePositions.append([x-1, z+1])
            if x < 7 and z < 7:
                if self.board[z+1][x+1].islower():
                    possiblePositions.append([x+1, z+1])
            if z < 7:
                if self.board[z+1][x] == ' ':
                    possiblePositions.append([x, z+1])
                    if z == 1 and self.board[3][x] == ' ':
                        possiblePositions.append([x, 3])
        elif self.board[z][x] == 'R':#rook
            for i in range(x + 1, 8):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].islower():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(x - 1, -1, -1):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].islower():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(z + 1, 8):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif not self.board[i][x].isupper():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
            for i in range(z - 1, -1, -1):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif not self.board[i][x].isupper():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
        elif self.board[z][x] == 'N':#knight
            for i in range(8):
                for j in range(8):
                    if abs(i-x) + abs(j-z) == 3 and i!=x and j!=z:
                        if self.board[j][i] == ' ' or (self.board[j][i].islower()):
                            possiblePositions.append([i, j])
        elif self.board[z][x] == 'B':#bishop
            for k in range(1, 8):
                i = x + k
                j = z + k
                if i > 7 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z - k
                if i < 0 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z + k
                if i < 0 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x + k
                j = z - k
                if i > 7 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
        elif self.board[z][x] == 'Q':#queen
            for i in range(x + 1, 8):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].islower():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(x - 1, -1, -1):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].islower():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(z + 1, 8):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif self.board[i][x].islower():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
            for i in range(z - 1, -1, -1):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif self.board[i][x].islower():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x + k
                j = z + k
                if i > 7 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z - k
                if i < 0 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z + k
                if i < 0 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x + k
                j = z - k
                if i > 7 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].islower():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
        elif self.board[z][x] == 'K':
            for i in range(8):
                for j in range(8):
                    if (abs(i-x) < 2 and abs(j-z) < 2) and (i != x or j != z):
                        if self.board[j][i] == ' ' or self.board[j][i].islower():
                            possiblePositions.append([i,j])


        self.chessboard.highlights = possiblePositions
        return possiblePositions

        if self.board[z][x] == 'p':#pawn
            if x > 0 and z < 7:
                if self.board[z-1][x-1].isupper():
                    possiblePositions.append([x-1, z-1])
            if x < 7 and z < 7:
                if self.board[z-1][x+1].isupper():
                    possiblePositions.append([x+1, z-1])
            if z < 7:
                if self.board[z-1][x] == ' ':
                    possiblePositions.append([x, z-1])
                    if z == 6 and self.board[4][x] == ' ':
                        possiblePositions.append([x, 4])
        elif self.board[z][x] == 'r':#rook
            for i in range(x + 1, 8):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].isupper():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(x - 1, -1, -1):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].isupper():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(z + 1, 8):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif self.board[i][x].isupper():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
            for i in range(z - 1, -1, -1):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif self.board[i][x].isupper():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
        elif self.board[z][x] == 'n':#knight
            for i in range(8):
                for j in range(8):
                    if abs(i-x) + abs(j-z) == 3 and i!=x and j!=z:
                        if self.board[j][i] == ' ' or (self.board[j][i].isupper()):
                            possiblePositions.append([i, j])
        elif self.board[z][x] == 'b':#bishop
            for k in range(1, 8):
                i = x + k
                j = z + k
                if i > 7 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z - k
                if i < 0 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z + k
                if i < 0 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x + k
                j = z - k
                if i > 7 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
        elif self.board[z][x] == 'q':#queen
            for i in range(x + 1, 8):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].isupper():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(x - 1, -1, -1):
                if self.board[z][i] == ' ':
                    possiblePositions.append([i, z])
                elif self.board[z][i].isupper():
                    possiblePositions.append([i, z])
                    break
                else:
                    break
            for i in range(z + 1, 8):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif self.board[i][x].isupper():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
            for i in range(z - 1, -1, -1):
                if self.board[i][x] == ' ':
                    possiblePositions.append([x, i])
                elif self.board[i][x].isupper():
                    possiblePositions.append([x, i])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x + k
                j = z + k
                if i > 7 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z - k
                if i < 0 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x - k
                j = z + k
                if i < 0 or j > 7:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
            for k in range(1, 8):
                i = x + k
                j = z - k
                if i > 7 or j < 0:
                    break
                if self.board[j][i] == ' ':
                    possiblePositions.append([i, j])
                elif self.board[j][i].isupper():
                    possiblePositions.append([i, j])
                    break
                else:
                    break
        elif self.board[z][x] == 'k':
            for i in range(8):
                for j in range(8):
                    if (abs(i-x) < 2 and abs(j-z) < 2) and (i != x or j != z):
                        if self.board[j][i] == ' ' or self.board[j][i].isupper():
                            possiblePositions.append([i,j])


        self.chessboard.highlights = possiblePositions
        return possiblePositions

    def computeHeight(self, hoveredPiece):
        changed = False
        for z in range(8):
            for x in range(8):
                if [x, z] == hoveredPiece and self.board[z][x] != " " and (self.board[z][x].isupper()):
                    if self.heights[z][x] < 20:
                        changed = True
                        self.heights[z][x] += 1  
                        if self.heights[z][x] >= 10: #now you have vision
                            possiblePositions = self.getPossiblePositions(x, z)
                            self.chessboard.highlights = possiblePositions
                            
                else:
                    if self.heights[z][x] > 0:
                        changed = True
                        if self.heights[z][x] >= 10:
                            self.heights[z][x] = 10
                            self.chessboard.highlights = []
                        self.heights[z][x] -= 1

        return changed
                        

    def getScreenCoord(self, point):
        temp = self.camera.getCoordOnScreen(point)
        return self.pygame.Vector2(temp[0], temp[1]), temp[2]

    def draw(self):
        class Piece:
            def __init__(self, sprite, point, vert, size, angle, depth, sizeY):
                self.sprite = sprite
                self.point = point
                self.vert = vert
                self.size = size
                self.angle = angle
                self.depth = depth
                self.sizeY = sizeY
                
        pieces = []
        for y in range(8):
            for x in range(8):
                if self.board[y][x] != " ":
                    height = self.size / 8
                    pointBottom = self.origin + np.array([x*self.size/8, 0, y*self.size/8])
                    pointTop = pointBottom + np.array([0, height, 0])
                    vertBottom, depthBottom = self.getScreenCoord(pointBottom)
                    vertTop, depthTop =self.getScreenCoord(pointTop)
                    spriteName = ''
                    if self.board[y][x].isupper():
                        spriteName += '_'
                    spriteName += self.board[y][x].lower()+'-'

                    viewAngle = str(int(np.round((self.angles[y][x]*45 - self.camera.theta/np.pi*180)/45.0 + 90) % 8 * 45))
                    spriteName += viewAngle
                    

                    vertVec = np.array([
                        vertTop[0] - vertBottom[0],
                        - vertTop[1] + vertBottom[1]
                    ])

                    pieces.append(Piece(
                        self.sprites[spriteName], 
                        pointBottom,
                        vertBottom + vertVec.dot(np.array([[1,0],[0,-1]]))*(self.altStandard + self.altitudeTable[self.heights[y][x]]), 
                        1.2*self.screenSize[0]*height/np.linalg.norm(pointBottom-self.camera.position), 
                        (np.arctan2(vertVec[1], vertVec[0]) - np.pi/2) % (2*np.pi), 
                        (depthBottom + depthTop) / 2,
                        1.2 *np.linalg.norm(vertTop - vertBottom) * self.screenSize[0] / self.screenSize[1]
                    ))
                    
        pieces.sort(key=lambda x: x.depth, reverse=True)
        for piece in pieces:
            sprite = self.pygame.transform.rotate(piece.sprite, piece.angle/np.pi*180)
            sprite = self.pygame.transform.scale(sprite, (int(piece.size), int(piece.size)))#if you change it to sizeY, it will not work
            rect = sprite.get_rect()
            rect.center = piece.vert
            self.screen.blit(sprite, rect)
            
            #self.pygame.draw.circle(self.screen, self.pygame.Color(255, 0, 0), piece.vert, 3)
            #self.pygame.draw.line(self.screen, self.pygame.Color(255, 0, 0), piece.vert, piece.vert + 50*np.array([np.cos(-piece.angle - np.pi / 2), np.sin(-piece.angle - np.pi / 2)]), 2)

    def click(self, pos):
        coord = self.chessboard.getHoverCell(pos)
        if coord == None:
            return (True, None) # still check for hover
        
        if self.clickedPiece == None:
            possiblePositions = self.getPossiblePositions(coord[0], coord[1])
            if possiblePositions == []:
                return (True, None)
            self.clickedPiece = coord
            self.hoveredPiece = coord
            self.heights[coord[1]][coord[0]] = 20
            self.chessboard.highlights = possiblePositions
            return (False, None)
        elif coord == self.clickedPiece:
            #self.clickedPiece = None
            #self.chessboard.highlights = []
            return (False, None)
        else:
            if coord in self.chessboard.highlights:
                
                #self.fullMove += 2
                self.halfMove += 1

                if self.board[self.clickedPiece[1]][self.clickedPiece[0]] == 'P':
                    self.halfMove = 0
                if self.board[coord[1]][coord[0]] != ' ': 
                    self.halfMove = 0

                if not self.castleQueenMoved and self.clickedPiece == [0, 0]:
                    self.castleQueenMoved = True

                if not self.castleKingMoved and self.clickedPiece == [7, 0]:
                    self.castleKingMoved = True

                if not self.kingMoved and self.clickedPiece == [4, 0]:
                    self.kingMoved = True

                if self.board[self.clickedPiece[1]][self.clickedPiece[0]] == 'P' and self.clickedPiece[1] == 1 and coord[1] == 3:
                    self.enPassant = chr(ord('a') + coord[0]) + '3'
                else:
                    self.enPassant = '-'

                newStr = ''
                
                for i in range(8):
                    newStr += " " if i == self.clickedPiece[0] else self.board[self.clickedPiece[1]][i]
                
                newBoard = self.board.copy()
                newBoard[self.clickedPiece[1]] = newStr
                newStr2 = ''
                for i in range(8):
                    newStr2 += self.board[self.clickedPiece[1]][self.clickedPiece[0]] if i == coord[0] else newBoard[coord[1]][i]
            
                for i in range(8):
                    if coord[1] == 7 and newStr2[i] == 'P':
                        newStr2 = newStr2[:i] + 'Q' + newStr2[i+1:]
                newBoard[coord[1]] = newStr2

                spriteName = ''
                if self.board[self.clickedPiece[1]][self.clickedPiece[0]].isupper():
                    spriteName = '_'
                spriteName += (self.board[self.clickedPiece[1]][self.clickedPiece[0]]).lower()+'-'
                
                nextAngle = (int((np.round((np.rad2deg(np.arctan2(coord[1]-self.clickedPiece[1], coord[0]-self.clickedPiece[0])))-90)/45.0 + 90) + 4) % 8)
                
                newAngles = self.angles.copy()
                newAngleStr = self.angles[coord[1]]
                newAngleStr[coord[0]] = nextAngle
                self.angles = newAngles

                viewAngle = str(int(np.round((nextAngle*45 - self.camera.theta/np.pi*180)/45.0 + 90) % 8 * 45))
                spriteName += viewAngle

                animation = Animation.Animation(
                    self.screenSize,
                    self.pygame,
                    self.screen,
                    self.camera,
                    self.sprites[spriteName],
                    self.size,
                    self.origin + np.array([self.clickedPiece[0]*self.size/8, self.altStandard + self.altElevated, self.clickedPiece[1]*self.size/8]),
                    self.origin + np.array([coord[0]*self.size/8, self.altStandard, coord[1]*self.size/8]),
                    500,
                    newBoard
                )

                self.board[self.clickedPiece[1]] = newStr
                self.clickedPiece = None
                self.chessboard.highlights = []
                
                return (True, animation)
            return (False, None)
            
            
            

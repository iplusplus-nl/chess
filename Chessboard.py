import numpy as np


def normalize(v):
    return v / np.linalg.norm(v)

class Chessboard:
    clickVerts = None
    highlights = []
    clockTexts = []
    yourTurn = True
    timeout = 0
    timeoutOpponent = 0
    

    def __init__(self, size, pygame, screen, camera, getScreenCoord, screenSize):
        self.size = size
        self.getScreenCoord = getScreenCoord
        self.pygame = pygame
        self.screen = screen
        self.camera = camera
        self.screenSize = screenSize
        origin = np.array([-size/2, 0, -size/2])
        self.points = []
        for z in range(9):
            row = []
            for x in range(9):
                row.append(origin + np.array([x*size/8, 0, z*size/8]))
            self.points.append(row)
        for t in range(600):
            temp = pygame.font.Font(None, 32).render(str(t // 60) + ':' + ((str(t % 60)) if t%60 > 9 else '0'+ str(t%60)) , False, "red")
            heightReq = temp.get_width() /2
            temp = pygame.transform.scale_by(temp, (1, heightReq/temp.get_height() ))
            self.clockTexts.append(temp)


    def draw(self):
        #draw cells
        verts = []
        pointsEdges = []
        for z in range(9):
            row = []
            for x in range(9):
                row.append(self.getScreenCoord(self.camera, self.points[z][x])[0])
            verts.append(row)
        for z in range(8):
            for x in range(8):
                self.pygame.draw.polygon(self.screen, self.pygame.Color(180, 170, 160) if (x+z) % 2 == 1 else self.pygame.Color(80, 70, 60), [verts[z][x], verts[z+1][x], verts[z+1][x+1], verts[z][x+1]])
        pointsEdges.append([verts[0][0], verts[0][8], verts[8][8], verts[8][0]])

       
        

        #draw borders
        border = self.size / 50
        height = self.size / 50
        pointsTop = [
            self.points[0][0], 
            self.points[0][0] + np.array([0, 0, -border]),
            self.points[0][8] + np.array([border, 0, -border]),
            self.points[0][8] + np.array([border, 0, 0]),
        ]
        pointsSide = [
            self.points[0][0] + np.array([-border, 0, -border]),
            self.points[0][0] + np.array([-border, -height, -border]),
            self.points[0][8] + np.array([border, -height, -border]),
            self.points[0][8] + np.array([border, 0, -border]),
        ]

        rotationMatrix = [
            np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]),
            np.array([
                [0, 0, -1],
                [0, 1, 0],
                [1, 0, 0]
            ]),
            np.array([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, -1]
            ]),
            np.array([
                [0, 0, 1],
                [0, 1, 0],
                [-1, 0, 0]
            ])
        ]

        
        for i in range(4):
            verts = []
            for point in pointsTop:
                verts.append(self.getScreenCoord(self.camera, point.dot(rotationMatrix[i]))[0])
            self.pygame.draw.polygon(self.screen, self.pygame.Color(70, 60, 50), verts)

        for i in range(4):
            pointsSideRotated = []
            for point in pointsSide:
                pointsSideRotated.append(point.dot(rotationMatrix[i]))
            normal = normalize(np.cross(pointsSideRotated[1] - pointsSideRotated[0], pointsSideRotated[2] - pointsSideRotated[0]))
            if normal.dot(self.camera.w) < 0:
                continue
            if normal.dot(pointsSideRotated[0]) < normal.dot(self.camera.position):
                continue
            verts = []
            for point in pointsSide:
                verts.append(self.getScreenCoord(self.camera, point.dot(rotationMatrix[i]))[0])
            
            brightness = np.abs(normal.dot(self.camera.w))
            brightness = 1 - 0.5 * brightness
            color = np.array([75, 60, 45]) * brightness
            self.pygame.draw.polygon(self.screen, color, verts)
            pointsEdges.append(verts)
            
        for pointsEdge in pointsEdges:
            self.pygame.draw.polygon(self.screen, "black", pointsEdge, 1)
    
        #draw clock
        #https://www.reddit.com/r/pygame/comments/z571pa/this_is_how_you_can_texture_a_polygon/

        def lerp(a, b, t):
            return a + (b - a) * t
        
        def lerp2( a, b, t ):
            return np.array([lerp(a[0], b[0], t), lerp(a[1], b[1], t)])

        def drawQuad(polygon, img):
            points = dict()
            for i in range(img.get_height()+1):
                b = lerp2(polygon[1], polygon[2], i/img.get_height())
                c = lerp2(polygon[0], polygon[3], i/img.get_height())
                for j in range(img.get_width()+1):
                    a = lerp2(c, b, j/img.get_width())
                    points[(j, i)] = a
            for i in range(img.get_width()):
                for j in range(img.get_height()):
                    color = img.get_at((i, j))
                    if color[0] == 0:
                        color = (31, 0, 31, 0)
                    self.pygame.draw.polygon(
                        self.screen, 
                        color, 
                        [
                            points[(i, j)], 
                            points[(i, j+1)], 
                            points[(i+1, j+1)], 
                            points[(i+1, j)]
                        ]
                    )

        def drawClockSurface(polygonPoints, reversed=False):
            normal = normalize(np.cross(polygonPoints[1] - polygonPoints[0], polygonPoints[3] - polygonPoints[0]))
            if reversed:
                normal = -normal
            if normal.dot(polygonPoints[0]) > normal.dot(self.camera.position):
                brightness = np.abs(normal.dot(self.camera.w))
                brightness = 1 - 0.5 * brightness
                color = np.array([100, 100, 100]) * brightness
                self.pygame.draw.polygon(self.screen, color, [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints])
                self.pygame.draw.polygon(self.screen, "black", [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints], 1)
        
        def drawSwitchSurface(polygonPoints, reversed=False):
            normal = normalize(np.cross(polygonPoints[1] - polygonPoints[0], polygonPoints[3] - polygonPoints[0]))
            if reversed:
                normal = -normal
            if normal.dot(polygonPoints[0]) > normal.dot(self.camera.position):
                brightness = np.abs(normal.dot(self.camera.w))
                brightness = 1 - 0.5 * brightness
                color = np.array([200, 200, 200]) * brightness
                self.pygame.draw.polygon(self.screen, color, [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints])
                self.pygame.draw.polygon(self.screen, "black", [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints], 1)
        
        clockRight = -4.5
        clockScreenHeight = 1
        clockMiddleBorder = 0.1
        cloudScreenOuter = 2.1
        clockX = 1.6
        screenBorder = 0.1

        polygonPoints = [
            np.array([clockRight, clockScreenHeight+height, -cloudScreenOuter-height]),#top left
            np.array([clockRight, clockScreenHeight+height, cloudScreenOuter+height]),#top right
            np.array([clockRight, -height, cloudScreenOuter+height]),#bottom right
            np.array([clockRight, -height, -cloudScreenOuter-height])#bottom left
        ]

        normal = -normalize(np.cross(polygonPoints[1] - polygonPoints[0], polygonPoints[3] - polygonPoints[0]))
        if normal.dot(polygonPoints[0]) > normal.dot(self.camera.position):
            brightness = np.abs(normal.dot(self.camera.w))
            brightness = 1 - 0.5 * brightness
            color = np.array([100, 100, 100]) * brightness

            self.pygame.draw.polygon(self.screen, color, [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints])
    
            polygonPoints = [
                np.array([clockRight, clockScreenHeight, clockMiddleBorder]),#top left
                np.array([clockRight, clockScreenHeight, cloudScreenOuter]),#top right
                np.array([clockRight, 0, cloudScreenOuter]),#bottom right
                np.array([clockRight, 0, clockMiddleBorder])#bottom left
            ]
            self.pygame.draw.polygon(self.screen, np.array([31, 0, 31]), [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints])
            self.pygame.draw.polygon(self.screen, "black", [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints], 1)

            polygonPoints = [
                np.array([clockRight, clockScreenHeight-screenBorder, clockMiddleBorder+screenBorder]),#top left
                np.array([clockRight, clockScreenHeight-screenBorder, cloudScreenOuter-screenBorder]),#top right
                np.array([clockRight, screenBorder, cloudScreenOuter-screenBorder]),#bottom right
                np.array([clockRight, screenBorder, clockMiddleBorder+screenBorder])#bottom left
            ]

            polygonVerts= []
            for point in polygonPoints:
                polygonVerts.append(self.getScreenCoord(self.camera, point)[0])
            drawQuad(polygonVerts, self.clockTexts[self.timeoutOpponent])

            polygonPoints = [
                np.array([clockRight, clockScreenHeight, -cloudScreenOuter]),#top left
                np.array([clockRight, clockScreenHeight, -clockMiddleBorder]),#top right
                np.array([clockRight, 0, -clockMiddleBorder]),#bottom right
                np.array([clockRight, 0, -cloudScreenOuter])#bottom left
            ]
            self.pygame.draw.polygon(self.screen, np.array([31, 0, 31]), [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints])
            self.pygame.draw.polygon(self.screen, "black", [self.getScreenCoord(self.camera, point)[0] for point in polygonPoints], 1)

            polygonPoints = [
                np.array([clockRight, clockScreenHeight-screenBorder, -cloudScreenOuter+screenBorder]),#top left
                np.array([clockRight, clockScreenHeight-screenBorder, -clockMiddleBorder-screenBorder]),#top right
                np.array([clockRight, screenBorder, -clockMiddleBorder-screenBorder]),#bottom right
                np.array([clockRight, screenBorder, -cloudScreenOuter+screenBorder])#bottom left
            ]

            polygonVerts= []
            for point in polygonPoints:
                polygonVerts.append(self.getScreenCoord(self.camera, point)[0])
            drawQuad(polygonVerts, self.clockTexts[self.timeout])

        #draw clock -z
        polygonPoints = [
            np.array([clockRight - clockX, clockScreenHeight+height, -cloudScreenOuter-height]),#top left
            np.array([clockRight, clockScreenHeight+height, -cloudScreenOuter-height]),#top right
            np.array([clockRight, 0-height, -cloudScreenOuter-height]),#bottom right
            np.array([clockRight - clockX, 0-height, -cloudScreenOuter-height])#bottom left
        ]
        drawClockSurface(polygonPoints, True)

        #draw clock +z
        polygonPoints = [
            np.array([clockRight - clockX, clockScreenHeight+height, cloudScreenOuter+height]),#top left
            np.array([clockRight, clockScreenHeight+height, cloudScreenOuter+height]),#top right
            np.array([clockRight, 0-height, cloudScreenOuter+height]),#bottom right
            np.array([clockRight - clockX, 0-height, cloudScreenOuter+height])#bottom left
        ]
        drawClockSurface(polygonPoints, False)

        #draw clock -x
        polygonPoints = [
            np.array([clockRight - clockX, clockScreenHeight+height, -cloudScreenOuter-height]),#top left
            np.array([clockRight - clockX, clockScreenHeight+height, cloudScreenOuter+height]),#top right
            np.array([clockRight - clockX, -height, cloudScreenOuter+height]),#bottom right
            np.array([clockRight - clockX, -height, -cloudScreenOuter-height])#bottom left
        ]
        drawClockSurface(polygonPoints, False)

        #draw clock +y
        polygonPoints = [
            np.array([clockRight - clockX, clockScreenHeight+height, -cloudScreenOuter-height]),#top left
            np.array([clockRight - clockX, clockScreenHeight+height, cloudScreenOuter+height]),#top right
            np.array([clockRight, clockScreenHeight+height, cloudScreenOuter+height]),#bottom right
            np.array([clockRight, clockScreenHeight+height, -cloudScreenOuter-height])#bottom left
        ]
        drawClockSurface(polygonPoints, True)

        #draw switch
        polygonPoints = [
            np.array([clockRight - clockX + height, clockScreenHeight+height, -cloudScreenOuter + height]),#top left
            np.array([clockRight - clockX + height, clockScreenHeight+height, cloudScreenOuter - height]),#top right
            np.array([clockRight - height, clockScreenHeight+height, cloudScreenOuter - height]),#bottom right
            np.array([clockRight - height, clockScreenHeight+height, -cloudScreenOuter + height])#bottom left
        ]
        drawSwitchSurface(polygonPoints, True)

        if self.yourTurn:
            polygonPoints = [
                np.array([clockRight - clockX + height, clockScreenHeight+height + height *1.5, -cloudScreenOuter + height + height * 0.2]),#top left
                np.array([clockRight - clockX + height, clockScreenHeight+height, 0]),#top right
                np.array([clockRight - height, clockScreenHeight+height, 0]),#bottom right
                np.array([clockRight - height, clockScreenHeight+height + height * 1.5, -cloudScreenOuter + height + height * 0.2])#bottom left
            ]
            drawSwitchSurface(polygonPoints, True)

            polygonPoints = [
                np.array([clockRight - height, clockScreenHeight+height + height *1.5, -cloudScreenOuter + height + height * 0.2]),#top left
                np.array([clockRight - clockX + height, clockScreenHeight+height + height *1.5, -cloudScreenOuter + height + height * 0.2]),#top right
                np.array([clockRight - clockX + height, clockScreenHeight+height, -cloudScreenOuter + height]),#bottom right
                np.array([clockRight - height, clockScreenHeight+height, -cloudScreenOuter + height])#bottom left
            ]
            drawSwitchSurface(polygonPoints, False)

            polygonPoints = [
                np.array([clockRight - height, clockScreenHeight+height + height *1.5, -cloudScreenOuter + height + height * 0.2]),#top left
                np.array([clockRight - height, clockScreenHeight+height, 0]),#top right
                np.array([clockRight - height, clockScreenHeight+height, 0]),#bottom right
                np.array([clockRight - height, clockScreenHeight+height, -cloudScreenOuter + height])#bottom left
            ]
            drawSwitchSurface(polygonPoints, True)

            polygonPoints = [
                np.array([clockRight - clockX + height, clockScreenHeight+height + height *1.5, -cloudScreenOuter + height + height * 0.2]),#top left
                np.array([clockRight - clockX + height, clockScreenHeight+height, 0]),#top right
                np.array([clockRight - clockX + height, clockScreenHeight+height, 0]),#bottom right
                np.array([clockRight - clockX + height, clockScreenHeight+height, -cloudScreenOuter + height])#bottom left
            ]
            drawSwitchSurface(polygonPoints, False)
        else: 
            polygonPoints = [
                np.array([clockRight - clockX + height, clockScreenHeight+height + height *1.5, cloudScreenOuter - height - height * 0.2]),#top left
                np.array([clockRight - clockX + height, clockScreenHeight+height, 0]),#top right
                np.array([clockRight - height, clockScreenHeight+height, 0]),#bottom right
                np.array([clockRight - height, clockScreenHeight+height + height * 1.5, cloudScreenOuter - height - height * 0.2])#bottom left
            ]
            drawSwitchSurface(polygonPoints, False)

            polygonPoints = [
                np.array([clockRight - height, clockScreenHeight+height + height *1.5, cloudScreenOuter - height - height * 0.2]),#top left
                np.array([clockRight - clockX + height, clockScreenHeight+height + height *1.5, cloudScreenOuter - height - height * 0.2]),#top right
                np.array([clockRight - clockX + height, clockScreenHeight+height, cloudScreenOuter - height]),#bottom right
                np.array([clockRight - height, clockScreenHeight+height, cloudScreenOuter - height])#bottom left
            ]
            drawSwitchSurface(polygonPoints, True)

            polygonPoints = [
                np.array([clockRight - height, clockScreenHeight+height + height *1.5, cloudScreenOuter - height - height * 0.2]),#top left
                np.array([clockRight - height, clockScreenHeight+height, 0]),#top right
                np.array([clockRight - height, clockScreenHeight+height, 0]),#bottom right
                np.array([clockRight - height, clockScreenHeight+height, cloudScreenOuter - height])#bottom left
            ]
            drawSwitchSurface(polygonPoints, False)

            polygonPoints = [
                np.array([clockRight - clockX + height, clockScreenHeight+height + height *1.5, cloudScreenOuter - height - height * 0.2]),#top left
                np.array([clockRight - clockX + height, clockScreenHeight+height, 0]),#top right
                np.array([clockRight - clockX + height, clockScreenHeight+height, 0]),#bottom right
                np.array([clockRight - clockX + height, clockScreenHeight+height, cloudScreenOuter - height])#bottom left
            ]
            drawSwitchSurface(polygonPoints, True)
        





                #draw cells with 0.2 +y, for users to click there to move a piece
        self.clickVerts = []
        for z in range(9):
            row = []
            for x in range(9):
                row.append(self.getScreenCoord(self.camera, self.points[z][x] + np.array([0, 0.2, 0]))[0])
            self.clickVerts.append(row)
        
        for z in range(8):
            for x in range(8):
                for highlight in self.highlights:
                    if [x, z] == highlight:
                        verts = [self.clickVerts[z][x], self.clickVerts[z+1][x], self.clickVerts[z+1][x+1], self.clickVerts[z][x+1]]
                        avg = np.mean(verts, axis=0)
                        scale = 0.7
                        verts = [avg + scale*(vert - avg) for vert in verts]
                        diff = 0
                        for vert in verts:
                            diff += np.linalg.norm(vert - avg)

                        lines = [
                            [verts[0], verts[0] * 0.8 + verts[1] * 0.2],
                            [verts[1], verts[0] * 0.2 + verts[1] * 0.8],
                            [verts[1], verts[1] * 0.8 + verts[2] * 0.2],
                            [verts[2], verts[1] * 0.2 + verts[2] * 0.8],
                            [verts[2], verts[2] * 0.8 + verts[3] * 0.2],
                            [verts[3], verts[2] * 0.2 + verts[3] * 0.8],
                            [verts[3], verts[3] * 0.8 + verts[0] * 0.2],
                            [verts[0], verts[3] * 0.2 + verts[0] * 0.8]
                        ]

                        
                        for line in lines:
                            self.pygame.draw.line(self.screen, "white", line[0], line[1], round(diff / 40))
                            self.pygame.draw.circle(self.screen, "white", line[0], round(diff / 80))
                            self.pygame.draw.circle(self.screen, "white", line[1], round(diff / 80))



    def getHoverCell(self, hoverVert):
        if self.clickVerts is None:
            return None
        
        def inPolygon(point, points):
            inside = False
            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i+1) % len(points)]
                if (y1 < point[1] and y2 >= point[1] or y2 < point[1] and y1 >= point[1]) and (x1 <= point[0] or x2 <= point[0]):
                    if x1 + (point[1] - y1) / (y2 - y1) * (x2 - x1) < point[0]:
                        inside = not inside
            return inside
        
        for j in range(2):
            for i in range(2):
                if inPolygon(hoverVert, [
                    self.clickVerts[j*4][i*4],
                    self.clickVerts[j*4][i*4+4],
                    self.clickVerts[j*4+4][i*4+4],
                    self.clickVerts[j*4+4][i*4]
                ]):
                    x, z = i*4, j*4
                    for j in range(2):
                        for i in range(2):
                            if inPolygon(hoverVert, [
                                self.clickVerts[z+j*2][x+i*2],
                                self.clickVerts[z+j*2][x+i*2+2],
                                self.clickVerts[z+j*2+2][x+i*2+2],
                                self.clickVerts[z+j*2+2][x+i*2]
                            ]):
                                x, z = x+i*2, z+j*2
                                for j in range(2):
                                    for i in range(2):
                                        if inPolygon(hoverVert, [
                                            self.clickVerts[z+j][x+i],
                                            self.clickVerts[z+j][x+i+1],
                                            self.clickVerts[z+j+1][x+i+1],
                                            self.clickVerts[z+j+1][x+i]
                                        ]):
                                            x, z = x+i, z+j
                                            return [x, z]
                                        
        return None

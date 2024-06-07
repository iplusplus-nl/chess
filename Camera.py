import numpy as np


def normalize(v):
    return v / np.linalg.norm(v)

class Camera:

    def __init__(self, d, theta, phi, fov, aspect, near, far, screenSize):
        self.theta = theta
        
        self.position = np.array([
            d * np.cos(phi) * np.cos(theta),
            d * np.sin(phi),
            d * np.cos(phi) * np.sin(theta)
        ])

        u = normalize(np.array([[0, 1], [-1, 0]]).dot(normalize(np.array([self.position[0], self.position[2]]))))
        u = -np.array([u[0], 0, u[1]])
        self.u = u
        v = np.array([
            [0, -u[2], u[1]],
            [u[2], 0, -u[0]],
            [-u[1], u[0], 0]
        ]).dot(-normalize(self.position))
        self.v = np.array([
            [0, -self.u[2], self.u[1]],
            [self.u[2], 0, -self.u[0]],
            [-self.u[1], self.u[0], 0]
        ]).dot(normalize(self.position))
        w = np.cross(u, v)
        self.w = np.cross(self.u, self.v)
        
        #https://skannai.medium.com/projecting-3d-points-into-a-2d-screen-58db65609f24
        #https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/orthographic-projection-matrix.html
        #https://ogldev.org/www/tutorial12/tutorial12.html

        R = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ]).dot(np.array([
            [np.cos(phi), -np.sin(phi), 0],
            [np.sin(phi), np.cos(phi), 0],
            [0, 0, 1]
        ]))
        
        Mcam = np.array([
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [w[0], w[1], w[2], 0],
            [0, 0, 0, 1]
        ]).dot(np.array([
            [1, 0, 0, -self.position[0]],
            [0, 1, 0, -self.position[1]],
            [0, 0, 1, -self.position[2]],
            [0, 0, 0, 1]
        ]))

        scale = np.tan(fov / 2.0)
        r = aspect * scale * near
        l = -r
        t = scale * near
        b = -t

        Mper = np.array([
            [2*near/(r-l), 0, (r+l)/(r-l), 0],
            [0, 2*near/(t-b), (t+b)/(t-b), 0],
            [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
            [0, 0, -1, 0]
        ])

        Mvp = np.array([
            [screenSize[0]/2, 0, 0, (screenSize[0]-1)/2],
            [0, screenSize[1]/2, 0, (screenSize[1]-1)/2],
            [0, 0, 0.5, 0.5],
        ])

        self.Mvp = Mvp
        self.Mper = Mper
        self.Mcam = Mcam


    def getCoordOnScreen(self, point):
        point_after_CM = self.Mcam.dot(np.array([point[0], point[1], point[2], 1]))
        point_after_per = (self.Mper.dot(point_after_CM))
        point_after_per = point_after_per / point_after_per[3]
        point_after_vp = self.Mvp.dot(point_after_per)
        return point_after_vp
import numpy as np
import random
from PIL import Image, ImageDraw

class cube:

    def __init__(self) -> None:

        #########################################################
        ##  COLORES:   0  =  NULO                              ##
        ##             1  =  BLANCO                            ##
        ##             2  =  AMARILLO                          ##
        ##             3  =  ROJO                              ##
        ##             4  =  NARANJA                           ##
        ##             5  =  AZUL                              ##
        ##             6  =  VERDE                             ##
        #########################################################
        ## -  0    -   1    -    2   -    3   -   4   -   5  - ##
        ## SUPERIOR INFERIOR IZQUIERDA FRONTAL DERECHA TRASERA ##
        #########################################################

        #########################################################
        ##                                                     ##
        ##                   ###############                   ##
        ##                   #             #                   ##
        ##                   #  SUPERIOR   #                   ##
        ##                   #   BLANCA    #                   ##
        ##                   #             #                   ##
        ##                   #             #                   ##
        ##                   #             #                   ##
        ##     ##########################################      ##
        ##     #             #             #            #      ##
        ##     #  IZQUIERDA  #   FRONTAL   #  DERECHA   #      ##
        ##     #    ROJA     #    AZUL     #  NARANJA   #      ##
        ##     #             #             #            #      ##
        ##     #             #             #            #      ##
        ##     ##########################################      ##
        ##                   #             #                   ##
        ##                   #             #                   ##
        ##                   #  INFERIOR   #                   ##
        ##                   #  AMARILLA   #                   ##
        ##                   #             #                   ##
        ##                   #             #                   ##
        ##                   ###############                   ##
        ##                   #             #                   ##
        ##                   #             #                   ##
        ##                   #   TRASERA   #                   ##
        ##                   #    VERDE    #                   ##
        ##                   #             #                   ##
        ##                   #             #                   ##
        ##                   ###############                   ##
        ##                                                     ##
        #########################################################

        self.cube = np.array([
            [[(1,0,3,5,0,0),(1,0,3,0,0,0),(1,0,3,0,0,6)],    [(1,0,0,5,0,0),(1,0,0,0,0,0),(1,0,0,0,0,6)],    [(1,0,0,5,4,0),(1,0,0,0,4,0),(1,0,0,0,4,6)]],
            [[(0,0,3,5,0,0),(0,0,3,0,0,0),(0,0,3,0,0,6)],    [(0,0,0,5,0,0),(0,0,0,0,0,0),(0,0,0,0,0,6)],    [(0,0,0,5,4,0),(0,0,0,0,4,0),(0,0,0,0,4,6)]],
            [[(0,2,3,5,0,0),(0,2,3,0,0,0),(0,2,3,0,0,6)],    [(0,2,0,5,0,0),(0,2,0,0,0,0),(0,2,0,0,0,6)],    [(0,2,0,5,4,0),(0,2,0,0,4,0),(0,2,0,0,4,6)]]
        ],dtype=object)
        self.solved_cube = np.copy(self.cube)

        self.img = Image.new('RGB', (415,312), color = 'black')
        self.draw = ImageDraw.Draw(self.img)
        self.frame_count = 0
    
    def get_faces(self,ml = False):
        if not ml:
            backup_cube = np.copy(self.cube)
            down = np.flip(np.flip(np.rot90(backup_cube[2,:,:])),axis=1)
            for index0, linea in enumerate(down):
                for index1, pieza in enumerate(linea):
                    down[index0][index1] = np.flip(pieza) #esto esta medio raro pero no encontré otra forma :(
            return {
                "frontal": self.cube[:,:,0],
                "left": np.flip(self.cube[:,0,:],axis=1),
                "right":self.cube[:,2,:],
                "up": np.rot90(self.cube[0,:,:]),
                "down": down,
                "back": np.flip(self.cube[:,:,2],axis=1),
            }
        elif ml:
            return self.cube
    def rotate_piece(self,pa,sentido,lado):
        # SE MANTIENEN SUPERIOR E INFERIOR
        if sentido == "UD":
            if lado == -90:
                return (pa[0],pa[1],pa[3],pa[4],pa[5],pa[2])
            if lado == 90:
                return (pa[0],pa[1],pa[5],pa[2],pa[3],pa[4])
        # SE MANTIENEN IZQUIERDA Y DERECHA
        if sentido == "LR":
            if lado == -90:
                return (pa[3],pa[5],pa[2],pa[1],pa[4],pa[0])
            if lado == 90:
                return (pa[5],pa[3],pa[2],pa[0],pa[4],pa[1])
        # SE MANTIENEN FRONTAL Y TRASERA
        if sentido == "FB":
            if lado == -90:
                return (pa[4],pa[2],pa[0],pa[3],pa[1],pa[5])
            if lado == 90:
                return (pa[2],pa[4],pa[1],pa[3],pa[0],pa[5])
    def turn_face(self,move):
        repetition = 1
        if move == "Fi" or move == "F":
            if move == "F":
                repetition = 3

            for o in range(repetition):
                #cara frontal = cara frontal girada -90º
                self.cube[:,:,0] = np.rot90(self.cube[:,:,0])
                for index0 ,row in enumerate(self.cube[:,:,0]):
                    for index1 ,piece in enumerate(row):
                        self.cube[:,:,0][index0][index1] = self.rotate_piece(piece,"FB",-90)
        
        if move == "Di" or move == "D":
            if move == "D":
                repetition = 3

            for o in range(repetition):
                #cara inferior = cara inferior girada -90º*3
                for i in range(3):
                    self.cube[2,:,:] = np.rot90(self.cube[2,:,:])
                for index0 ,row in enumerate(self.cube[2,:,:]):
                    for index1 ,piece in enumerate(row):
                        self.cube[2,:,:][index0][index1] = self.rotate_piece(piece,"UD",-90)

        if move == "Ui" or move == "U":
            if move == "U":
                repetition = 3

            for o in range(repetition):
                #cara superior = cara superior girada -90
                self.cube[0,:,:] = np.rot90(self.cube[0,:,:])
                for index0 ,row in enumerate(self.cube[0,:,:]):
                    for index1 ,piece in enumerate(row):
                        self.cube[0,:,:][index0][index1] = self.rotate_piece(piece,"UD",90)

        if move == "Ri" or move == "R":
            if move == "R":
                repetition = 3

            for o in range(repetition):
                self.cube[:,2,:] = np.rot90(self.cube[:,2,:])
                for index0 ,row in enumerate(self.cube[:,2,:]):
                    for index1 ,piece in enumerate(row):
                        self.cube[:,2,:][index0][index1] = self.rotate_piece(piece,"LR",90)

        if move == "Li" or move == "L":
            if move == "L":
                repetition = 3

            for o in range(repetition):
                for i in range(3):
                    self.cube[:,0,:] = np.rot90(self.cube[:,0,:])
                for index0 ,row in enumerate(self.cube[:,0,:]):
                    for index1 ,piece in enumerate(row):
                        self.cube[:,0,:][index0][index1] = self.rotate_piece(piece,"LR",-90)

        if move == "Bi" or move == "B":
            if move == "B":
                repetition = 3

            for o in range(repetition):
                for i in range(3):
                    self.cube[:,:,2] = np.rot90(self.cube[:,:,2])
                for index0 ,row in enumerate(self.cube[:,:,2]):
                    for index1 ,piece in enumerate(row):
                        self.cube[:,:,2][index0][index1] = self.rotate_piece(piece,"FB",90)
    
    def show_cube(self,save = False):

        def draw_face(x,y,face,view):
            actual_x = x
            actual_y = y

            for fila in face:
                for index, piece in enumerate(fila):

                    if piece[view] == 0: color = "black"
                    if piece[view] == 1: color = "white"
                    if piece[view] == 2: color = "yellow"
                    if piece[view] == 3: color = "red"
                    if piece[view] == 4: color = "orange"
                    if piece[view] == 5: color = "blue"
                    if piece[view] == 6: color = "green"

                    self.draw.rectangle((actual_x,actual_y,actual_x+30,actual_y+30),fill=color)
                    if index != 2:
                        actual_x += 35
                    else: 
                        actual_y += 35
                        actual_x = x

        center = (210,105)
        draw_face(center[0],center[1],self.get_faces()["frontal"],3)
        draw_face(center[0]+105,center[1],self.get_faces()["right"],4)
        draw_face(center[0]-105,center[1],self.get_faces()["left"],2)
        draw_face(center[0]-105*2,center[1],self.get_faces()["back"],5)
        draw_face(center[0],center[1]-105,self.get_faces()["up"],0)
        draw_face(center[0],center[1]+105,self.get_faces()["down"],1)

        if save:
            self.img.save(f"{self.frame_count}.png")
            self.frame_count += 1
        else: self.img.show(title="cube")

    def scramble_cube(self):
        for _ in range(50):
            move = random.choice([
                "R","Ri","L","Li","B","Bi","D","Di","F","Fi","U","Ui"])
            self.turn_face(move)

    def is_solved(self):
        comparacion = self.cube == self.solved_cube
        equal_arrays = comparacion.all()
        if equal_arrays:
            return True
        return False

    def reset(self):
        self.cube = np.copy(self.solved_cube)
    def get_reward(self):
        reward = 0
        for face, solved_face in zip(self.cube,self.solved_cube):
            for line, solved_line in zip(face,solved_face):
                for piece, solved_piece in zip(line,solved_line):
                    if piece.any() == solved_piece.any():
                        reward += 1
                        
        return(reward)


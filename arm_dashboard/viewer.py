#/usr/bin/env python3

#codigo que genera una vista en tiempo real del brazo

import pygame
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32  
from geometry_msgs.msg import Point
import threading
import time
from math import cos
from math import sin
from math import pi

class Viewer(Node):

    def __init__(self):
        super().__init__("viewer")
        self.posiciones = [0,0,0,0] 
        
        #listeners de posiciones
        self.joint1_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint1_deg",self.set_pos_1,10)

        self.joint2_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint2_deg",self.set_pos_2,10)

        self.joint3_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint3_deg",self.set_pos_3,10)

        self.joint4_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint4_deg",self.set_pos_4,10)
        self.get_logger().info("""
        --- controles ---
        zoom            | e d
        angulo picada   | w r
        rotar camara    | s f
        mover camara    | flechitas
        minimapa        | h
        resetear camara | espacio
        camara normal al brazo | enter

                               """)



    def set_pos_1(self,msg: Float32):
            self.posiciones[0] = msg.data
    def set_pos_2(self,msg: Float32):
            self.posiciones[1] = msg.data
    def set_pos_3(self,msg: Float32):
            self.posiciones[2] = msg.data
    def set_pos_4(self,msg: Float32):
        global angulo_pantalla
        global angulo_picada
        self.posiciones[3] = msg.data
        # try:
            # self.get_logger().info(f"{str(self.posiciones),angulo_pantalla}")
            # self.get_logger().info(f"{str(self.posiciones)}")
        # except Exception as e:
            # pass
    
    def set_coords(self,msg: Point):
        pass



    def get_positions(self):
        return list(self.posiciones)

class Punto():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other: 'Punto') -> 'Punto':
        """Overloads the + operator to perform component-wise addition."""
        if isinstance(other, Punto):
            return Punto(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented
    def __sub__(self, other: 'Punto') -> 'Punto':
        """Overloads the - operator to perform component-wise subtraction."""
        if isinstance(other, Punto):
            return Punto(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def get_y(self):
        return self.y
    def get_z(self):
        return self.z

    def set_x(self,a):
        self.x = a
    def set_y(self,a):
        self.y = a
    def set_z(self,a):
        self.z = a

    def proye(self):
        global angulo_pantalla,angulo_picada,desplazamiento_x,desplazamiento_y

        puwu = self.rotate_y(to_radians(angulo_pantalla))
        puwu = puwu.rotate_x(to_radians(angulo_picada)) 
        x = (width/2 + escala*puwu.x) + desplazamiento_x
        y = (height - (height/2 + escala*puwu.y)) - desplazamiento_y
        return (x,y)

    def simple_proye(self):
        puwu = Punto(self.x,self.y,self.z)
        x = (width/2 + 2.5*puwu.x) - 150 * pixel
        y = (height - (height/2 + 2.5*puwu.y)) + 250 * pixel
        return (x,y)
    def simple_proye1(self):
        puwu = Punto(self.x,self.y,self.z)
        x = (width/2 + 2.5*puwu.x) + 150 * pixel
        y = (height - (height/2 + 2.5*puwu.y)) + 250 * pixel
        return (x,y)


    
        
    def rotate_x(self, radians: float) -> 'Punto':
        """Rotates the point around the X axis by the given angle in radians."""
        cos_a = cos(radians)
        sin_a = sin(radians)
        
        new_x = self.x
        new_y = self.y * cos_a - self.z * sin_a
        new_z = self.y * sin_a + self.z * cos_a
        
        return Punto(new_x, new_y, new_z)

    def rotate_y(self, radians: float) -> 'Punto':
        """Rotates the point around the Y axis by the given angle in radians."""
        cos_a = cos(radians)
        sin_a = sin(radians)
        
        new_x = self.x * cos_a + self.z * sin_a
        new_y = self.y
        new_z = -self.x * sin_a + self.z * cos_a
        
        return Punto(new_x, new_y, new_z)

    def rotate_z(self, radians: float) -> 'Punto':
        """Rotates the point around the Z axis by the given angle in radians."""
        cos_a = cos(radians)
        sin_a = sin(radians)
        
        new_x = self.x * cos_a - self.y * sin_a
        new_y = self.x * sin_a + self.y * cos_a
        new_z = self.z
        
        return Punto(new_x, new_y, new_z)

    
def to_radians(degrees: float) -> float:
    """Converts an angle from degrees to radians."""
    return degrees * (pi / 180.0)


def graficar_ejes():
    puntos = [Punto(50,0,50),
              Punto(50,0,-50),
              Punto(-50,0,-50),
              Punto(-50,0,50)]
    for i in range(len(puntos)):
        puntos[i] = puntos[i].proye()
    pygame.draw.polygon(screen,(87, 83, 87),puntos)
    pygame.draw.line(screen, (255, 255, 255), px1.proye(), px2.proye(), width=1)
    pygame.draw.line(screen, (255, 0, 0), px2.proye(), px3.proye(), width=1)
    
    pygame.draw.line(screen,(255,255,255),py1.proye(),py2.proye(),width=1)
    pygame.draw.line(screen,(255,255,255),pz1.proye(),pz2.proye(),width=1)



def rotate_joint1():
    global l1p1,l1p2,l2p1,l2p2,l3p1,l3p2
    l1p1 = l1p1.rotate_y(to_radians(node.posiciones[0]))
    l1p2 = l1p2.rotate_y(to_radians(node.posiciones[0]))
    l2p1 = l2p1.rotate_y(to_radians(node.posiciones[0]))
    l2p2 = l2p2.rotate_y(to_radians(node.posiciones[0]))
    l3p1 = l3p1.rotate_y(to_radians(node.posiciones[0]))
    l3p2 = l3p2.rotate_y(to_radians(node.posiciones[0]))
    
    return l1p1,l1p2,l2p1,l2p2,l3p1,l3p2

def crear_puntos_l(p1,p2):
    vector_puntos = []
    vector_puntos.append()
    return vector_puntos
class SeccionBrazo():
    def __init__(self,p1,p2,ideuwu):
        global r
        self.root2 = 2*cos(pi/4)
        self.hipo = r/self.root2
        self.puntos_internos = [p1,p2]
        self.puntos_visibles = [Punto(p1.x,p1.y+self.hipo,p1.z+self.hipo),
                                Punto(p1.x,p1.y+self.hipo,p1.z-self.hipo),
                                Punto(p1.x,p1.y-self.hipo,p1.z+self.hipo),
                                Punto(p1.x,p1.y-self.hipo,p1.z-self.hipo),

                                Punto(p2.x,p2.y+self.hipo,p2.z+self.hipo),
                                Punto(p2.x,p2.y+self.hipo,p2.z-self.hipo),
                                Punto(p2.x,p2.y-self.hipo,p2.z+self.hipo),
                                Punto(p2.x,p2.y-self.hipo,p2.z-self.hipo),
                                self.puntos_internos[0],p2]
        self.id = ideuwu
        self.puntos_a_graficar = [0,0,0,0,0,0,0,0,0,0]
    def obtener_puntos_graficar(self,posiciones,punto_anterior):

        for i in range(10):
            # print(i)
                        
            if self.id == 1:
                self.puntos_a_graficar[i] = self.puntos_visibles[i]

            #
                self.puntos_a_graficar[i] = (self.puntos_a_graficar[i]).rotate_z(to_radians(posiciones[self.id]))
                # self.puntos_a_graficar[i] = (self.puntos_a_graficar[i]).rotate_z(to_radians(169))
            if self.id == 2:
                self.puntos_a_graficar[i] = self.puntos_visibles[i] - self.puntos_visibles[8]
                self.puntos_a_graficar[i] = (self.puntos_a_graficar[i]).rotate_z(to_radians(posiciones[self.id]+posiciones[self.id-1]))
                self.puntos_a_graficar[i] = self.puntos_a_graficar[i] + Punto(punto_anterior.x,punto_anterior.y,0)
                 
            if self.id == 3:
                self.puntos_a_graficar[i] = self.puntos_visibles[i] - self.puntos_visibles[8]
                self.puntos_a_graficar[i] = (self.puntos_a_graficar[i]).rotate_z(to_radians(posiciones[self.id]+posiciones[self.id-1]+posiciones[self.id-2]))
                self.puntos_a_graficar[i] = self.puntos_a_graficar[i] + Punto(punto_anterior.x,punto_anterior.y,+r)

            
               
    def rotar_joint1(self,angulo):
        # for i in range(len(self.puntos_a_graficar)):
        for i in range(8):
            self.puntos_a_graficar[i] = self.puntos_a_graficar[i].rotate_y(to_radians(angulo))
    def graficar(self,posiciones,punto_anterior,minimapa):
        global screen, ancho_rayas,color_l1,color_l2,color_l3
        self.obtener_puntos_graficar(posiciones,punto_anterior)
        if not minimapa:
            self.rotar_joint1(node.posiciones[0])
            self.proyectar_puntos()
        else:
            self.simple_proyectar_puntos()

        if self.id == 1:
            color = color_l1
        elif self.id == 2:
            color = color_l2
        elif self.id == 3:
            color= color_l3

        #base izquierda
        pygame.draw.line(screen, color, self.puntos_proyectados[0], self.puntos_proyectados[1], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[0], self.puntos_proyectados[2], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[1], self.puntos_proyectados[3], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[2], self.puntos_proyectados[3], width=ancho_rayas)
        #base derecha
        pygame.draw.line(screen, color, self.puntos_proyectados[4], self.puntos_proyectados[5], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[4], self.puntos_proyectados[6], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[5], self.puntos_proyectados[7], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[6], self.puntos_proyectados[7], width=ancho_rayas)
        # lineas a lo largo
        pygame.draw.line(screen, color, self.puntos_proyectados[0], self.puntos_proyectados[4], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[1], self.puntos_proyectados[5], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[2], self.puntos_proyectados[6], width=ancho_rayas)
        pygame.draw.line(screen, color, self.puntos_proyectados[3], self.puntos_proyectados[7], width=ancho_rayas)


        # pygame.draw.circle(screen, (255, 0, 255), self.puntos_proyectados[0], 5) 
        # for i in range(len(self.puntos_proyectados)):
            # pygame.draw.circle(screen, (255, 255, 255), self.puntos_proyectados[i], 5) 

        

    def proyectar_puntos(self):
        self.puntos_proyectados = [0,0,0,0,0,0,0,0]
        
        for i in range(8):
            self.puntos_proyectados[i] = self.puntos_a_graficar[i].proye()

    def simple_proyectar_puntos(self):
        self.puntos_proyectados = [0,0,0,0,0,0,0,0]
        
        for i in range(8):
            self.puntos_proyectados[i] = self.puntos_a_graficar[i].simple_proye()


    

class Brazo():
    def __init__(self):
        self.segmentos = [ SeccionBrazo(Punto(0,0 , r),Punto(l1,0,r),1),
                          SeccionBrazo(Punto(l1,0,-r),Punto(l1+l2,0,-r),2),
                          SeccionBrazo(Punto(l1+l2,0,r),Punto(l1+l2+l3,0,r),3) ]
    def graficar(self,posiciones):
        for i in range(len(self.segmentos)):
            if self.segmentos[i].id == 1:
                self.segmentos[i].graficar(posiciones,Punto(0,0,0),False)
            else:
                self.segmentos[i].graficar(posiciones,self.segmentos[i-1].puntos_a_graficar[9],False)
        if posiciones[0] != 0:
            #graficar el angulo de la joint1
            p1 = Punto(100,0,0).rotate_y(to_radians(posiciones[0]))
            pygame.draw.line(screen,(0,0,255),Punto(0,0,0).proye(),p1.proye(),width = 2)

    
class Minimapa(Brazo):
    def __init__(self):
        self.segmentos = [ SeccionBrazo(Punto(0,0 , r),Punto(l1,0,r),1),
                          SeccionBrazo(Punto(l1,0,-r),Punto(l1+l2,0,-r),2),
                          SeccionBrazo(Punto(l1+l2,0,r),Punto(l1+l2+l3,0,r),3) ]

    def graficar(self,posiciones):
        for i in range(len(self.segmentos)):
            if self.segmentos[i].id == 1:
                self.segmentos[i].graficar(posiciones,Punto(0,0,0),True)
            else:
                self.segmentos[i].graficar(posiciones,self.segmentos[i-1].puntos_a_graficar[9],True)  
        px1 = Punto(-50,0,0)
        px2 = Punto(0,0,0)
        px3 = Punto(+50,0,0)
        py1 = Punto(0,-50,0)
        py2 = Punto(0,50,0)
        pygame.draw.line(screen,(255,255,255),px1.simple_proye(),px2.simple_proye(),width=1)
        pygame.draw.line(screen,(0,0,255),px2.simple_proye(),px3.simple_proye(),width=1)
        pygame.draw.line(screen,(255,255,255),py1.simple_proye(),py2.simple_proye(),width=1)
        p = Punto(0,0,0)
        px2 = Punto(0,0,0)
        px3 = Punto(+30,0,0)
        pr = Punto(30,0,0)
        pr = pr.rotate_z(to_radians(posiciones[0]))
        pygame.draw.line(screen,(255,0,0),px2.simple_proye1(),px3.simple_proye1(),width=2)
        pygame.draw.circle(screen,(255,255,255),p.simple_proye1(),radius=80,width=2)
        pygame.draw.line(screen,(0,0,255),p.simple_proye1(),pr.simple_proye1(),width=2)
        

def main(args=None):
    global l1,l2,l3, color_l1,color_l2,color_l3
    l1 = 48
    l2 = 44
    l3 = 40
    color_l1 = (189, 205, 255)
    color_l2 = (55, 113, 217)
    color_l3 = (189, 205, 255)
    global r
    r = 5
    global desplazamiento_x, desplazamiento_y
    desplazamiento_x,desplazamiento_y = 0,0
    #cosas del nodo 
    rclpy.init(args=args)
    global node
    node = Viewer() 
    #ejecutar nodo en un thread
    ros_thread = threading.Thread(
        target=rclpy.spin, args=(node,), daemon=True
    )
    ros_thread.start()

    #cosas de pygame y graficos
    
    #definir ejes coordenados
    global px1, px2,px3, py1, py2, pz1, pz2
    px1 = Punto(-100,0,0)
    px2 = Punto(0,0,0)
    px3 = Punto(100,0,0)
    py1 = Punto(0,0,0)
    py2 = Punto(0,100,0)
    pz1 = Punto(0,0,-100)
    pz2 = Punto(0,0,100)
    
    pygame.init()
    global width
    global height
    global escala
    global angulo_pantalla
    global angulo_picada 
    global pixel
    angulo_pantalla,angulo_picada = 0,0
    escala = 3
    width = 900
    height = 600
    pixel = width / 900
    flags = pygame.NOFRAME | pygame.RESIZABLE
    global screen
    global ancho_rayas
    minimapa_activo = True
    ancho_rayas = 3
    screen = pygame.display.set_mode((width,height),flags)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    running = True

    while running:
        
        #controles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = screen.get_size()

            elif event.type == pygame.KEYDOWN:
                if event.unicode == 'e':
                    escala = escala + .3
                elif event.unicode == 'd':
                    escala = escala - .3
                elif event.unicode == 's':
                    angulo_pantalla += 15
                elif event.unicode == 'f':
                    angulo_pantalla -=15
                elif event.key == pygame.K_SPACE:
                    angulo_picada = 0
                    angulo_pantalla = 0
                    desplazamiento_y = 0
                    desplazamiento_x = 0
                elif event.key == pygame.K_RETURN:
                    angulo_pantalla = 0-(node.posiciones[0])
                    angulo_picada = 0
                    angulo_picada = 0
                elif event.unicode == 'r':
                    if angulo_picada == 90:
                        pass
                    else:
                        angulo_picada += 15
                elif event.unicode == 'w':
                    if angulo_picada == 0:
                        pass
                    else:
                        angulo_picada -= 15
                elif event.unicode == 'h':
                    minimapa_activo = not minimapa_activo
                elif event.key == pygame.K_UP:
                    desplazamiento_y -= 20
                elif event.key == pygame.K_DOWN:
                    desplazamiento_y += 20
                elif event.key == pygame.K_LEFT:
                    desplazamiento_x += 20
                elif event.key == pygame.K_RIGHT:
                    desplazamiento_x -= 20


        
        
        joint_angles = node.get_positions()

        
        screen.fill((30, 30, 30))
        graficar_ejes()

        #angulos en pantalla
        text_surface = font.render(
                f"Joint Angles: {[round(x, 1) for x in joint_angles]}", True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))

        #graficar lineas internas del brazo
        global l1p1, l1p2,l2p1,l2p2,l3p2,l3p1
        l1p1 = Punto(0,0,+r)
        l1p2 = Punto(l1*cos(to_radians(node.posiciones[1])),l1*sin(to_radians(node.posiciones[1])),+r)
        l2p1 = Punto(l1p2.x,l1p2.y,-r)
        l2p2 = l2p1 + (Punto(l2*cos(to_radians(node.posiciones[2])),l2*sin(to_radians(node.posiciones[2])),0).rotate_z(to_radians(node.posiciones[1])))

        l3p1 = Punto(l2p2.x,l2p2.y,+r)
        l3p2 = l3p1 + (Punto(l3*cos(to_radians(node.posiciones[3])),l3*sin(to_radians(node.posiciones[3])),0).rotate_z(to_radians(node.posiciones[2]+node.posiciones[1])))

        l1p1,l1p2,l2p1,l2p2,l3p1,l3p2 = rotate_joint1()

        # pygame.draw.circle(screen, (255, 0, 255), (l1p1.proye()), 5)
        # pygame.draw.line(screen, (0, 255, 0), l1p1.proye(), l1p2.proye(), width=5)
        # pygame.draw.line(screen, (0, 0, 255), l2p1.proye(), l2p2.proye(), width=5)
        # pygame.draw.line(screen, (255, 0, 0), l3p1.proye(), l3p2.proye(), width=5)
        # try:
        brazo = Brazo()
        brazo.graficar(node.posiciones)
        if minimapa_activo:
            minimapa = Minimapa()
            minimapa.graficar(node.posiciones)
        # except Exception as e:
            # node._logger().info(f"{e}")
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()   





#!/usr/bin/env python3
import sys
import termios
import tty
import rclpy
from rclpy.node import Node
# from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import threading 
from threading import Thread



def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    if key == '\x1b':
        key += sys.stdin.read(2)
    termios.tcsetattr(sys.stdin,termios.TCSANOW,settings)
    return key


class Keys(Node):
    def __init__(self):
        super().__init__("keys_control")
        self.posiciones_iniciales = [0,0,0,0]
        # self.posiciones_publicadas = [0,0,0,0]
        self.primera_vez = [True,True, True , True]
        #suscriptoree
        self.joint1_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint1_deg",self.set_pos_1,10)

        self.joint2_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint2_deg",self.set_pos_2,10)

        self.joint3_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint3_deg",self.set_pos_3,10)

        self.joint4_subscriber_ = self.create_subscription(Float32,"/arm_feedback/joint4_deg",self.set_pos_4,10)

        


        self.incremento = 10.0
        self.pub_joint1 = self.create_publisher(Float32,"/arm_teleop/joint1",10)
        self.pub_joint2 = self.create_publisher(Float32,"/arm_teleop/joint2",10)
        self.pub_joint3 = self.create_publisher(Float32,"/arm_teleop/joint3",10)
        self.pub_joint4 = self.create_publisher(Float32,"/arm_teleop/joint4",10)
        self.get_logger().info("control del brazo por teclas inciado")
        self.get_logger().info("joint| 1 | 2 | 3 | 4")
        self.get_logger().info("  +  | q | w | e | r")
        self.get_logger().info("  -  | a | s | d | f")
        self.get_logger().info(f"el incremento actual es {self.incremento} grados")
        
    def set_pos_1(self,msg: Float32):
        if self.primera_vez[0]:
            self.posiciones_iniciales[0] = msg.data
            self.primera_vez[0] = False
            
        else:
            msg1 = Float32()
            msg1.data = self.posiciones_iniciales[0]
            self.pub_joint1.publish(msg1)
            
    def set_pos_2(self,msg: Float32):
        if self.primera_vez[1]:
            self.posiciones_iniciales[1] = msg.data
            self.primera_vez[1] = False
        else:
            msg1 = Float32()
            msg1.data = self.posiciones_iniciales[1]
            self.pub_joint2.publish(msg1)
    def set_pos_3(self,msg: Float32):
        if self.primera_vez[2]:
            self.posiciones_iniciales[2] = msg.data
            self.primera_vez[2] = False
        else:
            msg1 = Float32()
            msg1.data = self.posiciones_iniciales[2]
            self.pub_joint3.publish(msg1)
    def set_pos_4(self,msg: Float32):
        if self.primera_vez[3]:
            self.posiciones_iniciales[3] = msg.data
            self.primera_vez[3] = False
        else:
            msg1 = Float32()
            msg1.data = self.posiciones_iniciales[3]
            self.pub_joint4.publish(msg1)
    

def main(args=None):
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = Keys()
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()
    

    try:
        while rclpy.ok():
            key = get_key(settings)
            if  key == '\x03':
                node.get_logger().info("desactivando")
                break            
            else:
                if key == '\x1b[A':
                    if node.incremento + 2 > 30:
                        node.incremento = 30.0
                        node.get_logger().info(f"el incremento es {node.incremento}")
                    else:
                        node.incremento += 2.0
                        node.get_logger().info(f"el incremento es {node.incremento}")
                elif key == '\x1b[B':

                    if node.incremento - 2.0 < 2:
                        node.incremento = 2.0
                    else:
                        node.incremento -= 2.0
                        node.get_logger().info(f"el incremento {node.incremento}")
                elif key == 'q':
                    node.posiciones_iniciales[0] += node.incremento
                elif key == 'a':
                    node.posiciones_iniciales[0] -= node.incremento
                elif key == 'w':
                    node.posiciones_iniciales[1] += node.incremento
                elif key == 's':
                    node.posiciones_iniciales[1] -= node.incremento
                elif key == 'e':
                    node.posiciones_iniciales[2] += node.incremento
                elif key == 'd':
                    node.posiciones_iniciales[2] -= node.incremento
                elif key == 'r':
                    node.posiciones_iniciales[3] += node.incremento
                elif key == 'f':
                    node.posiciones_iniciales[3] -= node.incremento
                    


            

    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin,termios.TCSANOW,settings)
        node.destroy_node()
        rclpy.shutdown()
    #rclpy.spin(node
    #rclpy.shutdown()


#/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Brazo(Node):
    def __init__(self):
        super().__init__("sim_arm")
        self.posiciones = [0.0,169.0,-169.0,0.0]
        self.moviendo1 = False
        self.moviendo2 = False
        self.moviendo3 = False
        self.moviendo4 = False

        self.TOLERANCE = 1

        
        
        # publicar
        self.pub_joint1 = self.create_publisher(Float32,"/arm_feedback/joint1_deg",10)
        self.pub_joint2 = self.create_publisher(Float32,"/arm_feedback/joint2_deg",10)
        self.pub_joint3 = self.create_publisher(Float32,"/arm_feedback/joint3_deg",10)
        self.pub_joint4 = self.create_publisher(Float32,"/arm_feedback/joint4_deg",10)

        self.timer = self.create_timer(0.5,self.send_data)
        self.get_logger().info("test arm started")
        
        # escuchar a cambios
        self.joint1_subscriber_ = self.create_subscription(Float32,"/arm_teleop/joint1",self.set_pos_1,10)

        self.joint2_subscriber_ = self.create_subscription(Float32,"/arm_teleop/joint2",self.set_pos_2,10)

        self.joint3_subscriber_ = self.create_subscription(Float32,"/arm_teleop/joint3",self.set_pos_3,10)

        self.joint4_subscriber_ = self.create_subscription(Float32,"/arm_teleop/joint4",self.set_pos_4,10)

        

    def send_data(self):
        msg1 = Float32()
        msg1.data = self.posiciones[0]
        self.pub_joint1.publish(msg1)

        msg2 = Float32()
        msg2.data = self.posiciones[1]
        self.pub_joint2.publish(msg2)

        msg3 = Float32()
        msg3.data = self.posiciones[2]
        self.pub_joint3.publish(msg3)

        msg4 = Float32()
        msg4.data = self.posiciones[3]
        self.pub_joint4.publish(msg4)

    def set_pos_1(self, msg: Float32):
        
        if abs(self.posiciones[0] - msg.data) < self.TOLERANCE:
            self.moviendo1 = False
        else:
            if not self.moviendo1:
                self.delta1 = self.posiciones[0] - msg.data
                self.moviendo1 = True
            else:
                if self.delta1 > 0:
                    self.posiciones[0] -= self.delta1 / 3
                elif self.delta1 < 0:
                    self.posiciones[0] -= self.delta1 / 3    

    def set_pos_2(self, msg: Float32):
        if abs(self.posiciones[1] - msg.data) < self.TOLERANCE:
            self.moviendo2 = False
        else:
            if not self.moviendo2:
                self.delta2 = self.posiciones[1] - msg.data
                self.moviendo2 = True
            else:
                if self.delta2 > 0:
                    self.posiciones[1] -= self.delta2 / 3
                elif self.delta2 < 0:
                    self.posiciones[1] -= self.delta2 / 3


    def set_pos_3(self, msg: Float32):
        if abs(self.posiciones[2] - msg.data) < self.TOLERANCE:
            self.moviendo3 = False
        else:
            if not self.moviendo3:
                self.delta3 = self.posiciones[2] - msg.data
                self.moviendo3 = True
            else:
                if self.delta3 > 0:
                    self.posiciones[2] -= self.delta3 / 3
                elif self.delta3 < 0:
                    self.posiciones[2] -= self.delta3 / 3


    def set_pos_4(self, msg: Float32):
        if abs(self.posiciones[3] - msg.data) < self.TOLERANCE:
            self.moviendo4 = False
        else:
            if not self.moviendo4:
                self.delta4 = self.posiciones[3] - msg.data
                self.moviendo4 = True
            else:
                if self.delta4 > 0:
                    self.posiciones[3] -= self.delta4 / 3
                elif self.delta4 < 0:
                    self.posiciones[3] -= self.delta4 / 3


def main(args=None):
    rclpy.init(args=args)
    node = Brazo()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

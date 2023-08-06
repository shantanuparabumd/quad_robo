#!/usr/bin/env python3
import rospy

from std_msgs.msg import Float64

import sys, select, termios, tty

import json
import os
import keyboard

class Gait:

    def __init__(self):
        rospy.init_node('gait_controller')

        self.rate = rospy.Rate(200)

        self.back_right_thigh = rospy.Publisher('/quad_robo/brt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
        self.back_right_leg = rospy.Publisher('/quad_robo/brl_position_controller/command', Float64, queue_size=10)
        self.back_right_shin= rospy.Publisher('/quad_robo/brs_position_controller/command', Float64, queue_size=10)

        self.back_left_thigh = rospy.Publisher('/quad_robo/blt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
        self.back_left_leg = rospy.Publisher('/quad_robo/bll_position_controller/command', Float64, queue_size=10)
        self.back_left_shin= rospy.Publisher('/quad_robo/bls_position_controller/command', Float64, queue_size=10)

        self.front_left_thigh = rospy.Publisher('/quad_robo/flt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
        self.front_left_leg = rospy.Publisher('/quad_robo/fll_position_controller/command', Float64, queue_size=10)
        self.front_left_shin= rospy.Publisher('/quad_robo/fls_position_controller/command', Float64, queue_size=10)

        self.front_right_thigh = rospy.Publisher('/quad_robo/frt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
        self.front_right_leg = rospy.Publisher('/quad_robo/frl_position_controller/command', Float64, queue_size=10)
        self.front_right_shin= rospy.Publisher('/quad_robo/frs_position_controller/command', Float64, queue_size=10)

        

        output=os.popen('rospack find quad_robo')
        self.base_dir=output.read()
        self.base_dir=self.base_dir[0:-1]

        self.settings = termios.tcgetattr(sys.stdin)
     

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key    
        
    def trot_right(self):
        with open(self.base_dir +'/src/gait/front_trot_right.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.step_walk(back_left,back_right,front_left,front_right)
    
    def trot_left(self):
        with open(self.base_dir +'/src/gait/front_trot_left.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.step_walk(back_left,back_right,front_left,front_right)

    def trot(self):
        self.trot_right()
        self.stand()
        self.trot_left()
        self.stand()

    def back(self):
        with open(self.base_dir +'/src/gait/reverse.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.step(back_left,back_right,front_left,front_right)

    def left_turn(self):
        with open(self.base_dir +'/src/gait/left_turn.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.step(back_left,back_right,front_left,front_right)
        

    def right_turn(self):
        with open(self.base_dir +'/src/gait/right_turn.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.step(back_left,back_right,front_left,front_right)

    def walk(self):
        with open(self.base_dir +'/src/gait/fast_trot.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.step_walk(back_left,back_right,front_left,front_right)
        # self.land()
    
    def right(self):
        with open(self.base_dir +'/src/gait/right_slide_gait.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        # self.rate=rospy.Rate(100000000000000)
        self.step(back_left,back_right,front_left,front_right)
        # self.rate=rospy.Rate(100)

    def left(self):
        with open(self.base_dir +'/src/gait/left_slide_gait.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        # self.rate=rospy.Rate(1000000000000000000)
        self.step(back_left,back_right,front_left,front_right)
        # self.rate=rospy.Rate(100)


    def step(self,back_left,back_right,front_left,front_right):
        step=0
        positions=[0,0,0,0,0,0,0,0,0,0,0,0]
        
        for leg1,leg2 in zip(back_left,front_right):
            
            positions=[0,-0.7,1.5,leg2[0],leg2[1],leg2[2],leg1[0],leg1[1],leg1[2],0,-0.7,1.5]
            self.publish_joint(positions)
            self.rate.sleep()
        
        for leg1,leg2 in zip(back_right,front_left):
            positions=[leg1[0],leg1[1],leg1[2],0,-0.7,1.5,0,-0.7,1.5,leg2[0],leg2[1],leg2[2]]
            self.publish_joint(positions)
            self.rate.sleep()

    # def step_walk(self,back_left,back_right,front_left,front_right):
    #     positions=[0,0,0,0,0,0,0,0,0,0,0,0]
    #     for leg1,leg2,leg3,leg4 in zip(back_left,front_right,back_right,front_left):
    #         positions=[leg3[0],leg3[1],leg3[2],leg2[0],leg2[1],leg2[2],leg1[0],leg1[1],leg1[2],leg4[0],leg4[1],leg4[2]]
    #         self.publish_joint(positions)
    #         self.rate.sleep()

    def step_walk(self,back_left,back_right,front_left,front_right):
        step=0
        positions=[0,0,0,0,0,0,0,0,0,0,0,0]
        i=0
        for leg1,leg2 in zip(back_left,front_right):
            
            positions=[0,-0.7,1.5,leg2[0],leg2[1],leg2[2],leg1[0],leg1[1],leg1[2],0,-0.7,1.5]
            if i>25:
                positions=[0,-0.9087,1.5168,leg2[0],leg2[1],leg2[2],leg1[0],leg1[1],leg1[2],0,-0.9087,1.5168]
            self.publish_joint(positions)
            self.rate.sleep()
            i+=1

        # positions=[0,-0.7,1.5,leg2[0],leg2[1],leg2[2],leg1[0],leg1[1],leg1[2],0,-0.7,1.5]
        # self.publish_joint(positions)
        # self.rate.sleep()
        i=0
        for leg1,leg2 in zip(back_right,front_left):
            positions=[leg1[0],leg1[1],leg1[2],0,-0.7,1.5,0,-0.7,1.5,leg2[0],leg2[1],leg2[2]]
            if i>25:
                positions=[leg1[0],leg1[1],leg1[2],0,-0.9087,1.5168,0,-0.9087,1.5168,leg2[0],leg2[1],leg2[2]]

            self.publish_joint(positions)
            self.rate.sleep()
            i+=1
        # positions=[leg1[0],leg1[1],leg1[2],0,-0.7,1.5,0,-0.7,1.5,leg2[0],leg2[1],leg2[2]]
        # self.publish_joint(positions)
        # self.rate.sleep()
        # positions=[0,-0.5,1.5,0,-0.5,1.5,0,-0.5,1.5,0,-0.5,1.5]
        # self.publish_joint(positions)
        # self.rate.sleep()


    def jump(self,back_left,back_right,front_left,front_right):
        positions=[0,0,0,0,0,0,0,0,0,0,0,0]
        for leg1,leg2,leg3,leg4 in zip(back_left,front_right,back_right,front_left):
            positions=[leg3[0],leg3[1],leg3[2],leg2[0],leg2[1],leg2[2],leg1[0],leg1[1],leg1[2],leg4[0],leg4[1],leg4[2]]
            self.publish_joint(positions)
            self.rate.sleep()
        

    def stand(self):
        positions=[0,-0.7,1.5,0,-0.7,1.5,0,-0.7,1.5,0,-0.7,1.5]
        # positions=[0,-0.7,1.2,0,-0.7,1.2,0,-0.7,1.2,0,-0.7,1.2]
        self.publish_joint(positions)
        self.rate.sleep()

    def land(self):
        # back_right,front_right,back_left,front_left
        positions=[0,-0.7,1.5,0,0.7,0,0,-0.7,1.5,0,0.7,0]
        self.publish_joint(positions)
        self.rate.sleep()

    
    def jump_forward(self):
        self.rate = rospy.Rate(100)
        with open(self.base_dir +'/src/gait/loaded_jump.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        # self.rate = rospy.Rate(100)
        self.jump(back_left,back_right,front_left,front_right)
        for i in range(5):
            self.rate.sleep()
        self.land()
        for i in range(40):
            self.rate.sleep()
        self.stand()
        self.rate = rospy.Rate(200)

    def up(self):
        self.rate = rospy.Rate(20000000000000000)
        with open(self.base_dir +'/src/gait/jump.json','r') as file:
            data=json.load(file)
        front_right=data["front_right"]
        front_left=data["front_left"]
        back_right=data["back_right"]
        back_left=data["back_left"]
        self.jump(back_left,back_right,front_left,front_right)
        self.stand()
        self.rate = rospy.Rate(200)
        


            
            


    def publish_joint(self,positions):
        t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12=positions
        print(positions)
         # Publish the message
        self.back_right_thigh.publish(t1) # publish the turn command.
        self.back_right_leg.publish(t2) # publish the turn command.
        self.back_right_shin.publish(t3) # publish the control speed. 
        self.front_right_thigh.publish(t4) # publish the turn command.
        self.front_right_leg.publish(t5) # publish the turn command.
        self.front_right_shin.publish(t6) # publish the control speed. 
        self.back_left_thigh.publish(t7) # publish the turn command.
        self.back_left_leg.publish(t8) # publish the turn command.
        self.back_left_shin.publish(t9) # publish the control speleft
        self.front_left_thigh.publish(t10) # publish the turn command.
        self.front_left_leg.publish(t11) # publish the turn command.
        self.front_left_shin.publish(t12) # publish the control speed. 


    def controller(self):
        
        # try:
        while(1):
            key = self.getKey()
            print(key)
            if key=='w':
                self.walk()
            if key=='p':
                self.walk()

            if key=='d':
                self.left()
            if key=='s':
                self.stand()
            if key=='a':
                self.right()
            if key=='j':
                self.jump_forward()
            if key=='x':
                self.back()
            if key=='e':
                self.left_turn()
            if key=='q':
                self.right_turn()
            if key=='k':
                self.up()
                
            if (key == 'c'):
                break

                

        # except:
        #     print ("eror")

        # finally:
        #     positions=[0,0,0,0,0,0,0,0,0,0,0,0]
        #     self.publish_joint(positions)
        #     self.rate.sleep()

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            


if __name__=="__main__":
 
    g=Gait()
    g.controller()
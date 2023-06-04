#!/usr/bin/env python3
import rospy

from std_msgs.msg import Float64

import sys, select, termios, tty

msg = """
Control Your Toy!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly
CTRL-C to quit
"""

moveBindings = {
        'i':(1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(-1,0),
        '.':(-1,1),
        'm':(-1,-1),
           }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
          }

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = 8
turn = 0.5

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('turtlebot_teleop')

    back_right_thigh = rospy.Publisher('/quad_robo/brt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    back_right_leg = rospy.Publisher('/quad_robo/brl_position_controller/command', Float64, queue_size=10)
    back_right_shin= rospy.Publisher('/quad_robo/brs_position_controller/command', Float64, queue_size=10)
    
    back_left_thigh = rospy.Publisher('/quad_robo/blt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    back_left_leg = rospy.Publisher('/quad_robo/bll_position_controller/command', Float64, queue_size=10)
    back_left_shin= rospy.Publisher('/quad_robo/bls_position_controller/command', Float64, queue_size=10)

    front_left_thigh = rospy.Publisher('/quad_robo/flt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    front_left_leg = rospy.Publisher('/quad_robo/fll_position_controller/command', Float64, queue_size=10)
    front_left_shin= rospy.Publisher('/quad_robo/fls_position_controller/command', Float64, queue_size=10)

    front_right_thigh = rospy.Publisher('/quad_robo/frt_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    front_right_leg = rospy.Publisher('/quad_robo/frl_position_controller/command', Float64, queue_size=10)
    front_right_shin= rospy.Publisher('/quad_robo/frs_position_controller/command', Float64, queue_size=10)

 
    try:
        print (msg)
        print (vels(speed,turn))
        while(1):
            key = getKey()
            # print(key)
            if (key == '\x03'):
                break
            val=0
            val1=-0.7
            val2=1.50

            # val=0
            # val1=0
            # val2=0

            back_right_thigh.publish(val) # publish the turn command.
            back_right_leg.publish(val1) # publish the turn command.
            back_right_shin.publish(val2) # publish the control speed. 
            
            front_right_thigh.publish(val) # publish the turn command.
            front_right_leg.publish(val1) # publish the turn command.
            front_right_shin.publish(val2) # publish the control speed. 

            back_left_thigh.publish(val) # publish the turn command.
            back_left_leg.publish(val1) # publish the turn command.
            back_left_shin.publish(val2) # publish the control speleft

            front_left_thigh.publish(val) # publish the turn command.
            front_left_leg.publish(val1) # publish the turn command.
            front_left_shin.publish(val2) # publish the control speed. 
    except:
        print (e)

    finally:
        print("Errro")
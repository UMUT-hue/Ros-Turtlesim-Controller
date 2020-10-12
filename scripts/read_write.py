#!/usr/bin/env python
import rospy
import redis
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from threading import Thread
import time

global x , y, theta, linearVelocity, angularVelocity 
x , y, theta, linearVelocity, angularVelocity = '', '', '', '', ''

def callback_pose(msg):
    global x , y, theta, linearVelocity, angularVelocity 
    x = msg.x
    y = msg.y
    theta = msg.theta
    linearVelocity = msg.linear_velocity
    angularVelocity = msg.angular_velocity

def write():
    global x , y, theta, linearVelocity, angularVelocity 
    while True:
        r.rpush("incoming_messages", "{},{},{},{},{}".format(x, y, theta, linearVelocity, angularVelocity))
        # print("{},{},{},{},{}".format(x, y, theta, linearVelocity, angularVelocity))
        
def read():
    while True:
        outgoing_msg = r.rpop('outgoing_messages')
        if outgoing_msg is None:
            time.sleep(0.1)
        else:
            outgoing_msg = outgoing_msg.decode()
            msg = Twist()
            if outgoing_msg == "forward":
                print("forward")
                msg.linear.x = 2.0
                pub.publish(msg)
                rate.sleep()
            elif outgoing_msg == "back":
                print("back")
                msg.linear.x = -2.0
                pub.publish(msg)
                rate.sleep()
            elif outgoing_msg == "left":
                print("left")
                msg.angular.z = 2.0
                pub.publish(msg)
                rate.sleep()
            elif outgoing_msg == "right":
                print("right")
                msg.angular.z = -2.0
                pub.publish(msg)
                rate.sleep()
            elif outgoing_msg == "close":
                break

if __name__ == "__main__":
    rospy.init_node("read_write", anonymous=True)
    rospy.Subscriber("/turtle1/pose", Pose, callback_pose)
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist , queue_size=10)
    rate = rospy.Rate(10)
    # rospy.spin()
    r = redis.Redis()
    th = Thread(target=read)
    th.start()
    write()

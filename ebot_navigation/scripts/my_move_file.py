#!/usr/bin/env python

import rospy
import actionlib
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
import math

from math import radians, pi
global move_base
global x
global y
x = 0
y = 0
global i 
i = 0

def odom_callback(data):
    global x 
    global y
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

def MoveBaseSquare():
    global i
    rospy.init_node('nav_test', anonymous=False)

    sub = rospy.Subscriber('/odom', Odometry, odom_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    velocity = Twist()   
        
    # Create a list to hold the waypoint poses
    waypoints1 = list()
    waypoints2 = list()
    # Append each of the four waypoints to the list.  Each waypoint
    # is a pose consisting of a position and orientation in the map frame.
    waypoints1 = [-9.1, 10.7,  12.6, 18.2, -2]
    waypoints2 = [-1.2, 10.5, -1.6, -1.4, 4]    

        
        # Subscribe to the move_base action server
    move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
    rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
    move_base.wait_for_server(rospy.Duration(60))
        
    rospy.loginfo("Connected to move base server")
    rospy.loginfo("Starting navigation test")
    goal = MoveBaseGoal()
            
            # Use the map frame to define goal poses
    goal.target_pose.header.frame_id = 'map'
            
            # Set the time stamp to "now"
    goal.target_pose.header.stamp = rospy.Time.now()
            
            # Set the goal pose to the i-th waypoint
    goal.target_pose.pose.position.x = waypoints1[i]
    goal.target_pose.pose.position.y = waypoints2[i]
    goal.target_pose.pose.orientation.w = 1.0
            
            # Start the robot moving toward the goal
    move_base.send_goal(goal)
            

        # Cycle through the 5 waypoints
    while i < 5 and not rospy.is_shutdown():

        distance = math.sqrt(math.pow((waypoints1[i] - x),2)+math.pow((waypoints2[i] - y),2))
        if i == 2 :
            dis = distance
        if i == 2 and dis < 0.3:
            velocity.angular.z = 0.65
            pub.publish(velocity)
            
        if distance < 0.3:
            
            i += 1
            move_base.cancel_goal()
            rospy.loginfo("Goal succeeded!")
                
                # Use the map frame to define goal poses
            goal.target_pose.header.frame_id = 'map'
                
                # Set the time stamp to "now"
            goal.target_pose.header.stamp = rospy.Time.now()
                
                # Set the goal pose to the i-th waypoint
            goal.target_pose.pose.position.x = waypoints1[i]
            goal.target_pose.pose.position.y = waypoints2[i]
            goal.target_pose.pose.orientation.w = 1.0
                
                # Start the robot moving toward the goal
            move_base.send_goal(goal)

        elif i > 4:
            break

        else:
            pass
    
    rospy.spin()

if __name__ == '__main__':
    try:
        MoveBaseSquare()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

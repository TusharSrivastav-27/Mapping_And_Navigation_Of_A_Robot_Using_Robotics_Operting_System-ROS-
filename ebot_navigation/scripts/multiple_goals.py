#!/usr/bin/env python

import rospy
import actionlib
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

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
        
    # Create a list to hold the waypoint poses
    waypoints1 = list()
    waypoints2 = list()
    # Append each of the four waypoints to the list.  Each waypoint
    # is a pose consisting of a position and orientation in the map frame.
    waypoints1 = [-9.7, 10.7, 12.6, 18.2, -2]
    waypoints2 = [-1.2, 10.5, -1.9, -1.4, 4]    

    check1 = list()
    check2 = list()
    check1 = [-9.6, 10.6, 12.4, 18.1, -2]
    check2 = [-1.2, 10.3, -1.9, -1.2, -3.7]

        # Publisher to manually control the robot (e.g. to stop it)
        
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
    move(goal)
            

        # Cycle through the 5 waypoints
    while i <=4 and not rospy.is_shutdown():
        
        if abs(x)>=abs(check1[i]) and abs(y)>=abs(check2[i]):
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
            move(goal)
                
        else:
            pass
    
        
def move(goal):
    global i
    move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        # Send the goal pose to the MoveBaseAction server
    move_base.send_goal(goal)

    waypoints1 = [-9.7, 10.7, 12.6, 18.2, -2]
    waypoints2 = [-1.2, 10.5, -1.9, -1.4, 4]    
            
    if abs(x) >=abs(waypoints1[i]):
        move_base.cancel_goal()
        rospy.loginfo("Goal succeeded!")
                    



if __name__ == '__main__':
    try:
        MoveBaseSquare()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
#!/usr/bin/env python3


'''
This is a boiler plate script that contains hint about different services that are to be used
to complete the task.
Use this code snippet in your code or you can also continue adding your code in the same file


This python file runs a ROS-node of name offboard_control which controls the drone in offboard mode.
See the documentation for offboard mode in px4 here() to understand more about offboard mode
This node publishes and subsribes the following topics:

	 Services to be called                   Publications                                          Subscriptions
	/mavros/cmd/arming                       /mavros/setpoint_position/local                       /mavros/state
    /mavros/set_mode                         /mavros/setpoint_velocity/cmd_vel                     /mavros/local_position/pose


'''

import rospy
from geometry_msgs.msg import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *


class offboard_control:

    def __init__(self):
        # Initialise rosnode
        rospy.init_node('offboard_control', anonymous=True)

        # self.velocity_publisher = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', queue_size=10)

        # self.pose_subscriber = rospy.Subscriber('/mavros/local_position/pose',Pose, self.update_pose)
        # /mavros/setpoint_velocity/cmd_vel                     /mavros/local_position/pose
        
    
    def setArm(self):
        # Calling to /mavros/cmd/arming to arm the drone and print fail message on failure
        rospy.wait_for_service('mavros/cmd/arming')  # Waiting untill the service starts 
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool) # Creating a proxy service for the rosservice named /mavros/cmd/arming for arming the drone 
            armService(True)
        except rospy.ServiceException as e:
            print ("Service arming call failed: %s"%e)

        # Similarly delacre other service proxies 

   
    def offboard_set_mode(self):
    
        # rospy.wait_for_service('mavros/set_mode')
        # try:
        #     setModeService = rospy.ServiceProxy('mavros/set_mode', SetMode)
        #     setModeService(0, 'OFFBOARD')
        # except rospy.ServiceException as e:
        #     print ("Service setting mode failed: %s"%e)

        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
            response = flightModeService(custom_mode='OFFBOARD')
            return response.mode_sent
        except rospy.ServiceException as e:
            print
            "service set_mode call failed: %s. Offboard Mode could not be set." % e
            return False

        # Call /mavros/set_mode to set the mode the drone to OFFBOARD
        # and print fail message on failure
    
   
class stateMoniter:
    def __init__(self):
        self.state = State()
        # Instantiate a setpoints message

        
    def stateCb(self, msg):
        # Callback function for topic /mavros/state
        self.state = msg

    # Create more callback functions for other subscribers    


def main():


    stateMt = stateMoniter()
    ofb_ctl = offboard_control()
    ofb_ctl.setArm()
    ofb_ctl.offboard_set_mode()
    # Initialize publishers
    ###############################  https://pastebin.com/0Qig6SRf #########################################
    local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
    # local_vel_pub = rospy.Publisher('mavros/setpoint_velocity/cmd_vel', Twist, queue_size=10)
    local_vel_pub = rospy.Publisher('mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)

    local_raw_pos = rospy.Publisher('mavros/setpoint_raw/local',PositionTarget, queue_size=10)
    # Specify the rate 
    rate = rospy.Rate(20.0)

    
    # Make the list of setpoints 
    setpoints = [] #List to setpoints

    # Similarly initialize other publishers 

    # Create empty message containers 
    pos =PoseStamped()
    pos.pose.position.x = 0
    pos.pose.position.y = 0
    pos.pose.position.z = 0

    rpos = PositionTarget()
    rpos.type_mask = 4035 #0b0000101111100011
    rpos.header.frame_id = "home"
    rpos.header.stamp = rospy.Time.now()
    rpos.coordinate_frame = 1
    rpos.position.z = 10

    rpos.position.y = 0
    rpos.position.x = 0

    rpos.velocity.x = 0
    rpos.velocity.y = 0
    rpos.position.z = 2
    
    # rospy._takeoff(rpos)


    # Set your velocity here
    vel = Twist()
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    
    # Similarly add other containers 

    # Initialize subscriber 
    rospy.Subscriber("/mavros/state",State, stateMt.stateCb)

    # Similarly initialize other subscribers 


    '''
    NOTE: To set the mode as OFFBOARD in px4, it needs atleast 100 setpoints at rate > 10 hz, so before changing the mode to OFFBOARD, send some dummy setpoints  
    '''
    for i in range(100):
        local_pos_pub.publish(pos)
        rate.sleep()


    # Arming the drone
    while not stateMt.state.armed:
        ofb_ctl.setArm()
        rate.sleep()
    print("Armed!!")

    # Switching the state to auto mode
    while not stateMt.state.mode=="OFFBOARD":
        ofb_ctl.offboard_set_mode()
        rate.sleep()
    print ("OFFBOARD mode activated")

    # Publish the setpoints 
    while not rospy.is_shutdown():
        '''
        Step 1: Set the setpoint 
        Step 2: Then wait till the drone reaches the setpoint, 
        Step 3: Check if the drone has reached the setpoint by checking the topic /mavros/local_position/pose 
        Step 4: Once the drone reaches the setpoint, publish the next setpoint , repeat the process until all the setpoints are done  


        Write your algorithm here 
        '''

        # telem = get_telemetry(frame_id='navigate_target')
        # telem.x
        # rospy.x
        # rospy.current_position.x



        local_pos_pub.publish(pos)
        local_vel_pub.publish(vel)
        local_raw_pos.publish(rpos)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

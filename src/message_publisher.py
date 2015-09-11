#!/usr/bin/python

import rospy
from my_message_package.msg import Odometry as MyOdometry
from nav_msgs.msg import Odometry

if __name__ == "__main__":
    rospy.init_node('message_publisher')
    pubm = rospy.Publisher('~myodom', MyOdometry, queue_size=10)
    pubn = rospy.Publisher('~odom', Odometry, queue_size=10)

    index = 0
    r = rospy.Rate(100)
    while not rospy.is_shutdown():
        msg = MyOdometry()
        msg.flag = index
        msg.info = 'info for #{} msg'.format(index)
        msg.odom.header.stamp = rospy.Time.now()
        msg.odom.header.frame_id = 'my_frame_id'
        msg.odom.pose.pose.position.x = 0.1 * index
        msg.odom.pose.pose.position.y = -0.1 * index
        msg.odom.pose.pose.position.z = 0.0
        msg.odom.pose.pose.orientation.w = 1.0
        msg.odom.pose.pose.orientation.x = 0.0
        msg.odom.pose.pose.orientation.y = 0.0
        msg.odom.pose.pose.orientation.z = 0.0

        pubm.publish(msg)
        pubn.publish(msg.odom)

        r.sleep()

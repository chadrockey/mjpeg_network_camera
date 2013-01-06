#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import roslib; roslib.load_manifest("mjpeg_network_camera")
import rospy
import std_srvs.srv as std_srvs
from sensor_msgs.msg import CompressedImage
import httplib2

rospy.init_node('polled_network_camera')
pub = rospy.Publisher('/camera/image/compressed', CompressedImage)

host = rospy.get_param('~host', '192.168.2.1')
request = rospy.get_param('~request', '/?action=snapshot')
frame_id = rospy.get_param('~frame_id', '/camera')
rate = float(rospy.get_param('~rate', 5.0))

http = httplib2.Http()

def grabFrame(event):
   msg = CompressedImage()
   msg.header.frame_id = frame_id
   msg.format = "jpeg"
   resp, msg.data = http.request("http://" + host + request)
   msg.header.stamp = rospy.Time.now()
   pub.publish(msg)

def grabFrameService(req):
	grabFrame(None)
	return std_srvs.EmptyResponse()

s = rospy.Service('/camera/grab_frame', std_srvs.Empty, grabFrameService)

if(rate > 0.001):
	rospy.Timer(rospy.Duration(1.0/rate), grabFrame)

rospy.spin()
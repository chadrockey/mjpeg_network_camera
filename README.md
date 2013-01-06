mjpeg_network_camera
====================

ROS driver for mjpeg and jpeg network cameras such as the Trek AI Ball.

---

Usage (all parameters are optional unless difference that defaults):
polled_camera.py _host:=192.168.2.1 _request:=/?action=snapshot _frame_id:=/camera _rate:=5.0

This node reads from a jpeg image response.  On the Trek AI ball, this location is: http://192.168.2.1/?action=snapshot.  This returns a single jpeg frame.

This node publishes on /camera/image/compressed.  It also exposes a service to grab and publish a frame on /camera/grab_frame

---

streamed_camera.py _host:=192.168.2.1 _port:=80 _request:=/?action=stream _frame_id:=/camera

This node connects to an mjpeg and publishes individal frames as ROS messages.

This node publishes on /camera/image/compressed

---

Viewing images

To view images, try: rosrun image_view image_view image:=/camera/image compressed

This requires image_transport_plugins to be installed.

---

Converting from sensor_msgs/CompressedImage to sensor_msgs/Image

Try: rosrun image_transport republish compressed in:=/camera/image out:=/full/image

This requires image_transport_plugins to be installed.

Note that camera_info is not published.  If people find use in this node, I can add the use of the python camera info manager library.
## AR Follower by AR Parrot 1.0 Quadcopter ##

This repository contains a code which works with ROS

This will let a AR Parrot 1.0 quadcopter follow the biggest AR tag detected by ar_recog.

Comments are in french.

### Dependencies ###

* Tested with ROS Fuerte Turtle
* Tested with [ardrone_brown](http://brown-ros- pkg.googlecode.com/svn/trunk/experimental/ardrone_brown)
  * Driver for AR Parrot 1.0
* [ar_recog](http://brown-ros- pkg.googlecode.com/svn/trunk/experimental/ar_recog)
  * Package for tracking the AR Tags

### Compilation ###

Make sure to put this repository in your sandbox folder and then:
* cmake .
* rosmake

### Launch ###

First, make sure ROS Core, ardrone brown and ar recog are running

Launch the algorithm: rosrun algorithm algorithm.py

Open a new terminal and:

To takeoff: rostopic pub -1 /ardrone/takeoff std_msgs/Empty

To land: rostopic pub -1 /ardrone/land std_msgs/Empty

### YouTube Videos ###

* [Clip 1](https://www.youtube.com/watch?v=Ggx_qCZsTa4)
* [Clip 2](https://www.youtube.com/watch?v=sqjcU5k1IpE)

### Improvements ###

* Use ardrone_autonomy driver for better performance
* Add elevation/height control for tag following
* Use with AR Parrot 2.0 for improved tag tracking (Better camera)

### Documentation ###

* [ardrone_brown](https://code.google.com/p/brown-ros-pkg/wiki/ardrone_brown)
* [ar_recog](https://code.google.com/p/brown-ros-pkg/wiki/ar_recog)

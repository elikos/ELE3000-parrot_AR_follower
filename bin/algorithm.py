#!/usr/bin/env python
import rospy
import roslib; roslib.load_manifest('algorithm')

# Importer les marqueurs
from ar_recog.msg import Tag, Tags
from geometry_msgs.msg import Twist
from time import time
from std_msgs.msg import Empty

class Delta:
	def __init__(self):
		self.old_speed = 0
		self.old_value = 0
		self.old_time = 0
 
	def get_velocity(self, new_value):
		new_time = time()
 
		# Vitesse = Distance/Temps
		speed = (new_value - self.old_value) / (new_time - self.old_time)
 
		# Pour avoir une variation de vitesse lente
		self.old_speed = self.old_speed + (speed - self.old_speed) * 0.1
		self.old_time = new_time
		self.old_value = new_value
 
		# Retourne la vitesse
		return self.old_speed
 
distance = Delta()
yRot = distance

# Lecture des marqueurs
def handleTags(msg):
	global pub
	global lastSeen
 
	twist = Twist()
	width = msg.image_width
	height = msg.image_height
 	biggest = Tag()

	# Recherche du marqueur le plus proche (ici diameter est la distance)
	for tag in msg.tags:
		if (tag.diameter > biggest.diameter):
			biggest = tag # Marqueur le plus proche
 
	if biggest.diameter == 0:
		twist.linear.x = 0
		# Faire tourner en rond le drone
		if (time() - lastSeen > .5):
			twist.angular.z = .5
		pub.publish(twist)
 
		# Réinitialiser a 0 au cas où on trouve un marqueur sur la prochaine image
		distance.get_velocity(0)
		yRot.get_velocity(0)
		return
 
	lastSeen = time()
 
	# Direction en x, on veut essayer de s'arrêter a stopping_dist
	stopping_dist = 5000.
	dist = (biggest.distance - stopping_dist) / stopping_dist

	dist_vel = distance.get_velocity(dist)

	if abs(dist) < 0.25:
		# Si on est proche de stopping_distance, on ralenti brusquement
		twist.linear.x = dist_vel * 0.2
	else:
		# Sinon on avance ou recule vers stopping_distancet
		twist.linear.x = dist * 0.25
	print twist.linear.x # Affiche sur le terminal la vitesse envoyé au drone
	
	# Limite la vitesse maximale du drone	
	twist.linear.x = max(0.03, min(0.05, twist.linear.x))
 
	# Algorithme pour se placer devant le marqueur (Gauche/Droite)
	yRot_velocity = yRot.get_velocity(biggest.yRot)
	if abs(biggest.yRot) < 0.5:
		# Si on presque devant, on ralenti brusquement la vitesse
		twist.linear.y = yRot_velocity * 0.2
	else:
		# Sinon, on va à gauche ou à droite
		twist.linear.y = biggest.yRot * 0.25

	# Limite la vitesse angulaire du drone
	twist.linear.y = max(-0.05, min(0.05, twist.linear.y))
 
	# Détecte l'orientation du marqueur
	cx = 0
	for i in [0,2,4,6]:
		cx = cx + biggest.cwCorners[i]
	cx = cx/4./width

	# Rotation du drone pour se placer perpendiculairement devant le marqueur
	twist.angular.z = (-(cx - .5)/.5)
 

	pub.publish(twist)
	print twist

if __name__ == "__main__":
	global lastSeen
	global pub
 
	lastSeen = 0
	rospy.init_node('algorithm', anonymous=True)
	pub = rospy.Publisher('cmd_vel', Twist)
	rospy.Subscriber("tags", Tags, handleTags)
	# Recommancer ce code jusqu'à ce que l'on arrête	
	rospy.spin()

import bge, json
from bge.logic import globalDict
from random import choice, random
from pprint import pprint
from ast import literal_eval as litev

if not 'player_active' in globalDict.keys():
	globalDict['player_active'] = False

def init(cont):
	""" Initializes the character. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	autostart = cont.sensors['autostart'].positive
	
	# Actuators
	track_to = cont.actuators['track_to']
	
	# Objects
	track_direction = own.childrenRecursive['track_direction']
	
	# Properties
	
	#### INITIALIZE ####
	if autostart:
		
		if track_to.object == None:
			track_to.object = track_direction
			
		cont.activate(track_to)
		
		own.childrenRecursive['char_mesh'].color[0] = random()
		
		own.childrenRecursive['camera_smooth'].timeOffset = 5
		
		if not globalDict['player_active']:
			scene.active_camera = own.childrenRecursive['camera_char']
			own['is_player'] = True
			globalDict['player_active'] = True
			
	pass

def set_direction(cont):
	""" Sets the direction of track object and properties of character. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	always = cont.sensors['always'].positive
	up = cont.sensors['up'].positive
	down = cont.sensors['down'].positive
	left = cont.sensors['left'].positive
	right = cont.sensors['right'].positive
	run = cont.sensors['run'].positive
	
	# Actuators
	track_to = cont.actuators['track_to']
	
	# Objects
	track_direction = own.childrenRecursive['track_direction']
	directions = [obj for obj in own.childrenRecursive if obj.name.startswith('dir_')]
	
	if len(directions) > 0:
		new_dic = {}
		for obj in directions:
			new_dic[obj.name] = obj
		directions = new_dic
	
	# Properties
	
	#### INITIALIZE ####
	
	if not run:
		own['run'] = False
		
	if not up and not down and not left and not right or up and down or left and right:
		own['walk'] = False
		own['run'] = False
		
	if up and not down or not up and down or left and not right or not left and right:
		own['walk'] = True
		
		if run:
			own['run'] = True
		
	if up and not down:
		
		if not left and not right:
			track_direction.worldPosition = directions['dir_U'].worldPosition
		
		elif left and not right:
			track_direction.worldPosition = directions['dir_UL'].worldPosition
		
		elif not left and right:
			track_direction.worldPosition = directions['dir_UR'].worldPosition
			
	if not up and down:
		
		if not left and not right:
			track_direction.worldPosition = directions['dir_D'].worldPosition
		
		elif left and not right:
			track_direction.worldPosition = directions['dir_DL'].worldPosition
		
		elif not left and right:
			track_direction.worldPosition = directions['dir_DR'].worldPosition
		
	if not up and not down:
		
		if left and not right:
			track_direction.worldPosition = directions['dir_L'].worldPosition
		
		elif not left and right:
			track_direction.worldPosition = directions['dir_R'].worldPosition
			
	pass

def mov_anim(cont):
	""" Moves the character and animates its armature. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	autostart = cont.sensors['autostart'].positive
	is_walk = cont.sensors['is_walk'].positive
	is_run = cont.sensors['is_run'].positive
	
	# Actuators
	motion = cont.actuators[0]
	
	# Objects
	char_armature = own.childrenRecursive['char_armature']
	
	# Properties
	LOOP = bge.logic.KX_ACTION_MODE_LOOP
	blend_in = 5
	motion_vec = [0, 0, 0]
	motion_spd = -0.07
	
	#### INITIALIZE ####
	if autostart:
		
		if not is_walk:
			char_armature.playAction('character', 0, 120, blendin=blend_in, play_mode=LOOP)
			motion_vec[1] = 0
		
		elif is_walk and not is_run:
			char_armature.playAction('character', 130, 145, blendin=blend_in, play_mode=LOOP)
			motion_vec[1] = motion_spd
			
		elif is_walk and is_run:
			char_armature.playAction('character', 150, 165, blendin=blend_in, play_mode=LOOP)
			motion_vec[1] = motion_spd * 2
			
		motion.dLoc = motion_vec
		cont.activate(motion)
		
	pass

def camera_collision(cont):
	""" Avoids the camera to pass through objects. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	always = cont.sensors['always'].positive
	
	# Objects
	camera = own.childrenRecursive['camera_char']
	axis = own.childrenRecursive['camera_axis']
	origin = own.childrenRecursive['camera_origin']
	
	# Properties
	dist = axis.getDistanceTo(origin)
	ray = own.rayCast(origin, axis, dist)
	
	#### INITIALIZE ####
	if always:
		
		if ray[0] != None:
			camera.worldPosition = ray[1]
			
		elif ray[0] == None:
			camera.worldPosition = origin.worldPosition
			
			

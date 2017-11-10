import bge, json
from bge.logic import globalDict
from random import choice, random
from pprint import pprint
from ast import literal_eval as litev

def cam_skybox(cont):
	""" Generates a random city, using a pre made set of rules. """
	
	own = cont.owner
	scene = own.scene
	active_scenes = bge.logic.getSceneList()
	
	# Sensors
	sensor = cont.sensors[0].positive
	
	# Properties
	
	#### INITIALIZE ####
	if sensor:
		
		if 'game' in active_scenes:
			own.worldOrientation = active_scenes['game'].active_camera.worldOrientation
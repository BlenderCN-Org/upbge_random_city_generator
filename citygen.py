import bge, json
from bge.logic import globalDict
from bge.render import setMipmapping
from random import choice, random
from pprint import pprint
from ast import literal_eval as litev

# Initialize globalDict
if not 'map' in globalDict.keys():
	globalDict['map'] = {}
	
if not 'player_active' in globalDict.keys():
	globalDict['player_active'] = False
	
def gen_coords(cont):
	""" Generates the coordinates of the active camera. Helper for the scenery dynamic loading. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	sensor = cont.sensors[0].positive
	
	# Properties
	camera = scene.active_camera
	
	#### INITIALIZE ####
	if sensor:
		
		cam_pos = camera.worldPosition
		coords = ( int((cam_pos.x//100*100)), int((cam_pos.y//100*100)), 0 )
		
		own['current_coords'] = str(coords)
		
		if own['current_coords'] in globalDict['map'].keys():
			print('Current type is', globalDict['map'][own['current_coords']]['type'])
			
		else:
			print(own['current_coords'], 'not in map')
	
	pass

def gen_city(cont):
	""" Generates a random city, using a pre made set of rules. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	sensor = cont.sensors[0].positive
	
	# Properties
	max_x = own['max_x'] * 100
	max_y = own['max_y'] * 100
	streets = ('DL', 'DLR', 'DR', 'LR', 'UD', 'UDL', 'UDLR', 'UDR', 'UL', 'ULR', 'UR', 'N')
	
	#### INITIALIZE ####
	if sensor:
		
		setMipmapping(False)
		
		scene.active_camera.worldPosition = (max_x/2, -max_y/2, 200)
		
		if not globalDict['player_active']:
			character = scene.addObject('character')
			character.groupMembers['char_collision'].worldPosition = (max_x/2, -max_y/2, 1)
		
		### Generates the given number of streets ###
		for x in range(0, max_x, 100):
			
			### Add streets at Y axis of current X street ###
			for y in range(0, max_y, 100):
				
				cur_street = {'position' : (x, -y, 0), 'type' : 'UD'}
				
				if cur_street['position'][1] == 0:
					
					if cur_street['position'][0] == 0:
						
						cur_street['type'] = choice([i for i in streets if 'D' in i or 'R' in i and not 'N' in i])
						own['last_added'] = str(cur_street)
						cur_street['position'] = (x, 0, 0)
						own['current_top'] = str(cur_street)
						
					elif cur_street['position'][0] > 0:
						
						cur_left = globalDict['map'][str((x-100, 0, 0))]
						possible_streets = []
						
						if 'R' in cur_left['type']:
							possible_streets = [i for i in streets if 'L' in i]
							
						elif not 'R' in cur_left['type']:
							possible_streets = [i for i in streets if not 'L' in i]
						
						cur_street['position'] = (x, 0, 0)
						cur_street['type'] = choice(possible_streets)
						own['current_top'] = str(cur_street)
						own['current_left'] = str(cur_left)
						own['last_added'] = str(cur_street)
						
				elif cur_street['position'][1] < 0:
					
					if cur_street['position'][0] == 0:
						
						possible_streets = []
						last_added = litev(own['last_added'])
						
						if 'D' in last_added['type']:
							possible_streets = [i for i in streets if 'U' in i and not 'N' in i]
							
						if not 'D' in last_added['type']:
							possible_streets = [i for i in streets if not 'U' in i]
							
						cur_street['type'] = choice(possible_streets)
						own['last_added'] = str(cur_street)
						
					if cur_street['position'][0] > 0:
						
						cur_left = globalDict['map'][str((x-100, -y, 0))]
						possible_streets = []
						last_added = litev(own['last_added'])
						
						if 'D' in last_added['type'] and not 'R' in cur_left['type']:
							possible_streets = [i for i in streets if 'U' in i and not 'L' in i and not 'N' in i]
							
						if not 'D' in last_added['type'] and 'R' in cur_left['type']:
							possible_streets = [i for i in streets if not 'U' in i and 'L' in i and not 'N' in i]
							
						if 'D' in last_added['type'] and 'R' in cur_left['type']:
							possible_streets = [i for i in streets if 'U' in i and 'L' in i and not 'N' in i]
							
						if not 'D' in last_added['type'] and not 'R' in cur_left['type']:
							possible_streets = [i for i in streets if not 'U' in i and not 'L' in i]
							
						cur_street['type'] = choice(possible_streets)
						own['last_added'] = str(cur_street)
					
				else:
					cur_street['type'] = 'N'
					
				### Add current street to globalDict and continue iteration
				globalDict['map'][str(cur_street['position'])] = cur_street
				
		### Add streets from globalDict to scene ###
		for obj in globalDict['map'].values():
			
			added = scene.addObject(obj['type'] + '_group')
			
			for i in added.groupMembers:
				i.setParent(added, 0, 0)
			
			added.worldPosition = obj['position']
			
	pass

def spawn_building(cont):
	
	""" Spawn buildings at specific spots. """
	
	own = cont.owner
	scene = own.scene
	
	# Sensors
	sensor = cont.sensors[0].positive
	
	# Properties
	buildings = ('building_01', 'building_02', 'building_03', 'building_04', 'building_05', 'house_01', 'house_02', 'house_03', 'house_04', 'house_05', 'house_06', 'house_07', 'house_08', 'house_09', 'house_10', 'house_11', 'house_12', 'house_13')
	fences = ('fence_01', 'fence_02', 'fence_03', 'fence_04', 'fence_05', 'fence_06')
	
	# Objects
	street = own.groupObject.groupMembers[own.groupObject.name.replace('_group', '')]
	
	#### INITIALIZE ####
	if sensor:
		
		# Add random building at spawner position
		building = scene.addObject(choice(buildings), own)
		
		fence = scene.addObject(choice(fences), own)
		
		# Set building to random color
		building.color[0] = random()
		fence.color[0] = random()
		
		# Warning message
		print('Added', building.name, 'at', tuple(building.worldPosition), 'with hue', building.color[0].__round__(2))

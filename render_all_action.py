import bpy

'''
################ AUTHOR ###################
+ Author: anhnam_xtanh
+ Updated: 2019/05/16
+ Scennario: 
implement.blend file have n actions,
each action have m cameras, render automatically

################# NOTE ##################

+ Remove an action:
bpy.data.actions.remove(bpy.data.actions['action name'])

+ Render command
blender -b implement.blend -noaudio -o content/ -P render_all_action.py > /dev/null 2>&1
or
blender implement.blend --background --python render_all_action.py 

+ Choose number of frames that you want to render (add_n_frame)
Default 3 frames. 3+(-1)=2, 3+1= 4, 3+5=8 ....
'''

add_n_frame = [-1,1,5,9,13,29]
# bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.frame_start = 0
for n in add_n_frame:
	bpy.context.scene.frame_end = 2 + n
	obj = bpy.data.objects['Armature']

	for cam_obj in bpy.data.objects:
		if ( cam_obj.type =='CAMERA'):
			bpy.data.scenes['Scene'].camera = cam_obj
			
			#bpy.context.object.data.clip_end = 105
			cam_obj.data.clip_end = 120

			for action in bpy.data.actions:
				# print(action.name)
				if(action.name == "Hand_roll_1" or action.name == "Hand_roll_2" or action.name == "start"):
					pass
				else:
					for fcurve in action.fcurves:
						point = fcurve.keyframe_points[-1]
						point.co.x += n
						point.handle_right.x += n

					obj.animation_data.action = bpy.data.actions.get(action.name)
					print(obj.animation_data.action)

					bpy.context.scene.render.filepath = './synthetic_' + str(n+3)+ '_frames/'  + action.name[:-4] + '/' + action.name+ '_' + cam_obj.name + '_'
					bpy.ops.render.render(use_viewport = True, write_still=True, animation=True)
import unreal

'''
	Summary:
		This is an example of how to work with Sequencer bool keys within sections. It simply flips the value of each present bool key.
		Iterates through all tracks/sections for any bool channels, so make sure the passed test sequence path has bool keys present, such as 
		a Object Binding with a Visibility Track, or checking "Expose to Cinematics" on a Blueprint variable and adding a track for that variable.
		Open the Python interactive console and use:
			import sequencer_key_examples
			sequencer_key_examples.bool_key_example("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - String that points to the Movie Scene sequence asset.
'''
def bool_key_example(sequencer_asset_path):
	# Load the sequence asset
	sequence = unreal.load_asset("/Game/TestKeySequence", unreal.LevelSequence)
	
	# Iterate over object bindings and tracks/sections
	all_tracks = sequence.get_master_tracks()
	
	for object_binding in sequence.get_bindings():
		all_tracks.extend(object_binding.get_tracks())
	
	# Now we iterate through each section and look for Bool channels within each track.
	print("Found " + str(len(all_tracks)) + " tracks, searching for bool channels...")
	num_bool_keys_modified = 0
	for track in all_tracks:
		# Tracks are composed of sections
		for section in track.get_sections():
			# Sections are composed of channels which contain the actual data!
			for channel in section.find_channels_by_type(unreal.MovieSceneScriptingBoolChannel):
				print("Found bool channel in section " + section.get_name() + " for track " + track.get_name() + " flipping values...")
				
				# Channels are often composed of some (optional) default values and keys.
				for key in channel.get_keys():
					key.set_value(not key.get_value())
					num_bool_keys_modified = num_bool_keys_modified + 1
					
	print ("Modified " + str(num_bool_keys_modified) + " keys!")	
	return

'''
	Summary:
		This is an example of how to work with Sequencer byte and integer keys within sections. This example simply adds the amount specified in the parameter
		to each key. This example only iterates through Object Bindings in a sequence so please expose an Integer/Byte property to an Actor, then add a binding
		to that actor and add several keys.
		Open the Python interactive console and use:
			import sequencer_key_examples
			sequencer_key_examples.int_byte_key_example("/Game/TestSequence", 25)
		
	Params:
		sequencer_asset_path - String that points to the Movie Scene sequence asset.
		amount_to_add - Integer that specifies the value to add to each key.
'''
def int_byte_key_example(sequencer_asset_path, amount_to_add = 5): 
	# Load the sequence asset
	sequence = unreal.load_asset("/Game/TestKeySequence", unreal.LevelSequence)
	
	# This example assumes you've created a Blueprint or C++ object with Byte/uint8 or Integer/int32 fields that have
	# been marked for interpolation in Cinematics ("Expose to Cinematics" in BP, or UPROPERTY(Interp) in C++) to modify.
	print("Adding the value " + str(amount_to_add) + " to all integer and byte keys in the sequence...")
	num_keys_modified = 0
	for object_binding in sequence.get_bindings():
		for track in object_binding.get_tracks():
			for section in track.get_sections():
				int_channels = section.find_channels_by_type(unreal.MovieSceneScriptingIntegerChannel)
				byte_channels = section.find_channels_by_type(unreal.MovieSceneScriptingByteChannel)
				
				print("Found " + str(len(int_channels)) + " Integer tracks and " + str(len(byte_channels)) + " Byte channels for track " + track.get_name() + " raising values...")
				combined_channels = []
				combined_channels.extend(int_channels)
				combined_channels.extend(byte_channels)
				for channel in combined_channels:
					for key in channel.get_keys():
						key.set_value(key.get_value() + amount_to_add)
						num_keys_modified = num_keys_modified + 1
					
	print("Modified " + str(num_keys_modified) + " + keys! Please note that at this time you will need to modify the structure of the sequence (rearrange track) for the changes to show up in the UI if it is currently open.")
	return
	
'''
	Summary:
		This is an example of how to work with Sequencer within sections. This example has several sub-examples within it so you will need
		to uncomment sections below as desired. This covers how to change the timing of float keys, how to change their values, and how to change
		their tangent data. This iterates through all tracks and object bindings.
		Open the Python interactive console and use:
			import sequencer_key_examples
			sequencer_key_examples.float_key_example("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - String that points to the Movie Scene sequence asset.
'''
def float_key_example(sequencer_asset_path):
	# Load the sequence asset
	sequence = unreal.load_asset("/Game/TestKeySequence", unreal.LevelSequence)
	unreal.log_warning("THIS EXAMPLE REQUIRES MODIFICATION TO SEE ANY CHANGES. SEE CODE.")
	unreal.log_warning("ONCE THE MODIFICATION HAS BEEN APPLIED, USE 'reload(sequencer_key_examples)' BEFORE CALLING THE FUNCTION AGAIN TO SEE THE RESULTS OF THE CHANGE.")
	
	# Float keys are more complicated than the other types of keys because they support weighted tangent data.
	# There are many properties you can set on a key - Value, Interp Mode, Tangent Mode, Arrive/Leave Tangents, Tangent Mode and Tangent Weights

	all_tracks = sequence.get_master_tracks()
	all_float_keys = []
	
	for object_binding in sequence.get_bindings():
		all_tracks.extend(object_binding.get_tracks())
		
	# We're going to go through all tracks and gather their float keys
	for track in all_tracks:
		# Tracks are composed of sections
		for section in track.get_sections():
			# Sections are composed of channels which contain the actual data!
			for channel in section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel):
				keys = channel.get_keys()
				print('Added {0} keys from channel: {1} on section: {2}'.format(len(keys), channel.get_name(), section.get_name()))
				all_float_keys.extend(keys)
	
	# Now we have all float keys in our sequence in all_float_keys, we can now perform a variety of operations on them.
	print("Writing float key properties:")
	for key in all_float_keys:
		print('Time: {0: 6d}:{1:4.3f} Value: {2: 6.2f} InterpMode: {3} TangentMode: {4} TangentWeightMode: {5} ArriveTangent: {6:+11.8f} ArriveTangentWeight: {7:+9.4f}  LeaveTangent: {8:+11.8f} LeaveTangentWeight: {9:+9.4f}'.format(
		key.get_time().frame_number.value, key.get_time().sub_frame, key.get_value(), key.get_interpolation_mode(), key.get_tangent_mode(), key.get_tangent_weight_mode(), key.get_arrive_tangent(), key.get_arrive_tangent_weight(), key.get_leave_tangent(), key.get_leave_tangent_weight())
		)
	
	# Time is the tick that the key is stored on. Sequences have a Display Rate (ie: 30fps) and an internal tick resolution (ie: 24,000).
	# They are easy to convert back and forth; Uncomment the following example to add 15 frames (at the current display rate) to each keys position.
	unreal.log_warning("Uncomment the following line to test moving each float key.")
	#add_time_to_keys(sequence, all_float_keys, 15)
	
	# Value is the floating point value of the key; Uncomment the following to add the value 35 to each float key.
	unreal.log_warning("Uncomment the following line to test adding a value to each float key.")
	#add_value_to_keys(all_float_keys, 35)
	
	# Float keys support changing the Interpolation mode, Tangent Mode, and Tangent Weight Mode, but only under some conditions. 
	# Interpolation Mode specifies how values are interpolated between keys. Your options are RichCurveInterpMode.RCIM_LINEAR, .RCIM_CONSTANT, and .RCIM_CUBIC
	#	Linear and Constant do not respect user-specified tangent data, only Cubic will.
	
	# Tangent Mode specifies how tangents are calculated (if Interpolation Mode is set to Cubic). Your options are RichCurveTangentMode.RCTM_AUTO, .RCTM_USER, and .RCTM_BREAK
	#	Auto does not respect user-specified tangent data. If set to User then both sides of the tangent will be unified and will respect the last set arrive/leave tangent,
	#	if set to Break then it will respect both tangents individually.
	
	# TangentWeightMode specifies how tangent weights are calculated. Your options are RichCurveTangentWeightMode.RCTWM_WEIGHTED_NONE, .RCTWM_WEIGHTED_ARRIVE, .RCTWM_WEIGHTED_LEAVE, and .RCTWM_WEIGHTED_BOTH.
	#	None will fallback to automatically calculated tangent weight values.
	#	Arrive / Leave / Both specifies which of the tangents are respected
	#		- Arrive means only the arrive tangent weight is respected for that key's tangent
	#		- Leave means only the leave tangent weight is respected for that key's tangent
	#		- Both means that both the arrive and leave tangent weight is respected for that key's tangent
	unreal.log_warning("Uncomment the following line to set all keys to Cubic Interpolation with Auto Tangents")
	# set_float_keys_to_cubic_auto(all_float_keys)
	
	# Calculating the Arrive/Leave Tangents and their Weights can be quite complicated depending on the source data they come from.
	# Tangents will only be evaluated and applied if the correct set of Interpolation, Tangent Mode and Tangent Weight Mode are applied.
	#	- Interpolation must be set to Cubic
	#	- Tangent Mode must be set to User or Break
	#	- Tangent Weight Mode can be set to any value
	# In Sequencer, the Arrive/Leave Tangents 
	#	- Represent the geometric tangents in the form of "tan(y/x)" where y is the key's value and x is the seconds
	#	- Seconds is relative to the key, not to the beginning of the sequence.
	#	- Value is relative to the key's value, not absolute
	# In Sequencer, the Arrive/Leave Tangent Weights
	#	- Represent the length of the hypotenuse in the form of "sqrt(x*x+y*y)" using the same definitions for x and y as before.
	unreal.log_warning("Uncomment the following line to halve the tangent weights, make sure you have keys with Cubic Interpolation, User/Break Tangent Mode, and Both Tangent Weight Mode.")
	#halve_tangent_weights(all_float_keys)
	return
	
'''
	Summary:
		This is an example of how to set string keys with Sequencer within sections. This sample assumes you have an object binding with a FString exposed to Cinematics
		Open the Python interactive console and use:
			import sequencer_key_examples
			sequencer_key_examples.string_key_example("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - String that points to the Movie Scene sequence asset.
'''
def string_key_example(sequencer_asset_path):
	# Load the sequence asset
	sequence = unreal.load_asset("/Game/TestKeySequence", unreal.LevelSequence)
	
	# This example assumes you've created a Blueprint or C++ object with a String field that has
	# been marked for interpolation in Cinematics ("Expose to Cinematics" in BP, or UPROPERTY(Interp) in C++) to modify.
	print("Modifying the string value on all string keys in the sequence...")
	for track in all_tracks:
		# Tracks are composed of sections
		for section in track.get_sections():
			# Sections are composed of channels which contain the actual data!
			for channel in section.find_channels_by_type(unreal.MovieSceneScriptingStringChannel):
				print("Found string  channel in section " + section.get_name() + " for track " + track.get_name() + " modifying values...")
				
				# Channels are often composed of some (optional) default values and keys.
				for key in channel.get_keys():
					key.set_value(key.get_value() + "_Modified!")
					num_bool_keys_modified = num_bool_keys_modified + 1
					
	print("Modified " + str(num_keys_modified) + " + keys! Please note that at this time you will need to modify the structure of the sequence (rearrange track) for the changes to show up in the UI if it is currently open.")
	return

'''
	Summary:
		This is an example of how to add keys to a section. This example will iterate through all bool tracks/sections/channels and insert a new key with a flipped value at half the time.
		This assumes that you have a bool track (such as a Visibility track on an Object Binding) with a key on it that has a non-zero time already on it.
		
		Open the Python interactive console and use:
			import sequencer_key_examples
			sequencer_key_examples.add_key_example("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - String that points to the Movie Scene sequence asset.
'''
def add_key_example(sequencer_asset_path):
	print("This example inserts a new key at half the current key's time with the opposite value as the current key. Assumes you have bool keys in an object binding!")
	
	# Create a test sequence for us to use.
	sequence = unreal.load_asset("/Game/TestKeySequence", unreal.LevelSequence)
	
	# Iterate over the Object Bindings in the sequence as they're more likely to have a track we can test with.
	for binding in sequence.get_bindings():
		for track in binding.get_tracks():
			print(track)
			for section in track.get_sections():
				print("\tSection: " + section.get_name())

				for channel in section.get_channels():
					print("\tChannel: " + channel.get_name())
					
					keys = channel.get_keys()
					for key in keys:				
						# Calculate a new Frame Number for the new key by halving the current time
						new_time = unreal.FrameNumber(key.get_time(unreal.SequenceTimeUnit.TICK_RESOLUTION).frame_number.value * 0.5)
						# Add a new key to this channel with the opposite value of the current key
						new_key = channel.add_key(new_time, not key.get_value(), 0.0, unreal.SequenceTimeUnit.TICK_RESOLUTION)
						
						# Print out our information. This shows how to convert between the Sequence Tick Resolution (which is the number a key is stored on)
						# and the Display Rate (which is what is shown in the UI) as well.
						new_time_in_display_rate = unreal.TimeManagementLibrary.transform_time(unreal.FrameTime(new_time), sequence.get_tick_resolution(), sequence.get_display_rate())
						print('Inserting a new key at Frame {0}:{1} (Tick {2}) with Value: {3}'.format(
							new_time_in_display_rate.frame_number.value, new_time_in_display_rate.sub_frame, new_time.value, new_key.get_value())
							)
						
	print("Finished!")
	return

def add_time_to_keys(sequence, key_array, time):
	print('Adding {0} frames (time) to {1} keys in array...'.format(time, len(key_array)))
	
	# Initialize a FrameNumber from the given time and then convert it to a FrameTime with no sub-frame. Keys can only exist on whole FrameNumbers.
	time_as_frame_time = unreal.FrameTime(unreal.FrameNumber(time))
	# Now transform from our Display Rate to the internal tick resolution.
	time_as_tick = unreal.TimeManagementLibrary.transform_time(time_as_frame_time, sequence.get_display_rate(), sequence.get_tick_resolution())
	
	# Now we apply the new offset to each key in the array. key.get_time() and key.set_time() can take a frame number in either
	# Display Rate space or Tick Resolution. If you only want keys on whole frames as shown by the UI then you can use Display Rate
	# (which is the default for these functions). However, if you want to put keys on frames between keys you can put one on
	# every tick of the Tick Resolution (sequence.get_tick_resolution()).
	# key.set_key(...) optionally supports using a sub-frame (clamped 0-1) when used in combination with a DISPLAY_RATE time unit.
	# Example:
	#	- set_key(5) 		- Sets the key to frame number 5 at your current display rate. If your sequence is at 30fps this will set you to 5/30, or 1/6th of a second.
	#	- set_key(5, 0.5)	- Sets the key to frame number 5.5. This will not be aligned in the UI and the precision is limited to your sequence's internal tick resolution.
	#	- set_key(5, 0.0, unreal.SequenceTimeUnit.TICK_RESOLUTION) 	- Sets the key to internal tick number 5. If you have a 24,000 tick resolution and a display rate of 30fps this sets it to 5/(24000/30) of a frame, aka 5/800th of a frame at 30fps = 0.00625s in!
	#	- set_key(5, 0.75, unreal.SequenceTimeUnit.TICK_RESOLUTION) - Invalid. Sub-Frames are not supported when using TICK_RESOLUTION. Will print a warning and set the sub-frame to 0.
	#
	# Conversely, key.get_time() can optionally take a uneal.SequenceTimeUnit enum value to determine what resolution to return the time in.
	# get_time() returns a unreal.FrameTime, because a FrameTime contains information about sub-frame values which is important if you've placed
	# a key between frames and want to get that again later.
	#
	# Example:
	#	- get_key()   - Returns the display rate frame of the key (which will match the UI). 
	#					This means "key.set_key(key.get_key().frame_number, key.get_key().sub_frame)" will not have any affect on position as the defaults for both are in the same resolution.
	#	- get_key(unreal.SequenceTimeUnit.DISPLAY_RATE) 	- Returns the internal tick that this key is on with a 0.0 subframe value.
	#														  This means "key.set_key(key.get_key(unreal.SequenceTimeUnit.TICK_RESOLUTION), 0.0, unreal.SequenceTimeUnit.TICK_RESOLUTION)" will not have any affect on position.
	for key in key_array:
		print('CurrentTime: {0} NewTime: {1}'.format(key.get_time().frame_number, key.get_time().frame_number + time))
		key.set_time(key.get_time().frame_number + time, 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE)
	
	print('Finished!')
	return
	
def add_value_to_keys(key_array, value):
	print('Adding {0} to the value of {1} keys...'.format(value, len(key_array)))
	
	for key in key_array:
		key.set_value(key.get_value() + value)
	
	print('Finished!')
	return
	
def set_float_keys_to_cubic_auto(key_array):
	print('Setting values of float keys to cubic/auto for {0} keys...'.format(len(key_array)))
	
	for key in key_array:
		key.set_interpolation_mode(unreal.RichCurveInterpMode.RCIM_CUBIC)
		key.set_tangent_mode(unreal.RichCurveTangentMode.RCTM_AUTO)
	print('Finished!')
	return
	
def halve_tangent_weights(key_array):
	print('Halving the Tangent Weight for {0} keys...'.format(len(key_array)))

	for key in key_array:
		if key.get_interpolation_mode() != unreal.RichCurveInterpMode.RCIM_CUBIC or key.get_tangent_mode() != unreal.RichCurveTangentMode.RCTM_USER or key.get_tangent_weight_mode() != unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_BOTH:
			unreal.log_warning("Skipping setting tangent weight on key due to invalid Interp Mode, Tangent Mode or Weight Mode for this example!")
			continue
		
		key.set_arrive_tangent_weight(key.get_arrive_tangent_weight() / 2)
		key.set_leave_tangent_weight(key.get_leave_tangent_weight() / 2)
		
	print('Finished!')
	return
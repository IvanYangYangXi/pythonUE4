#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Import the Unreal module to gain access to the UObject/UStruct types.
# Import the JSON module to gain access to json export 
import unreal, json, sequencer_key_examples

# Ensure you have enabled both the "Python Editor Script Plugin" and the "SequencerScripting" plugins for these examples to work.

'''
	Summary:
		这是一个通过Python使用Sequencer的Render to Movie API的最小示例。这包括设置输出工作所需的最小设置。
		确保在项目中同时启用了“Python Editor Script Plugin”和“sequencerscript”插件。

		打开Python交互控制台并使用：
			import sequencer_examples
			sequencer_examples.render_movie("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - 指向在渲染时应加载和播放的电影场景 sequence asset的路径字符串。
'''
def render_sequence_to_movie_minimal(sequencer_asset_path):
	# If you do not override all of the settings in the AutomatedLevelSequenceCapture then the other settings are inherited
	# from Unreal's Class Default Object (CDO). Previous versions of Unreal (4.19 and below) stored the Render to Movie UI's settings in config files. Config
	# values are automatically loaded and applied to the CDO when the editor starts up. Unreal 4.20 and above now store the UI settings in a unique
	# instance in the config files, so modifications to the Render to Movie UI will no longer affect the CDO. However, legacy projects that are upgrading
	# from 4.19 to 4.20 may end up with the CDO being modified by their last Render to Movie UI settings. The CDO settings for AutomatedLevelSequenceCapture
	# is stored in /Engine/Saved/Config/<Platform>/EditorSettings.ini under the sections labeled "[/Script/MovieSceneCapture.AutomatedLevelSequenceCapture]", 
	# and "[/Script/LevelSequence.LevelSequenceBurnInOptions]" .
	# If you happen to upgrade your engine and this file persists, then the old settings will be applied by default to the CDO, and thus to the instance created
	# in Python. If you want to ensure that your Python instances come with default settings set via C++ then you should remove that section from the config file
	# on each users machine, or you should override every possible setting via Python (see below).
	
	# Create an instance of UAutomatedLevelSequenceCapture
	capture_settings = unreal.AutomatedLevelSequenceCapture()
	capture_settings.level_sequence_asset = unreal.SoftObjectPath(sequencer_asset_path)
	
	# Invoke Sequencer's Render to Movie. This will throw an exception if a movie render is already
	# in progress, an invalid setting is passed, etc.
	try:
		print("Rendering to movie...")
		unreal.SequencerTools.render_movie(capture_settings)
	except Exception as e:
		print("Python Caught Exception:")
		print(e)
	
'''
	Summary:
		这是一个通过Python使用Sequencer的Render to Movie API的例子。这包括在settings对象上设置所有可能的值，并配置渲染到图像序列的单独过程。
		确保在项目中同时启用了“Python编辑器脚本插件”和“sequencerscript”插件。

		打开Python交互控制台并使用：
			import sequencer_examples
			sequencer_examples.render_movie("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - 指向在渲染时应加载和播放的电影场景 sequence asset的路径字符串。
	ToDo:
		InheritedCommandLineArguments - Look up how this works.
'''
def render_sequence_to_movie(sequencer_asset_path):
	# 1) Create an instance of our UAutomatedLevelSequenceCapture and override all of the settings on it. This class is currently
	# set as a config class so settings will leak between the Unreal Sequencer Render-to-Movie UI and this object. To work around
	# this, we set every setting via the script so that no changes the user has made via the UI will affect the script version.
	# The users UI settings will be reset as an unfortunate side effect of this.
	capture_settings = unreal.AutomatedLevelSequenceCapture()

	# Set all POD settings on the UMovieSceneCapture
	capture_settings.settings.output_directory = unreal.DirectoryPath("../../../QAGame/Saved/VideoCaptures/")
	
	# If you game mode is implemented in Blueprint, load_asset(...) is going to return you the C++ type ('Blueprint') and not what the BP says it inherits from.
	# Instead, because game_mode_override is a TSubclassOf<AGameModeBase> we can use unreal.load_class to get the UClass which is implicitly convertable.
	# ie: capture_settings.settings.game_mode_override = unreal.load_class(None, "/Game/AI/TestingSupport/AITestingGameMode.AITestingGameMode_C")
	capture_settings.settings.game_mode_override = None
	capture_settings.settings.output_format = "{world}"
	capture_settings.settings.overwrite_existing = True
	capture_settings.settings.use_relative_frame_numbers = False
	capture_settings.settings.handle_frames = 0
	capture_settings.settings.zero_pad_frame_numbers = 4
	capture_settings.settings.frame_rate = unreal.FrameRate(24,1)
	capture_settings.settings.resolution.res_x = 1280
	capture_settings.settings.resolution.res_y = 720
	capture_settings.settings.enable_texture_streaming = False
	capture_settings.settings.cinematic_engine_scalability = True
	capture_settings.settings.cinematic_mode = True
	capture_settings.settings.allow_movement = False 	# Requires cinematic_mode = True
	capture_settings.settings.allow_turning = False 	# Requires cinematic_mode = True
	capture_settings.settings.show_player = False 		# Requires cinematic_mode = True
	capture_settings.settings.show_hud = False 			# Requires cinematic_mode = True
	capture_settings.use_separate_process = False
	capture_settings.close_editor_when_capture_starts = False 					# Requires use_separate_process = True
	capture_settings.additional_command_line_arguments = "-NOSCREENMESSAGES"	# Requires use_separate_process = True
	capture_settings.inherited_command_line_arguments = ""						# Requires use_separate_process = True

	# Set all the POD settings on UAutomatedLevelSequenceCapture
	capture_settings.use_custom_start_frame = False 	# If False, the system will automatically calculate the start based on sequence content
	capture_settings.use_custom_end_frame = False 		# If False, the system will automatically calculate the end based on sequence content
	capture_settings.custom_start_frame = unreal.FrameNumber(0)		# Requires use_custom_start_frame = True
	capture_settings.custom_end_frame = unreal.FrameNumber(0)		# Requires use_custom_end_frame = True
	capture_settings.warm_up_frame_count = 0.0
	capture_settings.delay_before_warm_up = 0 # ToDo: Test int -> float
	capture_settings.delay_before_shot_warm_up = 0.0
	capture_settings.write_edit_decision_list = True

	# Tell the capture settings which level sequence to render with these settings. The asset does not need to be loaded, 
	# as we're only capturing the path to it and when the PIE instance is created it will load the specified asset.
	# If you only had a reference to the level sequence, you could use "unreal.SoftObjectPath(mysequence.get_path_name())"
	capture_settings.level_sequence_asset = unreal.SoftObjectPath(sequencer_asset_path)

	# Now let's work on setting some more complex settings. The image capture is composed of two fields that need to correspond to each other.
	# The first field is the CaptureType ("Output Format" on the UI). This is how you specify if you want to output custom render passes, a video sequence, etc.
	# Then, once you decide on a capture type you also need to create an instance of the settings object specific to that capture type and assign it.
	# In this example, we will be using a Custom Render Passes output as it is the most complicated one to set up.
	# 
	# The settings classes for each capture protocol can be found in the /Engine/Source/Runtime/MovieSceneCapture/Public/Protocols folder.
	# The identifier comes from MovieSceneCaptureModule.cpp ("CustomRenderPasses", "Video", "PNG", "JPG", "BMP")
	capture_settings.capture_type.identifier = "CustomRenderPasses"
	protocol_settings = unreal.CompositionGraphCaptureSettings()
	# The passes comes from BufferVisualizationData.cpp
	protocol_settings.include_render_passes.value.append("BaseColor")
	protocol_settings.include_render_passes.value.append("SceneDepth")
	protocol_settings.include_render_passes.value.append("Roughness")
	protocol_settings.capture_frames_in_hdr = False
	protocol_settings.hdr_compression_quality = 1 							# Requires capture_frames_in_hdr = True, 0 means no compression, 1 means standard.
	protocol_settings.capture_gamut = unreal.HDRCaptureGamut.HCGM_REC709 	# Requires capture_frames_in_hdr = True 
	# protocol_settings.post_processing_material = unreal.SoftObjectPath("/Game/Path/To/Material")
	protocol_settings.post_processing_material = unreal.SoftObjectPath("")  # Soft Object Paths use an empty string for None.
	protocol_settings.disable_screen_percentage = True


	# The other complex settings is the burn-in. Create an instance of the LevelSequenceBurnInOptions which is used to 
	# specify if we should use a burn in, and then which settings.
	burn_in_options = unreal.LevelSequenceBurnInOptions()
	burn_in_options.use_burn_in = True

	# You have to specify a path to a class to use for the burn in (if use_burn_in = True), and this class specifies a UClass to define the
	# settings object type. We've created a convinence function which takes the class path, loads the class at that path and assigns it to 
	# the Settings object.
	burn_in_options.set_burn_in(unreal.SoftClassPath("/Engine/Sequencer/DefaultBurnIn.DefaultBurnIn_C"))

	# The default burn in is implemented entirely in Blueprint which means that the method we've been using to set properties will not 
	# work for it. The python bindings that turn bSomeVariableName into "some_variable_name" only work for C++ classes with 
	# UPROPERTY(BlueprintReadWrite) marked fields. Python doesn't know about the existence of Blueprint classes and their fields, so we 
	# have to use an alternative method.
	burn_in_options.settings.set_editor_property('TopLeftText', "{FocalLength}mm,{Aperture},{FocusDistance}")
	burn_in_options.settings.set_editor_property('TopCenterText', "{MasterName} - {Date} - {EngineVersion}")
	burn_in_options.settings.set_editor_property('TopRightText', "{TranslationX} {TranslationY} {TranslationZ}, {RotationX} {RotationY} {RotationZ}")

	burn_in_options.settings.set_editor_property('BottomLeftText', "{ShotName}")
	burn_in_options.settings.set_editor_property('BottomCenterText', "{hh}:{mm}:{ss}:{ff} ({MasterFrame})")
	burn_in_options.settings.set_editor_property('BottomRightText', "{ShotFrame}")

	# Load a Texture2D asset and assign it to the UTexture2D reference that Watermark is.
	# burn_in_settings.set_editor_property('Watermark', None)
	burn_in_options.settings.set_editor_property('Watermark', unreal.load_asset("/Engine/EngineResources/AICON-Green"))
	burn_in_options.settings.set_editor_property('WatermarkTint', unreal.LinearColor(1.0, 0.5, 0.5, 0.5)) # Create a FLinearColor to tint our Watermark


	# Assign our created instances to our original capture_settings object.
	capture_settings.burn_in_options = burn_in_options
	capture_settings.protocol_settings = protocol_settings

	# Finally invoke Sequencer's Render to Movie functionality. This will examine the specified settings object and either construct a new PIE instance to render in,
	# or create and launch a new process (optionally shutting down your editor).
	unreal.SequencerTools.render_movie(capture_settings)


'''
	Summary:
		ToDo:
	Params:
		track - The UMovieSceneTrack to convert to a dictionary 要转换为字典的 UMovieSceneTrack
	Returns:
		ToDo:
'''
def track_to_dict(track):
	t = {
		'name' : str(track.get_display_name()),
		'type' : track.get_class().get_name(),
		'sections' : []
	}

	for section in track.get_sections():
		section_range = section.get_range()
		t['sections'].append({
			'range' : {
				'has_start' : section_range.has_start,
				'start' : section_range.inclusive_start,
				'has_end' : section_range.has_end,
				'end' : section_range.exclusive_end,
			},
			'type': section.get_class().get_name()
		})

	return t

'''
	Summary:
		ToDo:
	Params:
		sequence - The UMovieScene to convert to a dictionary
	Returns:
		ToDo:
'''
def sequence_to_dict(sequence):
	d = {
		'master_tracks' : [],
		'bindings' : []
	}

	for master_track in sequence.find_master_tracks_by_type(unreal.MovieSceneTrack):
		d['master_tracks'].append(track_to_dict(master_track))

	for binding in sequence.get_bindings():
		b = {
			'name' : 'todo',
			'type' : 'todo',
			'id' : str(binding.get_id()),
			'tracks' : [],
		}
		for track in binding.get_tracks():
			b['tracks'].append(track_to_dict(track))

		d['bindings'].append(b)

	return d
	
'''
	Summary:
		ToDo:
	Params:
		sequence - The UMovieScene to convert to export to JSON
	Returns:
		ToDo:
'''
def sequence_to_json(sequence):
	return json.dumps(sequence_to_dict(sequence))

'''
	Summary:
		Populates the specified sequence and track with some test sections. 用一些测试sections填充指定的序列和轨迹。
	Params:
		sequence - The UMovieScene to populate
		track - The track within the movie scene to create sections from.
		num_sections - The number of sections to create.
		section_length_seconds - The length of each section it is creating.
'''
def populate_track(sequence, track, num_sections = 1, section_length_seconds = 1):

	for i in range(num_sections):
		section_range = sequence.make_range_seconds(i*section_length_seconds, section_length_seconds)
		track.add_section().set_range(section_range)

'''
	Summary:
		使用指定的测试部分填充指定的序列和对象绑定。
	Params:
		track - The UMovieScene to populate
		binding - The FMovieSceneObjectBindingID to create sections for. 要为其创建 sections 的 FMovieSceneObjectBindingID。
		num_sections - The number of sections to create. 要创建的sections数。
		section_length_seconds - The length of each section it is creating. 它创建的每个sections的长度
'''
def populate_binding(sequence, binding, num_sections = 1, section_length_seconds = 1):

	for track in binding.get_tracks():
		populate_track(sequence, track, num_sections, section_length_seconds)

'''
	Summary:
		在指定目录下创建具有给定名称的 level sequence 。这是一个如何创建 level sequence 资源的示例，
		如何将当前映射中的对象添加到序列中，以及如何创建一些示例绑定/etc。
		Creates a level sequence with the given name under the specified directory. This is an example of how to create Level Sequence assets,
		how to add objects from the current map into the sequence and how to create some example bindings/etc.
	Params:
		asset_name - Name of the resulting asset, ie: "MyLevelSequence" 所得资产的名称，即：“MyLevelSequence”
		package_path - Name of the package path to put the asest into, ie: "/Game/LevelSequences/" 要将asest放入的包路径的名称
	Returns:
		The created LevelSequence asset. 创建LevelSequence资源。
'''
def create_level_sequence(asset_name, package_path = '/Game/'):

	sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, package_path, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())

	floor = unreal.load_object(None, "/Game/NewMap.NewMap:PersistentLevel.Floor")
	sm_component = unreal.load_object(None, "/Game/NewMap.NewMap:PersistentLevel.Floor.StaticMeshComponent0")

	floor_binding = sequence.add_possessable(floor)
	floor_binding.add_track(unreal.MovieScene3DTransformTrack)
	populate_binding(sequence, floor_binding, 5)

	print("Floor {0} is bound as {1}".format(floor, floor_binding.get_id()))

	sm_component_binding = sequence.add_possessable(sm_component)
	sm_component_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
	populate_binding(sequence, sm_component_binding, 5)

	print("Static mesh component {0} is bound as {1}".format(sm_component, sm_component_binding.get_id()))

	# Create a spawnable from the floor instance
	spawnable_floor_binding = sequence.add_spawnable_from_instance(floor)
	transform_track = spawnable_floor_binding.add_track(unreal.MovieScene3DTransformTrack)
	populate_track(sequence, transform_track, 5)

	# Create a spawnable from an actor class
	spawnable_camera_binding = sequence.add_spawnable_from_class(unreal.CineCameraActor)
	# add an infinite transform track
	spawnable_camera_binding.add_track(unreal.MovieScene3DTransformTrack).add_section().set_range(unreal.SequencerScriptingRange())

	return sequence

def create_sequence_from_selection(asset_name, length_seconds = 5, package_path = '/Game/'):

	sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, package_path, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())

	for actor in unreal.SelectedActorIterator(unreal.EditorLevelLibrary.get_editor_world()):
		binding = sequence.add_possessable(actor)
		track = binding.add_track(unreal.MovieScene3DTransformTrack)

		track.add_section().set_range(sequence.make_range_seconds(0, length_seconds))

		try:
			camera = unreal.CameraActor.cast(actor)
			camera_cut_track = sequence.add_master_track(unreal.MovieSceneCameraCutTrack)

			camera_cut_section = camera_cut_track.add_section()
			camera_cut_section.set_range(sequence.make_range_seconds(0, length_seconds))

			camera_binding_id = unreal.MovieSceneObjectBindingID()
			camera_binding_id.set_editor_property("Guid", binding.get_id())
			camera_cut_section.set_editor_property("CameraBindingID", camera_binding_id)
		except TypeError:
			pass

		print("{0} is bound as {1}".format(actor, binding.get_id()))

	return sequence


if __name__ == "__main__":
	create_level_sequence("MyLevelSequence", package_path = '/Game/a/')
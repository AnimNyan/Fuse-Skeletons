import bpy

#import the re library for re.search
import re

#import time for timing how long
#operators takes
import time

#------------code for drawing main panel in the 3D View
#don't register this class it is not a bpy panel or type so
#it does not need to be registereds
class FUSESKELETONS_PT_main_panel(bpy.types.Panel):
    bl_label = "Fuse Skeletons"
    bl_idname = "FUSESKELETONS_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Fuse Skel"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text ="Select the Skeletons you want to fuse > press 'Fuse Skeletons'")
        layout.label(text ="This will delete all bones with the same names")
        layout.label(text ="and the children will be parented to the base skeleton")
        layout.separator()
        layout.label(text ="Select Skeleton to Fuse to:")
        layout.operator_menu_enum("fuseskeletons.write_select_object", "select_objects")

        layout.operator("fuseskeletons.fuse_selected")


class FUSESKELETONS_OT_write_select_object(bpy.types.Operator):
    bl_idname = "fuseskeletons.write_select_object"
    bl_label = "Select Skeleton"
    bl_description = "Show Message for UEShaderScript"
    def available_objects(self,context):
        items = []

        #iterate over all objects
        #in scene and add an index to them
        for scene_object_index, scene_object in enumerate(bpy.data.objects):
            
            #only show the armatures in the select list
            #as we can only fuse skeletons together not other 
            #scene objects
            if (scene_object.type == "ARMATURE"):
                current_array_item = (str(scene_object_index), scene_object.name, scene_object.name)
                items.append(current_array_item)
        
        return items

    select_objects: bpy.props.EnumProperty(
        items = available_objects, 
        name = "Available Objects",
        description = "Available Objects"
    )
    
    def execute(self,context):
        #example behaviour, int(self.select_objects)] gives you the index of the selected object
        #set the active object so it will automatically be the skeleton to fuse to
        selected_obj = bpy.data.objects[int(self.select_objects)]
        bpy.context.view_layer.objects.active = selected_obj
        return {'FINISHED'}


class FUSESKELETONS_OT_fuse_selected(bpy.types.Operator):
    bl_idname = "fuseskeletons.fuse_selected"
    bl_label = "Fuse Skeletons"
    bl_description = "Fuse Skeletons, Delete Bones with Same Names and Reparent Children"
    bl_options = {'REGISTER'}

    #if poll returns False
    #execute and draw functions will not run
    #In this case execute function will always run 
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        #time the fuse selected operator
        time_start = time.time()

        scene = bpy.context.scene
        armatures = []
        active_object = bpy.context.view_layer.objects.active
        if active_object.type == "ARMATURE":
            #--------------------record the original skeleton's bone names to a list
            #record all bones in this list
            #so we know these are the original bones 
            #that we need to keep everything else must be deleted
            original_skeleton_bones_list = []

            #set to edit mode so then we can use edit bones
            #which can only be used in edit mode
            bpy.ops.object.mode_set(mode='EDIT') 

            #iterate through the active object which should be a skeleton's edit bones
            #and record all the active objects bones
            for bone in bpy.context.active_object.data.edit_bones:
                #debug
                #print("\n\nbone.name", bone.name)
                #add bone names to bone names list
                #don't append the the bone itself as they are structs
                #and they are much larger
                original_skeleton_bones_list.append(bone.name)

             
            #--------------------join all selected armatures together
            for object in bpy.context.selected_objects:
                #whatever objects you want to join...
                #in this case only armatures
                #should be joined
                if object.type == "ARMATURE":
                    armatures.append(object)

            #set to object mode so then we can join them
            #which can only be done in object mode 
            bpy.ops.object.mode_set(mode='OBJECT')



            #--------------THESE METHODS ARE ALL DEPRECATED IN BLENDER 4.0 new method of overriding context
            # #If you use a copy of the context, you can change some attributes 
            # #and pass it to an operator without affecting the actual context
            # #this is much faster for performance
            # #because blender does not need to update the scene every time if 
            # #join is called in a loop
            # #also it keeps the currently selected objects intact
            # ctx = bpy.context.copy()

            # #Make the active object
            # #one of the objects to join
            # #otherwise when trying to join it won't know which 
            # #skeleton to join to
            # #set the copy of the context's active object
            # #to the current context's active object
            # #this is because when joining skeletons it is the active object
            # #that is the skeleton every other skeleton is joined to
            # ctx['active_object'] = active_object

            # ctx['selected_objects'] = armatures

            # # In Blender 2.8x this needs to be the following instead:
            # ctx['selected_editable_objects'] = armatures
            # #debug
            # #print("armatures before join:", armatures)
            # #print("ctx['selected_editable_objects'] before join:", ctx['selected_editable_objects'])

            #  bpy.ops.object.join(ctx)

            with context.temp_override(active_object=active_object, selected_objects=armatures, selected_editable_objects=armatures):
                     bpy.ops.object.join()

           
            #debug
            #joined armatures will become <bpy_struct, Object invalid>
            #in the list
            #print("armatures after join:", armatures)
            #print("ctx['selected_editable_objects'] after join:", ctx['selected_editable_objects'])

            #set to edit mode so then we can use edit bones
            #which can only be used in edit mode
            bpy.ops.object.mode_set(mode='EDIT') 

            #----------------------delete all bones that have the following pattern .001 .002 .003 
            #and if their children do not have .001 .002 .003 reparent them to the original base skeleton

            #iterate through the active object which should be the skeleton 
            #which has joined all other skeletons to it. Iterate through the edit bones
            #and unparent all children bones that have parents with .001 or .002 in them
            #and were not in the original skeletons bone list
            for bone in bpy.context.active_object.data.edit_bones:
                bone_name = bone.name
                #debug
                #print("\n\nbone.name", bone_name)
                
                #do a regex match
                # \. matches the character . literally (case sensitive)
                # \d matches a digit (equivalent to [0-9])
                # + matches the previous token between one and unlimited times, 
                # as many times as possible, giving back as needed (greedy)
                # $ asserts position at the end of a line

                #essentially this matches anything with .001/ .002/ .003/ etc
                #re.search returns the first match
                #if there is no match match re.search will return None
                bone_num_suffix_match_obj = re.search("\.\d+$", bone_name)

                #assume it is not .001, .002 then correct assumption if required
                is_bone_num_suffix = False

                #make assumption that the bone name without suffix 
                #is the same as the bone name and correct it if requried
                bone_name_no_suffix = bone_name
                
                if bone_num_suffix_match_obj != None:
                    is_bone_num_suffix = True
                    #only try to access the group attribute if a successful match
                    #occurred otherwise if bone_num_suffix_match_obj is None there will be no group attribute
                    # need to access the match object data by accessing the group that it matched
                    bone_num_suffix_match = bone_num_suffix_match_obj.group()
                    #store the bone name without a suffix
                    bone_name_no_suffix = bone_name.replace(bone_num_suffix_match, "")
                    #print("bone_name_no_suffix:", bone_name_no_suffix)

                
                #to check if a bone really is a duplicate 
                #it must fulfill a few conditions
                #1. It must have .001/.002/etc as suffix as this suffix occurs when skeletons are joined together
                #2. The bone name without the suffix must be in the original skeleton bones list
                #3. The bone name with suffix must NOT be in the original skeleton bones list,
                #otherwise it might be a bone named head.001 in the original skeleton
                #as the bones from the original skeleton should be kept safe 
                #\ means statement is continued on next line
                if is_bone_num_suffix and bone_name_no_suffix in original_skeleton_bones_list and \
                not(bone_name in original_skeleton_bones_list):
                    #debug
                    #print("bone_name for duplicate:", bone_name)

                    #if the bone is a duplicate 
                    #check if it has children
                    #if it has no children it will bone.children will return []
                    if (bone.children != []):
                        #if it has children check if the children have .001 in their names

                        #debug
                        #print("bone.children:", bone.children)
                        
                        for child_bone in bone.children:
                            #debug
                            child_bone_name = child_bone.name
                            #print("child_bone.name:", child_bone_name)

                            child_bone_num_suffix_match_obj = re.search("\.\d+$", child_bone_name)

                            #make assumption then correct if needed
                            is_child_bone_num_suffix = False

                            if child_bone_num_suffix_match_obj != None:
                                is_child_bone_num_suffix = True
                            
                            if(not(is_child_bone_num_suffix)):
                                #if they do not have .001/.002/.003/etc in their names
                                #then unparent the child bone
                                child_bone.parent = None
                                
                                #then attach the child bone to the bone in the original skeleton which
                                #should have the same name as the parent bone without the suffix
                                #get it by referencing inside the list by name
                                child_bone.parent = bpy.context.active_object.data.edit_bones[bone_name_no_suffix]
                    
        
                    #then delete the duplicate bone
                    bpy.context.active_object.data.edit_bones.remove(bone)


            #set back to object mode so the user isn't confused 
            #after the loop of fusing both skeletons
            bpy.ops.object.mode_set(mode='OBJECT')

            #--------------fix the armature modifiers on the meshes attached to the fused skeletons
            #the problem is the meshes attached to the skeletons that were fused
            #will have empty Object input boxes for the armature object modifier
            #to fix this we will go over all child meshes object modifiers
            #and change the Object input to the base skeleton
            child_meshes = active_object.children
            
            #if there are child meshes attached to the base skeleton 
            #active_object.children returns () if no meshes parented to skeleton
            if child_meshes != ():
                for child_mesh in child_meshes:
                    #get the armature modifier by type
                    #do so by iterating through all the object modifiers
                    #and checking if it's of type ARMATURE
                    for obj_mod in child_mesh.modifiers:
                        if obj_mod.type == "ARMATURE":
                            #if it is type armature change the object attribute to
                            #the active skeleton
                            #change the Object Input 
                            #of the Armature Object Modifier to be the active skeleton
                            obj_mod.object = active_object
                    
                               
        #if the active object the user selects is not an armature
        #send an error message
        else:
            error_message = "Error: Active Object is not an Armature, make sure the active object is the Skeleton to Fuse to."
            bpy.ops.fuseskeletons.show_message(message = error_message)
            log(error_message)
        
        log("Finished fuse selected operator in: %.4f sec" % (time.time() - time_start))
        return {'FINISHED'}



class FUSESKELETONS_OT_show_message(bpy.types.Operator):
    bl_idname = "fuseskeletons.show_message"
    bl_label = ""
    bl_description = "Show Message for Fuse Skeletons"
    bl_options = {'REGISTER'}
    message: bpy.props.StringProperty(default="Message Dummy")
    called: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=self.message)

    def execute(self, context):
        if not self.called:
            wm = context.window_manager
            self.called = True
            return wm.invoke_props_dialog(self, width=700)
        return {'FINISHED'}


def log(msg):
    print("[Fuse Skeletons]:", msg)


classes = [FUSESKELETONS_PT_main_panel, FUSESKELETONS_OT_write_select_object,
FUSESKELETONS_OT_fuse_selected, FUSESKELETONS_OT_show_message]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    #register path_tool as a type which has all
    #the user input properties from the properties class 
    #bpy.types.Scene.fuseskeletons_tool = bpy.props.PointerProperty(type = FUSESKELETONS_skeleton_properties)
 
def unregister():
    #unregister in reverse order to registered so classes relying on other classes
    #will not lead to an error
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    #unregister path_tool as a type
    #del bpy.types.Scene.path_tool
 
 
if __name__ == "__main__":
    register()

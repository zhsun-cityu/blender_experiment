import bpy
import os

def clear_objects():
    """Clear all mesh objects from the current scene."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def import_obj(obj_file_path):
    """Import an .obj file."""
    obj_name = os.path.splitext(os.path.basename(obj_file_path))[0]
    # old_obj = bpy.data.objects[obj_name] if obj_name in bpy.data.objects else None
    old_obj = None
    # for obj in bpy.data.objects:
    #     # obj.select_set(True)
    #     print(f"Object Name: {obj.name}, Type: {obj.type}")
    #     if obj.name == obj_name:
    #         old_obj = obj
    #         break
    # if old_obj is None:
    #     print(f"Object {obj_name} not found in the scene.")
    #     return
    if obj_name in bpy.data.objects:
        old_obj = bpy.data.objects[obj_name]
    else:
        print(f"Object {obj_name} not found in the scene.")
        return
    bpy.ops.import_scene.obj(filepath=obj_file_path)

    # update imported object
    imported_obj = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH'][0]
    if imported_obj:
        imported_obj.name = obj_name
        imported_obj.location = old_obj.location
        imported_obj.rotation_euler = old_obj.rotation_euler
        imported_obj.scale = old_obj.scale
        # imported_obj.select_set(True)
        # bpy.context.view_layer.objects.active = imported_obj
        # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # # link the object to the scene
        for collection in old_obj.users_collection:
            # collection.objects.unlink(old_obj)
            try:
                collection.objects.link(imported_obj)
            except:
                print(f"Object {obj_name} already linked to collection {collection.name}")

        # link the texture to the object
        for mat in old_obj.data.materials:
            imported_obj.data.materials.append(mat)

        # transfer modifiers
        for mod in old_obj.modifiers:
            new_mod = imported_obj.modifiers.new(name=mod.name, type=mod.type)
            for attr in dir(mod):
                if not attr.startswith("_") and hasattr(mod, attr):
                    try:
                        setattr(new_mod, attr, getattr(mod, attr))
                    except:
                        print(f"Error setting attribute {attr} for modifier {mod.name}")

        # transfer constraints
        for constr in old_obj.constraints:
            new_constr = imported_obj.constraints.new(type=constr.type)
            for attr in dir(constr):
                if not attr.startswith("_") and hasattr(constr, attr):
                    try:
                        setattr(new_constr, attr, getattr(constr, attr))
                    except:
                        print(f"Error setting attribute {attr} for constraint {constr.name}")

        # transfer parent-child relationship
        if old_obj.parent:
            imported_obj.parent = old_obj.parent

        # transfer shape keys
        for shape_key in old_obj.data.shape_keys.key_blocks:
            new_shape_key = imported_obj.data.shape_keys.key_blocks.get(shape_key.name)
            if new_shape_key:
                new_shape_key.value = shape_key.value

        # transfer vertex groups
        for group in old_obj.vertex_groups:
            imported_obj.vertex_groups.new(name=group.name)
            for vert_idx, weight in group.weight():
                imported_obj.vertex_groups[group.name].add([vert_idx], weight, 'REPLACE')

        # transfer custom properties
        for prop in old_obj.keys():
            imported_obj[prop] = old_obj[prop]

        # transfer animation data
        if old_obj.animation_data:
            imported_obj.animation_data_create()
            imported_obj.animation_data.action = old_obj.animation_data.action
            imported_obj.animation_data.from_copy(old_obj.animation_data)

        # remove old object
        if old_obj:
            bpy.data.objects.remove(old_obj, do_unlink=True)

        print(f"Imported object: {obj_name}")

def import_obj2(obj_file_path):
    obj_name = os.path.splitext(os.path.basename(obj_file_path))[0]
    # old_obj = bpy.data.objects[obj_name] if obj_name in bpy.data.objects else None
    old_obj = None
    if obj_name in bpy.data.objects:
        old_obj = bpy.data.objects[obj_name]
    else:
        print(f"Object {obj_name} not found in the scene.")
        return

    bpy.ops.import_scene.obj(filepath=obj_file_path)
    imported_obj = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH'][0]
    # old_obj = bpy.data.objects.get(obj_name)



    if imported_obj and old_obj:
        # original_material = old_obj.active_material
        # original_material_slot = old_obj.material_slots
        original_materials = [slot.material for slot in old_obj.material_slots]
        original_uv_layers = [uv.name for uv in old_obj.data.uv_layers]
        original_vertex_groups = [vg.name for vg in old_obj.vertex_groups]
        original_custom_properties = old_obj.data.items()


        old_obj.data = imported_obj.data

        for i, material in enumerate(original_materials):
            if i < len(old_obj.material_slots):
                old_obj.material_slots[i].material = material
            else:
                old_obj.data.materials.append(material)

        for uv_layer_name in original_uv_layers:
            if uv_layer_name in old_obj.data.uv_layers:
                continue
            old_obj.data.uv_layers.new(name=uv_layer_name)

        for vg_name in original_vertex_groups:
            if vg_name in old_obj.vertex_groups:
                continue
            old_obj.vertex_groups.new(name=vg_name)

        for key, value in original_custom_properties:
            old_obj.data[key] = value

        # bpy.context.view_layer.update()

        # old_obj.active_material = original_material
        # for i in range(len(old_obj.material_slots)):
        #     old_obj.material_slots[i].material = original_material_slot[i].material

        bpy.data.objects.remove(imported_obj, do_unlink=True)
        print(f"Imported object: {obj_name}")
    else:
        print(f"Error importing object: {obj_name}")

def import_obj3(obj_file_path):
    obj_name = os.path.splitext(os.path.basename(obj_file_path))[0]
    # old_obj = bpy.data.objects[obj_name] if obj_name in bpy.data.objects else None
    old_obj = None
    if obj_name in bpy.data.objects:
        old_obj = bpy.data.objects[obj_name]
    else:
        print(f"Object {obj_name} not found in the scene.")
        return

    # if obj_file_path.endswith('.obj'):
    #     bpy.ops.import_scene.obj(filepath=obj_file_path)
    # elif obj_file_path.endswith('.ply'):
    #     bpy.ops.import_scene.ply(filepath=obj_file_path)
    bpy.ops.import_scene.obj(filepath=obj_file_path)
    # bpy.ops.import_scene.ply(filepath=obj_file_path)
    imported_obj = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH'][0]
    # old_obj = bpy.data.objects.get(obj_name)

    old_mesh = old_obj.data
    imported_mesh = imported_obj.data

    original_materials = list(old_mesh.materials)
    uv_layers = {uv_layer.name: uv_layer.data for uv_layer in old_mesh.uv_layers}
    # vertex_groups = {vg.name: [v.group for v in vg.weight_get()]  for vg in old_mesh.vertex_groups}

    new_mesh = bpy.data.meshes.new(name = "newmesh")
    new_mesh.from_pydata(
        vertices=[v.co for v in imported_mesh.vertices],
        edges=[(e.vertices[0], e.vertices[1]) for e in imported_mesh.edges],
        faces=[f.vertices[:] for f in imported_mesh.polygons]
    )
    new_mesh.update()

    # for uv_name, uv_data in uv_layers.items():
    #     uv_layer = new_mesh.uv_layers.new(name=uv_name)
    #     for loop in new_mesh.loops:
    #         uv_layer.data[loop.index].uv = uv_data[loop.index].uv

    for mat in original_materials:
        new_mesh.materials.append(mat)

    # for vg_name, vg_weights in vertex_groups.items():
    #     if vg_name not in old_obj.vertex_groups:
    #         new_vg = old_obj.vertex_groups.new(name=vg_name)
    #         for i, weight in enumerate(vg_weights):
    #             new_vg.add([i], weight, 'REPLACE')

    old_obj.data = new_mesh


    # old_mesh.clear_geometry()
    # old_mesh.from_pydata(
    #     vertices=[v.co for v in imported_mesh.vertices],
    #     edges=[(e.vertices[0], e.vertices[1]) for e in imported_mesh.edges],
    #     faces=[f.vertices[:] for f in imported_mesh.polygons]
    # )
    # old_mesh.update()

    bpy.data.objects.remove(imported_obj, do_unlink=True)

def render_and_save_image(output_path):
    """Render the scene and save the image."""
    bpy.context.scene.render.filepath = output_path

    # faster render setting
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.eevee.taa_render_samples = 16
    bpy.context.scene.eevee.use_gtao = True

    bpy.ops.render.render(write_still=True, )
    print(f"Rendered image saved at: {output_path}")

def process_obj_files(input_folder, output_folder):
    """Process all .obj files in the input folder and save rendered images to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.obj') or filename.endswith('.ply'):
            obj_file_path = os.path.join(input_folder, filename)
            # image_output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")

            # clear_objects()
            import_obj2(obj_file_path)
    image_output_path = os.path.join(output_folder, os.path.basename(input_folder)+".png")
    render_and_save_image(image_output_path)

def process_folders(root_folder, output_root_folder):
    """Traverse folders and process .obj files in each."""
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            # output_folder = os.path.join(output_root_folder, folder_name)
            process_obj_files(folder_path, output_root_folder)

# Load the initial .blend file
blend_file_path = "../blender_dataset/ocean-scene.blend"
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

for obj in bpy.data.objects:
    # obj.select_set(True)
    print(f"Object Name: {obj.name}, Type: {obj.type}, Collection: {obj.users_collection}")

# Example usage
root_folder = "../blender_dataset-ply2/ocean-scene-vmesh/decode/"
output_root_folder = "../blender_dataset-ply2/ocean-scene-vmesh"

# render_and_save_image(os.path.join(output_root_folder, "test.png"))

process_folders(root_folder, output_root_folder)

import bpy
import math
import mathutils
from bpy_extras.object_utils import world_to_camera_view


def calculate_distance(obj1, obj2):
    """Calculate the Euclidean distance between two objects."""
    loc1 = obj1.location
    loc2 = obj2.location
    return math.sqrt((loc2.x - loc1.x)**2 + (loc2.y - loc1.y)**2 + (loc2.z - loc1.z)**2)
def get_textures(obj):
    """Retrieve textures associated with the object's materials."""
    textures = []
    for material in obj.data.materials:
        if material and material.use_nodes:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    textures.append(node.image.filepath)
    return textures

def set_camera_opposite_direction_notgood(camera):
    """Set the camera direction to the opposite direction."""
    current_rotation = camera.rotation_euler
    opposite_rotation = mathutils.Euler((current_rotation.x, current_rotation.y, current_rotation.z + math.pi), 'XYZ')
    camera.rotation_euler = opposite_rotation
    print(f"Camera rotation set to: {camera.rotation_euler}")

def set_camera_top_view(camera, scene):
    """Set the camera to a top view of the scene."""
    # Calculate the center of the scene
    center = sum((obj.location for obj in scene.objects if obj.type == 'MESH'), mathutils.Vector()) / len([obj for obj in scene.objects if obj.type == 'MESH'])

    # Position the camera above the center
    camera.location = center + mathutils.Vector((0, 0, 10))  # Adjust the height (10 units above)

    # Set the camera to look straight down
    camera.rotation_euler = (math.radians(90), 0, math.radians(0))
    print(f"Camera position set to top view at location: {camera.location}")

def set_camera_opposite_direction(camera):
    """Set the camera direction to the opposite direction."""
    # Get the current camera direction
    camera_direction = camera.matrix_world.to_quaternion() @ mathutils.Vector((0.0, 0.0, -1.0))

    # Invert the direction vector components
    opposite_direction = -camera_direction

    # Calculate the new rotation for the camera to look in the opposite direction
    # This involves finding the quaternion that represents the new direction
    new_rotation = opposite_direction.to_track_quat('-Z', 'Y').to_euler()

    # Update the camera rotation
    camera.rotation_euler = new_rotation
    print(f"Camera rotation set to: {camera.rotation_euler}")

def render_image(output_image_path):
    """Render the current scene."""
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_image_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered image saved at {output_image_path}")

def is_object_visible(camera, obj, scene):
    """Check if the object is within the camera's view."""
    cam_ob = bpy.data.objects[camera.name]
    for vertex in obj.data.vertices:
        co_world = obj.matrix_world @ vertex.co
        co_cam = world_to_camera_view(scene, cam_ob, co_world)
        if 0.0 <= co_cam.x <= 1.0 and 0.0 <= co_cam.y <= 1.0 and co_cam.z >= 0.0:
            return True
    return False

def remove_invisible_objects(camera, scene):
    """Remove objects that are not visible from the camera's view."""
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and not is_object_visible(camera, obj, scene):
            bpy.data.objects.remove(obj, do_unlink=True)

def main():
    # Path to the .blend file
    blend_file_path = "../blender_dataset/classroom/classroom.blend"

    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Get the camera object
    # camera = bpy.data.objects.get("Camera")
    camera_position = None
    camera_direction = None
    camera_obj = None
    # Iterate over all objects in the scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'CAMERA':  # Only consider mesh objects
            camera_position = obj.location
            camera_obj = obj
            camera_direction = obj.matrix_world.to_quaternion() @ mathutils.Vector((0.0, 0.0, -1.0))

    if not camera_position:
        print("No camera found in the scene.")
        return

    print(f"Camera location: {camera_position}")
    print(f"Camera direction: {camera_direction}")



    # List to store distances and visibility status
    distances = []

    # Iterate over all objects in the scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':  # Only consider mesh objects
            distance = calculate_distance(camera_obj, obj)
            visible = is_object_visible(camera_obj, obj, bpy.context.scene)
            distances.append((obj.name, distance, obj, visible))

    # Sort the distances in descending order
    distances.sort(key=lambda x: x[1], reverse=True)

    # Display the distances and visibility status
    for obj_name, distance, obj, visible in distances:
        print(f"Distance from camera to {obj_name}: {distance:.2f}, Visible: {visible}")


    # Get the object with the largest distance
    if distances:
        farthest_object = bpy.data.objects.get(distances[0][0])
        print(f"Farthest object: {farthest_object.name}")

        # Get and display the textures associated with the farthest object
        textures = get_textures(farthest_object)
        if textures:
            print(f"Textures associated with {farthest_object.name}:")
            for texture in textures:
                print(f" - {texture}")
        else:
            print(f"No textures found for {farthest_object.name}")


    # Set the camera to top view
    set_camera_top_view(camera, bpy.context.scene)
    output_image_path = "classroom-top.png"
    render_image(output_image_path)

    # # Set the camera to the opposite direction
    # print(camera_direction)
    # set_camera_opposite_direction_notgood(camera_obj)
    # camera_direction = camera_obj.matrix_world.to_quaternion() @ mathutils.Vector((0.0, 0.0, -1.0))
    #
    # print(camera_direction)
    # # Render the image
    # output_image_path = "classroom-opposite.png"
    # render_image(output_image_path)

    # ## Remove invisible objects
    # remove_invisible_objects(camera_obj, bpy.context.scene)
    # # Save the updated .blend file
    # updated_blend_file_path = "classroom-new2.blend"
    # bpy.ops.wm.save_as_mainfile(filepath=updated_blend_file_path)
    # print(f"Updated .blend file saved at {updated_blend_file_path}")

if __name__ == "__main__":
    main()

import pyglet, math


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def is_colliding(object_a, object_b):
    """Determine if two objects collides with another"""
    # Calculate distance between object centers that would be a collision,
    # assuming square resources
    collision_distance = object_a.image.width * 0.5 * object_a.scale + object_b.image.width * 0.5 * object_b.scale
    # Get distance using position tuples
    actual_distance = distance(object_a.position, object_b.position)
    return actual_distance <= collision_distance


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

def get_vector_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

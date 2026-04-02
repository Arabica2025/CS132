import numpy as np


# Notes:
#
# * A 2D point is represented a a pair of floats.  A 3D point is
#   represented as a triple of floats.
#
# * A 2D line segment is represented as a pair of 2D points. A 3D line
#   segment is represent as a pair of 3D points.
#
# * a wireframe object (i.e., 3D shape) is represented as list of 3D
#   line segments.  A 2D shape is represented as a list of 2D line
#   segments

test_shape = [((0, 1, 2), (1, 2, 3)),
              ((5, 5, 5), (6, 6, 6)),
              ((-1, -2, -3), (2, 0, 0))]

print(type(test_shape[0][0][1])) # list of 3D line segments
def shape_to_matrix(shape: np.ndarray)-> np.ndarray:
    """converts a wireframe object to a matrix of points in
    homogeneous coordinates

    Parameters:

      shape: list of line segments

    Returns:

      2D numpy array with shape (4, 2 * N) where N = len(shape)

    Example:

      >>> shape_to_matrix(test_shape)
      array([[ 0.,  1.,  5.,  6., -1.,  2.],
             [ 1.,  2.,  5.,  6., -2.,  0.],
             [ 2.,  3.,  5.,  6., -3.,  0.],
             [ 1.,  1.,  1.,  1.,  1.,  1.]])

    """
    N: int = len(shape)
    matrix: np.ndarray = np.ones((4, 2 * N)) # fill up shape (4, 2*N) with 1s
    
    for i in range(N): # for each row
        for j in range(len(shape[i])): # for each col
          matrix[:3, 2*i + j] = shape[i][j] # transpose
    
    
    return matrix

  
# print(shape_to_matrix(test_shape))
def transform_matrix(x_tr: float, y_tr: float, z_tr: float, roll: float, pitch: float, yaw: float) -> np.ndarray:
    """the matrix applied to a shape in order to transformation it by
    translation and rotation

    Parameters:

      x_tr: distance to translate in the x direction (float)
      y_tr: distance to translate in the y direction (float)
      z_tr: distance to translate in the z direction (float)
      roll: angle in radians to rotation about roll axis (float)
      pitch: angle in radians to rotation about pitch axis (float)
      yaw: angle in radians to rotation about yaw axis (float)

    Returns:

      2D numpy array with shape (4, 4)

    Notes:

      * This matrix will be applied to homogeneous coordinates.

      * Make sure that translation is done AFTER rotation.  In
        particular, the centerpoint of the guide axes should remain
        fixed when rotating, even after translation.

    """
    # identity matrix generated for each rotation axis
    # all R^(4,4)
    rotate_roll: np.ndarray = np.identity(4) 
    rotate_pitch: np.ndarray = np.identity(4)
    rotate_yaw: np.ndarray = np.identity(4)

    # Defining 3D rotation matrices
    ## 1. roll
    rotate_roll[1][1] = np.cos(roll)
    rotate_roll[1][2] = -np.sin(roll)
    rotate_roll[2][1] = np.sin(roll)
    rotate_roll[2][2] = np.cos(roll)
    
    ## 2. pitch
    rotate_pitch[0][0] = np.cos(pitch)
    rotate_pitch[0][2] = np.sin(pitch)
    rotate_pitch[2][0] = -np.sin(pitch)
    rotate_pitch[2][2] = np.cos(pitch)
    
    ## 3. yaw
    rotate_yaw[0][0] = np.cos(yaw)
    rotate_yaw[0][1] = -np.sin(yaw)
    rotate_yaw[1][0] = np.sin(yaw)
    rotate_yaw[1][1] = np.cos(yaw)

    ## rotation combined: R^(4,4)
    rotation: np.ndarray = rotate_yaw @ rotate_pitch @ rotate_roll # combine the 3 rotation matrices by multiplying them together
    # rotation order matters!
    # roll -> pitch -> yaw
    # for matrix transformation, we need to multiply yaw to pitch to roll (reverse order)
    
    translation: np.ndarray = np.identity(4) # identity matrix generated for translation
    for i in range(3):
      translation[i, 3] = [x_tr, y_tr, z_tr][i] # rotate; apply x,y,z coordinate rotation on the identity matrix
    
    # translation AFTER rotation
    translation = translation @ rotation
    return translation

test_matrix = np.array(
    [[1, 2, 3, 4],
     [1, 2, 3, 4],
     [1, 2, 3, 4],
     [1, 1, 1, 1]])


def matrix_to_shape(m: np.ndarray) -> list[np.ndarray]:
    """converts a set of homogeneous coordinates to a 2D shape (a list
    of 2D line segments)

    Parameters:

      m : 2D matrix with shape (4, 2 * N) where N is the number of
          line segments

    Returns:

      list of 2D line segments (pairs of pairs of floats) after
      projection from distance 10, i.e., with viewing position at the
      point (0, 0, 10)

    Example:

      >>> matrix_to_shape(test_matrix)
      [((1.1111111111111112, 1.1111111111111112), (2.5, 2.5)),
       ((4.285714285714286, 4.285714285714286), (6.666666666666667, 6.666666666666667))]

    Notes:

      * Your values may differ slightly from those in the example
        above, but they should be very similiar.

      * The function numpy.apply_along_axis may be useful here

      * The function zip may be useful here

    """
    assert(m.shape[0] == 4)
    assert(m.shape[1] % 2 == 0)
    # projection from distance 10
    d: int = 10
    # shape((4, 4))
    projection_matrix: np.ndarray = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, -1/d, 1]]) # projection matrix for distance 10
    
    # projection_matrix now becomes R^(4, 2*N)
    projection = projection_matrix @ m # apply projection to the matrix of points
    
    # Drop last two coords; we only need x*, y*
    # divide by last row
    # x/(1-z/d)
    # y/(1-z/d)
    projection /= projection[3, :]

    # list of 2D line segments (pairs of pairs of floats) after projection from distance 10
    segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    
    for i in range(0, projection.shape[1], 2): # row 1 and row 2 are the only ones I need(grouping every two points)
      x_star = projection[0, i:i+2] # x* is row 1
      y_star = projection[1, i:i+2] # y* is row 2
      segments.append(((x_star[0], y_star[0]), (x_star[1], y_star[1]))) # append each element to segments
      

    return segments

def full_transform(x_tr: float, y_tr: float, z_tr: float, 
                   roll: float, pitch: float, yaw: float, 
                   shape: list[tuple[tuple[tuple[int,int,int]]]]):
  
  """step by step guide:
    1. convert the 3D shape to a matrix (shape_to_matrix)
    2. apply the transformation matrix (transform_matrix)
    3. convert the matrix to a 2D rendering. (matrix_to_shape)
  """
  # step 1: convert the 3D shape to a matrix (shape_to_matrix)
  shape_matrix: np.ndarray = shape_to_matrix(shape) 

  # step 2: apply the transformation matrix
  t_mtrx: np.ndarray = transform_matrix(x_tr, y_tr, z_tr, roll, pitch, yaw)
  
  # step 3: convert the matrix to a 2D rendering
  render = matrix_to_shape(t_mtrx @ shape_matrix) # apply the transformation matrix to the shape matrix, then convert it to a 2D rendering
  return render

# For extra credit, create your own wireframe and include an image of
# in the written part of your solution.  For full credit, you must
# make something sufficiently complex, and you must give it a name.
extra_credit_name = "umbrella"

def mk_umbrella_head(innerRadius, outerRadius, num_lines, z1_axis, z2_axis):
    """
    differentiated z-axis of the inner part and outer part to create 
    umbrella head

    inspired by mk_wheel_face and mk_wheel_edge
    """
    out = []
    for i in range(num_lines):
        # added tilting angle
        theta = 2 * np.pi * i / num_lines # 2*pi(radian) * i/n to calculate the angle

        # inner point (top part)
        # does not matter if theta does not change since innerRadius will be fixed to 0 (z1_axis)
        p1 = (innerRadius * np.cos(theta), innerRadius * np.sin(theta), z1_axis)

        # outer point (makes the shape tilted)
        p2 = (outerRadius * np.cos(theta), outerRadius * np.sin(theta), z2_axis)

        out.append((p1, p2))
    return out
  
def mk_umbrella_with_handle(innerRadius, outerRadius, num_lines, z1_axis, z2_axis, handle_len=5):
    # 1. umbrella head
    out = mk_umbrella_head(innerRadius, outerRadius, num_lines, z1_axis, z2_axis)
    
    # 2. umbrella Shaft
    # a line from the top (0,0,z1_axis) to the bottom (0,0,z1_axis - handle_len)
    shaft_bottom_z = z1_axis - handle_len
    out.append(((0, 0, z1_axis), (0, 0, shaft_bottom_z)))
        
    return out

extra_credit_shape = mk_umbrella_with_handle(0, 3, 50, -1, -3)



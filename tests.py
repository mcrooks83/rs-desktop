import math
# head_x = x_ref + scaling_factor * math.cos(flexion_radians) * math.sin(rotation_radians)
# head_y = y_ref + scaling_factor * math.sin(flexion_radians)

scaling_factor_rotation = 30
scaling_factor_flexion = 30

flexion_radians = math.radians(0)
rotation_radians = math.radians(30)

cos_flex = math.cos(flexion_radians)
cos_rot = math.cos(rotation_radians)
sin_flex = math.sin(flexion_radians)
sin_rot = math.sin(rotation_radians)

ref = 0

x = (scaling_factor_rotation * math.cos(flexion_radians) * math.sin(rotation_radians))
y = (scaling_factor_flexion * math.sin(flexion_radians))


print(x)

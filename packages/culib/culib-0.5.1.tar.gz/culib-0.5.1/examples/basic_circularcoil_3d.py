"""
Basic example of usage of calculating 3D field with CircularCoil
"""

import culib as cul

# Init dataframe that will contain fields (beware of huge size of df for 3D)
AXIS_LENGTH_MM = 100
RES_STEP_MM = 1

df_field_3d = cul.init_df_field_3d(AXIS_LENGTH_MM, RES_STEP_MM)

center_pos_mm = (0, 0, 0)

# Define coil
mycoil = cul.CircularCoil(
    axis = 'x_mm',
    r_in_mm = 14,
    r_out_mm = 40,
    L_mm = 32,
    pos_mm = center_pos_mm,
    cur_A = 3.2,
    wire=cul.RoundWire(awg=22),
)

# Print coil characteristics
print(mycoil)

# Calc all 3 components generated via 3d function
df_field_3d = mycoil.calc_field_3d(df_field_3d)

# Compare vs theoritetical values
## Calc Bz component via regular 1d function
df_field = cul.init_df_field()
df_field = mycoil.calc_field(df_field)
## Print value on revolution axis x_mm at position 12 mm
print(cul.get_field_at_pos(df_field, axis='x_mm', Baxis='Bx_total_mT', pos_mm=12))
print(cul.get_field_at_pos(df_field_3d, axis='x_mm', Baxis='Bx_total_mT', pos_mm=(12, 0, 0)))

# Plot 3D components along x_mm axis at fixed (y_mm, z_mm) = (12, -3)
check_pos_mm = (-15, 12, -3)
print(f"(Bx_mT, By_mT, Bz_mT) at position_mm {check_pos_mm} = {cul.get_field_3d_at_pos(df_field_3d, pos_mm=check_pos_mm)}")
chart_3d = cul.plot_field(
    df_field_3d, axis='x_mm', Baxis=['Bx_total_mT', 'By_total_mT', 'Bz_total_mT'],
    pos_mm = check_pos_mm,
    is_save=True, savepath_png='./basic_plots/', save_filename='basic_circularcoil_3d',
    title = '3D fields of my Circular solenoid',
)
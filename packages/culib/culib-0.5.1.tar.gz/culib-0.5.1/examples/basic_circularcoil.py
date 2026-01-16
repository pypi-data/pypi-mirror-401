"""
Basic example of usage of CircularCoil
"""

import culib as cul

# Init display of logging informations
cul.init_logging(log_level='INFO')

# Define coil
mycoil = cul.CircularCoil(
    axis = 'x_mm',              # Axis of revolution (x axis in mm)
    r_in_mm = 14,               # Inner coil radius (in mm
    r_out_mm = 20,              # Outer coil radius (in mm)
    L_mm = 32,                  # Coil length (in mm)
    pos_mm = 20,                # Position of coil center on axis (in mm) (voluntarily offsetted here)
    cur_A = 3.2,                # Current applied (in A)
    wire=cul.RoundWire(awg=22), # Wire definition via Wire object, defined with AWG number 22 (American Wire Gauge)
)

# Print coil characteristics
print(mycoil)

# Init dataframe that will contain columns and arrays for field calculation
df_field = cul.init_df_field(axis_length_mm=160, res_step_mm=0.05)

# Calc and plot field
df_field = mycoil.calc_field(df_field) # Add field of "mycoil" in df_field and update "total" columns
chart = cul.plot_field(
    df_field, axis='x_mm', Baxis='Bx_total_mT',
    is_save=True, savepath_png='./basic_plots/', save_filename='basic_circularcoil',
    subtitle=f"Current (A) = {mycoil.cur_A}, AWG = {mycoil.wire.awg}, My other param = v1.2",
)
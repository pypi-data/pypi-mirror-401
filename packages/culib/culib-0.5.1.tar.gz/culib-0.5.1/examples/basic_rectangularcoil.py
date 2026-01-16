"""
Basic example of usage of RectangularCoil
"""

import culib as cul

cul.init_logging()

# Init dataframe that will contain fields
AXIS_LENGTH_MM = 159.9
RES_STEP_MM = 0.05
df_field = cul.init_df_field(AXIS_LENGTH_MM, RES_STEP_MM)

# Define rectangular coils dimensions
X_in_C_mm = 42
Y_in_C_mm = 82
T_C_mm = 4 # Coil thickness
L_C_mm = 76 # Coil length

# Define coil
C = cul.RectangularCoil(
    axis = 'z_mm',
    X_in_mm = X_in_C_mm,
    Y_in_mm = Y_in_C_mm,
    T_mm = T_C_mm,
    L_mm = L_C_mm,
    pos_mm = 0,
    wire = cul.SquareWire(awg=22),
    cur_A = 3.2,
)

# Print coil characteristics
print(C)

# Print field generated at center in mT
Bz_center_mT = C.calc_field_at_center()
print(Bz_center_mT)

# Calc and plot field
df_field = C.calc_field(df_field)  # Add field of "C" in df_field and update "total" columns
chart = cul.plot_field(
    df_field, axis='z_mm', Baxis='Bz_total_mT',
    is_save=True, savepath_png='./basic_plots/', savepath_html='./basic_plots/interactive_html/', save_filename='basic_rectangularcoil',
    title = 'Field along central axis of Rectangular solenoid',
    subtitle=f"Bz at center (mT) = {Bz_center_mT:.3f}, Current (A) = {C.cur_A}",
)
import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. PROJECT CONFIGURATION & BRANDING ---
st.set_page_config(page_title="MUBAS Drill Auto-System", layout="wide")

# MUBAS Official Branding (Logo and Colors)
MUBAS_LOGO = "https://www.mubas.ac.mw"

# Custom Styling for Traffic Lights and Dashboard
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    .green-light { color: #00ff00; font-size: 30px; font-weight: bold; text-shadow: 0 0 10px #00ff00; border: 2px solid #00ff00; padding: 10px; border-radius: 10px; text-align: center; }
    .red-light { color: #ff4b4b; font-size: 30px; font-weight: bold; border: 2px solid #ff4b4b; padding: 10px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. APP HEADER & GROUP MEMBERS ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image(MUBAS_LOGO, width=150)
with col_title:
    st.title("AUTOMATION IN BLAST HOLE DRILLING")
    st.write("**FACULTY OF ENGINEERING | DEPARTMENT OF MINING**")
    st.info("""
    **Project Team:**  
    1. JOYCE CHIRWA (BMEN/21/SS/008)  
    2. MALACK CHAGWA (BMEN/21/SS/003)  
    3. BENARD MPHANGA (BMEN/19/SS/026)  
    **Supervisor:** DR. ENG. GEOFREY MFUNI
    """)

# --- 3. CONTROL ROOM: DRILL PARAMETER INPUT ---
with st.sidebar:
    st.header("Control Room Console")
    st.subheader("Step 1: Set Design Parameters")
    target_burden = st.number_input("Design Burden (m)", value=3.0)
    target_spacing = st.number_input("Design Spacing (m)", value=4.0)
    target_depth = st.number_input("Target Depth (m)", value=12.0)
    tolerance_angle = 0.1  # 0.1 degree accuracy req
    tolerance_pos = 0.2    # 0.2m position accuracy req
    
    if st.button("CHECK TARGET"):
        st.session_state['plan_active'] = True
        st.success("Plan Broadcasted via Network Tower")

# --- 4. OPERATOR DASHBOARD: REAL-TIME POSITIONING ---
st.divider()
st.header("Field Operator Dashboard")

# Simulating Coordinates (In a real rig, this comes from GPS/RTK sensors)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("###Current Coordinates")
    curr_lat = st.number_input("Live Northing (X)", value=100.15, step=0.01)
    curr_lon = st.number_input("Live Easting (Y)", value=200.45, step=0.01)
    target_lat, target_lon = 100.00, 200.00  # Example target point
    
    dist_err = np.sqrt((curr_lat-target_lat)**2 + (curr_lon-target_lon)**2)
    st.metric("Position Deviation", f"{dist_err:.3f} m", delta=f"{dist_err - tolerance_pos:.3f} m", delta_color="inverse")

with c2:
    st.markdown("###Mast Inclination")
    curr_angle = st.slider("Current Mast Angle (°)", 85.0, 95.0, 87.5, step=0.1)
    angle_err = abs(curr_angle - 90.0)
    st.metric("Angle Deviation", f"{angle_err:.1f}°", delta=f"{angle_err - tolerance_angle:.1f}°", delta_color="inverse")

with c3:
    st.markdown("###Ready to Drill?")
    # ACCURACY CONFIRMATION LOGIC
    is_pos_ok = dist_err <= tolerance_pos
    is_angle_ok = angle_err <= tolerance_angle

    if is_pos_ok and is_angle_ok:
        st.markdown('<div class="green-light">🟢 GREEN LIGHT: PROCEED</div>', unsafe_allow_html=True)
        st.success("Target Accuracy Confirmed: Aligning at 90.0°")
    else:
        st.markdown('<div class="red-light">🔴 RED LIGHT: RE-ALIGN</div>', unsafe_allow_html=True)
        if not is_pos_ok: st.warning("Position Error too high!")
        if not is_angle_ok: st.warning("Inclination Error too high!")

# --- 5. ENTIRE PLANNED AREA MAP ---
st.divider()
st.subheader("Planned Blast Pattern (Full Area View)")
# Create a grid of 50 holes based on burden and spacing
holes = []
for i in range(5):
    for j in range(10):
        holes.append({"X": 500 + (i * target_burden), "Y": 800 + (j * target_spacing), "Status": "Planned"})

df_holes = pd.DataFrame(holes)
# Mark current rig position on the map
df_holes.loc[0, 'Status'] = "CURRENT RIG POSITION"

st.scatter_chart(df_holes, x="Y", y="X", color="Status", size=800)
st.caption("Visualization of the 20-hole drill plan pattern.")

# --- 6. FEEDBACK TO CONTROL ROOM ---
st.divider()
st.subheader("Live Feed to Control Room")
st.write("Information currently being logged at the console:")

# Real-time Data Transmission Simulation
log_entry = {
    "Timestamp": [time.strftime("%H:%M:%S")],
    "Hole ID": ["H-001"],
    "X_Coord": [curr_lat],
    "Y_Coord": [curr_lon],
    "Inclination": [curr_angle],
    "Pos_Deviation": [f"{dist_err:.3f}m"],
    "Status": ["ACCURATE" if (is_pos_ok and is_angle_ok) else "DEVIATED"]
}
st.table(pd.DataFrame(log_entry))

if st.button("Finalize Hole & Save to Report"):
    st.balloons()
    st.success("Data successfully synced with Control Room database.")

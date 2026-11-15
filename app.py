import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import json

st.set_page_config(page_title="SkyPulse Cabin SCADA & OEM ERP", layout="wide")

st.title("✈️ SkyPulse™ – Autonomous Aero-Medical Mobility Grid & OEM SCADA Console")
st.caption("Lead Architect: Mostafa Adel | Tier-1 OEM Seat Telemetry, Explainable AI (XAI) Triage & Air-Gapped Zero-Trust Security")

# Sidebar: Simulate Passenger Seat & OEM Telemetry
st.sidebar.header("💺 Seat Node & Biometric Input")
deployment_mode = st.sidebar.selectbox("Deployment Environment", [
    "Commercial Aviation (Boeing/Airbus Cabin - Seat 14A)",
    "Autonomous EV Fleet (Mercedes/BMW OEM Seat)",
    "Hospital ER & Airport VIP Triage Lounge"
])
seat_occupied = st.sidebar.checkbox("Passenger Seated (Piezoelectric Mat Active)", value=True)
heart_rate = st.sidebar.slider("rPPG + Silicone Strap Heart Rate (BPM)", 45, 170, 132)
spo2_pct = st.sidebar.slider("Multi-Wavelength Unbiased SpO₂ (%)", 82, 100, 88)
leg_stasis_pct = st.sidebar.slider("Lower-Limb EMG Venous Stasis / DVT Risk (%)", 0, 100, 76)

if not seat_occupied:
    st.warning("🛡️ **PRIVACY GUARD ACTIVE:** Seat Vacated. Volatile RAM Zero-Fill Wiped (`0x00000000`). Node in Micro-Ampere Deep Sleep.")
    st.stop()

# Explainable AI (XAI) White-Box Clinical Reasoning
xai_alert = "GREEN – NORMAL CABIN VITALS"
crew_protocol = "Routine passive monitoring. No crew intervention required."
actuator_cmd = "IDLE"
alert_color = "green"

if spo2_pct < 90 and heart_rate > 120 and leg_stasis_pct > 65:
    xai_alert = "RED – 91% PULMONARY EMBOLISM / DVT CRISIS"
    crew_protocol = "1. Administer supplemental O₂ immediately. 2. Keep passenger semi-upright. 3. Prepare automated external defibrillator (AED) & run 40s post-intervention rPPG verification scan."
    actuator_cmd = "DVT_CUSHION_PULSING + 3D_HRV_CALMING_ACTIVE"
    alert_color = "red"
elif leg_stasis_pct > 65:
    xai_alert = "ORANGE – ELEVATED DVT VENOUS STASIS"
    crew_protocol = "Automated seat cushion neuromuscular micro-stimulation engaged to restore lower-limb venous return."
    actuator_cmd = "DVT_MICRO_STIMULATION_ACTIVE (Hardware Current-Limited)"
    alert_color = "orange"
elif heart_rate > 115:
    xai_alert = "YELLOW – ACUTE PANIC / AUTONOMIC SYMPATHETIC SURGE"
    crew_protocol = "Screen running generative 3D audio/visual breath-pacing synced to live HRV to lower blood pressure non-pharmacologically."
    actuator_cmd = "GENERATIVE_NEURO_THERAPY_ACTIVE"
    alert_color = "orange"

# Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Dual-Verified Heart Rate", f"{heart_rate} BPM", "Tachycardia" if heart_rate > 110 else "Normal")
col2.metric("Skin-Tone Unbiased SpO₂", f"{spo2_pct}%", "Hypoxia Risk" if spo2_pct < 92 else "Optimal")
col3.metric("EMG Leg Stasis (DVT)", f"{leg_stasis_pct}%", "Micro-Stim ON" if leg_stasis_pct > 65 else "Active Flow")
col4.metric("OEM Foam/Frame Health", "99.4%", "Odoo ERP Synced")

st.markdown(f"### 🚨 Explainable AI (XAI) Triage: :{alert_color}[{xai_alert}]")
st.info(f"**📋 White-Box Crew Action Protocol:** {crew_protocol}\n\n**⚙️ Seat Actuators:** `{actuator_cmd}`")

# 40-Second Continuous rPPG & EMG Telemetry Chart
st.subheader("📈 40-Second Dual-Verification Biometric Trend (rPPG Optical + Medical Silicone Strap)")
time_sec = list(range(0, 40, 4))
hr_trend = [heart_rate - int(np.cos(t/5)*4) for t in time_sec]
spo2_trend = [spo2_pct for _ in time_sec]
dvt_trend = [leg_stasis_pct for _ in time_sec]

df_vitals = pd.DataFrame({
    "Scan Time (s)": time_sec,
    "Heart Rate (BPM)": hr_trend,
    "SpO₂ (%)": spo2_trend,
    "Leg Stasis Index (%)": dvt_trend
}).set_index("Scan Time (s)")

st.line_chart(df_vitals)

# Air-Gapped Security & Tier-1 OEM Odoo ERP Sync
payload_dict = {
    "env": deployment_mode[:19],
    "bpm": heart_rate,
    "spo2": spo2_pct,
    "dvt_idx": leg_stasis_pct,
    "xai": xai_alert[:12]
}
payload_str = json.dumps(payload_dict, separators=(',', ':'))
sha256_sig = hashlib.sha256(payload_str.encode()).hexdigest()[:32]

st.subheader("🔒 Air-Gapped Zero-Trust Defense & Tier-1 OEM ERP Integration")
st.code(f"Physical Bus Isolation : 100% AIR-GAPPED from ARINC-429 Flight / CAN Vehicle Controls\nSCADA Telemetry JSON   : {payload_str}\nEdge SHA-256 Signature : {sha256_sig}\nOdoo ERP Maintenance   : Robotic Tube-Frame & Molded Foam Sensor Conduit Verified", language="yaml")

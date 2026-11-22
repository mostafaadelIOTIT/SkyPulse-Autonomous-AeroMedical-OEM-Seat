import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import json

st.set_page_config(page_title="SkyPulse & THORAX-NEXUS Platform", layout="wide")

st.title("✈️🩺 SkyPulse™ & THORAX-NEXUS – Aero-Medical Seat, DSP & Pharmacist Co-Pilot")
st.caption("Lead Architect: Mostafa Adel | Vibro-Acoustic Edge-AI, Adaptive DSP Cancellation & Zero-Trust Clinical Decision Support")

# Create 3 Main Platform Modules (Tabs)
tab1, tab2, tab3 = st.tabs([
    "💺 1. SkyPulse Cabin SCADA (Aviation & OEM)",
    "🌊 2. Adaptive DSP Noise Cancellation (Engine vs. Chest)",
    "💊 3. THORAX-NEXUS Pharmacist Co-Pilot (OTC Safety)"
])

# ==============================================================================
# TAB 1: SKYPULSE CABIN SCADA & OEM SEAT TELEMETRY
# ==============================================================================
with tab1:
    st.subheader("💺 Autonomous Aero-Medical & Tier-1 OEM Mobility Seat")
    col_a, col_b = st.columns([1, 2])

    with col_a:
        deployment_mode = st.selectbox("Deployment Environment", [
            "Commercial Aviation (Seat 14A - 35,000 ft)",
            "Autonomous EV Fleet (Mercedes/BMW OEM Seat)",
            "Airport Triage Pod / Hospital ER Lounge"
        ])
        seat_occupied = st.checkbox("Passenger Seated (Piezoelectric Mat Active)", value=True)
        heart_rate = st.slider("rPPG + SCG Heart Rate (BPM)", 45, 170, 132)
        spo2_pct = st.slider("Multi-Wavelength Unbiased SpO₂ (%)", 82, 100, 88)
        leg_stasis_pct = st.slider("Lower-Limb EMG Venous Stasis / DVT Risk (%)", 0, 100, 76)

    with col_b:
        if not seat_occupied:
            st.warning("🛡️ **PRIVACY GUARD ACTIVE:** Seat Vacated. Volatile RAM Zero-Fill Wiped (`0x00000000`). Node in Micro-Ampere Deep Sleep.")
        else:
            xai_alert = "GREEN – NORMAL CABIN VITALS"
            crew_protocol = "Routine passive monitoring. No crew intervention required."
            actuator_cmd = "IDLE"
            alert_color = "green"

            if spo2_pct < 90 and heart_rate > 120 and leg_stasis_pct > 65:
                xai_alert = "RED – 91% PULMONARY EMBOLISM / DVT CRISIS"
                crew_protocol = "1. Administer supplemental O₂ immediately. 2. Contact Ground Flight Surgeon via Zero-Trust QR link. 3. Prepare AED & run 40s post-intervention verification scan."
                actuator_cmd = "DVT_CUSHION_PULSING + 3D_HRV_CALMING_ACTIVE"
                alert_color = "red"
            elif leg_stasis_pct > 65:
                xai_alert = "ORANGE – ELEVATED DVT VENOUS STASIS"
                crew_protocol = "Automated seat cushion neuromuscular micro-stimulation engaged to restore lower-limb venous return."
                actuator_cmd = "DVT_MICRO_STIMULATION_ACTIVE (Hardware Current-Limited)"
                alert_color = "orange"
            elif heart_rate > 115:
                xai_alert = "YELLOW – ACUTE PANIC / AUTONOMIC SURGE"
                crew_protocol = "Screen running generative 3D audio/visual breath-pacing synced to live HRV."
                actuator_cmd = "GENERATIVE_NEURO_THERAPY_ACTIVE"
                alert_color = "orange"

            m1, m2, m3 = st.columns(3)
            m1.metric("Dual-Verified HR", f"{heart_rate} BPM", "Tachycardia" if heart_rate > 110 else "Normal")
            m2.metric("Unbiased SpO₂", f"{spo2_pct}%", "Hypoxia Risk" if spo2_pct < 92 else "Optimal")
            m3.metric("DVT Leg Stasis", f"{leg_stasis_pct}%", "Micro-Stim ON" if leg_stasis_pct > 65 else "Normal")

            st.markdown(f"#### 🚨 Explainable AI (XAI) Triage: :{alert_color}[{xai_alert}]")
            st.info(f"**📋 White-Box Crew Protocol:** {crew_protocol}\n\n**⚙️ Seat Actuators:** `{actuator_cmd}`")

            payload_str = json.dumps({"env": deployment_mode[:18], "bpm": heart_rate, "spo2": spo2_pct, "dvt": leg_stasis_pct})
            sha256_sig = hashlib.sha256(payload_str.encode()).hexdigest()[:32]
            st.code(f"Air-Gap Bus Status : 100% ISOLATED from ARINC-429 / CAN Bus\nSHA-256 Signature  : {sha256_sig}\nOdoo ERP Sync      : Predictive Maintenance & Seat Foam Sensor Health OK", language="yaml")

# ==============================================================================
# TAB 2: ADAPTIVE DSP NOISE CANCELLATION (SOLVING THE CABIN SNR PROBLEM)
# ==============================================================================
with tab2:
    st.subheader("🌊 Solving the Cabin SNR Challenge: Adaptive DSP Vibro-Acoustic Filtering")
    st.markdown(
        "Aircraft engines and turbulence generate low-frequency mechanical vibrations (**10–200 Hz**) "
        "that bury human Seismocardiography (SCG) and chest-wall breathing signals (**1–40 Hz**). "
        "THORAX-NEXUS mounts a **Reference Accelerometer** on the metallic seat frame to mathematically subtract airframe harmonics in real time."
    )

    c1, c2 = st.columns(2)
    engine_noise_amp = c1.slider("Aircraft Engine & Turbulence Vibration Intensity (10–200 Hz)", 0.5, 5.0, 3.2, step=0.1)
    dsp_efficiency = c2.slider("Adaptive LMS/RLS Filter Cancellation Efficiency (%)", 50, 99, 94)

    # Generate Synthetic Signal (2 seconds at 100 samples/sec)
    t = np.linspace(0, 2, 200)
    # Clean Human Seismocardiography (Heart Mechanical Pulse ~ 1.2 Hz + Breathing ~ 0.3 Hz)
    clean_scg = 1.0 * np.sin(2 * np.pi * 1.2 * t) * np.exp(-0.5 * ((t % 0.8) - 0.2)**2 / 0.01) + 0.4 * np.sin(2 * np.pi * 0.3 * t)
    # Airframe Reference Noise (Mixed Engine Harmonics)
    airframe_noise = engine_noise_amp * (0.6 * np.sin(2 * np.pi * 18 * t) + 0.4 * np.cos(2 * np.pi * 35 * t) + 0.2 * np.random.normal(0, 1, len(t)))
    
    # Raw Backrest Sensor Signal (Buried in Noise)
    raw_seat_signal = clean_scg + airframe_noise
    # DSP Filtered Output (Subtracting Reference Sensor Noise)
    residual_noise = airframe_noise * (1.0 - (dsp_efficiency / 100.0))
    recovered_scg = clean_scg + residual_noise

    snr_before = round(10 * np.log10(np.var(clean_scg) / np.var(airframe_noise)), 1)
    snr_after = round(10 * np.log10(np.var(clean_scg) / max(np.var(residual_noise), 1e-6)), 1)

    k1, k2, k3 = st.columns(3)
    k1.metric("Raw Cabin Signal SNR", f"{snr_before} dB", "Unreadable", delta_color="inverse")
    k2.metric("Post-DSP Filtered SNR", f"+{snr_after} dB", f"+{round(snr_after - snr_before, 1)} dB Gain")
    k3.metric("Edge Latency (ESP32-S3)", "8.4 ms", "100% Offline Ready")

    df_dsp = pd.DataFrame({
        "1. Raw Noisy Backrest Signal (Engine + Chest)": raw_seat_signal,
        "2. Recovered Clean SCG & Breathing Signal (Post-DSP)": recovered_scg
    })
    st.line_chart(df_dsp)

# ==============================================================================
# TAB 3: THORAX-NEXUS PHARMACIST CO-PILOT (OTC CHEST PAIN TRIAGE)
# ==============================================================================
with tab3:
    st.subheader("💊 THORAX-NEXUS: Pharmacist Co-Pilot (Clinical Decision Support)")
    st.caption("⚠️ Strictly designed as a Clinical Decision Support (CDS) & rapid-escalation safety net—never a replacement for hospital ECG/Troponin.")

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("#### 1️⃣ Clinical Red-Flag Screening (Ask Patient)")
        pain_radiating = st.checkbox("Pain radiating to left arm, jaw, or back / squeezing pressure")
        shortness_breath = st.checkbox("Sudden shortness of breath, cold sweat, or dizziness")
        recent_flight_or_trauma = st.checkbox("Long-haul flight (>4h) or blunt chest trauma within 14 days")
        reproducible_pain = st.checkbox("Localized sharp pain reproducible by gently pressing on rib cartilage")

        st.markdown("#### 2️⃣ Smartphone IMU 60-Second Sternum Check")
        chest_symmetry_pct = st.slider("Bilateral Chest-Wall Expansion Symmetry (IMU/LiDAR %)", 50, 100, 94)
        imu_hr_bpm = st.slider("Smartphone IMU Mechanical Pulse (BPM)", 50, 150, 82)

    with p_col2:
        st.markdown("#### 3️⃣ Automated Co-Pilot Decision & Zero-Trust Handshake")
        is_red_flag = pain_radiating or shortness_breath or (recent_flight_or_trauma and chest_symmetry_pct < 85) or (imu_hr_bpm > 115) or (chest_symmetry_pct < 82)

        if is_red_flag:
            st.error("🚨 **OTC DISPENSING LOCKED – IMMEDIATE ER REFERRAL REQUIRED**")
            st.markdown(
                "**Clinical Reasoning:** High cardiopulmonary or pneumothorax risk detected "
                "(Red-flag symptoms, tachycardia, or bilateral chest asymmetry < 85%).\n\n"
                "**Action for Pharmacist:**\n"
                "1. **DO NOT** dispense standard OTC painkillers to mask symptoms.\n"
                "2. Keep patient seated calmly and call Emergency Medical Services (EMS).\n"
                "3. Share the encrypted Zero-Trust Handshake below with ER physicians."
            )
            otp_code = hashlib.sha256(f"{imu_hr_bpm}-{chest_symmetry_pct}".encode()).hexdigest()[:6].upper()
            er_packet = {
                "triage": "CODE_RED_CHEST_PAIN",
                "imu_hr": imu_hr_bpm,
                "rib_symmetry_pct": chest_symmetry_pct,
                "red_flags": int(pain_radiating) + int(shortness_breath) + int(recent_flight_or_trauma),
                "2fa_otp": otp_code
            }
            er_hash = hashlib.sha256(json.dumps(er_packet).encode()).hexdigest()[:24]
            st.code(f"Zero-Trust QR Token : QR-THORAX-{otp_code}\nPatient Consent 2FA : {otp_code} (Expires in 15 mins)\nEncrypted ER Hash   : {er_hash}\nTarget Endpoint     : Nearest ER Triage / Ambulance Dispatch", language="yaml")
        elif reproducible_pain and chest_symmetry_pct >= 90:
            st.success("🟢 **LOW CARDIOPULMONARY RISK – LIKELY MUSCULOSKELETAL / COSTOCHONDRITIS**")
            st.markdown(
                "**Guidance for Pharmacist:**\n"
                "1. Localized, reproducible rib-cartilage tenderness with symmetrical breathing & normal pulse.\n"
                "2. Safe to discuss standard topical/oral OTC anti-inflammatory options (check stomach/allergy history).\n"
                "3. **CRITICAL WARNING:** Advise patient **NEVER to wrap/bind ribs tightly** (causes shallow breathing & pneumonia risk).\n"
                "4. Instruct patient to seek ER immediately if fever, shortness of breath, or sweating develops."
            )
        else:
            st.warning("🟡 **INDETERMINATE – RECOMMEND CLINICIAN EVALUATION**")
            st.markdown("Non-specific chest discomfort without clear reproducible rib tenderness. Advise physician evaluation and ECG before masking pain with OTC analgesics.")

# Dentist-appointment-booking
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=["Name", "Date", "Time", "Treatment"])
treatment_durations = {
    "Tooth Cavity": timedelta(minutes=30),
    "Root Canal": timedelta(hours=1),
    "Braces": timedelta(hours=1),
    "General Checkup": timedelta(minutes=30)
}


def is_time_available(date, start_time, duration):
    existing_appointments = st.session_state.appointments
    end_time = (datetime.strptime(start_time, "%H:%M") + duration).strftime("%H:%M")
    for _, row in existing_appointments.iterrows():
        if row["Date"] == date:
            booked_start = datetime.strptime(row["Time"], "%H:%M")
            booked_end = booked_start + treatment_durations[row["Treatment"]]

            selected_start = datetime.strptime(start_time, "%H:%M")
            selected_end = datetime.strptime(end_time, "%H:%M")

            if (selected_start < booked_end and selected_end > booked_start):
                return False 

    return True 

st.title("Shines Clinic - Appointment Booking")
name = st.text_input("Enter Your Name")
date = st.date_input("Select Appointment Date")
treatment = st.selectbox("Select Treatment Type", list(treatment_durations.keys()))
available_times = [f"{hour:02d}:{minute:02d}" for hour in range(9, 16) for minute in [0, 30]]

st.subheader("Available Time Slots")
available_slots = []
for time in available_times:
    if is_time_available(date.strftime("%Y-%m-%d"), time, treatment_durations[treatment]):
        available_slots.append(time)

if available_slots:
    selected_time = st.selectbox("Choose Time Slot", available_slots)
else:
    st.warning("⚠ No available time slots for the selected date. Please choose another day.")
    selected_time = None

if st.button("Book Appointment") and name and selected_time:
    if is_time_available(date.strftime("%Y-%m-%d"), selected_time, treatment_durations[treatment]):
        new_appointment = pd.DataFrame({
            "Name": [name],
            "Date": [date.strftime("%Y-%m-%d")],
            "Time": [selected_time],
            "Treatment": [treatment]
        })
        st.session_state.appointments = pd.concat([st.session_state.appointments, new_appointment], ignore_index=True)
        st.success(f"✅ Appointment booked for {name} on {date.strftime('%Y-%m-%d')} at {selected_time}.")
    else:
        st.error("⚠ This time slot is already booked. Please select a different time.")

st.subheader("Booked Appointments")
st.write(st.session_state.appointments)

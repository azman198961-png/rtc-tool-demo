import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Database Connection (Eta auto file create korbe)
conn = sqlite3.connect('rtc_data.db', check_same_thread=False)
c = conn.cursor()

# Table structure setup
c.execute('''CREATE TABLE IF NOT EXISTS interactions 
             (interaction_id TEXT, channel TEXT, user_id TEXT, vertical TEXT, 
              tag TEXT, reason TEXT, escalated TEXT, timestamp TEXT)''')
conn.commit()

# --- Page Config ---
st.set_page_config(page_title="RTC Beta Tool", layout="wide")

# --- Authentication Logic (Simplified) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to RTC Tool")
    email = st.text_input("Pathao Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email.endswith("@pathao.com") and len(password) > 3: # Basic logic
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Email or Password")
else:
    # --- Main Application ---
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title("🚀 Interaction Entry Tool")

    # --- 1. Search Section ---
    st.subheader("🔍 Search History")
    search_id = st.text_input("Search by Interaction ID (Number/Trip ID)")
    if search_id:
        query = f"SELECT * FROM interactions WHERE interaction_id = '{search_id}'"
        search_res = pd.read_sql(query, conn)
        if not search_res.empty:
            st.dataframe(search_res)
        else:
            st.warning("No previous interaction found with this ID.")

    st.divider()

    # --- 2. Entry Form ---
    st.subheader("📝 New Entry")
    with st.form("rtc_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            i_id = st.text_input("Interaction ID (Calling No/Chat ID)")
            channel = st.selectbox("Channel", ["Inbound", "Live Chat", "Report Issue & Email", "Complaint Management"])
            u_id = st.text_input("Customer/Driver ID")
            vertical = st.text_input("Business Vertical (e.g. Food, Ride)")

        with col2:
            tag = st.selectbox("Tag Category", ["Inquiry", "Complain", "Request", "Other"])
            u_type = st.text_input("User Type")
            escalate = st.radio("Escalated to Complaint Management?", ["No", "Yes"])
        
        reason = st.text_area("Reason for Interaction")
        
        if st.form_submit_button("Submit Entry"):
            if i_id and reason: # Basic validation
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO interactions VALUES (?,?,?,?,?,?,?,?)", 
                          (i_id, channel, u_id, vertical, tag, reason, escalate, timestamp))
                conn.commit()
                st.success(f"Entry Saved! Interaction ID: {i_id}")
            else:
                st.error("Please fill the mandatory fields.")
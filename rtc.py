import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Database Connection
conn = sqlite3.connect('rtc_database.db', check_same_thread=False)
c = conn.cursor()

# Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS interactions 
             (id TEXT, channel TEXT, user_id TEXT, vertical TEXT, tag TEXT, reason TEXT, escalated TEXT, timestamp TEXT)''')
conn.commit()

def main():
    st.set_page_config(page_title="RTC Tool", layout="wide")
    
    st.title("📞 Customer Support RTC Tool")

    # --- Sidebar Login (Simplified) ---
    st.sidebar.header("Login")
    user_type = st.sidebar.selectbox("Login As", ["Agent", "Admin"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        st.success(f"Logged in as {email}")

    # --- Search Bar ---
    st.subheader("🔍 Search Interaction History")
    search_id = st.text_input("Enter Interaction ID (Calling No / Trip ID)")
    if search_id:
        query = f"SELECT * FROM interactions WHERE id = '{search_id}'"
        results = pd.read_sql(query, conn)
        st.write(results)

    st.divider()

    # --- Interaction Entry Form ---
    st.subheader("📝 New Interaction Entry")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            i_id = st.text_input("Interaction ID")
            channel = st.selectbox("Channel", ["Inbound", "Live Chat", "Report Issue & Email", "Complaint Management"])
            u_id = st.text_input("Customer/Driver ID")
            vertical = st.text_input("Business Vertical")

        with col2:
            u_type = st.text_input("User Type")
            tag = st.selectbox("Tag Category", ["Inquiry", "Complain", "Request", "Other"])
            escalate = st.radio("Escalated to Complaint Management?", ["No", "Yes"])
            attachment = st.file_uploader("Attach Media", type=['png', 'jpg', 'mp3', 'mp4'])

        reason = st.text_area("Reason for Interaction")
        
        submit = st.form_submit_button("Submit Entry")

        if submit:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO interactions VALUES (?,?,?,?,?,?,?,?)", 
                      (i_id, channel, u_id, vertical, tag, reason, escalate, timestamp))
            conn.commit()
            st.success("Entry Saved Successfully!")

if __name__ == '__main__':
    main()
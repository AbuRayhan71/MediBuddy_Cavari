import streamlit as st
import pandas as pd
from database import SignupDatabase, validate_email
import datetime

st.set_page_config(
    page_title="MediBuddy Admin - Cavari", 
    page_icon="🏥",
    layout="wide"
)

# Simple authentication
def check_admin_password():
    """Simple password protection for admin panel"""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("# 🔐 Admin Login")
        st.markdown("### Access the MediBuddy Admin Panel")
        
        password = st.text_input("Enter admin password:", type="password")
        
        if st.button("Login"):
            # Change this password for production
            if password == "cavari2024admin":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid password!")
        
        st.stop()

check_admin_password()

# Initialize database
db = SignupDatabase()

# Admin panel CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .signup-table {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 MediBuddy Admin Panel</h1>
    <p>Early Access Signup Management | Powered by Cavari</p>
</div>
""", unsafe_allow_html=True)

# Logout button
if st.button("🚪 Logout", type="secondary"):
    st.session_state.admin_authenticated = False
    st.rerun()

# Get signup data
signups = db.get_all_signups()
total_signups = db.get_signup_count()

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📧 Total Signups", total_signups)

with col2:
    today_signups = len([s for s in signups if s['signup_date'].startswith(datetime.date.today().isoformat())])
    st.metric("📅 Today's Signups", today_signups)

with col3:
    # Last 7 days
    week_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    week_signups = len([s for s in signups if s['signup_date'] >= week_ago])
    st.metric("📊 This Week", week_signups)

with col4:
    # Pending signups
    pending_signups = len([s for s in signups if s['status'] == 'pending'])
    st.metric("⏳ Pending", pending_signups)

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 View Signups", "➕ Manual Add", "📤 Export Data"])

with tab1:
    st.markdown("### 📧 Email Signups")
    
    if signups:
        # Convert to DataFrame for better display
        df = pd.DataFrame(signups)
        df['signup_date'] = pd.to_datetime(df['signup_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Search functionality
        search_email = st.text_input("🔍 Search by email:")
        if search_email:
            df = df[df['email'].str.contains(search_email, case=False, na=False)]
        
        # Display table
        st.dataframe(
            df[['id', 'email', 'signup_date', 'status']], 
            use_container_width=True,
            hide_index=True
        )
        
        # Bulk actions
        st.markdown("### 🛠️ Bulk Actions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📩 Export All Emails"):
                emails = [signup['email'] for signup in signups]
                email_list = '\n'.join(emails)
                st.text_area("Copy emails below:", value=email_list, height=200)
        
        with col2:
            if st.button("🗑️ Clear All Signups", type="secondary"):
                if st.confirm("Are you sure you want to delete ALL signups?"):
                    # This would require a method in the database class
                    st.warning("⚠️ Feature not implemented for safety")
    
    else:
        st.info("📭 No signups yet. Share your early access link to get started!")

with tab2:
    st.markdown("### ➕ Manually Add Signup")
    
    with st.form("manual_add_form"):
        new_email = st.text_input("Email address:")
        manual_ip = st.text_input("IP Address (optional):")
        
        if st.form_submit_button("Add Signup"):
            if new_email:
                if validate_email(new_email):
                    if not db.email_exists(new_email):
                        if db.add_signup(new_email, manual_ip or "manual_add"):
                            st.success(f"✅ Successfully added {new_email}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add signup")
                    else:
                        st.error("❌ Email already exists in database")
                else:
                    st.error("❌ Please enter a valid email address")
            else:
                st.error("❌ Please enter an email address")

with tab3:
    st.markdown("### 📤 Export Signup Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download CSV"):
            filename = db.export_to_csv()
            st.success(f"✅ Exported to {filename}")
            
            # Read the CSV file and provide download
            with open(filename, 'r') as f:
                csv_data = f.read()
            
            st.download_button(
                label="💾 Download File",
                data=csv_data,
                file_name=filename,
                mime="text/csv"
            )
    
    with col2:
        if st.button("📧 Email List Only"):
            emails = [signup['email'] for signup in signups]
            email_string = '\n'.join(emails)
            
            st.download_button(
                label="💾 Download Email List",
                data=email_string,
                file_name=f"emails_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# Real-time stats
st.markdown("---")
st.markdown("### 📊 Quick Stats")

if signups:
    # Chart of signups over time
    df = pd.DataFrame(signups)
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['date'] = df['signup_date'].dt.date
    
    daily_signups = df.groupby('date').size().reset_index(name='signups')
    
    if len(daily_signups) > 1:
        st.line_chart(daily_signups.set_index('date')['signups'])
    else:
        st.info("📈 Chart will show once you have signups over multiple days")

st.markdown("---")
st.markdown("**🏥 MediBuddy Admin Panel** | Powered by Cavari | Last updated: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
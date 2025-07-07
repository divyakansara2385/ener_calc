import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Energy Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .summary-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">⚡ Energy Consumption Calculator</h1>', unsafe_allow_html=True)

# Sidebar for user information
st.sidebar.header("👤 Personal Information")
name = st.sidebar.text_input("Enter your name:", placeholder="Your Name")
age = st.sidebar.number_input("Enter your age:", min_value=1, max_value=120, value=25)
city = st.sidebar.text_input("Enter your city:", placeholder="City Name")
area = st.sidebar.text_input("Enter your area name:", placeholder="Area Name")
housing_type = st.sidebar.selectbox("Where do you live?", ["House", "Tenement"]).lower()

# Appliances section
st.sidebar.header("🏠 Appliances")
has_fridge = st.sidebar.selectbox("Do you have a fridge?", ["Yes", "No"])
has_washing_machine = st.sidebar.selectbox("Do you have a washing machine?", ["Yes", "No"])

# Main content area
if name:
    st.success(f"Welcome, {name}! 👋")
    
    # Display user info
    st.write(f"**Age:** {age} | **City:** {city} | **Area:** {area} | **Housing:** {housing_type.title()}")
    
    st.markdown("---")
    
    # Daily energy calculation section
    st.header("📅 Daily Energy Usage Calculator")
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    energy_results = []
    
    # Initialize session state for storing daily data
    if 'daily_data' not in st.session_state:
        st.session_state.daily_data = {}
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Daily Usage")
        
        # Create a form for each day
        for day in days:
            with st.expander(f"📅 {day}", expanded=False):
                # Room usage
                room_usage = st.selectbox(
                    f"How many BHK do you use on {day}?",
                    [1, 2, 3],
                    key=f"room_{day}"
                )
                
                # Calculate base energy for rooms
                if room_usage == 1:
                    base_energy = 2 * 0.4 + 2 * 0.8  # 2.4 kWh
                elif room_usage == 2:
                    base_energy = 3 * 0.4 + 3 * 0.8  # 3.6 kWh
                elif room_usage == 3:
                    base_energy = 4 * 0.4 + 4 * 0.8  # 4.8 kWh
                
                # AC usage
                ac_count = st.number_input(
                    f"How many ACs do you use on {day}?",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"ac_{day}"
                )
                
                # Fridge usage
                fridge_usage = False
                if has_fridge.lower() == 'yes':
                    fridge_usage = st.checkbox(f"Use fridge on {day}?", key=f"fridge_{day}")
                
                # Washing machine usage
                wm_usage = False
                if has_washing_machine.lower() == 'yes':
                    wm_usage = st.checkbox(f"Use washing machine on {day}?", key=f"wm_{day}")
                
                # Calculate total energy for the day
                total_energy = base_energy + (ac_count * 3)
                
                if fridge_usage:
                    total_energy += 4
                
                if wm_usage:
                    total_energy += 4
                
                # Store daily data
                st.session_state.daily_data[day] = {
                    'bhk': room_usage,
                    'ac_count': ac_count,
                    'fridge': fridge_usage,
                    'washing_machine': wm_usage,
                    'total_energy': total_energy,
                    'base_energy': base_energy
                }
                
                # Display daily summary
                st.info(f"**Total Energy for {day}: {total_energy:.1f} kWh**")
                st.write(f"Breakdown: Base ({room_usage} BHK): {base_energy:.1f} + AC: {ac_count * 3} + Fridge: {4 if fridge_usage else 0} + WM: {4 if wm_usage else 0}")
    
    with col2:
        st.subheader("Quick Summary")
        
        # Calculate weekly totals
        total_weekly = sum([data['total_energy'] for data in st.session_state.daily_data.values()])
        avg_daily = total_weekly / 7 if len(st.session_state.daily_data) == 7 else 0
        
        # Display metrics
        st.metric("Total Weekly Energy", f"{total_weekly:.1f} kWh")
        st.metric("Average Daily Energy", f"{avg_daily:.1f} kWh")
        
        if len(st.session_state.daily_data) > 0:
            max_day = max(st.session_state.daily_data, key=lambda x: st.session_state.daily_data[x]['total_energy'])
            min_day = min(st.session_state.daily_data, key=lambda x: st.session_state.daily_data[x]['total_energy'])
            
            st.metric("Highest Usage", f"{max_day}", f"{st.session_state.daily_data[max_day]['total_energy']:.1f} kWh")
            st.metric("Lowest Usage", f"{min_day}", f"{st.session_state.daily_data[min_day]['total_energy']:.1f} kWh")
    
    # Results section (matching original code output)
    if len(st.session_state.daily_data) > 0:
        st.markdown("---")
        st.header("📊 Results")
        
        # Create the energy list (matching original code format)
        energy_list = []
        for day in days:
            if day in st.session_state.daily_data:
                energy = st.session_state.daily_data[day]['total_energy']
                energy_list.append(f"{day} => {energy:.1f}")
        
        # Display results like the original code
        st.subheader("Energy Consumption List (Original Format)")
        st.code(str(energy_list))
        
        # Create a nice table
        st.subheader("📋 Detailed Daily Breakdown")
        
        table_data = []
        for day in days:
            if day in st.session_state.daily_data:
                data = st.session_state.daily_data[day]
                table_data.append({
                    'Day': day,
                    'BHK Used': data['bhk'],
                    'AC Count': data['ac_count'],
                    'Fridge Used': '✅' if data['fridge'] else '❌',
                    'Washing Machine': '✅' if data['washing_machine'] else '❌',
                    'Base Energy (kWh)': f"{data['base_energy']:.1f}",
                    'Total Energy (kWh)': f"{data['total_energy']:.1f}"
                })
        
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            st.subheader("📈 Energy Consumption Chart")
            
            # Create chart data
            chart_data = pd.DataFrame({
                'Day': [item['Day'] for item in table_data],
                'Energy (kWh)': [float(item['Total Energy (kWh)']) for item in table_data]
            })
            
            
            # Bar chart
            fig = px.bar(
                chart_data, 
                x='Day', 
                y='Energy (kWh)',
                title='Daily Energy Consumption',
                color='Energy (kWh)',
                color_continuous_scale='viridis'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Line chart
            fig_line = px.line(
                chart_data, 
                x='Day', 
                y='Energy (kWh)',
                title='Energy Consumption Trend',
                markers=True
            )
            fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
            st.plotly_chart(fig_line, use_container_width=True)
    
    # Reset button
    if st.button("🔄 Reset All Data", type="secondary"):
        st.session_state.daily_data = {}
        st.rerun()

else:
    st.info("👆 Please enter your name in the sidebar to get started!")
    
    # Show preview of the calculator
    st.subheader("📱 About This Calculator")
    st.write("""
    This Energy Consumption Calculator helps you track your daily electricity usage based on:
    
    - **Room Usage**: Calculate base energy consumption for 1, 2, or 3 BHK
    - **Air Conditioning**: Track AC usage (3 kWh per unit)
    - **Appliances**: Monitor fridge and washing machine usage (4 kWh each)
    - **Weekly Analysis**: Get insights into your consumption patterns
    
    **How to use:**
    1. Fill in your personal information in the sidebar
    2. Specify which appliances you have
    3. Enter daily usage for each day of the week
    4. View your results and charts
    """)
    
    # Energy calculation formula
    st.subheader("⚡ Energy Calculation Formula")
    st.write("""
    **Base Energy by Room Type:**
    - 1 BHK: 2×0.4 + 2×0.8 = 2.4 kWh
    - 2 BHK: 3×0.4 + 3×0.8 = 3.6 kWh  
    - 3 BHK: 4×0.4 + 4×0.8 = 4.8 kWh
    
    **Additional Appliances:**
    - Air Conditioner: 3 kWh per unit
    - Refrigerator: 4 kWh (if used)
    - Washing Machine: 4 kWh (if used)
    
    **Total = Base Energy + (AC Count × 3) + Fridge + Washing Machine**
    """)

# Footer
st.markdown("---")
st.markdown("**Built with Streamlit** | Energy Calculator v1.0")
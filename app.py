import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(page_title="IMU Data Trimmer", layout="wide")

# 2. Custom HTML and CSS Integration
st.markdown("""
    <style>
        /* Custom CSS to style the dashboard */
        .main {
            background-color: #f8f9fa;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #218838;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Dashboard Title
st.markdown("<h1>IMU Data Trimmer Dashboard</h1>", unsafe_allow_html=True)
st.write("Upload your IMU data, use the slider to trim the start/end, and download the cleaned file.")

# 3. Load Button (File Uploader)
uploaded_file = st.file_uploader("Upload IMU CSV File", type=['csv'])

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)
    
    st.write("### 📊 Data Preview")
    st.dataframe(df.head(), use_container_width=True)
    
    # Let user select the time axis and features to plot
    cols = list(df.columns)
    time_col = st.selectbox("Select Time/Index Column (X-axis):", cols, index=0)
    
    # Automatically select Acc and Gyro columns if they exist
    default_y = [c for c in cols if 'Acc' in c or 'Gyro' in c]
    feature_cols = st.multiselect("Select Features to Plot (Y-axis):", cols, default=default_y)
    
    if time_col and feature_cols:
        st.write("---")
        st.write("### ✂️ Trimmer Window")
        
        # 4. Trimmer Window (Dual-ended Slider)
        min_idx = 0
        max_idx = len(df) - 1
        
        start_idx, end_idx = st.slider(
            "Drag the handles to trim starting and ending data (by row index):",
            min_value=min_idx,
            max_value=max_idx,
            value=(min_idx, max_idx)
        )
        
        # Trim the dataframe based on slider values
        trimmed_df = df.iloc[start_idx:end_idx+1].copy()
        
        st.success(f"Data trimmed! Showing rows {start_idx} to {end_idx}. Total rows: {len(trimmed_df)}")
        
        # Plot the trimmed data
        fig = px.line(
            trimmed_df, 
            x=time_col, 
            y=feature_cols, 
            title="Trimmed IMU Signal Visualization"
        )
        fig.update_layout(xaxis_title=time_col, yaxis_title="Sensor Values", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("---")
        
        # 5. Download Button
        # Convert trimmed dataframe back to CSV
        csv_buffer = trimmed_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="⬇️ Download Trimmed Data (CSV)",
            data=csv_buffer,
            file_name=f"trimmed_{uploaded_file.name}",
            mime="text/csv"
        )
else:
    st.info("Please upload a CSV file to get started.")
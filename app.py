import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="California Housing Price Prediction", page_icon="🏠")

st.title("🏠 California Housing Price Prediction")
st.write("Enter housing features to predict median house value (in $100,000s)")

# Get secrets (token and endpoint)
try:
    pat = st.secrets["SNOWFLAKE_PAT"]
    scoring_endpoint = st.secrets["SCORING_ENDPOINT"]
except:
    st.error("❌ Missing secrets! Please configure SNOWFLAKE_PAT and SCORING_ENDPOINT")
    st.stop()

# Housing feature inputs
st.subheader("🏘️ Housing Features Input")

col1, col2 = st.columns(2)

with col1:
    med_inc = st.number_input(
        "Median Income (MedInc)",
        value=3.8462,
        step=0.1,
        format="%.4f",
        min_value=0.0,
        max_value=15.0,
        help="Median income in block group"
    )
    
    house_age = st.number_input(
        "House Age (HouseAge)", 
        value=27.0,
        step=1.0,
        format="%.1f",
        min_value=1.0,
        max_value=52.0,
        help="Median house age in block group"
    )
    
    ave_rooms = st.number_input(
        "Average Rooms (AveRooms)",
        value=5.4298,
        step=0.1,
        format="%.4f", 
        min_value=0.8,
        max_value=141.0,
        help="Average number of rooms per household"
    )
    
    ave_bedrms = st.number_input(
        "Average Bedrooms (AveBedrms)",
        value=1.0967,
        step=0.01,
        format="%.4f",
        min_value=0.3,
        max_value=34.0,
        help="Average number of bedrooms per household"
    )

with col2:
    population = st.number_input(
        "Population",
        value=3375.0,
        step=100.0,
        format="%.0f",
        min_value=3.0,
        max_value=35682.0,
        help="Block group population"
    )
    
    ave_occup = st.number_input(
        "Average Occupancy (AveOccup)",
        value=3.0625,
        step=0.1,
        format="%.4f",
        min_value=0.7,
        max_value=1243.0,
        help="Average number of household members"
    )
    
    latitude = st.number_input(
        "Latitude",
        value=33.69,
        step=0.01,
        format="%.2f",
        min_value=32.5,
        max_value=42.0,
        help="Block group latitude"
    )
    
    longitude = st.number_input(
        "Longitude", 
        value=-117.96,
        step=0.01,
        format="%.2f",
        min_value=-124.3,
        max_value=-114.3,
        help="Block group longitude"
    )

# Prediction button
if st.button("🔍 Get Housing Price Prediction", type="primary"):
    with st.spinner("Getting prediction from Snowflake..."):
        try:
            # Prepare the request - 8 feature format for housing
            headers = {"Authorization": f'Snowflake Token="{pat}"'}
            payload = {
                "data": [[
                    0,  # Index
                    med_inc, 
                    house_age, 
                    ave_rooms, 
                    ave_bedrms, 
                    population, 
                    ave_occup, 
                    latitude, 
                    longitude
                ]]
            }
            
            # Make the API call
            response = requests.post(
                scoring_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display result
                st.success("✅ Prediction successful!")
                
                # Extract prediction from your specific format
                try:
                    if "data" in result and len(result["data"]) > 0:
                        prediction_data = result["data"][0][1]  # Get the nested dict
                        
                        if isinstance(prediction_data, dict) and "output_feature_0" in prediction_data:
                            prediction_value = prediction_data["output_feature_0"]
                            
                            # Convert to actual dollar amount
                            house_price = prediction_value * 100000  # Convert from hundreds of thousands
                            
                            # Display in your requested format
                            st.markdown(f"### 🎯 Predicted Median House Value: **${house_price:,.0f}**")
                            st.markdown(f"*Raw prediction value: {prediction_value:.4f} (in $100,000s)*")
                            
                            # Also show as metric for visual appeal
                            col1, col2, col3 = st.columns([1,2,1])
                            with col2:
                                st.metric(
                                    label="Median House Value",
                                    value=f"${house_price:,.0f}"
                                )
                            
                            # Show input summary
                            st.info(f"🏠 Prediction for California housing district: **${house_price:,.0f}**")
                            
                        else:
                            st.warning("❌ Could not find 'output_feature_0' in prediction data")
                            st.write("**Received data:**")
                            st.json(prediction_data)
                    else:
                        st.warning("❌ No prediction data found in response")
                        
                except Exception as format_error:
                    st.error(f"❌ Error extracting prediction: {format_error}")
                    st.write("**Raw response for debugging:**")
                    st.json(result)
                
                # Optional: Show raw response in expandable section
                with st.expander("🔍 Show technical details"):
                    st.json(result)
                    
            else:
                st.error(f"❌ API Error {response.status_code}")
                st.code(response.text)
                
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection error. Check your endpoint URL.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Example housing districts section
st.subheader("💡 Try These Example California Districts")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏖️ Expensive Coastal Area"):
        st.rerun()

with col2:
    if st.button("🏘️ Average Suburban Area"):
        st.rerun()
        
with col3:
    if st.button("🌲 Rural Inland Area"):
        st.rerun()

# Feature information section
with st.expander("📊 Feature Information"):
    st.markdown("""
    **California Housing Dataset Features:**
    
    - **MedInc**: Median income in block group (in tens of thousands)
    - **HouseAge**: Median house age in block group (years)
    - **AveRooms**: Average number of rooms per household
    - **AveBedrms**: Average number of bedrooms per household  
    - **Population**: Block group population
    - **AveOccup**: Average number of household members
    - **Latitude**: Block group latitude (degrees)
    - **Longitude**: Block group longitude (degrees)
    
    **Target**: Median house value in hundreds of thousands of dollars
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Snowflake ML and Streamlit | California Housing Price Prediction*")

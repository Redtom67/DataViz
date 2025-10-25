
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Conclusions & Recommendations", page_icon="📋", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('./data/df_dataset.csv')

df = load_data()

st.title("Part 4: Conclusions & Recommendations")
st.markdown("""
## Key Findings

The data indicates that road safety initiatives should concentrate on specific driver groups and conditions that present the greatest risk.

### Focused Warnings for Drivers

**Young Male Drivers:**
- Drivers aged 21–30, particularly men (who represent 67.2% of accidents), are most frequently involved in crashes.
- Safety campaigns should be designed to reach this demographic, emphasizing risk perception, responsible speed management, and awareness of overconfidence.

**"Good Condition" Awareness:**
- Interestingly, the majority of accidents occur in normal weather and on dry roads.
- This suggests that complacency plays a significant role. Drivers should be reminded that safe conditions do not eliminate risk and that attention and caution are always required.

**Speed Limit Hotspots:**
- Serious collisions are most common at 50 km/h and 80 km/h speed zones — typically urban main roads and rural routes.
- Campaign messaging should reinforce the importance of speed discipline and situational awareness in these high-risk areas.

**Light Vehicle Emphasis:**
- Most crashes involve light vehicles (cars).
- Safety efforts should therefore prioritize car drivers, promoting defensive driving habits and adherence to traffic rules.

### Summary

Road safety messages should extend beyond poor weather warnings to focus on young male drivers, speed management, and the hidden risks of good driving conditions, where overconfidence often leads to accidents.
""")

col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    st.image("./images/back.jpg", use_container_width=True)
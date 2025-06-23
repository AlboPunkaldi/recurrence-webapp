import streamlit as st
import pandas as pd

# 1) Global CSS for theme, fonts, and responsive sidebar
st.markdown("""
<style>
/* Load Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

/* Global typography */
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
}

/* Header styling */
header {
  background-color: #0066FF !important;
  padding: 1rem;
  color: white !important;
}

/* Primary buttons */
button[kind="primary"] {
  background-color: #0066FF !important;
  border-radius: 0.5rem !important;
  padding: 0.5rem 1rem !important;
  font-weight: 600 !important;
}

/* Mobile sidebar slide-in */
@media (max-width: 768px) {
  .css-1d391kg {
    position: fixed !important;
    z-index: 1000;
    top: 0; left: 0; bottom: 0;
    width: 70% !important;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
  }
  .css-1d391kg.css-catel2 {
    transform: translateX(0);
  }
}

/* Table cell padding */
.stDataFrame td, .stDataFrame th {
  padding: 0.75rem;
  border-bottom: 1px solid #E0E0E0;
}
</style>
""", unsafe_allow_html=True)

# 2) Page configuration
st.set_page_config(
    page_title="Recurrence Explorer",
    page_icon="🔁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3) Sidebar inputs
with st.sidebar:
    MOD = st.number_input("Modulus", value=101, min_value=2)
    N   = st.number_input("Number of terms", value=300, min_value=1)
    initials = st.text_input("Initial terms (comma-separated)", "1,2,3")
    st.markdown("---")
    if st.button("Compute", use_container_width=True):
        st.session_state.compute = True

# 4) Title
st.markdown("<h1 style='text-align:center;'>Recurrence Explorer 🔁</h1>", unsafe_allow_html=True)

# 4.1) Intro paragraph
st.markdown(""" Welcome to Recurrence Explorer! This application lets you define any three-term integer recurrence, choose your modulus, see exactly how the sequence evolves, and which residues appear or are missing.""")

# 5) Compute and display when button clicked
if "compute" in st.session_state:
    # Parse initial terms
    init = [int(x.strip()) for x in initials.split(",") if x.strip()]

    # Define the recurrence
    def recurrence(seq, i):
        return seq[i-1]**2 - seq[i-2]*seq[i-3]

    # Build sequence and trace
    f = init.copy()
    trace = []
    for i in range(len(init), N):
        a, b, c = f[i-3], f[i-2], f[i-1]
        raw = recurrence(f, i)
        modded = raw % MOD
        trace.append({
            "n":           i,
            "f[n-3]":      a,
            "f[n-2]":      b,
            "f[n-1]":      c,
            "raw":         raw,
            f"f[n] mod {MOD}": modded
        })
        f.append(modded)

    # 6) Tabs
    tab1, tab2 = st.tabs(["📋 Detailed Trace", "📊 Summary"])

    # Detailed Trace
    with tab1:
        df = pd.DataFrame(trace)
        st.dataframe(df, use_container_width=True, height=400)

    # Summary
    with tab2:
        distinct_count = len(set(f))
        missing = sorted(set(range(MOD)) - set(f))
        modulus_val = MOD

        # Build a <br>-separated string of missing residues
        missing_html = "<br>".join(map(str, missing)) if missing else "None"

        # Render three uniform cards in a flex row
        cards_html = f"""
        <div style="display:flex; gap:1rem; flex-wrap:wrap;">
          <!-- Distinct residues card -->
          <div style="
            flex:1; min-width:8rem;
            background:white; border-radius:0.75rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.1);
            padding:1rem;
          ">
            <h3 style="margin:0 0 0.5rem;">Distinct residues</h3>
            <p style="font-size:2.5rem; margin:0;">{distinct_count}</p>
          </div>

          <!-- Missing residues card -->
          <div style="
            flex:1; min-width:8rem;
            background:white; border-radius:0.75rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.1);
            padding:1rem;
          ">
            <h3 style="margin:0 0 0.5rem;">Missing residue(s)</h3>
            <p style="
              font-size:2.5rem;
              margin:0;
              white-space:pre-wrap;
              line-height:1.2;
            ">{missing_html}</p>
          </div>

          <!-- Modulus card -->
          <div style="
            flex:1; min-width:8rem;
            background:white; border-radius:0.75rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.1);
            padding:1rem;
          ">
            <h3 style="margin:0 0 0.5rem;">Modulus</h3>
            <p style="font-size:2.5rem; margin:0;">{modulus_val}</p>
          </div>
        </div>
        """
        st.markdown(cards_html, unsafe_allow_html=True)
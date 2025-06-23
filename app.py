import streamlit as st
import pandas as pd

# Sidebar inputs
MOD = st.sidebar.number_input("Modulus", value=101, min_value=2)
N = st.sidebar.number_input("Number of terms", value=300, min_value=1)
initials = st.sidebar.text_input("Initial terms (comma-separated)", "1,2,3")

# Parse initial terms
init = [int(x.strip()) for x in initials.split(",") if x.strip()]

# Define the recurrence function here
def recurrence(seq, i):
    # Example: f[n] = f[n-1]^2 - f[n-2]*f[n-3]
    return seq[i-1]**2 - seq[i-2]*seq[i-3]

# Compute sequence and build trace
f = init.copy()
trace = []
for i in range(len(init), N):
    a, b, c = f[i-3], f[i-2], f[i-1]
    raw = recurrence(f, i)
    modded = raw % MOD
    trace.append({
        "n": i,
        "f[n-3]": a,
        "f[n-2]": b,
        "f[n-1]": c,
        "raw": raw,
        f"f[n] mod {MOD}": modded
    })
    f.append(modded)

# Display the detailed trace
st.title("Recurrence Computation Trace")
st.dataframe(pd.DataFrame(trace), height=400)

# Summary statistics
distinct = set(f)
missing = sorted(set(range(MOD)) - distinct)

st.subheader("Summary")
st.write(f"Computed first {N} terms mod {MOD}.")
st.write("Number of distinct residues:", len(distinct))
if missing:
    st.write("Missing residue(s):", missing)
else:
    st.write("All residues appeared.")
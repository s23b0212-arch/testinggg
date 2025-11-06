import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Genetic Algorithm Parameters", layout="centered")

# ------------------ PAGE STYLE ------------------
st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        color: #1E88E5;
        font-size: 36px;
        text-shadow: 1px 1px 2px #90CAF9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ PAGE TITLE ------------------
st.markdown("<h1>Genetic Algorithm Parameter Settings</h1>", unsafe_allow_html=True)

# ------------------ INPUT SECTION ------------------
st.subheader("Adjust the Parameters Below:")

# Create sliders for parameters
CO_R = st.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,          # Default
    step=0.01,
    help="Controls how much of the parents' genes are combined during crossover."
)

MUT_R = st.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.02,         # Default
    step=0.01,
    help="Determines how often random mutations occur in the population."
)

# ------------------ DISPLAY RESULTS ------------------
st.write("### Selected Parameters:")
st.write(f"- **Crossover Rate (CO_R):** {CO_R}")
st.write(f"- **Mutation Rate (MUT_R):** {MUT_R}")

st.success("Parameters successfully set! You can now proceed to run the Genetic Algorithm with these values.")

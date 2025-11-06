import streamlit as st
import pandas as pd
import random

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="TV Program Scheduler - User Input", layout="wide")

# ------------------ CSS STYLING ------------------
st.markdown("""
<style>
    body {
        background-color: #f5f5dc; /* Beige */
    }
    h1 {
        text-align: center;
        color: #e67e22;
        font-size: 42px;
        font-weight: bold;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    p {
        text-align: center;
        color: #444;
        font-weight: bold;
    }
    [data-testid="stSidebar"] {
        background-color: #FFE4B5; /* Light orange sidebar */
    }
    .stButton button {
        background-color: #e67e22;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #ca6f1e;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1>🎬 TV Program Scheduler - User Input</h1>", unsafe_allow_html=True)
st.markdown("<p>Enter your TV programs and viewer ratings manually to find the optimal schedule!</p>", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("GENETIC ALGORITHM PARAMETERS")
CO_R = st.sidebar.slider("Crossover Rate", 0.0, 0.95, 0.8, 0.01)
MUT_R = st.sidebar.slider("Mutation Rate", 0.01, 0.05, 0.02, 0.01)
GEN = st.sidebar.number_input("Generations", 50, 500, 100, 10)
POP = st.sidebar.number_input("Population Size", 10, 200, 50, 10)
EL_S = 2

# ------------------ USER INPUT SECTION ------------------
st.subheader("📺 Enter Program Ratings")
num_programs = st.number_input("Number of programs to schedule:", 3, 10, 5)

programs = []
ratings = {}

for i in range(num_programs):
    st.markdown(f"#### Program {i+1}")
    program_name = st.text_input(f"Enter program name {i+1}:", key=f"name_{i}")
    program_ratings = []
    
    cols = st.columns(3)
    for hour in range(6, 9):  # You can adjust time slots here
        rating = cols[hour-6].slider(f"Hour {hour}", 0.0, 1.0, random.uniform(0.2, 0.8), 0.1, key=f"rate_{i}_{hour}")
        program_ratings.append(rating)
    
    if program_name:
        programs.append(program_name)
        ratings[program_name] = program_ratings

# ------------------ GA FUNCTIONS ------------------
def fitness(schedule, ratings):
    return sum(ratings[prog][i % len(ratings[prog])] for i, prog in enumerate(schedule))

def initialize_population(programs, size):
    return [random.sample(programs, len(programs)) for _ in range(size)]

def crossover(p1, p2):
    point = random.randint(1, len(p1)-2)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def mutate(schedule, all_programs):
    i = random.randint(0, len(schedule)-1)
    schedule[i] = random.choice(all_programs)
    return schedule

def genetic_algorithm(all_programs, ratings):
    population = initialize_population(all_programs, POP)
    for _ in range(GEN):
        population = sorted(population, key=lambda s: fitness(s, ratings), reverse=True)
        new_pop = population[:EL_S]
        while len(new_pop) < POP:
            p1, p2 = random.choices(population[:10], k=2)
            if random.random() < CO_R:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            if random.random() < MUT_R:
                c1 = mutate(c1, all_programs)
            if random.random() < MUT_R:
                c2 = mutate(c2, all_programs)
            new_pop.extend([c1, c2])
        population = new_pop
    return max(population, key=lambda s: fitness(s, ratings))

# ------------------ RUN OPTIMIZATION ------------------
if st.button("Generate Optimal Schedule"):
    if len(programs) > 0:
        schedule = genetic_algorithm(programs, ratings)
        total_rating = fitness(schedule, ratings)
        hours = [f"Hour {i+6}" for i in range(len(schedule))]
        
        df_result = pd.DataFrame({"Hour": hours, "Program": schedule})
        
        # Stylish table with light orange background
        styled_df = df_result.style.set_properties(**{
            'background-color': '#FFE4B5',
            'color': 'black',
            'font-weight': 'bold'
        })
        
        st.success(f"Optimal schedule generated! ⭐ Total Rating: {total_rating:.2f}")
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.warning("Please enter at least one program.")

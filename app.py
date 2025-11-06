import streamlit as st
import pandas as pd
import random

# ------------------ 1. PAGE CONFIG ------------------
st.set_page_config(page_title="TV Program Scheduler using GA", layout="wide")

st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        color: #1E88E5;
        text-shadow: 1px 1px 2px #90CAF9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>📺 TV Program Scheduling using Genetic Algorithm</h1>", unsafe_allow_html=True)

# ------------------ 2. READ CSV FILE ------------------
st.subheader("📂 Upload Program Ratings CSV File")

uploaded_file = st.file_uploader("Upload your program_ratings.csv file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Original Rating Data:")
    st.dataframe(df)

    # ------------------ 3. MODIFY RATING DATA ------------------
    st.info("You can modify ratings below (optional).")

    edited_df = st.data_editor(df, num_rows="dynamic")
    st.write("### Modified Rating Data:")
    st.dataframe(edited_df)

    # Convert dataframe to dictionary {Program: [ratings]}
    program_ratings = {}
    for i, row in edited_df.iterrows():
        program = row[0]
        ratings = [float(x) for x in row[1:]]
        program_ratings[program] = ratings

    # ------------------ 4. STREAMLIT PARAMETER INPUT ------------------
    st.subheader("⚙️ Genetic Algorithm Parameters")

    CO_R = st.slider(
        "Crossover Rate (CO_R)",
        0.0, 0.95, 0.8, 0.01,
        help="Controls how much parent genes combine during crossover."
    )

    MUT_R = st.slider(
        "Mutation Rate (MUT_R)",
        0.01, 0.05, 0.02, 0.01,
        help="Determines how often random mutations occur in the population."
    )

    st.success(f"✅ Parameters set: Crossover = {CO_R}, Mutation = {MUT_R}")

    # ------------------ 5. RUN GENETIC ALGORITHM ------------------
    st.subheader("🚀 Run Genetic Algorithm")

    if st.button("Run Scheduler"):
        programs = list(program_ratings.keys())

        # Assume time slots equal number of programs
        num_slots = len(programs)
        population_size = 10
        generations = 20

        # Initialize population (each schedule is a random permutation)
        def create_population():
            return [random.sample(programs, num_slots) for _ in range(population_size)]

        # Fitness: total rating sum (for demonstration)
        def fitness(schedule):
            total = 0
            for i, prog in enumerate(schedule):
                total += program_ratings[prog][i % len(program_ratings[prog])]
            return total

        # Selection (Tournament)
        def selection(population):
            return max(random.sample(population, 2), key=fitness)

        # Crossover (single point)
        def crossover(p1, p2):
            if random.random() < CO_R:
                point = random.randint(1, num_slots - 2)
                child = p1[:point] + [p for p in p2 if p not in p1[:point]]
                return child
            else:
                return p1

        # Mutation (swap two programs)
        def mutate(schedule):
            if random.random() < MUT_R:
                i, j = random.sample(range(num_slots), 2)
                schedule[i], schedule[j] = schedule[j], schedule[i]
            return schedule

        # GA loop
        population = create_population()
        for _ in range(generations):
            new_pop = []
            for _ in range(population_size):
                parent1 = selection(population)
                parent2 = selection(population)
                child = crossover(parent1, parent2)
                child = mutate(child)
                new_pop.append(child)
            population = new_pop

        best_schedule = max(population, key=fitness)

        # ------------------ 6. DISPLAY RESULTING SCHEDULE ------------------
        st.subheader("🗓️ Generated TV Schedule")

        schedule_df = pd.DataFrame({
            "Time Slot": [f"Slot {i+1}" for i in range(num_slots)],
            "Program": best_schedule
        })

        st.table(schedule_df)
        st.success("✅ Genetic Algorithm completed successfully!")
else:
    st.warning("Please upload a CSV file to begin.")

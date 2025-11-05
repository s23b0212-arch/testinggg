import csv
import random
import streamlit as st

# --- Function to read the CSV file ---
def read_csv_to_dict(file_path):
    program_ratings = {}
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
    return program_ratings


# --- Streamlit UI ---
st.title("📺 TV Scheduling using Genetic Algorithm")
st.write("This app finds the **optimal TV program schedule** using a Genetic Algorithm based on viewer ratings.")

# Load the dataset
try:
    file_path = 'program_ratings.csv'  # make sure this file exists in your repo
    program_ratings_dict = read_csv_to_dict(file_path)
    st.success("✅ Successfully loaded program_ratings.csv!")
except FileNotFoundError:
    st.error("❌ program_ratings.csv not found! Please make sure it's uploaded in the same GitHub repo as app.py.")
    st.stop()

# --- Parameters ---
GEN = st.slider("Number of Generations (GEN)", 10, 200, 100)
POP = st.slider("Population Size (POP)", 10, 100, 50)
CO_R = st.slider("Crossover Rate (CO_R)", 0.1, 1.0, 0.8)
MUT_R = st.slider("Mutation Rate (MUT_R)", 0.0, 1.0, 0.2)
EL_S = st.slider("Elitism Size (EL_S)", 1, 5, 2)

ratings = program_ratings_dict
all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))


# --- Fitness Function ---
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot % len(ratings[program])]
    return total_rating


# --- Initialize Population ---
def initialize_pop(programs, time_slots):
    population = []
    for _ in range(POP):
        schedule = random.sample(programs, len(programs))
        population.append(schedule)
    return population


# --- Crossover ---
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2


# --- Mutation ---
def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule


# --- Genetic Algorithm ---
def genetic_algorithm(generations=GEN, population_size=POP, crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S):
    population = initialize_pop(all_programs, all_time_slots)

    for _ in range(generations):
        population.sort(key=fitness_function, reverse=True)
        new_population = population[:elitism_size]

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    return max(population, key=fitness_function)


# --- Run the Algorithm ---
if st.button("Run Genetic Algorithm"):
    best_schedule = genetic_algorithm()
    total_rating = fitness_function(best_schedule)

    st.subheader("📅 Final Optimal Schedule:")
    for time_slot, program in enumerate(best_schedule):
        st.write(f"Time Slot {all_time_slots[time_slot % len(all_time_slots)]:02d}:00 — {program}")

    st.success(f"⭐ Total Ratings: {total_rating}")

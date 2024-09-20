import pandas as pd
import numpy as np
import random
import time
import sofia_astar
import tkinter as tk
import csv
from tkinter import simpledialog, messagebox, Checkbutton, IntVar, Toplevel, Button

city_to_railways = {
            "Bhubaneswar": "Bhubaneswar Railway Station(Bhubaneswar)",
            "Cuttack": "Cuttack Junction Railway Station(Cuttack)",
            "Kolkata": "Howrah Junction Railway Station(Kolkata)",
            "Visakhapatnam": "Visakhapatnam Railway Station(Visakhapatnam)",
        }

class GeneticAlgorithm:
    def __init__(self, travel_data_path, places_data_path):
        self.travel_data = pd.read_csv(travel_data_path)
        self.places_data = pd.read_csv(places_data_path, index_col="PLACES")
        self.places_customization=[]
        self.merged_data = pd.merge(
            self.travel_data,
            self.places_data,
            left_on="Destination",
            right_index=True,
            how="left",
        )
        self.city_to_railways = {
            "Bhubaneswar": "Bhubaneswar Railway Station(Bhubaneswar)",
            "Cuttack": "Cuttack Junction Railway Station(Cuttack)",
            "Kolkata": "Howrah Junction Railway Station(Kolkata)",
            "Visakhapatnam": "Visakhapatnam Railway Station(Visakhapatnam)",
        }

    def save_merged_data_to_csv(self, filename="merged_data.csv"):
        self.merged_data.to_csv(filename, index=False)
        print(f"Merged data saved to {filename}")

    def show_customization_dialog(self, root,starting_city):
        dialog = Toplevel(root)
        dialog.title("Select Places to Customize from city f{starting_city}")
        dialog.geometry('600x400')
        places = list(self.places_data.index)
        city_places = [p for p in places if self.extract_city_name(p) == starting_city]
        vars = {}
        for place in city_places:
            var = IntVar()
            chk = Checkbutton(dialog, text=place, variable=var, anchor='w', width=40, pady=5)
            chk.pack()
            vars[place] = var
        def confirm():
            self.places_customization = [place for place, var in vars.items() if var.get() == 1]
            dialog.destroy()
            root.destroy()

        Button(dialog, text="Confirm", command=confirm).pack(pady=10)

        dialog.transient(root)
        dialog.grab_set()
        dialog.wait_window()

    def gui_input(self):
        root = tk.Tk()
        root.title("Main Window")
        root.geometry('25x25')
        starting_city = simpledialog.askstring("Input", "Enter the starting city:", parent=root)
        max_time = simpledialog.askfloat("Input", "Enter the maximum allowable time in hours:", parent=root)
        max_cost = simpledialog.askfloat("Input", "Enter the maximum allowable cost in Rs:", parent=root)
        source_astar = simpledialog.askstring("Input", "Where do you want to start your journey: ", parent=root)
        while True:
            value = simpledialog.askstring("Input", "Enter 1 for all places and 2 for customization: ", parent=root)
            if value not in ['1', '2']:
                tk.messagebox.showerror("Invalid Input", "Please enter 1 or 2")
                continue
            else:
                break
        if value == '1':
            places = list(self.places_data.index)
            self.places_customization = [p for p in places if self.extract_city_name(p) == starting_city]
            root.destroy()
        elif value == '2':
            self.show_customization_dialog(root,starting_city)    
        else:
            messagebox.showerror("Invalid Input", "Please enter 1 or 2")
        
        print("Selected Places:", self.places_customization)
        return starting_city, max_time, max_cost,source_astar

    def create_initial_population(self, size, starting_city, places):
        city_places = places
        population = []
        starting_place = self.city_to_railways[starting_city]
        for _ in range(size):
            tour = random.sample(
                [p for p in city_places if p != starting_place], len(city_places) - 1
            )
            population.append(tour)
        return population

    def calculate_fitness(self, tour, max_time, max_cost):
        total_time, total_cost, total_ratings = 0, 0, 0
        for i in range(len(tour) - 1):
            row = self.merged_data[
                (self.merged_data["Source"] == tour[i])
                & (self.merged_data["Destination"] == tour[i + 1])
            ]
            if not row.empty:
                time_inc = (
                    row["Time(hrs)"].values[0]
                    + self.places_data.at[tour[i + 1], "TIME(HOURS)"]
                )
                cost_inc = (
                    row["Cost(Rs)"].values[0] + self.places_data.at[tour[i + 1], "COST"]
                )
                rating_inc = self.places_data.at[tour[i + 1], "RATINGS"]
                total_time += time_inc
                total_cost += cost_inc
                total_ratings += rating_inc

        penalty = 0
        if total_time > max_time > 0:
            penalty += (total_time - max_time) * 50
        if total_cost > max_cost > 0:
            penalty += (total_cost - max_cost) * 50

        fitness = total_time + total_cost - total_ratings * 10 + penalty
        return fitness

    def select_parents(self, population, fitness_scores):
        tournament_size = 5
        tournament = random.sample(
            list(zip(population, fitness_scores)), tournament_size
        )
        tournament.sort(key=lambda x: x[1])
        return tournament[0][0]

    def crossover(self, parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [None] * len(parent1)
        child[start:end] = parent1[start:end]
        child_pos = end
        for gene in parent2:
            if gene not in child:
                while child[child_pos] is not None:
                    child_pos = (child_pos + 1) % len(child)
                child[child_pos] = gene
        return child

    def mutate(self, tour, mutation_rate=0.1):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(tour)), 2)
            tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
        return tour
    def extract_city_name(self, place):
        return place.split("(")[-1].strip(")")

    def evaluate_tour(self, tour):
        total_time, total_cost, total_ratings = 0, 0, 0
        for i in range(len(tour) - 1):
            row = self.merged_data[
                (self.merged_data["Source"] == tour[i])
                & (self.merged_data["Destination"] == tour[i + 1])
                | (self.merged_data["Destination"] == tour[i])
                & (self.merged_data["Source"] == tour[i + 1])
            ]
            if not row.empty:
                total_time += (
                    row["Time(hrs)"].values[0]
                    + self.places_data.at[tour[i + 1], "TIME(HOURS)"]
                )
                total_cost += (
                    row["Cost(Rs)"].values[0] + self.places_data.at[tour[i + 1], "COST"]
                )
                total_ratings += self.places_data.at[tour[i + 1], "RATINGS"]
        num_stops = len(tour) - 1
        average_rating = (total_ratings / num_stops) if num_stops > 0 else 0
        return total_time, total_cost, average_rating
    def run(
        self, starting_city, max_time, max_cost, population_size=10, generations=100
    ):
            
        city_places = [p for p in self.places_customization if self.extract_city_name(p) == starting_city]
        if not city_places:
            return None, None, None, None

        population = self.create_initial_population(
            population_size, starting_city, city_places
        )
        max_int64 = np.iinfo(np.int64).max
        best_tour, best_time, best_rating,generation_no, best_cost=None,0,0,0,max_int64
        for i in range(generations):
            fitness_scores = [
                self.calculate_fitness(tour, max_time, max_cost) for tour in population
            ]
            new_population = []
            while len(new_population) < population_size:
                parent1, parent2 = [
                    self.select_parents(population, fitness_scores) for _ in range(2)
                ]
                child1, child2 = self.crossover(parent1, parent2), self.crossover(
                    parent2, parent1
                )
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            population = new_population
            
            final_fitness_scores = [
                self.calculate_fitness(tour, max_time, max_cost) for tour in population
            ]

            index = np.argmin(final_fitness_scores)
            tour = population[index]
            tour = (
                    [self.city_to_railways[starting_city]]
                    + tour
                    + [self.city_to_railways[starting_city]]
                )
            time, cost, rating = self.evaluate_tour(tour)
            if ((best_time<=time)and (time <= max_time)) and ((cost<=best_cost)and(cost<=max_cost)):
                best_time=time
                best_cost=cost
                best_rating=rating
                best_tour=tour
                generation_no=i
        if best_tour:
            return best_tour, best_time, best_cost, best_rating,generation_no
        return None, None, None, None, None

    


# Example of how to use the TourOptimizer class
if __name__ == "__main__":

    optimizer = GeneticAlgorithm("travel.csv", "places.csv")
    print("Please enter details for the tour optimization.")
    starting_city, max_time, max_cost, source_astar = optimizer.gui_input()
    if not starting_city:
        print("No starting city provided. Exiting.")
        exit()
    with open('analysis.csv',mode = 'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["population","generation","execution_time","total_time","total_cost","avg_rating","path"])
        population_size, generations = 10, 50
        for i in range(50):
            population_size += 10
            generations += 10
            start_time = time.time()
            api_sol =sofia_astar.API(source_astar,city_to_railways[starting_city],max_time,max_cost)
            if not api_sol:
                print("no path exist to the city you want to travel ")
                exit()
            api_path = api_sol[0]
            N = len(api_path)
            avg_R = api_sol[3]
            R = avg_R*N

            max_cost = max_cost - api_sol[2]
            max_time = max_time - api_sol[1]
            optimal_tour, total_time, total_cost, average_rating, generation_no = optimizer.run(
                starting_city, max_time, max_cost, population_size, generations
            )
            mypath = []
            if not api_path:
                continue
            if not optimal_tour:
                continue
            for place in api_path:
                mypath.append(place)
                mypath.append("->")
            mypath.pop()
            mypath.pop()
            for place in optimal_tour:
                mypath.append(place)
                mypath.append("->")
            mypath.pop()
            path = ''.join(mypath)
            row = []
            row.append(population_size)
            row.append(generations)
            
            average_rating = average_rating*len(optimal_tour)
            average_rating = average_rating + R
            average_rating = average_rating/(len(optimal_tour)+N)
            
            end_time = time.time()
            execution_time = end_time - start_time
            row.append(execution_time)
            row.append(total_time)
            row.append(total_cost)
            row.append(average_rating)
            row.append(path)
            
            writer.writerow(row)

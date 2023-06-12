import networkx as nx
import random

# Define the grid
grid_size = 100
G = nx.erdos_renyi_graph(grid_size, 0.1)

# Define the generator
supply_capacity = 1000
production_cost = 0.1

# Define the agents
for i in range(grid_size):
    G.nodes[i]['demand'] = random.uniform(0, 1)
    G.nodes[i]['location'] = random.uniform(0, 1)

# Define the electricity supply process
def produce_electricity(generator, supply_capacity, production_cost):
    # Simple linear production function
    supply = min(supply_capacity, generator['demand'])
    cost = production_cost * supply
    return supply, cost

# Define the electricity demand process
def calculate_demand(customer, grid):
    # Simple linear demand function
    demand = customer['location'] * grid['supply']
    return demand

# Simulate the model
for i in range(100):
    generator = {'demand': supply_capacity}
    generator['supply'], generator['cost'] = produce_electricity(generator, supply_capacity, production_cost)
    for node in G.nodes:
        G.nodes[node]['demand'] = calculate_demand(G.nodes[node], generator)
    total_demand = sum([G.nodes[i]['demand'] for i in range(grid_size)])
    total_supply = generator['supply']
    print(f"Total demand: {total_demand}, Total supply: {total_supply}")

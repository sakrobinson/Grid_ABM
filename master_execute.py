# CAVEATS AND NOTES
# This is just a simple example, and there are many ways to make the model more realistic or complex depending on the specific problem you're trying to solve. 
# For example, in the future I will add more sophisticated models of electricity demand, 
# e.g.TOU pricing, Demand pricing, or demand response, or more complex models of electricity supply, 
# like renewable energy sources or transmission constraints.

# Demand
# customers will adjust their electricity demand based on the available supply. If the supply is plentiful, 
# customers may use more electricity; if the supply is limited, customers may reduce their electricity usage or face outages.
# "location" here is a proxy for customer heterogeneity. Multiplying the customer's location by the grid's supply captures the 
# idea that customers in certain locations may have different electricity demand profiles. For example, customers in hot and 
# humid climates may require more electricity for air conditioning during peak usage periods, while customers in colder 
# climates may require more electricity for heating during off-peak periods. Note Gas consumption is not modeled here, obviously.

import networkx as nx
import random

# Define the grid. Use a random Erdos Renyi network to start
grid_size = 100
G = nx.erdos_renyi_graph(grid_size, 0.1)
time_steps = 24*1 # hours, for x months

# Define the generator
supply_capacity = 1000
production_cost = 0.1 # Dollars per kWh Generated

# Define the agents. Each customer is definited by its location, and has a demand.
# Just residential and commercial for now.
for i in range(grid_size):
    if random.uniform(0, 1) < 0.7:
        G.nodes[i]['customer_type'] = 'residential'
        G.nodes[i]['load_shape'] = [0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0, 0, 0, 0]
    else:
        G.nodes[i]['customer_type'] = 'commercial'
        G.nodes[i]['load_shape'] = [0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    G.nodes[i]['location'] = random.uniform(0, 1)

# Define the electricity supply process
def produce_electricity(generator, supply_capacity, production_cost):
    # Simple linear production function
    supply = min(supply_capacity, generator['demand'])
    cost = production_cost * supply
    return supply, cost

# Define the electricity demand process
def calculate_demand(customer, grid, time_of_day):
    # Time-of-use demand function
    demand = customer['location'] * customer['load_shape'][time_of_day] * grid['supply']
    return demand

# Simulate the model
for i in range(time_steps):
    generator = {'demand': supply_capacity}
    generator['supply'], generator['cost'] = produce_electricity(generator, supply_capacity, production_cost)
    for node in G.nodes:
        if G.nodes[node]['customer_type'] == 'residential':
            G.nodes[node]['demand'] = calculate_demand(G.nodes[node], generator, i)
        else:
            G.nodes[node]['demand'] = calculate_demand(G.nodes[node], generator, i) * 2 # Commercial customers have a higher demand
    total_demand = sum([G.nodes[i]['demand'] for i in range(grid_size)])
    total_supply = generator['supply']
    print(f"Total demand: {total_demand}, Total supply: {total_supply}")

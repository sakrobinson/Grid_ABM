import matplotlib.pyplot as plt

# Aggregate the demand by customer type and time of day
residential_demand = [0] * 24
commercial_demand = [0] * 24
for node in G.nodes:
    if G.nodes[node]['customer_type'] == 'residential':
        for i in range(24):
            residential_demand[i] += G.nodes[node]['demand'][i]
    else:
        for i in range(24):
            commercial_demand[i] += G.nodes[node]['demand'][i]

# Create a stacked bar chart
fig, ax = plt.subplots()
ax.bar(range(24), residential_demand, label='Residential')
ax.bar(range(24), commercial_demand, bottom=residential_demand, label='Commercial')
ax.set_xlabel('Time of day')
ax.set_ylabel('Electricity demand')
ax.set_title('Electricity demand by customer type and time of day')
ax.legend()
plt.show()

#----------------#
# Create a scatter plot of individual agent demand over time
fig, ax = plt.subplots()
for node in G.nodes:
    if G.nodes[node]['customer_type'] == 'residential':
        ax.scatter(range(24), G.nodes[node]['demand'], color='blue', label='Residential')
    else:
        ax.scatter(range(24), G.nodes[node]['demand'], color='orange', label='Commercial')
ax.set_xlabel('Time of day')
ax.set_ylabel('Electricity demand')
ax.set_title('Electricity demand by individual customer and time of day')
ax.legend()
plt.show()

#------------------#
# Calculate the total demand and supply for each time step
total_demand = [0] * 24
total_supply = [0] * 24
for i in range(24):
    generator = {'demand': supply_capacity}
    generator['supply'], generator['cost'] = produce_electricity(generator, supply_capacity, production_cost)
    for node in G.nodes:
        if G.nodes[node]['customer_type'] == 'residential':
            G.nodes[node]['demand'] = calculate_demand(G.nodes[node], generator, i)
        else:
            G.nodes[node]['demand'] = calculate_demand(G.nodes[node], generator, i) * 2
    total_demand[i] = sum([G.nodes[j]['demand'] for j in range(grid_size)])
    total_supply[i] = generator['supply']

# Create a line plot of total demand and supply over time
fig, ax = plt.subplots()
ax.plot(range(24), total_demand, label='Demand')
ax.plot(range(24), total_supply, label='Supply')
ax.set_xlabel('Time of day')
ax.set_ylabel('Electricity demand/supply')
ax.set_title('Electricity demand and supply over time')
ax.legend()
plt.show()


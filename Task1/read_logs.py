#!/usr/bin/env python3.13

f = open("access.log.5","r")
user_agents = {}

for line in f:
	ip = line.split("-")[0]
	if ip in user_agents:
		user_agents[ip] += 1
	else:
		user_agents[ip] = 1
print("The number of user_agents is:")
print(len(user_agents))
for agent in user_agents:
	print(agent + str(user_agents[agent]))

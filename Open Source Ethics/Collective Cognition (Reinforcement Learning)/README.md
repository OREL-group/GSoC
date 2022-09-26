## Project Description 
A Collective Cognitions Model for AI Ethics. 

The main objective was to build an analytical model that helps in keeping open-source community self-sustaining. It takes into account various factors such as activities, recurrent relationships and shared resources of the open-source community which promotes people to stay in the community and become contributors. This was done by developing the environment as well as the agents who will be using such automated guidelines to interact and engage with the community.

There were 3 different approaches taken to this project. There was an Active Inference Model approach to Open Source Development Communities, A Personality Driven Analysis of Openness in Communities and A Reinforcement Learning approach to developing a Sustainable Community. I will be summarizing the multi agent reinforcement learning approach to this problem statement.

## Summary of work done

So what is Reinforcement Learning? Why should you care about it? How does it apply to Open Source Communities? 
Reinforcement learning is basically a machine learning training method based on rewarding desired behaviors and/or punishing undesired ones. It follows a particular structure in the way it models any problem i.e. called as **MDP** or **Markov Decision Process**

![MDP](https://user-images.githubusercontent.com/73215784/192312353-d7ce7a52-3535-450b-9e2b-bac4fb8b54bd.jpeg)

Here the agent takes an action and the environment gives it back a new state along with a reward. The goal of the agent is to maximize the reward it produce over a period of time. In theory, if you can map a problem to the reinforcement paradigm, you can then develop **rlagents** to solve the environment and get desired output. 

In multiagent setting, for example like a community this changes the scope of the problem drastically. Applying the concept of reinforcement learning in a multi-agent environment is really complex and a lot of problems that deal with concepts like Non-stationarity surface. 

## The netlogo environment 

The model I have developed is basically a **CodeSpace environment** on the Netlogo platform. The model assumes a community built of contributors and maintainers. Each member of the community has been a assigned a particular level depending on their prior contribution in that community. The person with the highest level is the maintainer. All the members of the community solve issues in the 2d-codespace. The issues are of varying degree and all members must satisfy a pre-requisite to solve a particular issue. The goal of the environment is to use **Reinforcement learning** to create rlagents that learn to solve the existing issues in the codespace. 

![codespaceNlogo](https://user-images.githubusercontent.com/73215784/192335335-e994db56-4d0c-4d7e-8511-9f4e492654a7.png)

This is the current implementation of the environment in Netlogo. The agents try to solve 3 types of issues of varying difficulty (Earth-shot < Moon-shot < Mars-Jupiter shot). At every instance of the runtime of simulation, the model takes into account the number of members of community, whether they are maintainers or contributors and the amount of issues currently unresolved. The agents use an algorithm called as [Q-Learning](https://github.com/KevinKons/qlearning-netlogo-extension) to solve the environment. 

![qlearning](https://user-images.githubusercontent.com/73215784/192337874-a9fe0dc0-faaa-41f8-9cda-bb193db21889.png)

This is the core of the algorithm the **Bellman equation** as a simple value iteration update, using the weighted average of the current value and the new information. 

The Netlogo Model has the RL Parameters related to Qlearning on the right slide and can be changed and explored. As the agents continue to solve issues they receive different reward depending on the issue they resolve. Finally the graph shows the average reward the agents generate while solving the codespace environment. 

## Future Scope 
- [ ] Extending the current implementation by adding more complex features and taking into account more factors as internal states of the agents
- [ ] Adding support to integrate actual community stats into Netlogo. 
- [ ] Taking a different route as a novel approach to MARL by creating an environment from scratch without the use of Netlogo.
- [ ] Creating a web based implementation so that the model can be used easily by anyone around the world.


## Conclusion and Acknowledgement 
Over the course of GSoC Period, I was able to implement a model of Open Source Community. There was definitely a research and interdisciplinary aspect to the project and overcoming the difficulties faced during the entire process was really fruitful. Finally I would like to thank my Mentors Bradly and Jessie for guiding and mentoring me every step of the way.    



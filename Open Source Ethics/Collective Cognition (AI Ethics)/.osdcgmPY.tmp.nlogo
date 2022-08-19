extensions [ py ]

globals [
  ;num_agents
  churn_rate
  repo_size
  unit
  horizon
]

breed [ members member ]

members-own [
  qual
  quan
  engag
  contrib_size
  role
  other_agents
]

to setup
  ca

  ; setup python
  py:setup py:python3
  ; test python
  ;show py:runresult "1 + 1"
  ; imports and such
  (py:run
    "import numpy as np"
    "import pymdp"
    "from pymdp import utils"
    "from pymdp.agent import Agent"
    "from pymdp.maths import softmax"
  )

  ; helper functions to plot likelihood and beliefs
  (py:run
    "import matplotlib.pyplot as plt"
    "import seaborn as sns"
    "def plot_likelihood(matrix, title_str = 'Likelihood distribution (A)'):"
    "  if not np.isclose(matrix.sum(axis=0), 1.0).all():"
    "    raise ValueError('Distribution not column-normalized! Please normalize (ensure matrix.sum(axis=0) == 1.0 for all columns)')"
    "  fig = plt.figure(figsize = (9,9))"
    "  ax = sns.heatmap(matrix, cmap = 'gray', cbar = False, vmin = 0.0, vmax = 1.0)"
    "  plt.title(title_str)"
    "  plt.show()"
    "def plot_beliefs(belief_dist, title_str=''):"
    "  if not np.isclose(belief_dist.sum(), 1.0):"
    "    raise ValueError('Distribution not normalized! Please normalize')"
    "  plt.grid(zorder = 0)"
    "  plt.bar(range(belief_dist.shape[0]), belief_dist, color='r', zorder=3)"
    "  plt.xticks(range(belief_dist.shape[0]))"
    "  plt.title(title_str)"
    "  plt.show()"
  )

  ; set up the agent matrix
  py:set "num_agents" num_agents
  py:run "agent_matrix = list(range(num_agents))"

  ; set up environment class
  ; define agent class for action interpretation
  ; NOTE: this is from an example notebook (https://pymdp-rtd.readthedocs.io/en/latest/notebooks/using_the_agent_class.html)
  ; which is an "Epistemic Two-Armed Bandit" with an extra action called "Get Hint" which here is "Get Horizon"
  (py:run
    "class CommunityMember(object):"
    "  def __init__(self, context = None, p_horizon = 1.0, p_reward = 0.8):"
    "    self.context_names = ['Qual Low','Qual Med','Qual High','Quan Low','Quan Med','Quan High','Eng Low','Eng Med','Eng High']"
    "    self.p_horizon = p_horizon"
    "    self.p_reward = p_reward"
    "    self.horizon_obs_names = ['Most Qual Decrease','Most Qual Nothing','Most Qual Increase','Most Quan Decrease','Most Quan Nothing','Most Quan Increase','Most Getting Duller','Most Staying Same','Most Getting Brighter']"
    "    self.reward_obs_names = ['Null','Loss','Reward']"
    "  def step(self, action):"
    "    #choice_action_names = ['Write Code','Create PR','Create Issue','Commit Code','Approve PR','Close Issue','Request Changes','Comment','Fork','Quiesce']"
    "    if action == 'Write Code':"
    "      observed_horizon = 'Most Qual Nothing'"
    "      observed_reward = 'Null'"
    "      observed_choice = 'Write Code'"
    "    elif action == 'Create PR':"
    "      observed_horizon = 'Most Qual Increase'"
    "      observed_reward = 'Reward'"
    "      observed_choice = 'Write Code'"
    "    elif action == 'Create Issue':"
    "      observed_horizon = 'Most Qual Increase'"
    "      observed_reward = 'Null'"
    "      observed_choice = 'Create Issuee'"
    "    elif action == 'Commit Code':"
    "      observed_horizon = 'Most Quan Increase'"
    "      observed_reward = 'Null'"
    "      observed_choice = 'Commit Code'"
    "    elif action == 'Approve PR':"
    "      observed_horizon = 'Most Quan Increase'"
    "      observed_reward = 'Reward'"
    "      observed_choice = 'Approve PR'"
    "    elif action == 'Close Issue':"
    "      observed_horizon = 'Most Getting Brighter'"
    "      observed_reward = 'Reward'"
    "      observed_choice = 'Close Issue'"
    "    elif action == 'Request Changes':"
    "      observed_horizon = 'Most Getting Brighter'"
    "      observed_reward = 'Reward'"
    "      observed_choice = 'Request Changes'"
    "    elif action == 'Comment':"
    "      observed_horizon = 'Most Getting Brighter'"
    "      observed_reward = 'Reward'"
    "      observed_choice = 'Comment'"
    "    elif action == 'Fork':"
    "      observed_horizon = 'Most Getting Brighter'"
    "      observed_reward = 'Null'"
    "      observed_choice = 'Fork'"
    "    elif action == 'Quiesce':"
    "      observed_horizon = 'Most Staying Same'"
    "      observed_reward = 'Loss'"
    "      observed_choice = 'Quiesce'"
    "    obs = [observed_horizon, observed_reward, observed_choice]"
    "    return obs"
  )
  ; define the active inference step function, for use in the go method
  (py:run
    "def run_active_inference_step(my_agent, my_env):"
    "  obs_label = ['Most Qual Nothing','Null','Quiesce']"
    "  obs = [horizon_obs_names.index(obs_label[0]), reward_obs_names.index(obs_label[1]), choice_obs_names.index(obs_label[2])]"
    "  qs = my_agent.infer_states(obs)"
    "  q_pi, efe = my_agent.infer_policies()"
    "  chosen_action_id = my_agent.sample_action()"
    "  movement_id = int(chosen_action_id[1])"
    "  choice_action = choice_action_names[movement_id]"
    "  obs_label = my_env.step(choice_action)"
    "  obs = [horizon_obs_names.index(obs_label[0]),reward_obs_names.index(obs_label[1]), choice_obs_names.index(obs_label[2])]"
    "  return choice_action"
  )

  set unit 10 ; amount we count repo size by
  set horizon 1;

  create-members num_agents [
    set qual ((random 100) / 100)
    set quan ((random 100) / 100)
    set engag ((random 100) / 100)

    set contrib_size (quan * unit) ; using the quantitative value, find the size they contribute

    set role (one-of ["admin" "dev" "other"])

    setxy (qual * max-pxcor) (quan * max-pycor)

    set shape "person"
    ifelse role = "admin" [
      set color (list (engag * 255) 0 0)
    ]
    [
      ifelse role = "dev" [
        set color (list 0 (engag * 255) 0)
      ]
      [
        set color (list 0 0 (engag * 255))
      ]
    ]

    ; setup agent code for active inference
    ; adapted from https://pymdp-rtd.readthedocs.io/en/stable/notebooks/using_the_agent_class.html
    ; note i've changed the 'hint' matrix from the two-armed bandit example
    ; to the 'horizon' matrix of the agent's observations from within its horizons
    py:set "who" who
    (py:run
      "context_names = ['Qual Low','Qual Med','Qual High','Quan Low','Quan Med','Quan High','Eng Low','Eng Med','Eng High']"
      "choice_names = ['Write Code','Create PR','Create Issue','Commit Code','Approve PR','Close Issue','Request Changes','Comment','Fork','Quiesce']"
      "num_states = [len(context_names), len(choice_names)] # hidden state factor dimensions"
      "num_factors = len(num_states)"
      "#context_action_names = ['Move Left','Dont Move LR','Move Right','Move Down','Dont Move UD','Move Up','Less Bright','Stay Same','More Bright']"
      "context_action_names = ['Do-nothing']"
      "choice_action_names = ['Write Code','Create PR','Create Issue','Commit Code','Approve PR','Close Issue','Request Changes','Comment','Fork','Quiesce']"
      "num_controls = [len(context_action_names), len(choice_action_names)] # control state factor dimensions"
      "horizon_obs_names = ['Most Qual Decrease','Most Qual Nothing','Most Qual Increase','Most Quan Decrease','Most Quan Nothing','Most Quan Increase','Most Getting Duller','Most Staying Same','Most Getting Brighter']"
      "#reward_obs_names = ['Qual Low','Qual Med','Qual High','Quan Low','Quan Med','Quan High','Eng Low','Eng Med','Eng High']"
      "reward_obs_names = ['Null','Loss','Reward']"
      "choice_obs_names = ['Write Code','Create PR','Create Issue','Commit Code','Approve PR','Close Issue','Request Changes','Comment','Fork','Quiesce']"
      "num_obs = [len(horizon_obs_names), len(reward_obs_names), len(choice_obs_names)]"
      "num_modalities = len(num_obs)"
    )
    ; create the A matrix
    ; starting with the Horizon Modality
    ; NOTE: at the moment this modality does very little, but it would be great to get some ToM going!
    (py:run
      "A = utils.obj_array( num_modalities )"
      "p_horizon = 0.7 # accuracy of horizon/hint for agent, how much they trust their perception"
      "A_horizon = np.zeros( ( len(horizon_obs_names), len(context_names), len(choice_names) ) )"
      "horizon_array = np.eye(9)"
      "for choice_id, choice_name in enumerate(choice_names):"
      "  if choice_name == 'Write Code':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Create PR':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Create Issue':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Commit Code':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Approve PR':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Close Issue':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Request Changes':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Comment':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Fork':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "  elif choice_name == 'Quiesce':"
      "    #A_horizon[0,:,choice_id] = 1.0"
      "    A_horizon[0:,:,choice_id] = horizon_array"
      "A[0] = A_horizon"
    )
    ; debug A matrix
    show py:runresult "A[0]"
    py:run "plot_likelihood(A[0][:,:,1], title_str = 'Probability of the horizon types for the states')"

    ; then make the reward A matrix
    ; NOTE: quantifying actions seems odd, perhaps this could be another type of matrix altogether?
    (py:run
      "A_reward = np.zeros((len(reward_obs_names), len(context_names), len(choice_names)))"
      "for choice_id, choice_name in enumerate(choice_names):"
      "  if choice_name == 'Write Code':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Create PR':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Create Issue':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Commit Code':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Approve PR':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Close Issue':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Request Changes':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Comment':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Fork':"
      "    A_reward[0,:,choice_id] = 1.0"
      "  elif choice_name == 'Quiesce':"
      "    A_reward[0,:,choice_id] = 1.0"
      "A[1] = A_reward"
    )
    py:run "plot_likelihood(A[1][:,:,2], 'Payoff structure if playing the Left Arm, for the two contexts')"

    ; then make the choice A matrix
    ; NOTE: in this case the choices are all equally likely
    (py:run
      "A_choice = np.zeros((len(choice_obs_names), len(context_names), len(choice_names)))"
      "for choice_id in range(len(choice_names)):"
      "  A_choice[choice_id, :, choice_id] = 1.0"
      "A[2] = A_choice"
    )

    ; create the B matrix
    ; the B matrix is our transition matrix, given a context which state will be next,
    ; which choice is likely given the current choice, etc
    ; starting with the context matrix
    (py:run
      "B = utils.obj_array(num_factors)"
      "B_context = np.zeros( (len(context_names), len(context_names), len(context_action_names)) )"
      "B_context[:,:,0] = np.eye(len(context_names))"
      "B[0] = B_context"
    )
    ; then make the choice matrix
    (py:run
      "B_choice = np.zeros( (len(choice_names), len(choice_names), len(choice_action_names)) )"
      "for choice_i in range(len(choice_names)):"
      "  B_choice[choice_i, :, choice_i] = 1.0"
      "B[1] = B_choice"
    )

    ; create the C matrix
    ; in this case C is our preferences or targets
    ; NOTE: at the moment this is a simple reward structure
    (py:run
      "C = utils.obj_array_zeros(num_obs)"
      "C_reward = np.zeros(len(reward_obs_names))"
      "C_reward[1] = -4.0"
      "C_reward[2] = 2.0"
      "C[1] = C_reward"
    )

    ; create the D matrix
    ; D here is our prior or starting situation
    ; NOTE: at the moment every agent begins by Quiescing
    (py:run
      "D = utils.obj_array(num_factors)"
      "D_context = softmax(np.ones(len(context_names)))"
      "D[0] = D_context"
      "D_choice = np.zeros(len(choice_names))"
      "D_choice[choice_names.index('Quiesce')] = 1.0"
      "D[1] = D_choice"
    )

    ; fill the agent_matrix with agents!
    ; NOTE: at the moment there is no way to make different numbers of agents without resetting
    (py:run
      "agent_matrix[who] = Agent( A = A, B = B, C = C, D = D )"
    )

    ; instantiate an environment
    ; with a horizon and reward variable
    (py:run
      "p_horizon_env = 1.0"
      "p_reward_env = 0.7"
      "env = CommunityMember(p_horizon = p_horizon_env, p_reward = p_reward_env)"
    )
  ]

  ask members [
    set repo_size (repo_size + contrib_size)
  ]

  reset-ticks
end

to go
  ask members [
    get-sensory-info
    take-action
    update-world
  ]

  tick
end

to get-sensory-info
  ; find the local horizon of the given agent
  let horizon_value (engag * horizon)
  ; look around at all the agents around that agent and their variables
  set other_agents (members in-radius horizon_value)
end

to take-action
  ; active inference to choose an action
  py:set "who" who
  (py:run
    "action = run_active_inference_step(agent_matrix[who], env)"
    "action_num = 0"
    "if action == 'Write Code' or action == 'Create PR' or action == 'Close Issue':"
    "  action_num = 0"
    "if action == 'Commit Code' or action == 'Approve PR' or action == 'Create Issue':"
    "  action_num = 1"
    "if action == 'Request Changes' or action == 'Comment' or action == 'Fork':"
    "  action_num = 2"
    "if action == 'Quiesce':"
    "  action_num = 3"
  )
  let chosen_action py:runresult "action_num"

  show chosen_action
  ; 0 => qual+ 1 => quan+ 2 => engag+ 3 => all-

  let change_val 0.01
  if role = "admin" [
    set change_val (change_val * 2)
  ]
  if role = "dev" [
    set change_val (change_val * 1.5)
  ]
  if chosen_action = 0 [ set qual (qual + change_val) ]
  if chosen_action = 1 [ set quan (quan + change_val) ]
  if chosen_action = 2 [ set engag (engag + change_val) ]
  if chosen_action = 3 [
    set qual (qual - change_val)
    set quan (quan - change_val)
    set engag (engag - change_val)
  ]
end

to update-world
  if (qual * max-pxcor) > max-pxcor [ set qual 1.0 ]
  if (quan * max-pycor) > max-pycor [ set quan 1.0 ]
  if (engag * 255) > 255 [ set engag 1.0 ]
  if (qual * max-pxcor) < min-pxcor [ set qual 0.1 ]
  if (quan * max-pycor) < min-pycor [ set quan 0.1 ]
  if (engag * 255) < 0 [ set engag 0.1 ]

  setxy (qual * max-pxcor) (quan * max-pycor)

  set shape "person"
  ifelse role = "admin" [ set color (list (engag * 255) 0 0) ]
    [ ifelse role = "dev" [ set color (list 0 (engag * 255) 0) ]
    [ set color (list 0 0 (engag * 255)) ] ]

  set repo_size (repo_size + contrib_size)
end
@#$#@#$#@
GRAPHICS-WINDOW
210
10
661
462
-1
-1
13.42424242424243
1
10
1
1
1
0
0
0
1
0
32
0
32
0
0
1
ticks
30.0

SLIDER
13
29
185
62
num_agents
num_agents
0
100
1.0
1
1
NIL
HORIZONTAL

PLOT
3
122
203
272
churn
ticks
burn out rate
0.0
100.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot (count members with [engag < 0.1]) / num_agents"

MONITOR
67
286
140
331
repo size
repo_size
17
1
11

BUTTON
6
293
62
326
setup
setup\n
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
144
294
199
327
go
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

@#$#@#$#@
## WHAT IS IT?

This is a model of an Open Source Development Community. The scope of the model is that of a single such community working under shared goals, with 3 roles of agents at work in the community: Admins, Devs, and Others.

The 3 types of agent have different effects on their contribution location and therefore on the agents around them.

The properties of each agent are primarily of their contributions, which are imagined as three index values: Quality and Quantity forming a 2-dimensional location regarding their code, and Engagement being a 3rd dimension representing how much they engage with the community. Engagement also extends the horizon line of how far each agent can see from its location. Quantity drives the size of their contributions.

The actions of each agent are to act to change the three index values representing their contributions. In this model, these actions are abstract, but in "real life" they would correspond as follows: increase quality index (reuse code of other agents, engage with an issue), increase quantity index (write code, submit pull request), increase engagement index (fork repo, comment on issue or pull request), decrease all index values (quiesce or do nothing).

The environment is a 3-dimensional contribution location with Quality and Quantity as a 2-dimensional graph and Engagement as the intensity of the color of each agent.

The order of events begins with initializing the agents with random index values, then updating the overall repo size.
After initialization, each iteration will get sensory data (in this case the agents which are within a given agent's horizon), take an action based on that data (using the information gleaned), and finally update the values of the environment/world based on that agent's actions.

The inputs to this model are simply a given size of the community. The output is the churn rate, or amount of agents which end up with a low engagement score.

## HOW IT WORKS

This particular model is more of an outline for a more comprehensive and sophisticated model to come. See "Extending the Model" for vision information.

Each agent has a location in the contribution featurespace, given its Engagement Index value, it has a "horizon" from which it can see around itself and note the index values of those agents within the horizon. Each agent chooses an action which will advance the index value which those around it have most strongly.

## HOW TO USE IT

To use this model, adjust the number of agents slider to a given size, then watch as agents changes over time, noting the churn rate and position in the feature space.

## THINGS TO NOTICE

Beginning with a low number of initial agents can cause agents to spin off into their own cliques, some high quality and quantity agents losing engagement scores and others with high engagement scores but low quality and quantity scores.

Beginning with a high number of agents creates a bit more sustainability in that the churn rate takes a longer time to increase and each agent group moves more slowly, as they have more neighbors to respond to.

## THINGS TO TRY

Try starting with different numbers of agents.

## EXTENDING THE MODEL

The back-end of this model is where most of the extension occurs, it could be made as an active inference model, a POMDP model, a simple HMM, or even such a simple rule based model as I have here.

## NETLOGO FEATURES

We use the "breed" function to simplify things a bit.

## RELATED MODELS

Value Iteration in an MDP

## CREDITS AND REFERENCES

Google Summer of Code
International Neuroinformatics Coordinating Facility
Orthogonal Research and Education Laboratory
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.2.2
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@

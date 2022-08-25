globals [
  ;num_agents
  num_cooperating
  ;uncertainty
  ;reevaluate_rate
  churn_rate
  repo_size
  ;unit
  ;horizon
  dynamics_of_coop
  fraction_cooperating
  ;max_noise
]

breed [ members member ]

members-own [
  qual
  quan
  engag
  contrib_size
  role
  other_agents
  utility
  benefit_rate
  personal_cost
  cooperating?
  local_num_cooperating
  horizon_length
  success_prob
  f_crit
]

to setup
  ca

  ;set unit 1 ; amount we count repo size by
  ;set horizon 2;

  create-members num_agents [
    ; initialize values
    set utility random-normal 0.0 100.0
    set benefit_rate random-normal 0.0 100.0
    set personal_cost random-normal 0.0 100.0
    ifelse (one-of [0 1]) = 1 [set cooperating? TRUE] [set cooperating? FALSE]
    set horizon_length random-normal 0 100
    set success_prob random-normal 0.0 1.0

    ; find f_crit
    set f_crit ((num_agents * personal_cost - benefit_rate) / (horizon_length * reevaluate_rate * (benefit_rate - personal_cost)))

    ; estimate num_cooperating based on current values
    let cooperating_val 0
    if cooperating? [ set cooperating_val 1 ]
    set local_num_cooperating ((num_agents / benefit_rate) * (utility + (personal_cost * cooperating_val)))

    ifelse f_crit > local_num_cooperating
    [ set cooperating? TRUE ]
    [ set cooperating? FALSE ]

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

  set num_cooperating (count members with [cooperating? = TRUE])
  set dynamics_of_coop find-dynamics

  tick
end

to-report find-dynamics
  set fraction_cooperating (num_cooperating / num_agents)
  report (- reevaluate_rate) * (fraction_cooperating - (1 / 2) * (1 + error-func))
end

to-report error-func
  let mean_f_crit (mean [f_crit] of members)
  let mean_success_prob (mean [success_prob] of members)
  let mean_num_cooperating (mean [local_num_cooperating] of members)
  let f_coop (mean_success_prob * mean_num_cooperating + (1 - mean_success_prob) * (1 - mean_num_cooperating))
  let coop_function ((f_coop - mean_f_crit) / (uncertainty * (sqrt 2)))
  report coop_function
end

to get-sensory-info
  ; find the local horizon of the given agent
  let horizon_value (engag * horizon)
  ; look around at all the agents around that agent and their variables
  set other_agents (members in-radius horizon_value)

  ; find f_crit
  set f_crit (((num_agents * personal_cost) - benefit_rate) / (horizon_length * reevaluate_rate * (benefit_rate - personal_cost)))
  ;show f_crit

  ; set the cooperating value (kroenecker delta)
  let cooperating_val 0.0
  if cooperating? [ set cooperating_val 1.0 ]

  ; calculate local utility using last known local_num_cooperating
  set utility (benefit_rate * (local_num_cooperating / num_agents) - (personal_cost * cooperating_val))

  ; estimate local_num_cooperating based on current values
  set local_num_cooperating (((count other_agents) / benefit_rate) * (utility + (personal_cost * cooperating_val)))
  ;show local_num_cooperating

  ifelse f_crit > local_num_cooperating
  [ set cooperating? TRUE ]
  [ set cooperating? FALSE ]
end

to take-action
  let chosen_action 3

  if cooperating?
  [  set chosen_action one-of [0 1 2]  ]

  ;show chosen_action
  ; 0 => qual+ 1 => quan+ 2 => engag+ 3 => all-

  let change_val ((contrib_size * (random-normal 1.0 max_noise)) / repo_size)
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

  set contrib_size (quan * unit) ; using the quantitative value, find the size they contribute
end

to update-world
  if (qual * max-pxcor) > max-pxcor [ set qual 1.0 ]
  if (quan * max-pycor) > max-pycor [ set quan 1.0 ]
  if (engag * 255) > 255 [ set engag 1.0 ]
  if (qual * max-pxcor) < min-pxcor [ set qual 0.0 ]
  if (quan * max-pycor) < min-pycor [ set quan 0.0 ]
  if (engag * 255) < 0 [ set engag 0.0 ]

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
14
10
186
43
num_agents
num_agents
0
1000
312.0
1
1
NIL
HORIZONTAL

PLOT
4
270
204
420
dynamics of cooperation
ticks
cooperating agents
0.0
100.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot dynamics_of_coop"

BUTTON
7
426
63
459
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
145
427
200
460
go
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
12
126
184
159
uncertainty
uncertainty
0.01
1.0
0.16
0.01
1
NIL
HORIZONTAL

SLIDER
11
162
186
195
reevaluate_rate
reevaluate_rate
0.01
1.0
0.7
0.01
1
NIL
HORIZONTAL

MONITOR
67
422
142
467
NIL
repo_size
0
1
11

SLIDER
10
200
182
233
unit
unit
0.01
10.0
1.09
0.01
1
NIL
HORIZONTAL

SLIDER
10
238
182
271
horizon
horizon
1
100
19.0
1
1
NIL
HORIZONTAL

MONITOR
36
44
162
89
NIL
num_cooperating
2
1
11

SLIDER
12
90
184
123
max_noise
max_noise
1.0
500.0
20.1
0.1
1
NIL
HORIZONTAL

TEXTBOX
36
117
186
135
will cause craziness
10
0.0
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

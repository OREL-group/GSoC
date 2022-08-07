extensions [ array matrix py ]

;;
;  Variable Instantiations
;;

; globals are float repo size, and two lists of prs and issues, made up of prs and issues
; with an index which corresponds to an integer in each agent's respective arrays of prs and issues which they created
globals [
  repo_size
  prs
  issues
  horizon
  ; num_agents
  ; churn_rate
  ; GLOBALS from Kaufmann et al
  ENV_SIZE
  names
]

; members are members of the open source development community under consideration
breed [ members member ]

; turtles own variables belong to each agent, and correspond to the aforementioned pr and issue arrays
; also their code contributions (and corresponding size), efficiency and engagement index, their role,
; and the states they are in, which contains the state space matrices, along with their target encodings
; also each agent's theory of mind (ToM) and goal alginment
members-own [
  agent_name
  ; repo variables
  agent_prs
  agent_issues
  agent_contrib_size
  agent_efficiency_quality
  agent_efficiency_quantity
  agent_engagement
  agent_role
  ; active inference variables
  agent_states
  agent_targets
  agent_ToM
  agent_goal_alignment
  agent_actions
  ; POMDP variables
  agent_state
  agent_transitions
  agent_prior
  matrix_A
  matrix_B
  matrix_C
  matrix_D
  matrix_G
  ; other agent variables
  other_agents
]


; set up the world, and the agents
to setup
  ca

  ; initialize python
  py:setup py:python3
  py:run "import numpy as np"
  ;py:run "import pandas as pd"
  ;show py:runresult "1 + 1"
  initialize-world
  initialize-agents

  reset-ticks
end


; run a timestep on sensory, internal, active, and external states
to go
  ; run the active inference loop
  ; see Kaufmann et al, Sense->Understand->Act,
  ; sense environment,
  ; optimize belief distribution relative to sensory inputs and
  ; act to reduce FE relative to desired beliefs
  ask members [
    get-sensory-info
    update-internal
    take-action
    ; update world after action
    update-world
  ]

  tick
end


;;
;  Initialization Functions
;;

; initialize variables of the world, repo size, PRs, Issues, number of agents
to initialize-world
  set issues array:from-list []
  ;set repo_size (random 1000.0) ; set a random repo size to start
  make-prs (random 6) ; make a random number of PRs
  make-issues (random 6) ; make a random number of Issues
  set horizon max-pxcor
  set ENV_SIZE max-pxcor
  ; check that python is working

  set names [ "Abigail" "Adelard" "Astrid" "Alvin" "Arthur" "Annie" "Axel" "Adam" "Alf" "Alice" "Ansel" "Adelaide" "Arturo" "Amabalis" "Anais" "Angela" "Adolfo"
              "Beatrix" "Bernice" "Bob" "Barbie" "Baxter" "Bigby" "Brian" "Bullet" "Budgie" "Barbara" "Baron" "Byron" "Billy" "Beanie" "Bootsy" "Bobo" "Bono"
              "Cedric" "Christina" "Christian" "Christopher" "Christie" "Copernicus" "Calvin" "Calder" "Cecil" "Colin" "Cady" "Caitlin" "Caligula" "Charles" "Crissy" "Cinder"
              "Debra" "Delores" "Dudley" "Dilbert" "Dodge" "Dan" "Danielle" "David" "Duke" "Devina" "Denny" "Dingus" "Donathan" "Donny" "Dante" "Diogenes" "Dawn"
              "Edmund" "Edgar" "Eloise" "EttaLou" "Elvira" "Elsie" "Elmer" "Ettiene" "Erasmus" "Elohim" "Exeter" "Ever" "Eunice" "Eustice" "Eduardo" "Edwina" "Edith"
              "Francine" "Fallon" "Frank" "Feivel" "Fifi" "Francois" "Ferdinand" "Felicia" "Felix" "Fred" "Flannery" "Fido" "Faust" "Francisco" "Fanny" "Fenwick"
              "George" "Gertrude" "Georgie" "Gus" "Gary" "Gene" "Gramps" "Granny" "Gringo" "Geronimo" "Geraldo" "Glen" "Georgette" "Geoff" "Gunther" "Garland"
              "Howie" "Hannah" "Havarah" "Heinrick" "Henna" "Havana" "Heaven" "Holly" "Hope" "Heiman" "Heimy" "Howard" "Hulk" "Honey" "Hannibal" "Herod"
              "Icarus" "Ionia" "Isabelle" "Isis" "Israel" "Issy" "Ione" "Ingrid" "Ibex" "Ivy" "Imogen" "Inez" "Ignacio" "Isadora" "Irma" "Iggy" "India" "Inju"
              "Justine" "Joe" "Jack" "Jake" "Janet" "Jill" "Jonathan" "Jasper" "Janelle" "Janice" "Joaquin" "Jay" "Jerry" "Jessica" "Josephine" "Joa" "Joan" "Jolene"
              "Katya" "Kate" "Kathleen" "Karl" "Kathy" "Kortney" "Kronkite" "Kirby" "Kimberly" "Kim" "Kadisha" "Kristina" "Keith" "Kalamity" "Kenji" "Kendall"
              "Louise" "Louis" "Linda" "Loretta" "Lionel" "Lyle" "Lewis" "Lumpy" "Linette" "Lenny" "Lorene" "Lola" "Letecia" "Lisette" "Lucy" "Lucian" "Landry"
              "Montgomery" "Margerie" "Maggie" "Midge" "Myron" "Mark" "Mike" "Miles" "Minerva" "Mykael" "Michael" "Melissa" "Melanie" "Macy" "Moira" "Manny"
              "Nick" "Nicholas" "Nigel" "Nanine" "Nancy" "Ninette" "Naomi" "Ned" "Noona" "Nona" "Nina" "Nissa" "Nancy" "Neva" "Nieva" "Nora" "Newt" "Noam"
              "Octavius" "Oliver" "Ollie" "Olivia" "Ormand" "Oswald" "Orville" "Owen" "Oswaldo" "Olivander" "Orson" "Orex" "Onmund" "Offenglove" "Ozzy"
              "Peter" "Patricia" "Patrice" "Patrick" "Prince" "Pierce" "Patty" "Pygmalia" "Pigeon" "Paul" "Petey" "Pliny" "Penelope" "Ptomely" "Piper"
              "Quinn" "Quan"
              "Robert" "Raymond" "Reinhart" "Rachel" "Raquel" "Ringo" "Robbie" "Raleigh" "Riley" "Rory" "Roland" "Ryan" "Raphael" "Rapunzel" "Rupolph" "Rupbert" "Rufus" "Rusty"
              "Steve" "Steinway" "Sarah" "Sandra" "Sigourney" "Susie" "Sissy" "Sally" "Susan" "Silver" "Stella" "Stellathe" "Stewart" "Sylvia" "Sophie" "Sage" "Sophia" "Sonia"
              "Todd" "Timothy" "Talus" "Tallulah" "Ted" "Tyler" "Theodore" "Tom" "Thomas" "Tammy" "Tanya" "Titus" "Thor" "Tyra" "Tyree" "Thaddeus" "Thucydides" "Teal" "Tanner" "Tyson"
              "Ulysses" "Ulrich" "Undine" "Ulgar" "Uniqwa" "Ursula" "Ursaline" "Uzaki" "Usher"
              "Vanover" "Victor" "Valerie" "Valmor" "Val" "Veronica" "Vaughn" "Viviana" "Vivian" "Vivianca" "Vlad"
              "Wallace" "Walter" "William" "Wilemena" "Wilemette" "Wilhelm" "Wole" "Winona" "Winnie" "Wales" "Wyatt" "Wilt" "Wilson" "Waldo" "Wilbur" "Watson"
              "Xerxes" "Xander" "Xandra" "Xanadu" "Xiah" "Xavier" "Xerox"
              "Yaro" "Yahweh"
              "Zed" "Zena" "Zenon" "Zero" "Zeb"
  ]
end

; initialize the agents, number of agents, role (admin, dev, or other),
; engagement index, and efficiency index
to initialize-agents
  create-members num_agents [ ; create a number of turtles
    ; (note: this should all be more sophisticated)
    set agent_contrib_size (random 1000.0) ; set a random
    set repo_size (repo_size + agent_contrib_size)

    set agent_role (one-of ["admin" "dev" "other"]) ; set their roles randomly
    set agent_engagement (random 100) / 100 ; set the engagement index
    set agent_efficiency_quantity (random 100) / 100 ; set the quantity position
    set agent_efficiency_quality (random 100) / 100 ; set the quality position

    set agent_state 2 ; start the agent at 2, engagement

    ; bootstrap active inference variables
    ; set up Active Inference arrays
    ;set agent_states array:from-list [0.1 0.1 0.1 0.7]
    ;set agent_targets array:from-list [0.7 0.1 0.1 0.1]
    ;set agent_ToM array:from-list [0.1 0.9]
    ;set agent_goal_alignment array:from-list [0.2 0.8]
    ; set up HMM matrices
    ; A = outcomes (qual+, quan+, qual-, quan-, eng+, eng-) x states (maximal: qual, quan, eng)
    set agent_states matrix:from-row-list [[1 0 0] [0 1 0] [-1 0 0] [0 -1 0] [0 0 1] [0 0 -1]]
    ; B = which index is maxed, next state by current state
    set agent_transitions matrix:from-row-list [[2 1 1] [0 2 0] [1 0 2]]
    set agent_transitions (agent_transitions matrix:* (1 / 3))
    ; D = prior index, states by first state
    set agent_prior matrix:from-row-list [[0] [0] [1]]
    ; actions able to be taken are:
    ; make code, PRs, Issues   QUAL+
    ; commit code, approve PRs, close Issues QUAN+
    ; request changes, comment, forks ENG+
    ; quiesce QUAL- QUAN- ENG-
    ;set agent_actions matrix:from-row-list [
    ;  ["make code" "make PR" "make Issue"] ; QUAL+
    ;  ["commit code" "approve PRs" "close Issues"] ; QUAN+
    ;  ["request changes" "comment" "fork"] ; ENG+
    ;  ["quiesce"] ; QUAL- QUAN- ENG-
    ;]

    ; other_agent information
    ;create array of all other agents within horizon range
    ; find the local horizon of the given agent
    let horizon-value (agent_engagement * horizon)
    ; look around at all the agents around that agent and their variables
    set other_agents (list (members in-radius horizon-value))
    ;fill array with information on these agents, position (quantity, quality), engagement, goal alignment, ToM

    ; arrange on screen
    ;setxy random-xcor random-ycor
    ;setxy (random 10.0) (random 10.0)
    setxy ((agent_efficiency_quantity * max-pxcor * 2) - max-pxcor) ((agent_efficiency_quality * max-pycor * 2) - max-pycor)

    set shape "person"
    ifelse agent_role = "admin" [
      ;set shape "house"
      set color (list (agent_engagement * 255) 0 0)
    ]
    [
      ifelse agent_role = "dev" [
        set color (list 0 (agent_engagement * 255) 0)
      ]
      [
        set shape "person"
        set color (list 0 0 (agent_engagement * 255))
      ]
    ]

    ; POMDP matrices init
    ; A = outcomes x states = eng-hi, end-mid, eng-lo, quan-hi, quan-med, quan-lo, qual-hi, qual-med, qual-lo
    set matrix_A matrix:from-row-list [[1.0 0.0 0.0 0.0 0.0 0.0] [0.0 1.0 0.0 0.0 0.0 0.0] [0.0 0.0 1.0 0.0 0.0 0.0] [0.0 0.0 0.0 1.0 0.0 0.0] [0.0 0.0 0.0 0.0 1.0 0.0] [0.0 0.0 0.0 0.0 0.0 1.0]]
    ; B = next state x state = eng-hi, end-mid, eng-lo, quan-hi, quan-med, quan-lo, qual-hi, qual-med, qual-lo
    set matrix_B matrix:from-row-list [[1.0 0.0 0.0 0.0 0.0 0.0] [0.0 1.0 0.0 0.0 0.0 0.0] [0.0 0.0 1.0 0.0 0.0 0.0] [0.0 0.0 0.0 1.0 0.0 0.0] [0.0 0.0 0.0 0.0 1.0 0.0] [0.0 0.0 0.0 0.0 0.0 1.0]]
    ; C = softmax(preferences)
    set matrix_C (softmax [3 0 -3 3 0 -3 3 0 -3])
    ; D = prior probs transposed
    set matrix_D [1 1 1 1 1 1 1 1 1]
    set matrix_D map [x -> x / (length matrix_D)] matrix_D
    ; G = policy probabilities


    ; convert list to matrix!
    ;let n_matrix matrix:make-constant 1 (length matrix_C) 0
    ;matrix:set-row n_matrix 0 matrix_C

    show (length names)
    set agent_name (one-of names)
  ]
end


;;
;  Ported Python Functions
;;

; not sure if this is useful yet
to-report softmax_matrix [f_b]
  let soft_exp (matrix:map exp (matrix:map - f_b (max f_b)))
  let soft_sum (matrix:map sum soft_exp)
  report (matrix:map / soft_exp soft_sum)
end

; softmax function for lists
; shifted by b_max for numerical stability
; tested against python
to-report softmax [f_b]
  let b_max (max f_b)
  let b_exp f_b
  set b_exp map [x -> (exp (x - b_max)) ] b_exp
  let b_sum (sum b_exp)
  set b_exp map [x -> (x / b_sum)] f_b
  report f_b
end

to-report D_softmax [f_b]
    let n_matrix matrix:make-constant 1 (length f_b) 0
    matrix:set-row n_matrix 0 f_b
  report (np_diag f_b) matrix:- (np_outer n_matrix n_matrix)
end

to-report model_encoding [f_b]
  report (softmax f_b)
end

to-report variational_density [f_b]
  report (model_encoding f_b)
end


;;
;  Ported Kaufmann functions
;;
to-report initialize_b_star [targets sharpness]
  ;B_STANDARD
  let f_b_star matrix:make-constant 1 ENV_SIZE 0
  set f_b_star map [x -> (exp (-(x - ENV_SIZE / 2) / (ENV_SIZE / sharpness) ^ 2))] f_b_star
  report f_b_star
end



;;
;  Numpy functions
;;

to-report np_diag [b]
  let b_diag (matrix:make-identity (length b))
  let cnt 0
  foreach b [ x ->
    matrix:set b_diag cnt cnt x
    set cnt (cnt + 1)
  ]
  report b_diag
end

to-report np_outer [a b]
  report ((matrix:transpose b) matrix:* a)
end


;;
;  Helper Functions
;;

to make-prs [num_prs]
  set prs array:from-list n-values num_prs [""]
  let i 0 ; starting with i=0
  loop [ ; make num_prs PRs
    if num_prs = i [ stop ]
    let code "code string"
    let new_pr code
    array:set prs i new_pr ; add created PR to prs
    set i (i + 1)
  ]
end

to make-issues [num_issues]
  set issues array:from-list n-values num_issues [""]
  let i 0
  loop [
    if num_issues = i [ stop ]
    let new_issue "issue string"
    array:set issues i new_issue ; add create Issue to issues
    set i (i + 1)
  ]
end


;;
;  Index Functions
;;

to-report agent_quality_index
  report agent_efficiency_quality
end

to-report agent_quantity_index
  report agent_efficiency_quantity
end

to-report agent_engagement_index
  report agent_engagement
end


;;
;  Update Functions
;;

; update the sensory state with variables from world, within engagement horizon, globals (PR, Issues, Repo Size)
to get-sensory-info
  ; find the local horizon of the given agent
  let horizon_value (agent_engagement * horizon)
  ; look around at all the agents around that agent and their variables
  set other_agents (members in-radius horizon_value)
end

; update internal state based on sensory state, ToM, position/index values,
to update-internal
  ;let nearest_sizes ([agent_contrib_size] of other_agents)
  ;let nearest_engagement ([agent_engagement] of other_agents)
  ;let nearest_quality ([agent_efficiency_quality] of other_agents)
  ;let nearest_quantity ([agent_efficiency_quantity] of other_agents)
end

; take an action based on target encoding
to take-action
  ; decide an action
  let max_nearest_quality (max ([agent_efficiency_quality] of other_agents))
  let max_nearest_quantity (max ([agent_efficiency_quantity] of other_agents))
  let min_nearest_quality (min ([agent_efficiency_quality] of other_agents))
  let min_nearest_quantity (min ([agent_efficiency_quantity] of other_agents))
  let max_nearest_engagement (max ([agent_engagement] of other_agents))
  let min_nearest_engagement (min ([agent_engagement] of other_agents))
  ;set agent_efficiency_quality (agent_efficiency_quality + ((max_nearest_quality - min_nearest_quality) / 2))
  ;set agent_efficiency_quantity (agent_efficiency_quantity + ((max_nearest_quantity - min_nearest_quantity) / 2))
  ;set agent_engagement (agent_engagement + ((max_nearest_engagement - min_nearest_engagement) / 2))
  ; HACKY FIXES - should be irrelevant very soon
  ;show agent_engagement
  ;show agent_efficiency_quality
  ;show agent_efficiency_quantity
  if agent_engagement > 1.0 [ set agent_engagement 1.0 ]
  if agent_engagement < 1.0 [ set agent_engagement 0.0 ]
  if (agent_efficiency_quality * max-pxcor) > max-pxcor [ set agent_efficiency_quality 1.0 ]
  if (agent_efficiency_quantity * max-pycor) > max-pycor [ set agent_efficiency_quantity 1.0 ]
  if (agent_efficiency_quality * min-pxcor) < min-pxcor [ set agent_efficiency_quality 0.0 ]
  if (agent_efficiency_quantity * min-pycor) < min-pycor [ set agent_efficiency_quantity 0.0 ]


  let eps (0.999 + (random 3) * 0.002)
  let SHORTEST_PATH (int (ENV_SIZE / 3))
  let TARGET_DELTA (int (ENV_SIZE / 3))

  let EPOCHS 100 ; originally 200
  let N_STEPS 50 ; number of grad desc steps
  let LEARNING_RATE 0.7 ; stochastic grad descent rate

  let shared_target 0 ; originally FOOD_POSITION = 15, now a point in the agent's horizon to move to
  let perceptiveness 0 ; originally MAX_SENSE_PROBABILITY = [0.99, 0.05] strong, weak agents
  let alterity 0 ; originally CONDITIONS[MODEL]['tom'] where MODEL is a number corresponding to a [0,0] or [0,0.5] ToM array and an alignment number (0-1)
  let alignment 0 ; originally CONDITIONS[MODEL]['alignment']

  let initial_positions (list (shared_target + SHORTEST_PATH) (shared_target - SHORTEST_PATH)) ; originally contained % ENV_SIZE on each list element

  let target_0 (shared_target - TARGET_DELTA) ; note these also had % ENV_SIZE
  let target_1 (shared_target + TARGET_DELTA) ; note these also had % ENV_SIZE

  ;let init_b_matrix matrix:from-row-list (list shared_target target_0 target_1)
  ;let init_b_matrix2 matrix:from-row-list (list shared_target target_1 target_0)
  ;let b_star_0 (initialize_b_star init_b_matrix 6)
  ;let b_star_1 (initialize_b_star init_b_matrix2 6)

  ;let epoch 0
  ;while [epoch < EPOCHS]
  ;  [ let delta matrix:make-constant 0 2 0
  ;    ;matrix:set 0 0 delta ()]
  ;    set epoch (epoch + 1)
  ;]
end

; update world state
to update-world
  set repo_size (agent_contrib_size + repo_size)
  ;setxy ((agent_efficiency_quantity * max-pxcor) - max-pxcor) ((agent_efficiency_quality * max-pycor) - max-pycor)
  setxy (agent_efficiency_quantity * max-pxcor) (agent_efficiency_quality * max-pycor)
  set shape "person"
  ifelse agent_role = "admin" [
      ;set shape "house"
      set color (list (agent_engagement * 255) 0 0)
    ]
    [
      ifelse agent_role = "dev" [
        set color (list 0 (agent_engagement * 255) 0)
      ]
      [
        set color (list 0 0 (agent_engagement * 255))
      ]
    ]
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
-16
16
-16
16
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
500
49.0
1
1
NIL
HORIZONTAL

SLIDER
14
75
186
108
churn_rate
churn_rate
0
1.0
0.5
0.01
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
"default" 1.0 0 -16777216 true "" "plot count turtles"

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

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
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

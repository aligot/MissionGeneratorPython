# MissionGeneratorPython

First generator of missions for robot swarms. Creates XML configuration files (.argos) for the ARGoS3 simulator.

For more info about the generator, see:
A. Ligot, A. Cotorruelo, E. Garone, and M. Birattari (2022). Towards an empirical practice in off-line fully-automatic 
design of robot swarms. IEEE Transactions on Evolutionary Computation, 26(6):1236-1245.




The generator of strings of parameters resembles the one used in
IRACE. It takes a file of parameters description as input. These
parameters description will include the range of values that can be
taken, and conditions (logical expressions) to create relations
between parameters. The generator samples the values for
the parameters that meet the conditions.

Example:
<name>    <label>   <type>        <range>                       <conditions>
mission   --m       categorical   ('foraging', 'agg', 'dg')     NA
expLength --el      ordinal       (60, 90, 120, 150, 180)       NA
robots    --r       integer       (15, 25)                      NA
initPosit --ip      categorical   ('area', 'fixed')             NA
initOrient --io     categorical   ('uniform', 'fixed')          NA
floorCol   --fc     categorical   ('white', 'black', 'gray')    NA


Currently, for the reference model RM1.1/2, all the missions that we
liked can be categorized into three classes: foraging, aggregation,
and directional gate.

Conditions are a bit more complex that the ones of IRACE. For example, in a
foraging mission, at least two patches of different colors need to be
instantiated in the environment: one for the nest, one for the food
source. Also, if obstacles are instantiated, they should allow for a
clear path between the nest and the food source. The generator incorporates 
these predefined conditions, maybe in classes dedicated to the missions.

Example:
<name>             <label>      <type>             <range>                  <conditions>
nPatchesFor        --npf        integer            (2, 3)                   mission == 'foraging'
nPatchesAgg        --npa        integer            (0, 3)                   mission == 'agg'
nPatchesDg         --npdg       integer            ?                        mission == 'dg'

## Foraging
typePatchFor1      --tpf1       categorical       ('circ', 'rect')            nPatchesFor > 0
dimPatchFor1       --dpf1       real              (0.2, 0.6)                  nPatchesFor > 0
posPatchFor1       --ppf1       categorical       {'unif'}                    nPatchesFor > 0
rangeXPatchFor1    --rxpf1      real              (-1.0, 1.0)                 posPatchFor1 == 'unif'
rangeYPatchFor1    --rypf1      real              (-1.0, 1.0)                 posPatchFor1 == 'unif'
centerXPatchFor1   --cxpf1      real              function()                  randomly sample X and Y + checkOverlap
centerYPatchFor1   --cypf1      real              function()
colorPatchFor1     --cpf1       categorical       {'w', 'g', 'b'} - floorCol  nPatchesFor > 0

typePatchFor2      --tpf2       categorical       ('circ', 'rect')            nPatchesFor > 1
dimPatchFor2       --dpf2       real              (0.2, 0.6)                  nPatchesFor > 1
posPatchFor2       --ppf2       categorical       {'unif', 'relation'}        nPatchesFor > 1
relPatchFor2       --rpf2       categorical       {1}                         #index of patch to be in relation with.
rangeXPatchFor2    --rxpf2      real              (-1.0, 1.0)                 posPatchFor2 == 'unif'
rangeYPatchFor2    --rypf2      real              (-1.0, 1.0)                 posPatchFor2 == 'unif'
distPatchFor2      --dpf2      real               (0.0, 0.6)                  posPatchFor2 == 'relation'
centerXPatchFor2   --cxpf2      real              function()                  if posPatchFor2 == 'unif', randomly sample X and Y + checkOverlap
                                                                                 posPatchFor2 == 'relation', sample X and Y so that + checkOverlap
centerYPatchFor2   --cypf2      real              function()
colorPatchFor2     --cpf2       categorical       {'w', 'g', 'b'} - floorCol  nPatchesFor > 1 AND if nPatchesFor==2, colorPatchFor2 != colorPatchFor1



nObstacles    --no      integer     (0, 5)             NA
obstacle0     --o0      real        (0.05, 0.80)       nObstacles > 0
distObs0      --dist0   categorical ('random', 'side') nObstacles > 0, side iff at least one rectangular patch exists


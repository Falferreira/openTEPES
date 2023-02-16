"""
Open Generation, Storage, and Transmission Operation and Expansion Planning Model with RES and ESS (openTEPES) - February 16, 2023
"""

import datetime
import time
import math
import os
import pandas        as pd
from   pyomo.environ import DataPortal, Set, Param, Var, Binary, NonNegativeReals, PositiveReals, PositiveIntegers, NonNegativeIntegers, Reals, UnitInterval, Boolean, Any


def InputData(DirName, CaseName, mTEPES, pIndLogConsole):
    print('Input data                             ****')

    _path = os.path.join(DirName, CaseName)
    StartTime = time.time()

    #%% reading data from CSV
    dfOption             = pd.read_csv(_path+'/oT_Data_Option_'                +CaseName+'.csv', index_col=[0    ])
    dfParameter          = pd.read_csv(_path+'/oT_Data_Parameter_'             +CaseName+'.csv', index_col=[0    ])
    dfPeriod             = pd.read_csv(_path+'/oT_Data_Period_'                +CaseName+'.csv', index_col=[0    ])
    dfScenario           = pd.read_csv(_path+'/oT_Data_Scenario_'              +CaseName+'.csv', index_col=[0,1  ])
    dfStage              = pd.read_csv(_path+'/oT_Data_Stage_'                 +CaseName+'.csv', index_col=[0    ])
    dfDuration           = pd.read_csv(_path+'/oT_Data_Duration_'              +CaseName+'.csv', index_col=[0    ])
    dfReserveMargin      = pd.read_csv(_path+'/oT_Data_ReserveMargin_'         +CaseName+'.csv', index_col=[0    ])
    dfDemand             = pd.read_csv(_path+'/oT_Data_Demand_'                +CaseName+'.csv', index_col=[0,1,2])
    dfInertia            = pd.read_csv(_path+'/oT_Data_Inertia_'               +CaseName+'.csv', index_col=[0,1,2])
    dfUpOperatingReserve = pd.read_csv(_path+'/oT_Data_OperatingReserveUp_'    +CaseName+'.csv', index_col=[0,1,2])
    dfDwOperatingReserve = pd.read_csv(_path+'/oT_Data_OperatingReserveDown_'  +CaseName+'.csv', index_col=[0,1,2])
    dfGeneration         = pd.read_csv(_path+'/oT_Data_Generation_'            +CaseName+'.csv', index_col=[0    ])
    dfVariableMinPower   = pd.read_csv(_path+'/oT_Data_VariableMinGeneration_' +CaseName+'.csv', index_col=[0,1,2])
    dfVariableMaxPower   = pd.read_csv(_path+'/oT_Data_VariableMaxGeneration_' +CaseName+'.csv', index_col=[0,1,2])
    dfVariableMinCharge  = pd.read_csv(_path+'/oT_Data_VariableMinConsumption_'+CaseName+'.csv', index_col=[0,1,2])
    dfVariableMaxCharge  = pd.read_csv(_path+'/oT_Data_VariableMaxConsumption_'+CaseName+'.csv', index_col=[0,1,2])
    dfVariableMinStorage = pd.read_csv(_path+'/oT_Data_VariableMinStorage_'    +CaseName+'.csv', index_col=[0,1,2])
    dfVariableMaxStorage = pd.read_csv(_path+'/oT_Data_VariableMaxStorage_'    +CaseName+'.csv', index_col=[0,1,2])
    dfVariableMinEnergy  = pd.read_csv(_path+'/oT_Data_VariableMinEnergy_'     +CaseName+'.csv', index_col=[0,1,2])
    dfVariableMaxEnergy  = pd.read_csv(_path+'/oT_Data_VariableMaxEnergy_'     +CaseName+'.csv', index_col=[0,1,2])
    dfEnergyInflows      = pd.read_csv(_path+'/oT_Data_EnergyInflows_'         +CaseName+'.csv', index_col=[0,1,2])
    dfEnergyOutflows     = pd.read_csv(_path+'/oT_Data_EnergyOutflows_'        +CaseName+'.csv', index_col=[0,1,2])
    dfNodeLocation       = pd.read_csv(_path+'/oT_Data_NodeLocation_'          +CaseName+'.csv', index_col=[0    ])
    dfNetwork            = pd.read_csv(_path+'/oT_Data_Network_'               +CaseName+'.csv', index_col=[0,1,2])

    # substitute NaN by 0
    dfOption.fillna            (0  , inplace=True)
    dfParameter.fillna         (0.0, inplace=True)
    dfPeriod.fillna            (0.0, inplace=True)
    dfScenario.fillna          (0.0, inplace=True)
    dfStage.fillna             (0.0, inplace=True)
    dfDuration.fillna          (0  , inplace=True)
    dfReserveMargin.fillna     (0.0, inplace=True)
    dfDemand.fillna            (0.0, inplace=True)
    dfInertia.fillna           (0.0, inplace=True)
    dfUpOperatingReserve.fillna(0.0, inplace=True)
    dfDwOperatingReserve.fillna(0.0, inplace=True)
    dfGeneration.fillna        (0.0, inplace=True)
    dfVariableMinPower.fillna  (0.0, inplace=True)
    dfVariableMaxPower.fillna  (0.0, inplace=True)
    dfVariableMinCharge.fillna (0.0, inplace=True)
    dfVariableMaxCharge.fillna (0.0, inplace=True)
    dfVariableMinStorage.fillna(0.0, inplace=True)
    dfVariableMaxStorage.fillna(0.0, inplace=True)
    dfVariableMinEnergy.fillna (0.0, inplace=True)
    dfVariableMaxEnergy.fillna (0.0, inplace=True)
    dfEnergyInflows.fillna     (0.0, inplace=True)
    dfEnergyOutflows.fillna    (0.0, inplace=True)
    dfNodeLocation.fillna      (0.0, inplace=True)
    dfNetwork.fillna           (0.0, inplace=True)

    dfReserveMargin      = dfReserveMargin.where     (dfReserveMargin      > 0.0, other=0.0)
    dfInertia            = dfInertia.where           (dfInertia            > 0.0, other=0.0)
    dfUpOperatingReserve = dfUpOperatingReserve.where(dfUpOperatingReserve > 0.0, other=0.0)
    dfDwOperatingReserve = dfDwOperatingReserve.where(dfDwOperatingReserve > 0.0, other=0.0)
    dfVariableMinPower   = dfVariableMinPower.where  (dfVariableMinPower   > 0.0, other=0.0)
    dfVariableMaxPower   = dfVariableMaxPower.where  (dfVariableMaxPower   > 0.0, other=0.0)
    dfVariableMinCharge  = dfVariableMinCharge.where (dfVariableMinCharge  > 0.0, other=0.0)
    dfVariableMaxCharge  = dfVariableMaxCharge.where (dfVariableMaxCharge  > 0.0, other=0.0)
    dfVariableMinStorage = dfVariableMinStorage.where(dfVariableMinStorage > 0.0, other=0.0)
    dfVariableMaxStorage = dfVariableMaxStorage.where(dfVariableMaxStorage > 0.0, other=0.0)
    dfVariableMinEnergy  = dfVariableMinEnergy.where (dfVariableMinEnergy  > 0.0, other=0.0)
    dfVariableMaxEnergy  = dfVariableMaxEnergy.where (dfVariableMaxEnergy  > 0.0, other=0.0)
    dfEnergyInflows      = dfEnergyInflows.where     (dfEnergyInflows      > 0.0, other=0.0)
    dfEnergyOutflows     = dfEnergyOutflows.where    (dfEnergyOutflows     > 0.0, other=0.0)

    # show some statistics of the data
    if pIndLogConsole == 1:
        print('Reserve margin               \n', dfReserveMargin.describe     ())
        print('Demand                       \n', dfDemand.describe            ())
        print('Inertia                      \n', dfInertia.describe           ())
        print('Upward   operating reserves  \n', dfUpOperatingReserve.describe())
        print('Downward operating reserves  \n', dfDwOperatingReserve.describe())
        print('Generation                   \n', dfGeneration.describe        ())
        print('Variable minimum generation  \n', dfVariableMinPower.describe  ())
        print('Variable maximum generation  \n', dfVariableMaxPower.describe  ())
        print('Variable minimum consumption \n', dfVariableMinCharge.describe ())
        print('Variable maximum consumption \n', dfVariableMaxCharge.describe ())
        print('Variable minimum storage     \n', dfVariableMinStorage.describe())
        print('Variable maximum storage     \n', dfVariableMaxStorage.describe())
        print('Variable minimum energy      \n', dfVariableMinEnergy.describe ())
        print('Variable maximum energy      \n', dfVariableMaxEnergy.describe ())
        print('Energy inflows               \n', dfEnergyInflows.describe     ())
        print('Energy outflows              \n', dfEnergyOutflows.describe    ())
        print('Network                      \n', dfNetwork.describe           ())

    #%% reading the sets
    dictSets = DataPortal()
    dictSets.load(filename=_path+'/oT_Dict_Period_'      +CaseName+'.csv', set='p'   , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Scenario_'    +CaseName+'.csv', set='sc'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Stage_'       +CaseName+'.csv', set='st'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_LoadLevel_'   +CaseName+'.csv', set='n'   , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Generation_'  +CaseName+'.csv', set='g'   , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Technology_'  +CaseName+'.csv', set='gt'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Storage_'     +CaseName+'.csv', set='et'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Node_'        +CaseName+'.csv', set='nd'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Zone_'        +CaseName+'.csv', set='zn'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Area_'        +CaseName+'.csv', set='ar'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Region_'      +CaseName+'.csv', set='rg'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Circuit_'     +CaseName+'.csv', set='cc'  , format='set')
    dictSets.load(filename=_path+'/oT_Dict_Line_'        +CaseName+'.csv', set='lt'  , format='set')

    dictSets.load(filename=_path+'/oT_Dict_NodeToZone_'  +CaseName+'.csv', set='ndzn', format='set')
    dictSets.load(filename=_path+'/oT_Dict_ZoneToArea_'  +CaseName+'.csv', set='znar', format='set')
    dictSets.load(filename=_path+'/oT_Dict_AreaToRegion_'+CaseName+'.csv', set='arrg', format='set')

    mTEPES.pp   = Set(initialize=dictSets['p' ],   ordered=True,  doc='periods',         within=PositiveIntegers)
    mTEPES.scc  = Set(initialize=dictSets['sc'],   ordered=True,  doc='scenarios'       )
    mTEPES.stt  = Set(initialize=dictSets['st'],   ordered=True,  doc='stages'          )
    mTEPES.nn   = Set(initialize=dictSets['n' ],   ordered=True,  doc='load levels'     )
    mTEPES.gg   = Set(initialize=dictSets['g' ],   ordered=False, doc='units'           )
    mTEPES.gt   = Set(initialize=dictSets['gt'],   ordered=False, doc='technologies'    )
    mTEPES.et   = Set(initialize=dictSets['et'],   ordered=False, doc='ESS types'       )
    mTEPES.nd   = Set(initialize=dictSets['nd'],   ordered=False, doc='nodes'           )
    mTEPES.ni   = Set(initialize=dictSets['nd'],   ordered=False, doc='nodes'           )
    mTEPES.nf   = Set(initialize=dictSets['nd'],   ordered=False, doc='nodes'           )
    mTEPES.zn   = Set(initialize=dictSets['zn'],   ordered=False, doc='zones'           )
    mTEPES.ar   = Set(initialize=dictSets['ar'],   ordered=False, doc='areas'           )
    mTEPES.rg   = Set(initialize=dictSets['rg'],   ordered=False, doc='regions'         )
    mTEPES.cc   = Set(initialize=dictSets['cc'],   ordered=False, doc='circuits'        )
    mTEPES.c2   = Set(initialize=dictSets['cc'],   ordered=False, doc='circuits'        )
    mTEPES.lt   = Set(initialize=dictSets['lt'],   ordered=False, doc='line types'      )

    mTEPES.ndzn = Set(initialize=dictSets['ndzn'], ordered=False, doc='node to zone'    )
    mTEPES.znar = Set(initialize=dictSets['znar'], ordered=False, doc='zone to area'    )
    mTEPES.arrg = Set(initialize=dictSets['arrg'], ordered=False, doc='area to region'  )

    #%% parameters
    pIndBinGenInvest     = dfOption   ['IndBinGenInvest'    ][0].astype('int')                                                            # Indicator of binary generation expansion decisions, 0 continuous  - 1 binary - 2 no investment variables
    pIndBinNetInvest     = dfOption   ['IndBinNetInvest'    ][0].astype('int')                                                            # Indicator of binary network    expansion decisions, 0 continuous  - 1 binary - 2 no investment variables
    pIndBinGenRetire     = dfOption   ['IndBinGenRetirement'][0].astype('int')                                                            # Indicator of binary generation retirement decisions,0 continuous  - 1 binary - 2 no retirement variables
    pIndBinGenOperat     = dfOption   ['IndBinGenOperat'    ][0].astype('int')                                                            # Indicator of binary generation operation decisions, 0 continuous  - 1 binary
    pIndBinSingleNode    = dfOption   ['IndBinSingleNode'   ][0].astype('int')                                                            # Indicator of single node although with network,     0 network     - 1 single node
    pIndBinGenRamps      = dfOption   ['IndBinGenRamps'     ][0].astype('int')                                                            # Indicator of ramp constraints,                      0 no ramps    - 1 ramp constraints
    pIndBinGenMinTime    = dfOption   ['IndBinGenMinTime'   ][0].astype('int')                                                            # Indicator of minimum up/down time constraints,      0 no min time - 1 min time constraints
    pIndBinLineCommit    = dfOption   ['IndBinLineCommit'   ][0].astype('int')                                                            # Indicator of binary network    switching decisions, 0 continuous  - 1 binary
    pIndBinNetLosses     = dfOption   ['IndBinNetLosses'    ][0].astype('int')                                                            # Indicator of network losses,                        0 lossless    - 1 ohmic losses
    pENSCost             = dfParameter['ENSCost'            ][0] * 1e-3                                                                   # cost of energy not served                [MEUR/GWh]
    pCO2Cost             = dfParameter['CO2Cost'            ][0]                                                                          # cost of CO2 emission                     [EUR/t CO2]
    pEconomicBaseYear    = dfParameter['EconomicBaseYear'   ][0]                                                                          # economic base year                       [year]
    pAnnualDiscRate      = dfParameter['AnnualDiscountRate' ][0]                                                                          # annual discount rate                     [p.u.]
    pUpReserveActivation = dfParameter['UpReserveActivation'][0]                                                                          # upward   reserve activation              [p.u.]
    pDwReserveActivation = dfParameter['DwReserveActivation'][0]                                                                          # downward reserve activation              [p.u.]
    pMinRatioDwUp        = dfParameter['MinRatioDwUp'       ][0]                                                                          # minimum ratio down up operating reserves [p.u.]
    pMaxRatioDwUp        = dfParameter['MaxRatioDwUp'       ][0]                                                                          # maximum ratio down up operating reserves [p.u.]
    pSBase               = dfParameter['SBase'              ][0] * 1e-3                                                                   # base power                               [GW]
    pReferenceNode       = dfParameter['ReferenceNode'      ][0]                                                                          # reference node
    pTimeStep            = dfParameter['TimeStep'           ][0].astype('int')                                                            # duration of the unit time step           [h]
    # pStageDuration       = dfParameter['StageDuration'      ][0].astype('int')                                                          # duration of each stage                   [h]

    pPeriodWeight        = dfPeriod        ['Weight'        ].astype('int')                                                               # weights of periods                       [p.u.]
    pScenProb            = dfScenario      ['Probability'   ].astype('float')                                                             # probabilities of scenarios               [p.u.]
    pStageWeight         = dfStage         ['Weight'        ].astype('int')                                                               # weights of stages                        [p.u.]
    pDuration            = dfDuration      ['Duration'      ]    * pTimeStep                                                              # duration of load levels                  [h]
    pReserveMargin       = dfReserveMargin ['ReserveMargin' ]                                                                             # minimum adequacy reserve margin          [p.u.]
    pLevelToStage        = dfDuration      ['Stage'         ]                                                                             # load levels assignment to stages
    pDemand              = dfDemand               [mTEPES.nd]    * 1e-3                                                                   # demand                                   [GW]
    pSystemInertia       = dfInertia              [mTEPES.ar]                                                                             # inertia                                  [s]
    pOperReserveUp       = dfUpOperatingReserve   [mTEPES.ar]    * 1e-3                                                                   # upward   operating reserve               [GW]
    pOperReserveDw       = dfDwOperatingReserve   [mTEPES.ar]    * 1e-3                                                                   # downward operating reserve               [GW]
    pVariableMinPower    = dfVariableMinPower     [mTEPES.gg]    * 1e-3                                                                   # dynamic variable minimum power           [GW]
    pVariableMaxPower    = dfVariableMaxPower     [mTEPES.gg]    * 1e-3                                                                   # dynamic variable maximum power           [GW]
    pVariableMinCharge   = dfVariableMinCharge    [mTEPES.gg]    * 1e-3                                                                   # dynamic variable minimum charge          [GW]
    pVariableMaxCharge   = dfVariableMaxCharge    [mTEPES.gg]    * 1e-3                                                                   # dynamic variable maximum charge          [GW]
    pVariableMinStorage  = dfVariableMinStorage   [mTEPES.gg]                                                                             # dynamic variable minimum storage         [GWh]
    pVariableMaxStorage  = dfVariableMaxStorage   [mTEPES.gg]                                                                             # dynamic variable maximum storage         [GWh]
    pVariableMinEnergy   = dfVariableMinEnergy    [mTEPES.gg]    * 1e-3                                                                   # dynamic variable minimum energy          [GW]
    pVariableMaxEnergy   = dfVariableMaxEnergy    [mTEPES.gg]    * 1e-3                                                                   # dynamic variable maximum energy          [GW]
    pEnergyInflows       = dfEnergyInflows        [mTEPES.gg]    * 1e-3                                                                   # dynamic energy inflows                   [GW]
    pEnergyOutflows      = dfEnergyOutflows       [mTEPES.gg]    * 1e-3                                                                   # dynamic energy outflows                  [GW]

    # compute the demand as the mean over the time step load levels and assign it to active load levels. Idem for operating reserve, variable max power, variable min and max storage and inflows
    if pTimeStep > 1:
        pDemand             = pDemand.rolling            (pTimeStep).mean()
        pSystemInertia      = pSystemInertia.rolling     (pTimeStep).mean()
        pOperReserveUp      = pOperReserveUp.rolling     (pTimeStep).mean()
        pOperReserveDw      = pOperReserveDw.rolling     (pTimeStep).mean()
        pVariableMinPower   = pVariableMinPower.rolling  (pTimeStep).mean()
        pVariableMaxPower   = pVariableMaxPower.rolling  (pTimeStep).mean()
        pVariableMinCharge  = pVariableMinCharge.rolling (pTimeStep).mean()
        pVariableMaxCharge  = pVariableMaxCharge.rolling (pTimeStep).mean()
        pVariableMinStorage = pVariableMinStorage.rolling(pTimeStep).mean()
        pVariableMaxStorage = pVariableMaxStorage.rolling(pTimeStep).mean()
        pVariableMinEnergy  = pVariableMinEnergy.rolling (pTimeStep).mean()
        pVariableMaxEnergy  = pVariableMaxEnergy.rolling (pTimeStep).mean()
        pEnergyInflows      = pEnergyInflows.rolling     (pTimeStep).mean()
        pEnergyOutflows     = pEnergyOutflows.rolling    (pTimeStep).mean()

    pDemand.fillna            (0.0, inplace=True)
    pSystemInertia.fillna     (0.0, inplace=True)
    pOperReserveUp.fillna     (0.0, inplace=True)
    pOperReserveDw.fillna     (0.0, inplace=True)
    pVariableMinPower.fillna  (0.0, inplace=True)
    pVariableMaxPower.fillna  (0.0, inplace=True)
    pVariableMinCharge.fillna (0.0, inplace=True)
    pVariableMaxCharge.fillna (0.0, inplace=True)
    pVariableMinStorage.fillna(0.0, inplace=True)
    pVariableMaxStorage.fillna(0.0, inplace=True)
    pVariableMinEnergy.fillna (0.0, inplace=True)
    pVariableMaxEnergy.fillna (0.0, inplace=True)
    pEnergyInflows.fillna     (0.0, inplace=True)
    pEnergyOutflows.fillna    (0.0, inplace=True)

    if pTimeStep > 1:
        # assign duration 0 to load levels not being considered, active load levels are at the end of every pTimeStep
        for i in range(pTimeStep-2,-1,-1):
            pDuration.iloc[[range(i,len(mTEPES.nn),pTimeStep)]] = 0

    #%% generation parameters
    pGenToNode          = dfGeneration  ['Node'                  ]                                                                            # generator location in node
    pGenToTechnology    = dfGeneration  ['Technology'            ]                                                                            # generator association to technology
    pGenToExclusiveGen  = dfGeneration  ['MutuallyExclusive'     ]                                                                            # mutually exclusive generator
    pIndBinUnitInvest   = dfGeneration  ['BinaryInvestment'      ]                                                                            # binary unit investment decision             [Yes]
    pIndBinUnitRetire   = dfGeneration  ['BinaryRetirement'      ]                                                                            # binary unit retirement decision             [Yes]
    pIndBinUnitCommit   = dfGeneration  ['BinaryCommitment'      ]                                                                            # binary unit commitment decision             [Yes]
    pIndBinStorInvest   = dfGeneration  ['StorageInvestment'     ]                                                                            # storage linked to generation investment     [Yes]
    pIndOperReserve     = dfGeneration  ['NoOperatingReserve'    ]                                                                            # no contribution to operating reserve        [Yes]
    pMustRun            = dfGeneration  ['MustRun'               ]                                                                            # must-run unit                               [Yes]
    pInertia            = dfGeneration  ['Inertia'               ]                                                                            # inertia constant                            [s]
    pPeriodIniGen       = dfGeneration  ['InitialPeriod'         ]                                                                            # initial period                              [year]
    pPeriodFinGen       = dfGeneration  ['FinalPeriod'           ]                                                                            # final   period                              [year]
    pAvailability       = dfGeneration  ['Availability'          ]                                                                            # unit availability for adequacy              [p.u.]
    pEFOR               = dfGeneration  ['EFOR'                  ]                                                                            # EFOR                                        [p.u.]
    pRatedMinPower      = dfGeneration  ['MinimumPower'          ] * 1e-3 * (1.0-dfGeneration['EFOR'])                                        # rated minimum power                         [GW]
    pRatedMaxPower      = dfGeneration  ['MaximumPower'          ] * 1e-3 * (1.0-dfGeneration['EFOR'])                                        # rated maximum power                         [GW]
    pLinearFuelCost     = dfGeneration  ['LinearTerm'            ] * 1e-3 *      dfGeneration['FuelCost']                                     # fuel     term variable cost                 [MEUR/GWh]
    pLinearOMCost       = dfGeneration  ['OMVariableCost'        ] * 1e-3                                                                     # O&M      term variable cost                 [MEUR/GWh]
    pConstantVarCost    = dfGeneration  ['ConstantTerm'          ] * 1e-6 *      dfGeneration['FuelCost']                                     # constant term variable cost                 [MEUR/h]
    pOperReserveCost    = dfGeneration  ['OperReserveCost'       ] * 1e-3                                                                     # operating reserve      cost                 [MEUR/GW]
    pStartUpCost        = dfGeneration  ['StartUpCost'           ]                                                                            # startup  cost                               [MEUR]
    pShutDownCost       = dfGeneration  ['ShutDownCost'          ]                                                                            # shutdown cost                               [MEUR]
    pRampUp             = dfGeneration  ['RampUp'                ] * 1e-3                                                                     # ramp up   rate                              [GW/h]
    pRampDw             = dfGeneration  ['RampDown'              ] * 1e-3                                                                     # ramp down rate                              [GW/h]
    pCO2EmissionCost    = dfGeneration  ['CO2EmissionRate'       ] * 1e-3 * pCO2Cost                                                          # emission  cost                              [MEUR/GWh]
    pCO2EmissionRate    = dfGeneration  ['CO2EmissionRate'       ]                                                                            # emission  rate                              [tCO2/MWh]
    pUpTime             = dfGeneration  ['UpTime'                ]                                                                            # minimum up    time                          [h]
    pDwTime             = dfGeneration  ['DownTime'              ]                                                                            # minimum down  time                          [h]
    pShiftTime          = dfGeneration  ['ShiftTime'             ]                                                                            # maximum shift time for DSM                  [h]
    pGenInvestCost      = dfGeneration  ['FixedInvestmentCost'   ] *        dfGeneration['FixedChargeRate']                                   # generation fixed cost                       [MEUR]
    pGenRetireCost      = dfGeneration  ['FixedRetirementCost'   ] *        dfGeneration['FixedChargeRate']                                   # generation fixed retirement cost            [MEUR]
    pRatedMinCharge     = dfGeneration  ['MinimumCharge'         ] * 1e-3                                                                     # rated minimum ESS charge                    [GW]
    pRatedMaxCharge     = dfGeneration  ['MaximumCharge'         ] * 1e-3                                                                     # rated maximum ESS charge                    [GW]
    pRatedMinStorage    = dfGeneration  ['MinimumStorage'        ]                                                                            # rated minimum ESS storage                   [GWh]
    pRatedMaxStorage    = dfGeneration  ['MaximumStorage'        ]                                                                            # rated maximum ESS storage                   [GWh]
    pInitialInventory   = dfGeneration  ['InitialStorage'        ]                                                                            # initial       ESS storage                   [GWh]
    pEfficiency         = dfGeneration  ['Efficiency'            ]                                                                            #         ESS round-trip efficiency           [p.u.]
    pStorageType        = dfGeneration  ['StorageType'           ]                                                                            #         ESS storage  type
    pOutflowsType       = dfGeneration  ['OutflowsType'          ]                                                                            #         ESS outflows type
    pEnergyType         = dfGeneration  ['EnergyType'            ]                                                                            #         unit  energy type
    pRMaxReactivePower  = dfGeneration  ['MaximumReactivePower'  ] * 1e-3                                                                     # rated maximum reactive power                [Gvar]
    pGenLoInvest        = dfGeneration  ['InvestmentLo'          ]                                                                            # Lower bound of the investment decision      [p.u.]
    pGenUpInvest        = dfGeneration  ['InvestmentUp'          ]                                                                            # Upper bound of the investment decision      [p.u.]
    pGenLoRetire        = dfGeneration  ['RetirementLo'          ]                                                                            # Lower bound of the retirement decision      [p.u.]
    pGenUpRetire        = dfGeneration  ['RetirementUp'          ]                                                                            # Upper bound of the retirement decision      [p.u.]

    pLinearOperCost     = pLinearFuelCost + pCO2EmissionCost
    pLinearVarCost      = pLinearFuelCost + pLinearOMCost

    pNodeLat            = dfNodeLocation['Latitude'              ]                                                                            # node latitude                               [º]
    pNodeLon            = dfNodeLocation['Longitude'             ]                                                                            # node longitude                              [º]

    pLineType           = dfNetwork     ['LineType'              ]                                                                            # line type
    pLineLength         = dfNetwork     ['Length'                ]                                                                            # line length                                 [km]
    pLineVoltage        = dfNetwork     ['Voltage'               ]                                                                            # line voltage                                [kV]
    pPeriodIniNet       = dfNetwork     ['InitialPeriod'         ]                                                                            # initial period
    pPeriodFinNet       = dfNetwork     ['FinalPeriod'           ]                                                                            # final   period
    pLineLossFactor     = dfNetwork     ['LossFactor'            ]                                                                            # loss factor                                 [p.u.]
    pLineR              = dfNetwork     ['Resistance'            ]                                                                            # resistance                                  [p.u.]
    pLineX              = dfNetwork     ['Reactance'             ].sort_index()                                                               # reactance                                   [p.u.]
    pLineBsh            = dfNetwork     ['Susceptance'           ]                                                                            # susceptance                                 [p.u.]
    pLineTAP            = dfNetwork     ['Tap'                   ]                                                                            # tap changer                                 [p.u.]
    pLineNTCFrw         = dfNetwork     ['TTC'                   ] * 1e-3 * dfNetwork['SecurityFactor' ]                                      # net transfer capacity in forward  direction [GW]
    pLineNTCBck         = dfNetwork     ['TTCBck'                ] * 1e-3 * dfNetwork['SecurityFactor' ]                                      # net transfer capacity in backward direction [GW]
    pNetFixedCost       = dfNetwork     ['FixedInvestmentCost'   ] *        dfNetwork['FixedChargeRate']                                      # network    fixed cost                       [MEUR]
    pIndBinLineSwitch   = dfNetwork     ['Switching'             ]                                                                            # binary line switching  decision             [Yes]
    pIndBinLineInvest   = dfNetwork     ['BinaryInvestment'      ]                                                                            # binary line investment decision             [Yes]
    pSwitchOnTime       = dfNetwork     ['SwOnTime'              ].astype('int')                                                              # minimum on  time                            [h]
    pSwitchOffTime      = dfNetwork     ['SwOffTime'             ].astype('int')                                                              # minimum off time                            [h]
    pAngMin             = dfNetwork     ['AngMin'                ] * math.pi / 180                                                            # Min phase angle difference                  [rad]
    pAngMax             = dfNetwork     ['AngMax'                ] * math.pi / 180                                                            # Max phase angle difference                  [rad]
    pNetLoInvest        = dfNetwork     ['InvestmentLo'          ]                                                                            # Lower bound of the investment decision      [p.u.]
    pNetUpInvest        = dfNetwork     ['InvestmentUp'          ]                                                                            # Upper bound of the investment decision      [p.u.]

    # replace pLineNTCBck = 0.0 by pLineNTCFrw
    pLineNTCBck     = pLineNTCBck.where(pLineNTCBck   > 0.0, other=pLineNTCFrw)
    # replace pLineNTCFrw = 0.0 by pLineNTCBck
    pLineNTCFrw     = pLineNTCFrw.where(pLineNTCFrw   > 0.0, other=pLineNTCBck)
    # replace pGenUpInvest = 0.0 by 1.0
    pGenUpInvest    = pGenUpInvest.where(pGenUpInvest > 0.0, other=1.0        )
    # replace pGenUpRetire = 0.0 by 1.0
    pGenUpRetire    = pGenUpRetire.where(pGenUpRetire > 0.0, other=1.0        )
    # replace pNetUpInvest = 0.0 by 1.0
    pNetUpInvest    = pNetUpInvest.where(pNetUpInvest > 0.0, other=1.0        )

    # minimum up- and downtime converted to an integer number of time steps
    pSwitchOnTime  = round(pSwitchOnTime /pTimeStep).astype('int')
    pSwitchOffTime = round(pSwitchOffTime/pTimeStep).astype('int')

    ReadingDataTime = time.time() - StartTime
    StartTime       = time.time()
    print('Reading    input data                  ... ', round(ReadingDataTime), 's')

    #%% Getting the branches from the network data
    sBr = [(ni,nf) for (ni,nf,cc) in dfNetwork.index]
    # Dropping duplicate keys
    sBrList = [(ni,nf) for n,(ni,nf) in enumerate(sBr) if (ni,nf) not in sBr[:n]]

    #%% defining subsets: active load levels (n,n2), thermal units (t), RES units (r), ESS units (es), candidate gen units (gc), candidate ESS units (ec), all the lines (la), candidate lines (lc), candidate DC lines (cd), existing DC lines (cd), lines with losses (ll), reference node (rf), and reactive generating units (gq)
    mTEPES.p   = Set(initialize=mTEPES.pp,          ordered=True , doc='periods'              , filter=lambda mTEPES,pp      :  pp     in mTEPES.pp  and pPeriodWeight     [pp] >  0.0)
    mTEPES.sc  = Set(initialize=mTEPES.scc,         ordered=True , doc='scenarios'            , filter=lambda mTEPES,scc     :  scc    in mTEPES.scc                                  )
    mTEPES.ps  = Set(initialize=mTEPES.p*mTEPES.sc, ordered=True , doc='periods/scenarios'    , filter=lambda mTEPES,p,sc    :  (p,sc) in mTEPES.p*mTEPES.sc and pScenProb[p,sc] > 0.0)
    mTEPES.st  = Set(initialize=mTEPES.stt,         ordered=True , doc='stages'               , filter=lambda mTEPES,stt     :  stt    in mTEPES.stt and pStageWeight     [stt] >  0.0)
    mTEPES.n   = Set(initialize=mTEPES.nn,          ordered=True , doc='load levels'          , filter=lambda mTEPES,nn      :  nn     in mTEPES.nn  and pDuration         [nn] >  0  )
    mTEPES.n2  = Set(initialize=mTEPES.nn,          ordered=True , doc='load levels'          , filter=lambda mTEPES,nn      :  nn     in mTEPES.nn  and pDuration         [nn] >  0  )
    mTEPES.g   = Set(initialize=mTEPES.gg,          ordered=False, doc='generating      units', filter=lambda mTEPES,gg      :  gg     in mTEPES.gg  and (pRatedMaxPower   [gg] >  0.0 or  pRatedMaxCharge[gg] >  0.0) and pPeriodIniGen[gg] <= mTEPES.p.last() and pPeriodFinGen[gg] >= mTEPES.p.first() and pGenToNode.reset_index().set_index(['index']).isin(mTEPES.nd)['Node'][gg])  # excludes generators with empty node
    mTEPES.t   = Set(initialize=mTEPES.g ,          ordered=False, doc='thermal         units', filter=lambda mTEPES,g       :  g      in mTEPES.g   and pLinearOperCost   [g ] >  0.0)
    mTEPES.r   = Set(initialize=mTEPES.g ,          ordered=False, doc='RES             units', filter=lambda mTEPES,g       :  g      in mTEPES.g   and pLinearOperCost   [g ] == 0.0 and pRatedMaxStorage[g] == 0.0)
    mTEPES.es  = Set(initialize=mTEPES.g ,          ordered=False, doc='ESS             units', filter=lambda mTEPES,g       :  g      in mTEPES.g   and                                  (pRatedMaxStorage[g] >  0.0   or pRatedMaxCharge[g] > 0.0))
    mTEPES.gc  = Set(initialize=mTEPES.g ,          ordered=False, doc='candidate       units', filter=lambda mTEPES,g       :  g      in mTEPES.g   and pGenInvestCost    [g ] >  0.0)
    mTEPES.gd  = Set(initialize=mTEPES.g ,          ordered=False, doc='retirement      units', filter=lambda mTEPES,g       :  g      in mTEPES.g   and pGenRetireCost    [g ] != 0.0)
    mTEPES.ec  = Set(initialize=mTEPES.es,          ordered=False, doc='candidate   ESS units', filter=lambda mTEPES,es      :  es     in mTEPES.es  and pGenInvestCost    [es] >  0.0)
    mTEPES.br  = Set(initialize=sBrList,            ordered=False, doc='all input branches'                                                                                           )
    mTEPES.ln  = Set(initialize=dfNetwork.index,    ordered=False, doc='all input lines'                                                                                              )
    mTEPES.la  = Set(initialize=mTEPES.ln,          ordered=False, doc='all real        lines', filter=lambda mTEPES,*ln     :  ln     in mTEPES.ln  and pLineX            [ln] != 0.0 and pLineNTCFrw[ln] > 0.0 and pLineNTCBck[ln] > 0.0 and pPeriodIniNet[ln] <= mTEPES.p.last() and pPeriodFinNet[ln] >= mTEPES.p.first())
    mTEPES.ls  = Set(initialize=mTEPES.la,          ordered=False, doc='all real switch lines', filter=lambda mTEPES,*la     :  la     in mTEPES.la  and pIndBinLineSwitch [la])
    mTEPES.lc  = Set(initialize=mTEPES.la,          ordered=False, doc='candidate       lines', filter=lambda mTEPES,*la     :  la     in mTEPES.la  and pNetFixedCost     [la] >  0.0)
    mTEPES.cd  = Set(initialize=mTEPES.la,          ordered=False, doc='             DC lines', filter=lambda mTEPES,*la     :  la     in mTEPES.la  and pNetFixedCost     [la] >  0.0 and pLineType[la] == 'DC')
    mTEPES.ed  = Set(initialize=mTEPES.la,          ordered=False, doc='             DC lines', filter=lambda mTEPES,*la     :  la     in mTEPES.la  and pNetFixedCost     [la] == 0.0 and pLineType[la] == 'DC')
    mTEPES.ll  = Set(initialize=mTEPES.la,          ordered=False, doc='loss            lines', filter=lambda mTEPES,*la     :  la     in mTEPES.la  and pLineLossFactor   [la] >  0.0 and pIndBinNetLosses > 0 )
    mTEPES.rf  = Set(initialize=mTEPES.nd,          ordered=True , doc='reference node'       , filter=lambda mTEPES,nd      :  nd     in                pReferenceNode               )
    mTEPES.gq  = Set(initialize=mTEPES.gg,          ordered=False, doc='gen    reactive units', filter=lambda mTEPES,gg      :  gg     in mTEPES.gg  and pRMaxReactivePower[gg] >  0.0 and pPeriodIniGen[gg] <= mTEPES.p.last() and pPeriodFinGen[gg] >= mTEPES.p.first())
    mTEPES.sq  = Set(initialize=mTEPES.gg,          ordered=False, doc='syn    reactive units', filter=lambda mTEPES,gg      :  gg     in mTEPES.gg  and pRMaxReactivePower[gg] >  0.0 and pPeriodIniGen[gg] <= mTEPES.p.last() and pPeriodFinGen[gg] >= mTEPES.p.first() and pGenToTechnology[gg] == 'SynchronousCondenser')
    mTEPES.sqc = Set(initialize=mTEPES.sq,          ordered=False, doc='syn    reactive cand '                                                                                           )
    mTEPES.shc = Set(initialize=mTEPES.sq,          ordered=False, doc='shunt           cand '                                                                                           )

    # non-RES units, they can be committed and also contribute to the operating reserves
    mTEPES.nr = mTEPES.g - mTEPES.r

    # machines able to provide reactive power
    mTEPES.tq = mTEPES.gq - mTEPES.sq

    # existing lines (le)
    mTEPES.le = mTEPES.la - mTEPES.lc

    # instrumental sets
    mTEPES.psc   = [(p,sc     ) for p,sc      in mTEPES.p  *mTEPES.sc]
    mTEPES.psn   = [(p,sc,n   ) for p,sc,n    in mTEPES.ps *mTEPES.n ]
    mTEPES.psng  = [(p,sc,n,g ) for p,sc,n,g  in mTEPES.psn*mTEPES.g ]
    mTEPES.psngg = [(p,sc,n,gg) for p,sc,n,gg in mTEPES.psn*mTEPES.gg]
    mTEPES.psnr  = [(p,sc,n,r ) for p,sc,n,r  in mTEPES.psn*mTEPES.r ]
    mTEPES.psnnr = [(p,sc,n,nr) for p,sc,n,nr in mTEPES.psn*mTEPES.nr]
    mTEPES.psnes = [(p,sc,n,es) for p,sc,n,es in mTEPES.psn*mTEPES.es]
    mTEPES.psnec = [(p,sc,n,ec) for p,sc,n,ec in mTEPES.psn*mTEPES.ec]
    mTEPES.psnnd = [(p,sc,n,nd) for p,sc,n,nd in mTEPES.psn*mTEPES.nd]
    mTEPES.psnar = [(p,sc,n,ar) for p,sc,n,ar in mTEPES.psn*mTEPES.ar]
    mTEPES.psngt = [(p,sc,n,gt) for p,sc,n,gt in mTEPES.psn*mTEPES.gt]

    mTEPES.psnla = [(p,sc,n,ni,nf,cc) for p,sc,n,ni,nf,cc in mTEPES.psn*mTEPES.la]
    mTEPES.psnln = [(p,sc,n,ni,nf,cc) for p,sc,n,ni,nf,cc in mTEPES.psn*mTEPES.ln]
    mTEPES.psnll = [(p,sc,n,ni,nf,cc) for p,sc,n,ni,nf,cc in mTEPES.psn*mTEPES.ll]
    mTEPES.psnls = [(p,sc,n,ni,nf,cc) for p,sc,n,ni,nf,cc in mTEPES.psn*mTEPES.ls]

    mTEPES.pgc   = [(p,gc           ) for p,gc            in mTEPES.p  *mTEPES.gc]
    mTEPES.pec   = [(p,ec           ) for p,ec            in mTEPES.p  *mTEPES.ec]
    mTEPES.pgd   = [(p,gd           ) for p,gd            in mTEPES.p  *mTEPES.gd]
    mTEPES.plc   = [(p,ni,nf,cc     ) for p,ni,nf,cc      in mTEPES.p  *mTEPES.lc]

    # assigning a node to an area
    mTEPES.ndar = [(nd,ar) for (nd,zn,ar) in mTEPES.ndzn*mTEPES.ar if (zn,ar) in mTEPES.znar]

    # assigning a line to an area. Both nodes are in the same area. Cross-area lines not included
    mTEPES.laar = [(ni,nf,cc,ar) for ni,nf,cc,ar in mTEPES.la*mTEPES.ar if (ni,ar) in mTEPES.ndar and (nf,ar) in mTEPES.ndar]

    # replacing string values by numerical values
    idxDict = dict()
    idxDict[0    ] = 0
    idxDict[0.0  ] = 0
    idxDict['No' ] = 0
    idxDict['NO' ] = 0
    idxDict['no' ] = 0
    idxDict['N'  ] = 0
    idxDict['n'  ] = 0
    idxDict['Yes'] = 1
    idxDict['YES'] = 1
    idxDict['yes'] = 1
    idxDict['Y'  ] = 1
    idxDict['y'  ] = 1

    pIndBinUnitInvest = pIndBinUnitInvest.map(idxDict)
    pIndBinUnitRetire = pIndBinUnitRetire.map(idxDict)
    pIndBinUnitCommit = pIndBinUnitCommit.map(idxDict)
    pIndBinStorInvest = pIndBinStorInvest.map(idxDict)
    pIndOperReserve   = pIndOperReserve.map  (idxDict)
    pMustRun          = pMustRun.map         (idxDict)
    pIndBinLineInvest = pIndBinLineInvest.map(idxDict)
    pIndBinLineSwitch = pIndBinLineSwitch.map(idxDict)

    # define AC existing  lines     non-switchable
    mTEPES.lea = Set(initialize=mTEPES.le, ordered=False, doc='AC existing  lines and non-switchable lines', filter=lambda mTEPES,*le: le in mTEPES.le and  pIndBinLineSwitch[le] == 0                             and not pLineType[le] == 'DC')
    # define AC candidate lines and     switchable lines
    mTEPES.lca = Set(initialize=mTEPES.la, ordered=False, doc='AC candidate lines and     switchable lines', filter=lambda mTEPES,*la: la in mTEPES.la and (pIndBinLineSwitch[la] == 1 or pNetFixedCost[la] > 0.0) and not pLineType[la] == 'DC')

    mTEPES.laa = mTEPES.lea | mTEPES.lca

    # define DC existing  lines     non-switchable
    mTEPES.led = Set(initialize=mTEPES.le, ordered=False, doc='DC existing  lines and non-switchable lines', filter=lambda mTEPES,*le: le in mTEPES.le and  pIndBinLineSwitch[le] == 0                             and     pLineType[le] == 'DC')
    # define DC candidate lines and     switchable lines
    mTEPES.lcd = Set(initialize=mTEPES.la, ordered=False, doc='DC candidate lines and     switchable lines', filter=lambda mTEPES,*la: la in mTEPES.la and (pIndBinLineSwitch[la] == 1 or pNetFixedCost[la] > 0.0) and     pLineType[la] == 'DC')

    mTEPES.lad = mTEPES.led | mTEPES.lcd

    # line type
    pLineType = pLineType.reset_index().set_index(['level_0','level_1','level_2','LineType'])

    mTEPES.pLineType = Set(initialize=pLineType.index, ordered=False, doc='line type')

    #%% inverse index load level to stage
    pStageToLevel = pLevelToStage.reset_index().set_index('Stage').set_axis(['LoadLevel'], axis=1, copy=False)[['LoadLevel']]
    pStageToLevel = pStageToLevel.loc[pStageToLevel['LoadLevel'].isin(mTEPES.n)]
    pStage2Level  = pStageToLevel.reset_index().set_index(['Stage','LoadLevel'])

    mTEPES.s2n = Set(initialize=pStage2Level.index, ordered=False, doc='load level to stage')

    if pAnnualDiscRate == 0.0:
        pDiscountFactor = pd.Series([                        pPeriodWeight[p]                                                                                          for p in mTEPES.p], index=mTEPES.p)
    else:
        pDiscountFactor = pd.Series([((1.0+pAnnualDiscRate)**pPeriodWeight[p]-1.0) / (pAnnualDiscRate*(1.0+pAnnualDiscRate)**(pPeriodWeight[p]-1+p-pEconomicBaseYear)) for p in mTEPES.p], index=mTEPES.p)

    mTEPES.pLoadLevelWeight = Param(mTEPES.n, initialize=0.0, within=NonNegativeIntegers, doc='Load level weight', mutable=True)
    for st,n in mTEPES.s2n:
        mTEPES.pLoadLevelWeight[n] = pStageWeight[st]

    #%% inverse index node to generator
    pNodeToGen = pGenToNode.reset_index().set_index('Node').set_axis(['Generator'], axis=1, copy=False)[['Generator']]
    pNodeToGen = pNodeToGen.loc[pNodeToGen['Generator'].isin(mTEPES.g)]
    pNode2Gen  = pNodeToGen.reset_index().set_index(['Node', 'Generator'])

    mTEPES.n2g = Set(initialize=pNode2Gen.index, ordered=False, doc='node   to generator')

    pZone2Gen   = [(zn,g) for (nd,g,zn      ) in mTEPES.n2g*mTEPES.zn                     if (nd,zn) in mTEPES.ndzn                                                      ]
    pArea2Gen   = [(ar,g) for (nd,g,zn,ar   ) in mTEPES.n2g*mTEPES.zn*mTEPES.ar           if (nd,zn) in mTEPES.ndzn and [zn,ar] in mTEPES.znar                           ]
    pRegion2Gen = [(rg,g) for (nd,g,zn,ar,rg) in mTEPES.n2g*mTEPES.zn*mTEPES.ar*mTEPES.rg if (nd,zn) in mTEPES.ndzn and [zn,ar] in mTEPES.znar and [ar,rg] in mTEPES.arrg]

    mTEPES.z2g = Set(initialize=mTEPES.zn*mTEPES.g, ordered=False, doc='zone   to generator', filter=lambda mTEPES,zn,g: (zn,g) in pZone2Gen  )
    mTEPES.a2g = Set(initialize=mTEPES.ar*mTEPES.g, ordered=False, doc='area   to generator', filter=lambda mTEPES,ar,g: (ar,g) in pArea2Gen  )
    mTEPES.r2g = Set(initialize=mTEPES.rg*mTEPES.g, ordered=False, doc='region to generator', filter=lambda mTEPES,rg,g: (rg,g) in pRegion2Gen)

    #%% inverse index generator to technology
    pTechnologyToGen = pGenToTechnology.reset_index().set_index('Technology').set_axis(['Generator'], axis=1, copy=False)[['Generator']]
    pTechnologyToGen = pTechnologyToGen.loc[pTechnologyToGen['Generator'].isin(mTEPES.g)]
    pTechnology2Gen  = pTechnologyToGen.reset_index().set_index(['Technology', 'Generator'])

    mTEPES.t2g = Set(initialize=pTechnology2Gen.index, ordered=False, doc='technology to generator')

    # ESS and RES technologies
    mTEPES.ot = Set(initialize=mTEPES.gt, ordered=False, doc='ESS technologies', filter=lambda mTEPES,gt: gt in mTEPES.gt and sum(1 for es in mTEPES.es if (gt,es) in mTEPES.t2g))
    mTEPES.rt = Set(initialize=mTEPES.gt, ordered=False, doc='RES technologies', filter=lambda mTEPES,gt: gt in mTEPES.gt and sum(1 for r  in mTEPES.r  if (gt,r ) in mTEPES.t2g))

    mTEPES.psnot = [(p,sc,n,ot) for p,sc,n,ot in mTEPES.ps*mTEPES.n*mTEPES.ot]
    mTEPES.psnrt = [(p,sc,n,rt) for p,sc,n,rt in mTEPES.ps*mTEPES.n*mTEPES.rt]

    #%% inverse index generator to mutually exclusive generator
    pExclusiveGenToGen = pGenToExclusiveGen.reset_index().set_index('MutuallyExclusive').set_axis(['Generator'], axis=1, copy=False)[['Generator']]
    pExclusiveGenToGen = pExclusiveGenToGen.loc[pExclusiveGenToGen['Generator'].isin(mTEPES.g)]
    pExclusiveGen2Gen  = pExclusiveGenToGen.reset_index().set_index(['MutuallyExclusive', 'Generator'])

    mTEPES.g2g = Set(initialize=pExclusiveGen2Gen.index, ordered=False, doc='mutually exclusive generator to generator', filter=lambda mTEPES,gg,g: (gg,g) in mTEPES.gg*mTEPES.g)

    # minimum and maximum variable power
    pVariableMinPower   = pVariableMinPower.replace(0.0, float('nan'))
    pVariableMaxPower   = pVariableMaxPower.replace(0.0, float('nan'))
    pMinPower           = pd.DataFrame([pRatedMinPower]*len(pVariableMinPower.index), index=pd.Index(pVariableMinPower.index), columns=pRatedMinPower.index)
    pMaxPower           = pd.DataFrame([pRatedMaxPower]*len(pVariableMaxPower.index), index=pd.Index(pVariableMaxPower.index), columns=pRatedMaxPower.index)
    pMinPower           = pMinPower.reindex        (sorted(pMinPower.columns        ), axis=1)
    pMaxPower           = pMaxPower.reindex        (sorted(pMaxPower.columns        ), axis=1)
    pVariableMinPower   = pVariableMinPower.reindex(sorted(pVariableMinPower.columns), axis=1)
    pVariableMaxPower   = pVariableMaxPower.reindex(sorted(pVariableMaxPower.columns), axis=1)
    pMinPower           = pVariableMinPower.where         (pVariableMinPower > pMinPower, other=pMinPower)
    pMaxPower           = pVariableMaxPower.where         (pVariableMaxPower < pMaxPower, other=pMaxPower)
    pMinPower           = pMinPower.where                 (pMinPower         > 0.0,       other=0.0)
    pMaxPower           = pMaxPower.where                 (pMaxPower         > 0.0,       other=0.0)

    # minimum and maximum variable charge
    pVariableMinCharge  = pVariableMinCharge.replace(0.0, float('nan'))
    pVariableMaxCharge  = pVariableMaxCharge.replace(0.0, float('nan'))
    pMinCharge          = pd.DataFrame([pRatedMinCharge]*len(pVariableMinCharge.index), index=pd.Index(pVariableMinCharge.index), columns=pRatedMinCharge.index)
    pMaxCharge          = pd.DataFrame([pRatedMaxCharge]*len(pVariableMaxCharge.index), index=pd.Index(pVariableMaxCharge.index), columns=pRatedMaxCharge.index)
    pMinCharge          = pMinCharge.reindex        (sorted(pMinCharge.columns        ), axis=1)
    pMaxCharge          = pMaxCharge.reindex        (sorted(pMaxCharge.columns        ), axis=1)
    pVariableMinCharge  = pVariableMinCharge.reindex(sorted(pVariableMinCharge.columns), axis=1)
    pVariableMaxCharge  = pVariableMaxCharge.reindex(sorted(pVariableMaxCharge.columns), axis=1)
    pMinCharge          = pVariableMinCharge.where         (pVariableMinCharge > pMinCharge, other=pMinCharge)
    pMaxCharge          = pVariableMaxCharge.where         (pVariableMaxCharge < pMaxCharge, other=pMaxCharge)
    pMinCharge          = pMinCharge.where                 (pMinCharge         > 0.0,        other=0.0)
    pMaxCharge          = pMaxCharge.where                 (pMaxCharge         > 0.0,        other=0.0)

    # minimum and maximum variable storage capacity
    pVariableMinStorage = pVariableMinStorage.replace(0.0, float('nan'))
    pVariableMaxStorage = pVariableMaxStorage.replace(0.0, float('nan'))
    pMinStorage         = pd.DataFrame([pRatedMinStorage]*len(pVariableMinStorage.index), index=pd.Index(pVariableMinStorage.index), columns=pRatedMinStorage.index)
    pMaxStorage         = pd.DataFrame([pRatedMaxStorage]*len(pVariableMaxStorage.index), index=pd.Index(pVariableMaxStorage.index), columns=pRatedMaxStorage.index)
    pMinStorage         = pMinStorage.reindex        (sorted(pMinStorage.columns        ), axis=1)
    pMaxStorage         = pMaxStorage.reindex        (sorted(pMaxStorage.columns        ), axis=1)
    pVariableMinStorage = pVariableMinStorage.reindex(sorted(pVariableMinStorage.columns), axis=1)
    pVariableMaxStorage = pVariableMaxStorage.reindex(sorted(pVariableMaxStorage.columns), axis=1)
    pMinStorage         = pVariableMinStorage.where         (pVariableMinStorage > pMinStorage, other=pMinStorage)
    pMaxStorage         = pVariableMaxStorage.where         (pVariableMaxStorage < pMaxStorage, other=pMaxStorage)
    pMinStorage         = pMinStorage.where                 (pMinStorage         > 0.0,         other=0.0)
    pMaxStorage         = pMaxStorage.where                 (pMaxStorage         > 0.0,         other=0.0)

    # parameter that allows the initial inventory to change with load level
    pIniInventory       = pd.DataFrame([pInitialInventory]*len(pVariableMinStorage.index), index=pd.Index(pVariableMinStorage.index), columns=pInitialInventory.index)
    # initial inventory must be between minimum and maximum
    # pIniInventory       = pMinStorage.where(pMinStorage > pIniInventory, other=pIniInventory)
    # pIniInventory       = pMaxStorage.where(pMaxStorage < pIniInventory, other=pIniInventory)

    # minimum up and down time and maximum shift time converted to an integer number of time steps
    pUpTime    = round(pUpTime   /pTimeStep).astype('int')
    pDwTime    = round(pDwTime   /pTimeStep).astype('int')
    pShiftTime = round(pShiftTime/pTimeStep).astype('int')

    # %% definition of the time-steps leap to observe the stored energy at an ESS
    idxCycle            = dict()
    idxCycle[0        ] = 8736
    idxCycle[0.0      ] = 8736
    idxCycle["Hourly" ] = 1
    idxCycle["Daily"  ] = 1
    idxCycle["Weekly" ] = round(  24/pTimeStep)
    idxCycle["Monthly"] = round( 168/pTimeStep)
    idxCycle["Yearly" ] = round( 168/pTimeStep)

    idxOutflows            = dict()
    idxOutflows[0        ] = 8736
    idxOutflows[0.0      ] = 8736
    idxOutflows["Daily"  ] = round(  24/pTimeStep)
    idxOutflows["Weekly" ] = round( 168/pTimeStep)
    idxOutflows["Monthly"] = round( 672/pTimeStep)
    idxOutflows["Yearly" ] = round(8736/pTimeStep)

    idxEnergy            = dict()
    idxEnergy[0        ] = 8736
    idxEnergy[0.0      ] = 8736
    idxEnergy["Daily"  ] = round(  24/pTimeStep)
    idxEnergy["Weekly" ] = round( 168/pTimeStep)
    idxEnergy["Monthly"] = round( 672/pTimeStep)
    idxEnergy["Yearly" ] = round(8736/pTimeStep)

    pCycleTimeStep    = pStorageType.map (idxCycle                                                                                  ).astype('int')
    pOutflowsTimeStep = pOutflowsType.map(idxOutflows).where(pEnergyOutflows.sum()                               > 0.0, other = 8736).astype('int')
    pEnergyTimeStep   = pEnergyType.map  (idxEnergy  ).where(pVariableMinEnergy.sum() + pVariableMaxEnergy.sum() > 0.0, other = 8736).astype('int')

    pCycleTimeStep    = pd.concat([pCycleTimeStep, pOutflowsTimeStep, pEnergyTimeStep], axis=1).min(axis=1)

    # drop load levels with duration 0
    pDuration          = pDuration.loc         [mTEPES.n    ]
    pDemand            = pDemand.loc           [mTEPES.psn  ]
    pSystemInertia     = pSystemInertia.loc    [mTEPES.psnar]
    pOperReserveUp     = pOperReserveUp.loc    [mTEPES.psnar]
    pOperReserveDw     = pOperReserveDw.loc    [mTEPES.psnar]
    pMinPower          = pMinPower.loc         [mTEPES.psn  ]
    pMaxPower          = pMaxPower.loc         [mTEPES.psn  ]
    pMinCharge         = pMinCharge.loc        [mTEPES.psn  ]
    pMaxCharge         = pMaxCharge.loc        [mTEPES.psn  ]
    pEnergyInflows     = pEnergyInflows.loc    [mTEPES.psn  ]
    pEnergyOutflows    = pEnergyOutflows.loc   [mTEPES.psn  ]
    pMinStorage        = pMinStorage.loc       [mTEPES.psn  ]
    pMaxStorage        = pMaxStorage.loc       [mTEPES.psn  ]
    pVariableMaxEnergy = pVariableMaxEnergy.loc[mTEPES.psn  ]
    pVariableMinEnergy = pVariableMinEnergy.loc[mTEPES.psn  ]
    pIniInventory      = pIniInventory.loc     [mTEPES.psn  ]

    # separate positive and negative demands to avoid converting negative values to 0
    pDemandPos        = pDemand.where        (pDemand >= 0.0, other=0.0)
    pDemandNeg        = pDemand.where        (pDemand <  0.0, other=0.0)

    # small values are converted to 0
    pPeakDemand         = pd.Series([0.0 for ar in mTEPES.ar], index=mTEPES.ar)
    for ar in mTEPES.ar:
        # values < 1e-5 times the maximum demand for each area (an area is related to operating reserves procurement, i.e., country) are converted to 0
        pPeakDemand[ar] = pDemand      [[nd for nd in mTEPES.nd if (nd,ar) in mTEPES.ndar]].sum(axis=1).max()
        pEpsilon        = pPeakDemand[ar]*2.5e-5
        # values < 1e-5 times the maximum system demand are converted to 0
        # pEpsilon      = pDemand.sum(axis=1).max()*1e-5

        # these parameters are in GW
        pDemandPos     [pDemandPos     [[nd for nd in mTEPES.nd if (nd,ar) in mTEPES.ndar]] <  pEpsilon] = 0.0
        pDemandNeg     [pDemandNeg     [[nd for nd in mTEPES.nd if (nd,ar) in mTEPES.ndar]] > -pEpsilon] = 0.0
        pSystemInertia [pSystemInertia [[                                              ar]] <  pEpsilon] = 0.0
        pOperReserveUp [pOperReserveUp [[                                              ar]] <  pEpsilon] = 0.0
        pOperReserveDw [pOperReserveDw [[                                              ar]] <  pEpsilon] = 0.0
        pMinPower      [pMinPower      [[g  for  g in mTEPES.g  if (ar,g)  in mTEPES.a2g ]] <  pEpsilon] = 0.0
        pMaxPower      [pMaxPower      [[g  for  g in mTEPES.g  if (ar,g)  in mTEPES.a2g ]] <  pEpsilon] = 0.0
        pMinCharge     [pMinCharge     [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon] = 0.0
        pMaxCharge     [pMaxCharge     [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon] = 0.0
        pEnergyInflows [pEnergyInflows [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon/pTimeStep] = 0.0
        pEnergyOutflows[pEnergyOutflows[[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon/pTimeStep] = 0.0

        # these parameters are in GWh
        pMinStorage    [pMinStorage    [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon] = 0.0
        pMaxStorage    [pMaxStorage    [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon] = 0.0
        pIniInventory  [pIniInventory  [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g ]] <  pEpsilon] = 0.0

        pInitialInventory.update(pd.Series([0 for es in mTEPES.es if (ar,es) in mTEPES.a2g and pInitialInventory[es] < pEpsilon], index=[es for es in mTEPES.es if (ar,es) in mTEPES.a2g and pInitialInventory[es] < pEpsilon], dtype='float64'))

        pLineNTCFrw.update(pd.Series([0.0 for ni,nf,cc in mTEPES.la if pLineNTCFrw[ni,nf,cc] < pEpsilon], index=[(ni,nf,cc) for ni,nf,cc in mTEPES.la if pLineNTCFrw[ni,nf,cc] < pEpsilon], dtype='float64'))
        pLineNTCBck.update(pd.Series([0.0 for ni,nf,cc in mTEPES.la if pLineNTCBck[ni,nf,cc] < pEpsilon], index=[(ni,nf,cc) for ni,nf,cc in mTEPES.la if pLineNTCBck[ni,nf,cc] < pEpsilon], dtype='float64'))

        # merging positive and negative values of the demand
        pDemand            = pDemandPos.where(pDemandNeg >= 0.0, other=pDemandNeg)

        pMaxPower2ndBlock  = pMaxPower  - pMinPower
        pMaxCharge2ndBlock = pMaxCharge - pMinCharge

        pMaxPower2ndBlock [pMaxPower2ndBlock [[es for es in mTEPES.es if (ar,es) in mTEPES.a2g]] < pEpsilon] = 0.0
        pMaxCharge2ndBlock[pMaxCharge2ndBlock[[es for es in mTEPES.es if (ar,es) in mTEPES.a2g]] < pEpsilon] = 0.0

    # replace very small costs by 0
    pEpsilon = 1e-4           # this value in €/GWh is related to the smallest reduced cost, independent of the area
    pLinearOperCost.update (pd.Series([0 for gg in mTEPES.gg if pLinearOperCost [gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pLinearOperCost [gg] < pEpsilon]))
    pLinearVarCost.update  (pd.Series([0 for gg in mTEPES.gg if pLinearVarCost  [gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pLinearVarCost  [gg] < pEpsilon]))
    pLinearOMCost.update   (pd.Series([0 for gg in mTEPES.gg if pLinearOMCost   [gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pLinearOMCost   [gg] < pEpsilon]))
    pConstantVarCost.update(pd.Series([0 for gg in mTEPES.gg if pConstantVarCost[gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pConstantVarCost[gg] < pEpsilon]))
    pOperReserveCost.update(pd.Series([0 for gg in mTEPES.gg if pOperReserveCost[gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pOperReserveCost[gg] < pEpsilon]))
    pCO2EmissionCost.update(pd.Series([0 for gg in mTEPES.gg if pCO2EmissionCost[gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pCO2EmissionCost[gg] < pEpsilon]))
    pStartUpCost.update    (pd.Series([0 for gg in mTEPES.gg if pStartUpCost    [gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pStartUpCost    [gg] < pEpsilon]))
    pShutDownCost.update   (pd.Series([0 for gg in mTEPES.gg if pShutDownCost   [gg] < pEpsilon], index=[gg for gg in mTEPES.gg if pShutDownCost   [gg] < pEpsilon]))

    # replace < 0.0 by 0.0
    pMaxPower2ndBlock  = pMaxPower2ndBlock.where (pMaxPower2ndBlock  > 0.0, other=0.0)
    pMaxCharge2ndBlock = pMaxCharge2ndBlock.where(pMaxCharge2ndBlock > 0.0, other=0.0)

    # BigM maximum flow to be used in the Kirchhoff's 2nd law disjunctive constraint
    pBigMFlowBck = pLineNTCBck*0.0
    pBigMFlowFrw = pLineNTCFrw*0.0
    for lea in mTEPES.lea:
        pBigMFlowBck.loc[lea] = pLineNTCBck[lea]
        pBigMFlowFrw.loc[lea] = pLineNTCFrw[lea]
    for lca in mTEPES.lca:
        pBigMFlowBck.loc[lca] = pLineNTCBck[lca]*1.5
        pBigMFlowFrw.loc[lca] = pLineNTCFrw[lca]*1.5
    for led in mTEPES.led:
        pBigMFlowBck.loc[led] = pLineNTCBck[led]
        pBigMFlowFrw.loc[led] = pLineNTCFrw[led]
    for lcd in mTEPES.lcd:
        pBigMFlowBck.loc[lcd] = pLineNTCBck[lcd]*1.5
        pBigMFlowFrw.loc[lcd] = pLineNTCFrw[lcd]*1.5

    # if BigM are 0.0 then converted to 1.0 to avoid division by 0.0
    pBigMFlowBck = pBigMFlowBck.where(pBigMFlowBck != 0.0, other=1.0)
    pBigMFlowFrw = pBigMFlowFrw.where(pBigMFlowFrw != 0.0, other=1.0)

    # maximum voltage angle
    pMaxTheta = pDemand*0.0 + math.pi/2
    pMaxTheta = pMaxTheta.loc[mTEPES.psn]

    # this option avoids a warning in the following assignments
    pd.options.mode.chained_assignment = None

    # %% parameters
    mTEPES.pIndBinGenInvest      = Param(initialize=pIndBinGenInvest     , within=NonNegativeIntegers, doc='Indicator of binary generation investment decisions', mutable=True)
    mTEPES.pIndBinGenRetire      = Param(initialize=pIndBinGenRetire     , within=NonNegativeIntegers, doc='Indicator of binary generation retirement decisions', mutable=True)
    mTEPES.pIndBinGenOperat      = Param(initialize=pIndBinGenOperat     , within=Boolean,             doc='Indicator of binary generation operation  decisions', mutable=True)
    mTEPES.pIndBinSingleNode     = Param(initialize=pIndBinSingleNode    , within=Boolean,             doc='Indicator of single node within a network case',      mutable=True)
    mTEPES.pIndBinGenRamps       = Param(initialize=pIndBinGenRamps      , within=Boolean,             doc='Indicator of using or not the ramp constraints',      mutable=True)
    mTEPES.pIndBinGenMinTime     = Param(initialize=pIndBinGenMinTime    , within=Boolean,             doc='Indicator of using or not the min time constraints',  mutable=True)
    mTEPES.pIndBinNetInvest      = Param(initialize=pIndBinNetInvest     , within=NonNegativeIntegers, doc='Indicator of binary network    investment decisions', mutable=True)
    mTEPES.pIndBinLineCommit     = Param(initialize=pIndBinLineCommit    , within=Boolean,             doc='Indicator of binary network    switching  decisions', mutable=True)
    mTEPES.pIndBinNetLosses      = Param(initialize=pIndBinNetLosses     , within=Boolean,             doc='Indicator of binary network ohmic losses',            mutable=True)

    mTEPES.pENSCost              = Param(initialize=pENSCost             , within=NonNegativeReals,    doc='ENS cost'                                          )
    mTEPES.pCO2Cost              = Param(initialize=pCO2Cost             , within=NonNegativeReals,    doc='CO2 emission cost'                                 )
    mTEPES.pAnnualDiscRate       = Param(initialize=pAnnualDiscRate      , within=UnitInterval    ,    doc='Annual discount rate'                              )
    mTEPES.pUpReserveActivation  = Param(initialize=pUpReserveActivation , within=UnitInterval    ,    doc='Proportion of upward   reserve activation'         )
    mTEPES.pDwReserveActivation  = Param(initialize=pDwReserveActivation , within=UnitInterval    ,    doc='Proportion of downward reserve activation'         )
    mTEPES.pMinRatioDwUp         = Param(initialize=pMinRatioDwUp        , within=UnitInterval    ,    doc='Minimum ration between upward and downward reserve')
    mTEPES.pMaxRatioDwUp         = Param(initialize=pMaxRatioDwUp        , within=UnitInterval    ,    doc='Maximum ration between upward and downward reserve')
    mTEPES.pSBase                = Param(initialize=pSBase               , within=PositiveReals   ,    doc='Base power'                                        )
    mTEPES.pTimeStep             = Param(initialize=pTimeStep            , within=PositiveIntegers,    doc='Unitary time step'                                 )
    mTEPES.pEconomicBaseYear     = Param(initialize=pEconomicBaseYear    , within=PositiveIntegers,    doc='Base year'                                         )

    mTEPES.pReserveMargin        = Param(mTEPES.ar,    initialize=pReserveMargin.to_dict()            , within=NonNegativeReals,    doc='Adequacy reserve margin'                             )
    mTEPES.pPeakDemand           = Param(mTEPES.ar,    initialize=pPeakDemand.to_dict()               , within=NonNegativeReals,    doc='Peak demand'                                         )
    mTEPES.pDemand               = Param(mTEPES.psnnd, initialize=pDemand.stack().to_dict()           , within=           Reals,    doc='Demand'                                              )
    mTEPES.pPeriodWeight         = Param(mTEPES.p,     initialize=pPeriodWeight.to_dict()             , within=NonNegativeIntegers, doc='Period weight'                                       )
    mTEPES.pDiscountFactor       = Param(mTEPES.p,     initialize=pDiscountFactor.to_dict()           , within=NonNegativeReals,    doc='Discount factor'                                     )
    mTEPES.pScenProb             = Param(mTEPES.psc,   initialize=pScenProb.to_dict()                 , within=UnitInterval    ,    doc='Probability'                                         )
    mTEPES.pStageWeight          = Param(mTEPES.stt,   initialize=pStageWeight.to_dict()              , within=NonNegativeIntegers, doc='Stage weight'                                        )
    mTEPES.pDuration             = Param(mTEPES.n,     initialize=pDuration.to_dict()                 , within=PositiveIntegers,    doc='Duration',                               mutable=True)
    mTEPES.pNodeLon              = Param(mTEPES.nd,    initialize=pNodeLon.to_dict()                  ,                             doc='Longitude'                                           )
    mTEPES.pNodeLat              = Param(mTEPES.nd,    initialize=pNodeLat.to_dict()                  ,                             doc='Latitude'                                            )
    mTEPES.pSystemInertia        = Param(mTEPES.psnar, initialize=pSystemInertia.stack().to_dict()    , within=NonNegativeReals,    doc='System inertia'                                      )
    mTEPES.pOperReserveUp        = Param(mTEPES.psnar, initialize=pOperReserveUp.stack().to_dict()    , within=NonNegativeReals,    doc='Upward   operating reserve'                          )
    mTEPES.pOperReserveDw        = Param(mTEPES.psnar, initialize=pOperReserveDw.stack().to_dict()    , within=NonNegativeReals,    doc='Downward operating reserve'                          )
    mTEPES.pMinPower             = Param(mTEPES.psngg, initialize=pMinPower.stack().to_dict()         , within=NonNegativeReals,    doc='Minimum power'                                       )
    mTEPES.pMaxPower             = Param(mTEPES.psngg, initialize=pMaxPower.stack().to_dict()         , within=NonNegativeReals,    doc='Maximum power'                                       )
    mTEPES.pMinCharge            = Param(mTEPES.psngg, initialize=pMinCharge.stack().to_dict()        , within=NonNegativeReals,    doc='Minimum charge'                                      )
    mTEPES.pMaxCharge            = Param(mTEPES.psngg, initialize=pMaxCharge.stack().to_dict()        , within=NonNegativeReals,    doc='Maximum charge'                                      )
    mTEPES.pMaxPower2ndBlock     = Param(mTEPES.psngg, initialize=pMaxPower2ndBlock.stack().to_dict() , within=NonNegativeReals,    doc='Second block power'                                  )
    mTEPES.pMaxCharge2ndBlock    = Param(mTEPES.psngg, initialize=pMaxCharge2ndBlock.stack().to_dict(), within=NonNegativeReals,    doc='Second block charge'                                 )
    mTEPES.pEnergyInflows        = Param(mTEPES.psngg, initialize=pEnergyInflows.stack().to_dict()    , within=NonNegativeReals,    doc='Energy inflows',                         mutable=True)
    mTEPES.pEnergyOutflows       = Param(mTEPES.psngg, initialize=pEnergyOutflows.stack().to_dict()   , within=NonNegativeReals,    doc='Energy outflows',                        mutable=True)
    mTEPES.pMinStorage           = Param(mTEPES.psngg, initialize=pMinStorage.stack().to_dict()       , within=NonNegativeReals,    doc='ESS Minimum storage capacity'                        )
    mTEPES.pMaxStorage           = Param(mTEPES.psngg, initialize=pMaxStorage.stack().to_dict()       , within=NonNegativeReals,    doc='ESS Maximum storage capacity'                        )
    mTEPES.pMinEnergy            = Param(mTEPES.psngg, initialize=pVariableMinEnergy.stack().to_dict(), within=NonNegativeReals,    doc='Unit minimum energy demand'                          )
    mTEPES.pMaxEnergy            = Param(mTEPES.psngg, initialize=pVariableMaxEnergy.stack().to_dict(), within=NonNegativeReals,    doc='Unit maximum energy demand'                          )
    mTEPES.pRatedMaxPower        = Param(mTEPES.gg,    initialize=pRatedMaxPower.to_dict()            , within=NonNegativeReals,    doc='Rated maximum power'                                 )
    mTEPES.pRatedMaxCharge       = Param(mTEPES.gg,    initialize=pRatedMaxCharge.to_dict()           , within=NonNegativeReals,    doc='Rated maximum charge'                                )
    mTEPES.pMustRun              = Param(mTEPES.gg,    initialize=pMustRun.to_dict()                  , within=Boolean         ,    doc='must-run unit'                                       )
    mTEPES.pInertia              = Param(mTEPES.gg,    initialize=pInertia.to_dict()                  , within=NonNegativeReals,    doc='unit inertia constant'                               )
    mTEPES.pPeriodIniGen         = Param(mTEPES.gg,    initialize=pPeriodIniGen.to_dict()             , within=PositiveIntegers,    doc='installation year',                                  )
    mTEPES.pPeriodFinGen         = Param(mTEPES.gg,    initialize=pPeriodFinGen.to_dict()             , within=PositiveIntegers,    doc='retirement   year',                                  )
    mTEPES.pAvailability         = Param(mTEPES.gg,    initialize=pAvailability.to_dict()             , within=UnitInterval    ,    doc='unit availability',                      mutable=True)
    mTEPES.pEFOR                 = Param(mTEPES.gg,    initialize=pEFOR.to_dict()                     , within=UnitInterval    ,    doc='EFOR'                                                )
    mTEPES.pLinearOperCost       = Param(mTEPES.gg,    initialize=pLinearOperCost.to_dict()           , within=NonNegativeReals,    doc='Linear   variable cost'                              )
    mTEPES.pLinearVarCost        = Param(mTEPES.gg,    initialize=pLinearVarCost.to_dict()            , within=NonNegativeReals,    doc='Linear   variable cost'                              )
    mTEPES.pLinearOMCost         = Param(mTEPES.gg,    initialize=pLinearOMCost.to_dict()             , within=NonNegativeReals,    doc='Linear   O&M      cost'                              )
    mTEPES.pConstantVarCost      = Param(mTEPES.gg,    initialize=pConstantVarCost.to_dict()          , within=NonNegativeReals,    doc='Constant variable cost'                              )
    mTEPES.pOperReserveCost      = Param(mTEPES.gg,    initialize=pOperReserveCost.to_dict()          , within=NonNegativeReals,    doc='Operating reserve cost'                              )
    mTEPES.pCO2EmissionCost      = Param(mTEPES.gg,    initialize=pCO2EmissionCost.to_dict()          , within=NonNegativeReals,    doc='CO2 Emission      cost'                              )
    mTEPES.pCO2EmissionRate      = Param(mTEPES.gg,    initialize=pCO2EmissionRate.to_dict()          , within=NonNegativeReals,    doc='CO2 Emission      rate'                              )
    mTEPES.pStartUpCost          = Param(mTEPES.gg,    initialize=pStartUpCost.to_dict()              , within=NonNegativeReals,    doc='Startup  cost'                                       )
    mTEPES.pShutDownCost         = Param(mTEPES.gg,    initialize=pShutDownCost.to_dict()             , within=NonNegativeReals,    doc='Shutdown cost'                                       )
    mTEPES.pRampUp               = Param(mTEPES.gg,    initialize=pRampUp.to_dict()                   , within=NonNegativeReals,    doc='Ramp up   rate'                                      )
    mTEPES.pRampDw               = Param(mTEPES.gg,    initialize=pRampDw.to_dict()                   , within=NonNegativeReals,    doc='Ramp down rate'                                      )
    mTEPES.pUpTime               = Param(mTEPES.gg,    initialize=pUpTime.to_dict()                   , within=NonNegativeIntegers, doc='Up    time'                                          )
    mTEPES.pDwTime               = Param(mTEPES.gg,    initialize=pDwTime.to_dict()                   , within=NonNegativeIntegers, doc='Down  time'                                          )
    mTEPES.pShiftTime            = Param(mTEPES.gg,    initialize=pShiftTime.to_dict()                , within=NonNegativeIntegers, doc='Shift time'                                          )
    mTEPES.pGenInvestCost        = Param(mTEPES.gg,    initialize=pGenInvestCost.to_dict()            , within=NonNegativeReals,    doc='Generation fixed cost'                               )
    mTEPES.pGenRetireCost        = Param(mTEPES.gg,    initialize=pGenRetireCost.to_dict()            , within=Reals           ,    doc='Generation fixed retire cost'                        )
    mTEPES.pIndBinUnitInvest     = Param(mTEPES.gg,    initialize=pIndBinUnitInvest.to_dict()         , within=Boolean         ,    doc='Binary investment decision'                          )
    mTEPES.pIndBinUnitRetire     = Param(mTEPES.gg,    initialize=pIndBinUnitRetire.to_dict()         , within=Boolean         ,    doc='Binary retirement decision'                          )
    mTEPES.pIndBinUnitCommit     = Param(mTEPES.gg,    initialize=pIndBinUnitCommit.to_dict()         , within=Boolean         ,    doc='Binary commitment decision'                          )
    mTEPES.pIndBinStorInvest     = Param(mTEPES.gg,    initialize=pIndBinStorInvest.to_dict()         , within=Boolean         ,    doc='Storage linked to generation investment'             )
    mTEPES.pIndOperReserve       = Param(mTEPES.gg,    initialize=pIndOperReserve.to_dict()           , within=Boolean         ,    doc='Indicator of operating reserve'                      )
    mTEPES.pEfficiency           = Param(mTEPES.gg,    initialize=pEfficiency.to_dict()               , within=UnitInterval    ,    doc='Round-trip efficiency'                               )
    mTEPES.pCycleTimeStep        = Param(mTEPES.gg,    initialize=pCycleTimeStep.to_dict()            , within=PositiveIntegers,    doc='ESS Storage cycle'                                   )
    mTEPES.pOutflowsTimeStep     = Param(mTEPES.gg,    initialize=pOutflowsTimeStep.to_dict()         , within=PositiveIntegers,    doc='ESS Outflows cycle'                                  )
    mTEPES.pEnergyTimeStep       = Param(mTEPES.gg,    initialize=pEnergyTimeStep.to_dict()           , within=PositiveIntegers,    doc='Unit energy cycle'                                   )
    mTEPES.pIniInventory         = Param(mTEPES.psngg, initialize=pIniInventory.stack().to_dict()     , within=NonNegativeReals,    doc='ESS Initial storage',                    mutable=True)
    mTEPES.pInitialInventory     = Param(mTEPES.gg,    initialize=pInitialInventory.to_dict()         , within=NonNegativeReals,    doc='ESS Initial storage without load levels'             )
    mTEPES.pStorageType          = Param(mTEPES.gg,    initialize=pStorageType.to_dict()              , within=Any             ,    doc='ESS Storage type'                                    )
    mTEPES.pGenLoInvest          = Param(mTEPES.gg,    initialize=pGenLoInvest.to_dict()              , within=NonNegativeReals,    doc='Lower bound of the investment decision', mutable=True)
    mTEPES.pGenUpInvest          = Param(mTEPES.gg,    initialize=pGenUpInvest.to_dict()              , within=NonNegativeReals,    doc='Upper bound of the investment decision', mutable=True)
    mTEPES.pGenLoRetire          = Param(mTEPES.gg,    initialize=pGenLoRetire.to_dict()              , within=NonNegativeReals,    doc='Lower bound of the retirement decision', mutable=True)
    mTEPES.pGenUpRetire          = Param(mTEPES.gg,    initialize=pGenUpRetire.to_dict()              , within=NonNegativeReals,    doc='Upper bound of the retirement decision', mutable=True)

    mTEPES.pLoadLevelDuration    = Param(mTEPES.n,     initialize=0                                   , within=NonNegativeIntegers, doc='Load level duration',                    mutable=True)
    for n in mTEPES.n:
        mTEPES.pLoadLevelDuration[n] = mTEPES.pLoadLevelWeight[n] * mTEPES.pDuration[n]

    mTEPES.pPeriodProb           = Param(mTEPES.ps,    initialize=0.0                                 , within=NonNegativeReals,    doc='Period probability',                     mutable=True)
    for p,sc in mTEPES.ps:
        mTEPES.pPeriodProb[p,sc] = mTEPES.pPeriodWeight[p] * mTEPES.pScenProb[p,sc]

    mTEPES.pLineLossFactor       = Param(mTEPES.ln,    initialize=pLineLossFactor.to_dict()           , within=           Reals,    doc='Loss factor'                                         )
    mTEPES.pLineR                = Param(mTEPES.ln,    initialize=pLineR.to_dict()                    , within=NonNegativeReals,    doc='Resistance'                                          )
    mTEPES.pLineX                = Param(mTEPES.ln,    initialize=pLineX.to_dict()                    , within=           Reals,    doc='Reactance'                                           )
    mTEPES.pLineBsh              = Param(mTEPES.ln,    initialize=pLineBsh.to_dict()                  , within=NonNegativeReals,    doc='Susceptance',                            mutable=True)
    mTEPES.pLineTAP              = Param(mTEPES.ln,    initialize=pLineTAP.to_dict()                  , within=NonNegativeReals,    doc='Tap changer',                            mutable=True)
    mTEPES.pLineLength           = Param(mTEPES.ln,    initialize=pLineLength.to_dict()               , within=NonNegativeReals,    doc='Length',                                 mutable=True)
    mTEPES.pPeriodIniNet         = Param(mTEPES.ln,    initialize=pPeriodIniNet.to_dict()             , within=PositiveIntegers,    doc='Installation period'                                 )
    mTEPES.pPeriodFinNet         = Param(mTEPES.ln,    initialize=pPeriodFinNet.to_dict()             , within=PositiveIntegers,    doc='Retirement   period'                                 )
    mTEPES.pLineVoltage          = Param(mTEPES.ln,    initialize=pLineVoltage.to_dict()              , within=NonNegativeReals,    doc='Voltage'                                             )
    mTEPES.pLineNTCFrw           = Param(mTEPES.ln,    initialize=pLineNTCFrw.to_dict()               , within=NonNegativeReals,    doc='NTC forward'                                         )
    mTEPES.pLineNTCBck           = Param(mTEPES.ln,    initialize=pLineNTCBck.to_dict()               , within=NonNegativeReals,    doc='NTC backward'                                        )
    mTEPES.pNetFixedCost         = Param(mTEPES.ln,    initialize=pNetFixedCost.to_dict()             , within=NonNegativeReals,    doc='Network fixed cost'                                  )
    mTEPES.pIndBinLineInvest     = Param(mTEPES.ln,    initialize=pIndBinLineInvest.to_dict()         , within=Boolean         ,    doc='Binary investment decision'                          )
    mTEPES.pIndBinLineSwitch     = Param(mTEPES.ln,    initialize=pIndBinLineSwitch.to_dict()         , within=Boolean         ,    doc='Binary switching  decision'                          )
    mTEPES.pSwOnTime             = Param(mTEPES.ln,    initialize=pSwitchOnTime.to_dict()             , within=NonNegativeIntegers, doc='Minimum switching on  time'                          )
    mTEPES.pSwOffTime            = Param(mTEPES.ln,    initialize=pSwitchOffTime.to_dict()            , within=NonNegativeIntegers, doc='Minimum switching off time'                          )
    mTEPES.pBigMFlowBck          = Param(mTEPES.ln,    initialize=pBigMFlowBck.to_dict()              , within=NonNegativeReals,    doc='Maximum backward capacity',              mutable=True)
    mTEPES.pBigMFlowFrw          = Param(mTEPES.ln,    initialize=pBigMFlowFrw.to_dict()              , within=NonNegativeReals,    doc='Maximum forward  capacity',              mutable=True)
    mTEPES.pMaxTheta             = Param(mTEPES.psnnd, initialize=pMaxTheta.stack().to_dict()         , within=NonNegativeReals,    doc='Maximum voltage angle',                  mutable=True)
    mTEPES.pAngMin               = Param(mTEPES.ln,    initialize=pAngMin.to_dict()                   , within=Reals,               doc='Minimum phase angle diff',               mutable=True)
    mTEPES.pAngMax               = Param(mTEPES.ln,    initialize=pAngMax.to_dict()                   , within=Reals,               doc='Maximum phase angle diff',               mutable=True)
    mTEPES.pNetLoInvest          = Param(mTEPES.ln,    initialize=pNetLoInvest.to_dict()              , within=NonNegativeReals,    doc='Lower bound of the investment decision', mutable=True)
    mTEPES.pNetUpInvest          = Param(mTEPES.ln,    initialize=pNetUpInvest.to_dict()              , within=NonNegativeReals,    doc='Upper bound of the investment decision', mutable=True)

    # if unit availability = 0 changed to 1
    for g in mTEPES.g:
        if  mTEPES.pAvailability[g]() == 0.0:
            mTEPES.pAvailability[g]   =  1.0

    # if line length = 0 changed to geographical distance with an additional 10%
    for ni,nf,cc in mTEPES.la:
        if  mTEPES.pLineLength[ni,nf,cc]() == 0.0:
            mTEPES.pLineLength[ni,nf,cc]   =  1.1 * 6371 * 2 * math.asin(math.sqrt(math.pow(math.sin((mTEPES.pNodeLat[nf]-mTEPES.pNodeLat[ni])*math.pi/180/2),2) + math.cos(mTEPES.pNodeLat[ni]*math.pi/180)*math.cos(mTEPES.pNodeLat[nf]*math.pi/180)*math.pow(math.sin((mTEPES.pNodeLon[nf]-mTEPES.pNodeLon[ni])*math.pi/180/2),2)))

    # initialize generation output, unit commitment and line switching
    pInitialOutput = pd.DataFrame([[0.0]*len(mTEPES.gg)]*len(mTEPES.psn), index=pd.Index(mTEPES.psn), columns=list(mTEPES.gg))
    pInitialUC     = pd.DataFrame([[0  ]*len(mTEPES.gg)]*len(mTEPES.psn), index=pd.Index(mTEPES.psn), columns=list(mTEPES.gg))
    pInitialSwitch = pd.DataFrame([[0  ]*len(mTEPES.ln)]*len(mTEPES.psn), index=pd.Index(mTEPES.psn), columns=list(mTEPES.ln))

    mTEPES.pInitialOutput = Param(mTEPES.psngg, initialize=pInitialOutput.stack().to_dict(), within=NonNegativeReals, doc='unit initial output',     mutable=True)
    mTEPES.pInitialUC     = Param(mTEPES.psngg, initialize=pInitialUC.stack().to_dict()    , within=Boolean,          doc='unit initial commitment', mutable=True)
    mTEPES.pInitialSwitch = Param(mTEPES.psnln, initialize=pInitialSwitch.stack().to_dict(), within=Boolean,          doc='line initial switching',  mutable=True)

    SettingUpDataTime = time.time() - StartTime
    print('Setting up input data                  ... ', round(SettingUpDataTime), 's')


def SettingUpVariables(OptModel, mTEPES):

    StartTime = time.time()

    #%% variables
    OptModel.vTotalSCost            = Var(              within=NonNegativeReals,                                                                                                                doc='total system                         cost      [MEUR]')
    OptModel.vTotalICost            = Var(              within=NonNegativeReals,                                                                                                                doc='total system investment              cost      [MEUR]')
    OptModel.vTotalFCost            = Var(mTEPES.p,     within=NonNegativeReals,                                                                                                                doc='total system fixed                   cost      [MEUR]')
    OptModel.vTotalGCost            = Var(mTEPES.psn,   within=NonNegativeReals,                                                                                                                doc='total variable generation  operation cost      [MEUR]')
    OptModel.vTotalCCost            = Var(mTEPES.psn,   within=NonNegativeReals,                                                                                                                doc='total variable consumption operation cost      [MEUR]')
    OptModel.vTotalECost            = Var(mTEPES.psn,   within=NonNegativeReals,                                                                                                                doc='total system emission                cost      [MEUR]')
    OptModel.vTotalRCost            = Var(mTEPES.psn,   within=NonNegativeReals,                                                                                                                doc='total system reliability             cost      [MEUR]')
    OptModel.vTotalOutput           = Var(mTEPES.psng , within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,g : (0.0,                                mTEPES.pMaxPower         [p,sc,n,g ]),  doc='total output of the unit                         [GW]')
    OptModel.vOutput2ndBlock        = Var(mTEPES.psnnr, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,nr: (0.0,                                mTEPES.pMaxPower2ndBlock [p,sc,n,nr]),  doc='second block of the unit                         [GW]')
    OptModel.vReserveUp             = Var(mTEPES.psnnr, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,nr: (0.0,                                mTEPES.pMaxPower2ndBlock [p,sc,n,nr]),  doc='upward   operating reserve                       [GW]')
    OptModel.vReserveDown           = Var(mTEPES.psnnr, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,nr: (0.0,                                mTEPES.pMaxPower2ndBlock [p,sc,n,nr]),  doc='downward operating reserve                       [GW]')
    OptModel.vEnergyInflows         = Var(mTEPES.psnec, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,ec: (0.0,                                mTEPES.pEnergyInflows    [p,sc,n,ec]),  doc='unscheduled inflows  of candidate ESS units      [GW]')
    OptModel.vEnergyOutflows        = Var(mTEPES.psnes, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,es: (0.0,max(mTEPES.pMaxPower[p,sc,n,es],mTEPES.pMaxCharge        [p,sc,n,es])), doc='scheduled   outflows of all       ESS units      [GW]')
    OptModel.vESSInventory          = Var(mTEPES.psnes, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,es: (      mTEPES.pMinStorage[p,sc,n,es],mTEPES.pMaxStorage       [p,sc,n,es]),  doc='ESS inventory                                   [GWh]')
    OptModel.vESSSpillage           = Var(mTEPES.psnes, within=NonNegativeReals,                                                                                                                doc='ESS spillage                                    [GWh]')
    OptModel.vESSTotalCharge        = Var(mTEPES.psnes, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,es: (0.0,                                mTEPES.pMaxCharge        [p,sc,n,es]),  doc='ESS total charge power                           [GW]')
    OptModel.vCharge2ndBlock        = Var(mTEPES.psnes, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,es: (0.0,                                mTEPES.pMaxCharge2ndBlock[p,sc,n,es]),  doc='ESS       charge power                           [GW]')
    OptModel.vESSReserveUp          = Var(mTEPES.psnes, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,es: (0.0,                                mTEPES.pMaxCharge2ndBlock[p,sc,n,es]),  doc='ESS upward   operating reserve                   [GW]')
    OptModel.vESSReserveDown        = Var(mTEPES.psnes, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,es: (0.0,                                mTEPES.pMaxCharge2ndBlock[p,sc,n,es]),  doc='ESS downward operating reserve                   [GW]')
    OptModel.vENS                   = Var(mTEPES.psnnd, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,nd: (0.0,                                max(0.0,mTEPES.pDemand   [p,sc,n,nd])), doc='energy not served in node                        [GW]')

    if mTEPES.pIndBinGenInvest() == 0:
        OptModel.vGenerationInvest  = Var(mTEPES.pgc,           within=UnitInterval,                                                                                                            doc='generation investment decision exists in a year [0,1]')
    else:
        OptModel.vGenerationInvest  = Var(mTEPES.pgc,           within=Binary,                                                                                                                  doc='generation investment decision exists in a year {0,1}')

    if mTEPES.pIndBinGenRetire() == 0:
        OptModel.vGenerationRetire  = Var(mTEPES.pgd,           within=UnitInterval,                                                                                                            doc='generation retirement decision exists in a year [0,1]')
    else:
        OptModel.vGenerationRetire  = Var(mTEPES.pgd,           within=Binary,                                                                                                                  doc='generation retirement decision exists in a year {0,1}')

    if mTEPES.pIndBinNetInvest() == 0:
        OptModel.vNetworkInvest     = Var(mTEPES.plc,           within=UnitInterval,                                                                                                            doc='network    investment decision exists in a year [0,1]')
    else:
        OptModel.vNetworkInvest     = Var(mTEPES.plc,           within=Binary,                                                                                                                  doc='network    investment decision exists in a year {0,1}')

    if mTEPES.pIndBinGenOperat() == 0:
        OptModel.vCommitment        = Var(mTEPES.psnnr,         within=UnitInterval,     initialize=0.0,                                                                                        doc='commitment         of the unit                  [0,1]')
        OptModel.vStartUp           = Var(mTEPES.psnnr,         within=UnitInterval,     initialize=0.0,                                                                                        doc='startup            of the unit                  [0,1]')
        OptModel.vShutDown          = Var(mTEPES.psnnr,         within=UnitInterval,     initialize=0.0,                                                                                        doc='shutdown           of the unit                  [0,1]')
        OptModel.vMaxCommitment     = Var(mTEPES.ps, mTEPES.nr, within=UnitInterval,     initialize=0.0,                                                                                        doc='maximum commitment of the unit                  [0,1]')
    else:
        OptModel.vCommitment        = Var(mTEPES.psnnr,         within=Binary,           initialize=0  ,                                                                                        doc='commitment         of the unit                  {0,1}')
        OptModel.vStartUp           = Var(mTEPES.psnnr,         within=Binary,           initialize=0  ,                                                                                        doc='startup            of the unit                  {0,1}')
        OptModel.vShutDown          = Var(mTEPES.psnnr,         within=Binary,           initialize=0  ,                                                                                        doc='shutdown           of the unit                  {0,1}')
        OptModel.vMaxCommitment     = Var(mTEPES.ps, mTEPES.nr, within=Binary,           initialize=0  ,                                                                                        doc='maximum commitment of the unit                  {0,1}')

    if mTEPES.pIndBinLineCommit() == 0:
        OptModel.vLineCommit        = Var(mTEPES.psnla,         within=UnitInterval,     initialize=0.0,                                                                                        doc='line switching      of the line                 [0,1]')
        OptModel.vLineOnState       = Var(mTEPES.psnla,         within=UnitInterval,     initialize=0.0,                                                                                        doc='switching on  state of the line                 [0,1]')
        OptModel.vLineOffState      = Var(mTEPES.psnla,         within=UnitInterval,     initialize=0.0,                                                                                        doc='switching off state of the line                 [0,1]')
    else:
        OptModel.vLineCommit        = Var(mTEPES.psnla,         within=Binary,           initialize=0  ,                                                                                        doc='line switching      of the line                 {0,1}')
        OptModel.vLineOnState       = Var(mTEPES.psnla,         within=Binary,           initialize=0  ,                                                                                        doc='switching on  state of the line                 {0,1}')
        OptModel.vLineOffState      = Var(mTEPES.psnla,         within=Binary,           initialize=0  ,                                                                                        doc='switching off state of the line                 {0,1}')

    # relax binary condition in generation and network investment decisions
    for p,gc in mTEPES.pgc:
        if mTEPES.pIndBinGenInvest() != 0 and mTEPES.pIndBinUnitInvest[gc      ] == 0:
            OptModel.vGenerationInvest[p,gc      ].domain = UnitInterval
        if mTEPES.pIndBinGenInvest() == 2:
            OptModel.vGenerationInvest[p,gc      ].fix(0)
    for p,ni,nf,cc in mTEPES.plc:
        if mTEPES.pIndBinNetInvest() != 0 and mTEPES.pIndBinLineInvest[ni,nf,cc] == 0:
            OptModel.vNetworkInvest   [p,ni,nf,cc].domain = UnitInterval
        if mTEPES.pIndBinNetInvest() == 2:
            OptModel.vNetworkInvest   [p,ni,nf,cc].fix(0)

    # relax binary condition in generation retirement decisions
    for p,gd in mTEPES.pgd:
        if mTEPES.pIndBinGenRetire() != 0 and mTEPES.pIndBinUnitRetire[gd      ] == 0:
            OptModel.vGenerationRetire[p,gd      ].domain = UnitInterval
        if mTEPES.pIndBinGenRetire() == 2:
            OptModel.vGenerationRetire[p,gd      ].fix(0)

    # relax binary condition in unit generation, startup and shutdown decisions
    for p,sc,n,nr in mTEPES.psnnr:
        if mTEPES.pIndBinUnitCommit[nr] == 0:
            OptModel.vCommitment   [p,sc,n,nr].domain = UnitInterval
            OptModel.vStartUp      [p,sc,n,nr].domain = UnitInterval
            OptModel.vShutDown     [p,sc,n,nr].domain = UnitInterval
    for p,sc,  nr in mTEPES.ps*         mTEPES.nr:
        if mTEPES.pIndBinUnitCommit[nr] == 0:
            OptModel.vMaxCommitment[p,sc,  nr].domain = UnitInterval

    # existing lines are always committed if no switching decision is modeled
    for p,sc,n,ni,nf,cc in mTEPES.psn*mTEPES.le:
        if mTEPES.pIndBinLineSwitch[ni,nf,cc] == 0:
            OptModel.vLineCommit  [p,sc,n,ni,nf,cc].fix(1)
            OptModel.vLineOnState [p,sc,n,ni,nf,cc].fix(0)
            OptModel.vLineOffState[p,sc,n,ni,nf,cc].fix(0)

    OptModel.vLineLosses = Var(mTEPES.ps, mTEPES.n, mTEPES.ll, within=NonNegativeReals, bounds=lambda OptModel,p,sc,n,*ll: (0.0,0.5*mTEPES.pLineLossFactor[ll]*max(mTEPES.pLineNTCBck[ll],mTEPES.pLineNTCFrw[ll])), doc='half line losses [GW]')
    if mTEPES.pIndBinSingleNode() == 0:
        OptModel.vFlow   = Var(mTEPES.ps, mTEPES.n, mTEPES.la, within=Reals,            bounds=lambda OptModel,p,sc,n,*la: (                                      -mTEPES.pLineNTCBck[la],mTEPES.pLineNTCFrw[la]),  doc='flow             [GW]')
    else:
        OptModel.vFlow   = Var(mTEPES.ps, mTEPES.n, mTEPES.la, within=Reals,                                                                                                                                        doc='flow             [GW]')
    OptModel.vTheta      = Var(mTEPES.ps, mTEPES.n, mTEPES.nd, within=Reals,            bounds=lambda OptModel,p,sc,n, nd: (                            -mTEPES.pMaxTheta[p,sc,n,nd],mTEPES.pMaxTheta[p,sc,n,nd]),  doc='voltage angle   [rad]')

    # fix the must-run units and their output
    for p,sc,n,g  in mTEPES.psn*mTEPES.g :
        # must run units must produce at least their minimum output
        if mTEPES.pMustRun[g] == 1:
            OptModel.vTotalOutput[p,sc,n,g].setlb(mTEPES.pMinPower[p,sc,n,g])
        # if no max power, no total output
        if mTEPES.pMaxPower[p,sc,n,g] == 0.0:
            OptModel.vTotalOutput[p,sc,n,g].fix(0.0)
    #for p,sc,n,r  in mTEPES.psn*mTEPES.r :
    #    if mTEPES.pMinPower[p,sc,n,r] == mTEPES.pMaxPower[p,sc,n,r] and mTEPES.pLinearOMCost[r] == 0.0:
    #        OptModel.vTotalOutput[p,sc,n,r].fix(mTEPES.pMaxPower[p,sc,n,r])

    for p,sc,n,nr in mTEPES.psnnr:
        # must run units or units with no minimum power or ESS existing units are always committed and must produce at least their minimum output
        # not applicable to mutually exclusive units
        if (mTEPES.pMustRun[nr] == 1 or (mTEPES.pMinPower[p,sc,n,nr] == 0.0 and mTEPES.pConstantVarCost[nr] == 0.0) or nr in mTEPES.es) and nr not in mTEPES.ec and sum(1 for g in mTEPES.nr if (nr,g) in mTEPES.g2g or (g,nr) in mTEPES.g2g) == 0:
            OptModel.vCommitment    [p,sc,n,nr].fix(1)
            OptModel.vStartUp       [p,sc,n,nr].fix(0)
            OptModel.vShutDown      [p,sc,n,nr].fix(0)
            OptModel.vMaxCommitment [p,sc,  nr].fix(1)
        # if min and max power coincide there are neither second block, nor operating reserve
        if  mTEPES.pMaxPower2ndBlock[p,sc,n,nr] ==  0.0:
            OptModel.vOutput2ndBlock[p,sc,n,nr].fix(0.0)
            OptModel.vReserveUp     [p,sc,n,nr].fix(0.0)
            OptModel.vReserveDown   [p,sc,n,nr].fix(0.0)
        if  mTEPES.pIndOperReserve  [       nr] !=  0.0:
            OptModel.vReserveUp     [p,sc,n,nr].fix(0.0)
            OptModel.vReserveDown   [p,sc,n,nr].fix(0.0)

    for p,sc,n,es in mTEPES.psnes:
        # ESS with no charge capacity or not storage capacity can't charge
        if mTEPES.pMaxCharge        [p,sc,n,es] ==  0.0:
            OptModel.vESSTotalCharge[p,sc,n,es].fix(0.0)
        # ESS with no charge capacity and no inflows can't produce
        if mTEPES.pMaxCharge        [p,sc,n,es] ==  0.0 and sum(mTEPES.pEnergyInflows[pp,scc,nn,es]() for pp,scc,nn in mTEPES.psn) == 0.0:
            OptModel.vTotalOutput   [p,sc,n,es].fix(0.0)
            OptModel.vOutput2ndBlock[p,sc,n,es].fix(0.0)
            OptModel.vReserveUp     [p,sc,n,es].fix(0.0)
            OptModel.vReserveDown   [p,sc,n,es].fix(0.0)
            OptModel.vESSSpillage   [p,sc,n,es].fix(0.0)
        if mTEPES.pMaxCharge2ndBlock[p,sc,n,es] ==  0.0:
            OptModel.vCharge2ndBlock[p,sc,n,es].fix(0.0)
            OptModel.vESSReserveUp  [p,sc,n,es].fix(0.0)
            OptModel.vESSReserveDown[p,sc,n,es].fix(0.0)
        if  mTEPES.pIndOperReserve  [       es] !=  0.0:
            OptModel.vESSReserveUp  [p,sc,n,es].fix(0.0)
            OptModel.vESSReserveDown[p,sc,n,es].fix(0.0)
        if mTEPES.pMaxStorage       [p,sc,n,es] ==  0.0:
            OptModel.vESSInventory  [p,sc,n,es].fix(0.0)

    # thermal and RES units ordered by increasing variable operation cost, excluding reactive generating units
    if len(mTEPES.tq):
        mTEPES.go = [k for k in sorted(mTEPES.pLinearVarCost, key=mTEPES.pLinearVarCost.__getitem__) if k not in mTEPES.sq]
    else:
        mTEPES.go = [k for k in sorted(mTEPES.pLinearVarCost, key=mTEPES.pLinearVarCost.__getitem__)                      ]

    for p,sc,st in mTEPES.ps*mTEPES.stt:
        # activate only period, scenario, and load levels to formulate
        mTEPES.del_component(mTEPES.st)
        mTEPES.del_component(mTEPES.n )
        mTEPES.st = Set(initialize=mTEPES.stt, ordered=True, doc='stages',      filter=lambda mTEPES,stt: stt in mTEPES.stt and st == stt and mTEPES.pStageWeight[stt] and sum(1 for (st,nn) in mTEPES.s2n))
        mTEPES.n  = Set(initialize=mTEPES.nn , ordered=True, doc='load levels', filter=lambda mTEPES,nn : nn  in                              mTEPES.pDuration         and           (st,nn) in mTEPES.s2n)

        if len(mTEPES.n):
            # determine the first load level of each stage
            n1 = next(iter(mTEPES.ps*mTEPES.n))
            # commit the units and their output at the first load level of each stage
            pSystemOutput = 0.0
            for nr in mTEPES.nr:
                if pSystemOutput < sum(mTEPES.pDemand[n1,nd] for nd in mTEPES.nd) and mTEPES.pMustRun[nr] == 1:
                    mTEPES.pInitialOutput[n1,nr] = mTEPES.pMaxPower[n1,nr]
                    mTEPES.pInitialUC    [n1,nr] = 1
                    pSystemOutput               += mTEPES.pInitialOutput[n1,nr]()

            # determine the initial committed units and their output at the first load level of each period, scenario, and stage
            for go in mTEPES.go:
                if pSystemOutput < sum(mTEPES.pDemand[n1,nd] for nd in mTEPES.nd) and mTEPES.pMustRun[go] != 1:
                    if go in mTEPES.r:
                        mTEPES.pInitialOutput[n1,go] = mTEPES.pMaxPower[n1,go]
                    else:
                        mTEPES.pInitialOutput[n1,go] = mTEPES.pMinPower[n1,go]
                    mTEPES.pInitialUC[n1,go] = 1
                    pSystemOutput = pSystemOutput + mTEPES.pInitialOutput[n1,go]()

            # determine the initial committed lines
            for la in mTEPES.la:
                if la in mTEPES.lc:
                    mTEPES.pInitialSwitch[n1,la] = 0
                else:
                    mTEPES.pInitialSwitch[n1,la] = 1

            # fixing the ESS inventory at the last load level of the stage for every period and scenario if between storage limits
            for p,sc,es in mTEPES.ps*mTEPES.es:
                if mTEPES.pInitialInventory[es] >= mTEPES.pMinStorage[p,sc,mTEPES.n.last(),es] and mTEPES.pInitialInventory[es] <= mTEPES.pMaxStorage[p,sc,mTEPES.n.last(),es]:
                    OptModel.vESSInventory[p,sc,mTEPES.n.last(),es].fix(mTEPES.pInitialInventory[es])

    # activate all the periods, scenarios, and load levels again
    mTEPES.del_component(mTEPES.st)
    mTEPES.del_component(mTEPES.n )
    mTEPES.st = Set(initialize=mTEPES.stt, ordered=True, doc='stages',      filter=lambda mTEPES,stt: stt in mTEPES.stt and mTEPES.pStageWeight[stt] and sum(1 for (stt,nn) in mTEPES.s2n))
    mTEPES.n  = Set(initialize=mTEPES.nn,  ordered=True, doc='load levels', filter=lambda mTEPES,nn : nn  in                mTEPES.pDuration                                              )

    # fixing the ESS inventory at the end of the following pCycleTimeStep (daily, weekly, monthly) if between storage limits, i.e., for daily ESS is fixed at the end of the week, for weekly/monthly ESS is fixed at the end of the year
    for p,sc,n,es in mTEPES.psnes:
        if mTEPES.pInitialInventory[es] >= mTEPES.pMinStorage[p,sc,n,es] and mTEPES.pInitialInventory[es] <= mTEPES.pMaxStorage[p,sc,n,es]:
            if mTEPES.pStorageType[es] == 'Hourly'  and mTEPES.n.ord(n) % int(  24/mTEPES.pTimeStep()) == 0:
                OptModel.vESSInventory[p,sc,n,es].fix(mTEPES.pInitialInventory[es])
            if mTEPES.pStorageType[es] == 'Daily'   and mTEPES.n.ord(n) % int( 168/mTEPES.pTimeStep()) == 0:
                OptModel.vESSInventory[p,sc,n,es].fix(mTEPES.pInitialInventory[es])
            if mTEPES.pStorageType[es] == 'Weekly'  and mTEPES.n.ord(n) % int(8736/mTEPES.pTimeStep()) == 0:
                OptModel.vESSInventory[p,sc,n,es].fix(mTEPES.pInitialInventory[es])
            if mTEPES.pStorageType[es] == 'Monthly' and mTEPES.n.ord(n) % int(8736/mTEPES.pTimeStep()) == 0:
                OptModel.vESSInventory[p,sc,n,es].fix(mTEPES.pInitialInventory[es])

    for p,sc,n,ec in mTEPES.psnec:
        if mTEPES.pEnergyInflows [p,sc,n,ec]() == 0.0:
            OptModel.vEnergyInflows        [p,sc,n,ec].fix(0.0)

    # if no operating reserve is required no variables are needed
    for p,sc,n,ar,nr in mTEPES.psn*mTEPES.ar*mTEPES.nr:
        if (ar,nr) in mTEPES.a2g:
            if mTEPES.pOperReserveUp    [p,sc,n,ar] ==  0.0:
                OptModel.vReserveUp     [p,sc,n,nr].fix(0.0)
            if mTEPES.pOperReserveDw    [p,sc,n,ar] ==  0.0:
                OptModel.vReserveDown   [p,sc,n,nr].fix(0.0)
    for p,sc,n,ar,es in mTEPES.psn*mTEPES.ar*mTEPES.es:
        if (ar,es) in mTEPES.a2g:
            if mTEPES.pOperReserveUp    [p,sc,n,ar] ==  0.0:
                OptModel.vESSReserveUp  [p,sc,n,es].fix(0.0)
            if mTEPES.pOperReserveDw    [p,sc,n,ar] ==  0.0:
                OptModel.vESSReserveDown[p,sc,n,es].fix(0.0)

    # if there are no energy outflows no variable is needed
    for es in mTEPES.es:
        if sum(mTEPES.pEnergyOutflows[p,sc,n,es]() for p,sc,n in mTEPES.psn) == 0:
            for p,sc,n in mTEPES.psn:
                OptModel.vEnergyOutflows[p,sc,n,es].fix(0.0)

    # fixing the voltage angle of the reference node for each scenario, period, and load level
    if mTEPES.pIndBinSingleNode() == 0:
        for p,sc,n in mTEPES.psn:
            OptModel.vTheta[p,sc,n,mTEPES.rf.first()].fix(0.0)

    # fixing the ENS in nodes with no demand
    for p,sc,n,nd in mTEPES.psnnd:
        if mTEPES.pDemand[p,sc,n,nd] == 0.0:
            OptModel.vENS[p,sc,n,nd].fix(0.0)

    # do not install/retire power plants and lines if not allowed in this period
    for p,gc in mTEPES.pgc:
        if mTEPES.pPeriodIniGen[gc] > p or mTEPES.pPeriodFinGen[gc] < p:
            OptModel.vGenerationInvest[p,gc].fix(0)

    for p,gd in mTEPES.pgd:
        if mTEPES.pPeriodIniGen[gd] > p or mTEPES.pPeriodFinGen[gd] < p:
            OptModel.vGenerationRetire[p,gd].fix(0)

    for p,ni,nf,cc in mTEPES.plc:
        if mTEPES.pPeriodIniNet[ni,nf,cc] > p or mTEPES.pPeriodFinNet[ni,nf,cc] < p:
                OptModel.vNetworkInvest[p,ni,nf,cc].fix(0)

    # remove power plants and lines not installed in this period
    for p,g in mTEPES.p*mTEPES.g:
        if g  not in mTEPES.gc and (mTEPES.pPeriodIniGen[g ] > p or mTEPES.pPeriodFinGen[g ] < p):
            for sc,n in mTEPES.sc*mTEPES.n:
                OptModel.vTotalOutput   [p,sc,n,g].fix(0.0)

    for p,sc,nr in mTEPES.ps*mTEPES.nr:
        if nr not in mTEPES.gc and (mTEPES.pPeriodIniGen[nr] > p or mTEPES.pPeriodFinGen[nr] < p):
            OptModel.vMaxCommitment[p,sc,nr].fix(0)
            for n in mTEPES.n:
                OptModel.vOutput2ndBlock[p,sc,n,nr].fix(0.0)
                OptModel.vReserveUp     [p,sc,n,nr].fix(0.0)
                OptModel.vReserveDown   [p,sc,n,nr].fix(0.0)
                OptModel.vCommitment    [p,sc,n,nr].fix(0  )
                OptModel.vStartUp       [p,sc,n,nr].fix(0  )
                OptModel.vShutDown      [p,sc,n,nr].fix(0  )

    for p,es in mTEPES.p*mTEPES.es:
        if es not in mTEPES.gc and (mTEPES.pPeriodIniGen[es] > p or mTEPES.pPeriodFinGen[es] < p):
            for sc,n in mTEPES.sc*mTEPES.n:
                OptModel.vEnergyOutflows[p,sc,n,es].fix(0.0)
                OptModel.vESSInventory  [p,sc,n,es].fix(0.0)
                OptModel.vESSSpillage   [p,sc,n,es].fix(0.0)
                OptModel.vESSTotalCharge[p,sc,n,es].fix(0.0)
                OptModel.vCharge2ndBlock[p,sc,n,es].fix(0.0)
                OptModel.vESSReserveUp  [p,sc,n,es].fix(0.0)
                OptModel.vESSReserveDown[p,sc,n,es].fix(0.0)
                mTEPES.pIniInventory    [p,sc,n,es] =   0.0
                mTEPES.pEnergyInflows   [p,sc,n,es] =   0.0

    for p,ni,nf,cc in mTEPES.p*mTEPES.la:
        if (ni,nf,cc) not in mTEPES.lc and (mTEPES.pPeriodIniNet[ni,nf,cc] > p or mTEPES.pPeriodFinNet[ni,nf,cc] < p):
            for sc,n in mTEPES.sc*mTEPES.n:
                OptModel.vFlow        [p,sc,n,ni,nf,cc].fix(0.0)
                OptModel.vLineCommit  [p,sc,n,ni,nf,cc].fix(0  )
                OptModel.vLineOnState [p,sc,n,ni,nf,cc].fix(0  )
                OptModel.vLineOffState[p,sc,n,ni,nf,cc].fix(0  )

    for p,ni,nf,cc in mTEPES.p*mTEPES.ll:
        if (ni,nf,cc) not in mTEPES.lc and (mTEPES.pPeriodIniNet[ni,nf,cc] > p or mTEPES.pPeriodFinNet[ni,nf,cc] < p):
            for sc,n in mTEPES.sc*mTEPES.n:
                OptModel.vLineLosses  [p,sc,n,ni,nf,cc].fix(0.0)

    # tolerance to consider 0 a number
    pEpsilon = 1e-3
    for p,gc in mTEPES.pgc:
        if  mTEPES.pGenLoInvest   [  gc      ]() <       pEpsilon:
            mTEPES.pGenLoInvest   [  gc      ]   = 0
        if  mTEPES.pGenUpInvest   [  gc      ]() <       pEpsilon:
            mTEPES.pGenUpInvest   [  gc      ]   = 0
        if  mTEPES.pGenLoInvest   [  gc      ]() > 1.0 - pEpsilon:
            mTEPES.pGenLoInvest   [  gc      ]   = 1
        if  mTEPES.pGenUpInvest   [  gc      ]() > 1.0 - pEpsilon:
            mTEPES.pGenUpInvest   [  gc      ]   = 1
        if  mTEPES.pGenLoInvest   [  gc      ]() >   mTEPES.pGenUpInvest[gc      ]():
            mTEPES.pGenLoInvest   [  gc      ]   =   mTEPES.pGenUpInvest[gc      ]()
        OptModel.vGenerationInvest[p,gc      ].setlb(mTEPES.pGenLoInvest[gc      ])
        OptModel.vGenerationInvest[p,gc      ].setub(mTEPES.pGenUpInvest[gc      ])
    for p,gd in mTEPES.pgd:
        if  mTEPES.pGenLoRetire   [  gd      ]() < pEpsilon:
            mTEPES.pGenLoRetire   [  gd      ]   = 0
        if  mTEPES.pGenUpRetire   [  gd      ]() <       pEpsilon:
            mTEPES.pGenUpRetire   [  gd      ]   = 0
        if  mTEPES.pGenLoRetire   [  gd      ]() > 1.0 - pEpsilon:
            mTEPES.pGenLoRetire   [  gd      ]   = 1
        if  mTEPES.pGenUpRetire   [  gd      ]() > 1.0 - pEpsilon:
            mTEPES.pGenUpRetire   [  gd      ]   = 1
        if  mTEPES.pGenLoRetire   [  gd      ]() >   mTEPES.pGenUpRetire[gd      ]():
            mTEPES.pGenLoRetire   [  gd      ]   =   mTEPES.pGenUpRetire[gd      ]()
        OptModel.vGenerationRetire[p,gd      ].setlb(mTEPES.pGenLoRetire[gd      ])
        OptModel.vGenerationRetire[p,gd      ].setub(mTEPES.pGenUpRetire[gd      ])
    for p,ni,nf,cc in mTEPES.plc:
        if  mTEPES.pNetLoInvest   [  ni,nf,cc]() <       pEpsilon:
            mTEPES.pNetLoInvest   [  ni,nf,cc]   = 0
        if  mTEPES.pNetUpInvest   [  ni,nf,cc]() <       pEpsilon:
            mTEPES.pNetUpInvest   [  ni,nf,cc]   = 0
        if  mTEPES.pNetLoInvest   [  ni,nf,cc]() > 1.0 - pEpsilon:
            mTEPES.pNetLoInvest   [  ni,nf,cc]   = 1
        if  mTEPES.pNetUpInvest   [  ni,nf,cc]() > 1.0 - pEpsilon:
            mTEPES.pNetUpInvest   [  ni,nf,cc]   = 1
        if  mTEPES.pNetLoInvest   [  ni,nf,cc]() >   mTEPES.pNetUpInvest[ni,nf,cc]():
            mTEPES.pNetLoInvest   [  ni,nf,cc]   =   mTEPES.pNetUpInvest[ni,nf,cc]()
        OptModel.vNetworkInvest   [p,ni,nf,cc].setlb(mTEPES.pNetLoInvest[ni,nf,cc])
        OptModel.vNetworkInvest   [p,ni,nf,cc].setub(mTEPES.pNetUpInvest[ni,nf,cc])

    # detecting infeasibility: sum of scenario probabilities must be 1 in each period
    # for p in mTEPES.p:
    #     if abs(sum(mTEPES.pScenProb[p,sc] for sc in mTEPES.sc)-1.0) > 1e-6:
    #         print('### Sum of scenario probabilities different from 1 in period ', p)
    #         assert (0 == 1)

    for es in mTEPES.es:
        # detecting infeasibility: total min ESS output greater than total inflows, total max ESS charge lower than total outflows
        if sum(mTEPES.pMinPower [p,sc,n,es]-mTEPES.pEnergyInflows [p,sc,n,es]() for p,sc,n in mTEPES.psn) > 0.0:
            print('### Total minimum output greater than total inflows for ESS unit ', es)
            assert (0 == 1)
        if sum(mTEPES.pMaxCharge[p,sc,n,es]-mTEPES.pEnergyOutflows[p,sc,n,es]() for p,sc,n in mTEPES.psn) < 0.0:
            print('### Total maximum charge lower than total outflows for ESS unit ', es)
            assert (0 == 1)

        # detect inventory infeasibility
        for p,sc,n in mTEPES.psn:
            if   mTEPES.n.ord(n) == mTEPES.pCycleTimeStep[es]                                                      and mTEPES.pMaxCharge[p,sc,n,es] + mTEPES.pMaxPower[p,sc,n,es]:
                if mTEPES.pIniInventory[p,sc,n,es]()                                      + sum(mTEPES.pDuration[n2]()*(mTEPES.pEnergyInflows[p,sc,n2,es]() - mTEPES.pMinPower[p,sc,n2,es] + mTEPES.pEfficiency[es]*mTEPES.pMaxCharge[p,sc,n2,es]) for n2 in list(mTEPES.n2)[mTEPES.n.ord(n)-mTEPES.pCycleTimeStep[es]:mTEPES.n.ord(n)]) < mTEPES.pMinStorage[p,sc,n,es]:
                    print('### Inventory equation violation ', p, sc, n, es)
                    assert (0 == 1)
            elif mTEPES.n.ord(n) >  mTEPES.pCycleTimeStep[es] and mTEPES.n.ord(n) % mTEPES.pCycleTimeStep[es] == 0 and mTEPES.pMaxCharge[p,sc,n,es] + mTEPES.pMaxPower[p,sc,n,es]:
                if mTEPES.pMaxStorage[p,sc,mTEPES.n.prev(n,mTEPES.pCycleTimeStep[es]),es] + sum(mTEPES.pDuration[n2]()*(mTEPES.pEnergyInflows[p,sc,n2,es]() - mTEPES.pMinPower[p,sc,n2,es] + mTEPES.pEfficiency[es]*mTEPES.pMaxCharge[p,sc,n2,es]) for n2 in list(mTEPES.n2)[mTEPES.n.ord(n)-mTEPES.pCycleTimeStep[es]:mTEPES.n.ord(n)]) < mTEPES.pMinStorage[p,sc,n,es]:
                    print('### Inventory equation violation ', p, sc, n, es)
                    assert (0 == 1)

    # detect minimum energy infeasibility
    for g in mTEPES.g:
        for p,sc,n in mTEPES.psn:
            if mTEPES.n.ord(n) % mTEPES.pEnergyTimeStep[g] == 0 and sum(mTEPES.pMinEnergy[p,sc,n2,g] for n2 in mTEPES.n2):
                if sum((mTEPES.pMaxPower[p,sc,n2,g] - mTEPES.pMinEnergy[p,sc,n2,g])*mTEPES.pDuration[n2]() for n2 in list(mTEPES.n2)[mTEPES.n.ord(n) - mTEPES.pEnergyTimeStep[g]:mTEPES.n.ord(n)]) < 0.0:
                    print('### Minimum energy violation ', p, sc, n, g)
                    assert (0 == 1)

    SettingUpVariablesTime = time.time() - StartTime
    print('Setting up variables                   ... ', round(SettingUpVariablesTime), 's')

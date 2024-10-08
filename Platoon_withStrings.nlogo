; Jose Fernando Jimenez

; patch 0.1 m x 0.1 m
; 1 Second SimulatedTime = 20 ticks


globals [

 ;default   For movement. Global Variable created in the interface in order to set the simulation On: Netlogo Control Off: It will be controlled by another program

 SimulationTime

]

breed [Products Product]
breed [Vehicles Vehicle]
breed [Machines Machine]
breed [Recharge-Stations Recharge-Station]

Products-Own [
  ProductID                   ; Indicates the identifier of the product within the ProductionOrder. ID is diferent than who
  ProductType                 ; AA, BB, CC, DD, EE, FF, GG, HH, II, JJ,
  ProductWeight               ; AA =, BB =, CC =, DD =, EE = , FF = , GG = , HH = , II = , JJ =
  ProductState                ; To-be-released, Releasing, Transport, Being-Processed, Finished
  ProductOperations           ; List of operations of the product
  ProductReleaseOrder         ; Indicates the Release order within the production order
  ProductDueDate              ; Indicates the due date for the product
  ProductCurrentOperation     ; Indicates the position of the list of operations that have been already processed
  ProductNextOperation        ; Indicates what would be the next operation
  ProductStartOperation       ; Indicates in a list when the operation started processing. The order in the list follows the position of the operarion list "ProductOperations"
  ProductCompletionOperation  ; Indicates in a list when the operation finished processing. The order in the list follows the position of the operarion list "ProductOperations"
  ProductInVehicle            ; Indicates which is the vehicle moving the product. "-" when is not on a vehicle
  ProductInMachine            ; Indicates which machine is processing product. "-" when is not on a vehicle
]

Vehicles-Own [
  MathematicalAngle           ; Indicate the heading but in mathematical angles
  VehicleID                   ; Indicates the identifier of the vehicle within the production layout. ID is diferent than who
  VehicleType                 ; T1, T2, T3
  VehicleState                ; Moving, WaitingMachine, WaitingCharging, WaitingOutside, WaitingLoading, GoingCharger, Charging
  VehicleWithProduct          ; Indicates the product being carried/ "-" Otherwise
  VehicleBattery              ; T1 = 21, T2 = 42, T3 = 63
  VehicleDestinationNode      ; Indicates the node of destination
  VehicleDestinationEntity    ; Indicates the entity of destination. Could be: Machine, RechargingStation, RestArea, LoadingStation, UnloadingStation
  VehicleSpeed-X              ; Indicates the speed in the x-axis
  VehicleSpeed-Y              ; Indicates the speed in the y-axis
  VehicleSpeed-Total          ; Indicates the speed in the heading direction
  VehicleBatteryCharge        ; Indicates the charge of battery
  VehicleValues
]

Machines-Own [
  MachineID                   ; Indicates the identifier of the machine within the production layout. ID is diferent than who
  MachineType                 ; Type of machine. For A.Bozzi, it has only one type.
  MachineState                ; MachineBusy, MachineIdle, MachineBrakedown. For A.Bozzi, just first two.
  MachinePossibleOperations   ; Indicates what are the operations that the machine is capable fo process.
  MachineOperProcessingTime   ; Indicates the processing times of each operation. Order must be follow the list of operations "MachinePossibleOperations"
  MachineNextCompletion       ; Important attribute that controls the completion time of an operation. Normally, it has the time of completion of next operation, or a big number (M)
  MachineProcessingProduct    ; Indicates which product is being process. "-" when is not processing product
  MachineWithVehicle          ; Indicates the Vehicle in the machine. "-" otherwise
  MachineValues
]

Recharge-Stations-Own [
  Rech.StationID              ; Indicates the identifier of the recharging Station within the production layout. ID is diferent than who
  Rech.Type                   ; Type of Recharching Station. For A.Bozzi, it has only one type.
  Rech.State                  ; RechargeStationBusy, RechargeStationIdle, RechargeStatioBrakedown. For A.Bozzi, just first two.
  Rech.NextCompletion         ; Important attribute that controls the completion time of an operation. Normally, it has the time of completion of next operation, or a big number (M)
  Rech.WithVehicle            ; Indicates which vechike is being process. "-" when is not processing product
  Rech.ReservedForVehicle     ; Indicates which Vehicle will arrive here

]

to A-Setup

  clear-all
  reset-ticks

  set SimulationTime 0

  Z-Layout
  X-SetupMachines
  Y-Setup-Corridor
  L-CreatingVehiclesFleet (list "T1" "T2" "T3" "T1" "T1" "T2" "T3" "T1" "T3" "T1")

  J-CreatingProductionOrder

  ;test

end

to test

  ask machines [
    set MachineValues (list (word who) (word xcor) (word ycor) machineid MachineState MachineProcessingProduct (word MachineWithVehicle))
  ]

   ask vehicles [
    set VehicleValues (list (word who) (word xcor) (word ycor) VehicleID (word VehicleDestinationNode) )
  ]

end


to up
  ask vehicle 23 [
    set VehicleSpeed-X 0
    set VehicleSpeed-Y 0.8
  ]
end

to down
  ask vehicle 23 [
    set VehicleSpeed-X 0
    set VehicleSpeed-Y -0.8
  ]
end

to left-arrow
  ask vehicle 23 [
    set VehicleSpeed-X -0.8
    set VehicleSpeed-Y 0
  ]
end

to right-arrow
  ask vehicle 23 [
    set VehicleSpeed-X 0.8
    set VehicleSpeed-Y 0
  ]
end


to B-Go

  C-ReleasingProducts
  D-MovingVehicles
  O-MovingToChargers
  P-EnteringChargers
  R-ExitingChargers
  E-MachineEntry
  F-MachineExit
  V-MovementVehicleOutside
  I-CompletingProduct
  N-UpdateBateryDecharging

  tick
  set SimulationTime precision (SimulationTime + 0.05) 3
 test

end

to C-ReleasingProducts

  ask products with [xcor = 23 and ycor = 70] with-min [ProductReleaseOrder][
    if((count vehicles with [xcor = 34 and ycor = 70] = 1) and (count products with [xcor > 23 and xcor <= 34 and ycor = 70] = 0)) [
      set heading 90
      set ProductState "Releasing"
      set ProductStartOperation lput SimulationTime ProductStartOperation
    ]
  ]

  ask turtle 0 [
    let ProductReleaseVar ""
    if(count products in-radius 2 with [ProductState = "Releasing"] = 1)[
      ask products in-radius 2 with [ProductState = "Releasing"][
        set ProductReleaseVar who
        move-to turtle 0
        set ProductState "Transport"
      ]
      ask product ProductReleaseVar [
        set ProductCompletionOperation lput SimulationTime ProductCompletionOperation
        let temporalProductVar who
        set ProductNextOperation 1
        let TemporalProNextOperVar item ProductNextOperation ProductOperations

        set ProductInVehicle item 0 [who] of vehicles with [xcor = 34 and ycor = 70]
        ask vehicles with [xcor = 34 and ycor = 70][
          if (VehicleType = "T1") [set shape "newsquare-t1"]
          if (VehicleType = "T2") [set shape "newsquare-t2"]
          if (VehicleType = "T3") [set shape "newsquare-t3"]
          set VehicleState "Moving"
          set VehicleWithProduct temporalProductVar
          let TemporalDestNodeVar [who] of machines with [item 0 MachinePossibleOperations = TemporalProNextOperVar]
          set VehicleDestinationNode item 0 TemporalDestNodeVar
          set VehicleDestinationEntity "Machine"
          set VehicleSpeed-X 0.8
          set VehicleSpeed-Y 0
          set VehicleSpeed-Total 0.8
        ]
      ]
    ]
  ]




end

to D-MovingVehicles

  ifelse (Default = false)[
    ask vehicles with [VehicleState = "Moving"][
      if (VehicleWithProduct != "None")[
        set VehicleSpeed-Total sqrt (VehicleSpeed-X ^ 2 + VehicleSpeed-Y ^ 2)

        if(VehicleSpeed-X >= 0 and VehicleSpeed-Y >= 0 ) [set heading 450 - (asin (VehicleSpeed-Y / VehicleSpeed-Total))]
        if(VehicleSpeed-X < 0 and VehicleSpeed-Y >= 0 ) [set heading 450 - (acos (VehicleSpeed-X / VehicleSpeed-Total))]
        if(VehicleSpeed-X < 0 and VehicleSpeed-Y < 0 ) [set heading 0 - 90 + (asin (VehicleSpeed-Y / VehicleSpeed-Total))]
        if(VehicleSpeed-X >= 0 and VehicleSpeed-Y < 0 ) [set heading 450 - (asin (VehicleSpeed-Y / VehicleSpeed-Total))]


        set heading precision heading 3
        if (count vehicles in-cone 10 40 < 2) [forward VehicleSpeed-Total]                                    ; Change according to speed
        set xcor  precision xcor 3
        set ycor  precision ycor 3
        ask product VehicleWithProduct [move-to turtle ProductInVehicle]
      ]
      if (VehicleWithProduct = "None")[
        if (count vehicles in-cone 25 70 < 2) [forward 0.8]                                   ; Change according to speed
        set xcor  precision xcor 3
        set ycor  precision ycor 3
      ]
    ]
  ][
    ask vehicles with [VehicleState = "Moving"][
      if (VehicleWithProduct != "None")[
        face turtle VehicleDestinationNode
        set heading precision heading 3
        set VehicleSpeed-Total 0.8
        set VehicleSpeed-X VehicleSpeed-Total * cos W-HeadingToAngle heading
        set VehicleSpeed-Y VehicleSpeed-Total * sin W-HeadingToAngle heading
        set VehicleSpeed-X precision VehicleSpeed-X 3
        set VehicleSpeed-Y precision VehicleSpeed-Y 3
        if (count vehicles in-cone 10 70 < 2) [forward 0.8]                                     ; Change according to speed
        set xcor  precision xcor 3
        set ycor  precision ycor 3
        ask product VehicleWithProduct [move-to turtle ProductInVehicle]
      ]
      if (VehicleWithProduct = "None")[
        if (count vehicles in-cone 25 70 < 2) [forward 0.8]                                     ; Change according to speed, change in-cone xx for changing teh spacing
        set xcor  precision xcor 3
        set ycor  precision ycor 3
      ]
    ]
  ]


  ask products with [ProductState = "Releasing"][
    forward 0.32                                          ; Speed of releasing product
    set xcor  precision xcor 3
    set ycor  precision ycor 3
  ]
  ask products with [ProductState = "Exiting"][
    forward 0.32                                          ; Speed of existing product
    set xcor  precision xcor 3
    set ycor  precision ycor 3
  ]


end

to E-MachineEntry

  ask machines [
    let temporalMachineVar who

    if(count vehicles in-radius 2 with [VehicleState = "Moving" and VehicleDestinationNode = temporalMachineVar] = 1)[

      let temporalVehicleVar ""
      let TemporalOperationVar ""
      ask vehicles in-radius 2 [
        set temporalVehicleVar who
        move-to machine temporalMachineVar
        ask product VehicleWithProduct [move-to machine temporalMachineVar]
      ]
      set MachineState "MachineBusy"
      let temporalX xcor
      let temporalY ycor
      set MachineWithVehicle item 0 [who] of vehicles with [xcor = temporalX and ycor = temporalY]
      set MachineProcessingProduct [VehicleWithProduct] of vehicle MachineWithVehicle
      ask vehicle MachineWithVehicle [
        set VehicleState "WaitingMachine"
      ]
      ask product MachineProcessingProduct[
        set ProductState "Being-Processed"
        set ProductStartOperation lput SimulationTime ProductStartOperation
        set ProductInMachine TemporalMachineVar
        set TemporalOperationVar item ProductNextOperation ProductOperations
      ]
      set MachineNextCompletion SimulationTime + item (position TemporalOperationVar MachinePossibleOperations) MachineOperProcessingTime
    ]
  ]


end

to F-MachineExit

  ask machines [
    let MachineTemp who
    if (MachineNextCompletion <= SimulationTime) [
      let TemporalDestNodeVar ""
      ask product MachineProcessingProduct[
        set ProductState "Transport"
        set ProductCurrentOperation (length ProductCompletionOperation)
        set ProductCompletionOperation lput SimulationTime ProductCompletionOperation
        set ProductNextOperation ProductCurrentOperation + 1
        set ProductInMachine "-"
        let TemporalProNextOperVar item ProductNextOperation ProductOperations
        ifelse(length ProductCompletionOperation < (length productoperations) - 1)[
          set TemporalDestNodeVar [who] of machines with [item 0 MachinePossibleOperations = TemporalProNextOperVar]
        ][
          set TemporalDestNodeVar (list 11)
        ]
      ]
      ask vehicle MachineWithVehicle[
        set VehicleState "Moving"
        set VehicleDestinationNode item 0 TemporalDestNodeVar
        set VehicleDestinationEntity "Machine"
        ifelse (MachineTemp <= 5)[
          set VehicleSpeed-X 0
          set VehicleSpeed-Y -0.8
          set VehicleSpeed-Total 0.8
        ][
          set VehicleSpeed-X 0
          set VehicleSpeed-Y 0.8
          set VehicleSpeed-Total 0.8
        ]
      ]
      set MachineState "MachineIdle"
      set MachineNextCompletion  10000000
      set MachineProcessingProduct "-"
      set MachineWithVehicle "-"
    ]
  ]

end

to G-RechargingStationEntry

end

to H-RechargingStationExit

end

to I-CompletingProduct


  ask vehicles with [xcor >= 33.6 and xcor <= 34.4 and ycor >= 49.6 and ycor <= 50.4][
    if(VehicleWithProduct != "None")[
      move-to turtle 11
      set heading 180
      if (VehicleType = "T1") [set shape "t1"]
      if (VehicleType = "T2") [set shape "t2"]
      if (VehicleType = "T3") [set shape "t3"]
      set VehicleState "Moving"
      ask Product VehicleWithProduct [
        set ProductState "Exiting"
        set heading 270
        set ProductCurrentOperation ProductCurrentOperation + 1
        set ProductnextOperation "finished"
        set ProductStartOperation lput SimulationTime ProductStartOperation
      ]
      set VehicleWithProduct "None"
      set VehicleDestinationNode 22
      set vehicleDestinationEntity "ExitingVehicle"
      let tempVehicleAssignStation who
      if (VehicleBatteryCharge <= 10 and (count vehicles with [VehicleState =  "GoingCharger"] + count vehicles with [VehicleState = "Charging"]) < 5) [
        set VehicleState  "GoingCharger"
        set vehicleDestinationEntity "ChargingStation"
        set VehicleDestinationNode one-of Recharge-Stations with [Rech.ReservedForVehicle =  "None"]
        face VehicleDestinationNode
        ask VehicleDestinationNode [
           set Rech.ReservedForVehicle tempVehicleAssignStation
        ]
        set VehicleSpeed-X 0.8
        set VehicleSpeed-Y 0
        set VehicleSpeed-Total 0.8
      ]
    ]
  ]

  ask products with [xcor >= 22.7 and xcor <= 23.3 and ycor >= 49.7 and ycor <= 50.3][
    if(ProductState != "Finished")[
      set ProductCompletionOperation lput SimulationTime ProductCompletionOperation
      set ProductState "Finished"
    ]
  ]
end

to J-CreatingProductionOrder

  if (Default = True)[
    K-CreatingProduct "P-504" "AA" 0 2000
    K-CreatingProduct "P-504" "HH" 1 2000
    K-CreatingProduct "P-504" "AA" 2 2000
    K-CreatingProduct "P-504" "HH" 3 2000
    K-CreatingProduct "P-504" "AA" 4 2000
    K-CreatingProduct "P-504" "AA" 5 2000
    K-CreatingProduct "P-504" "AA" 6 2000
    K-CreatingProduct "P-504" "HH" 7 2000
    K-CreatingProduct "P-504" "AA" 8 2000
    K-CreatingProduct "P-504" "HH" 9 2000
    K-CreatingProduct "P-504" "AA" 0.1 2000
    K-CreatingProduct "P-504" "HH" 0.2 2000
    K-CreatingProduct "P-504" "AA" 12 2000
    K-CreatingProduct "P-504" "HH" 13 2000
    K-CreatingProduct "P-504" "AA" 14 2000
  ]

  if (Default = False)[
    K-CreatingProduct "P-504" "AA" 0 2000
  ]

end

to K-CreatingProduct [#1 #2 #3 #4] ; #1: Id of product, #2: Type of product, #3: Order of Release, #4: Due date of product

  create-products 1 [
    move-to turtle 17
    set heading 90
    set shape "circle"
    set color blue
    set size 5.5
    set ProductID #1
    set ProductType #2
    if (productType = "AA") [set ProductWeight 20 set ProductOperations (list "OP0" "OP1" "OP4" "OP7" "OP11")]
    if (productType = "BB") [set ProductWeight 20 set ProductOperations (list "OP0" "OP1" "OP5" "OP8" "OP11")]
    if (productType = "CC") [set ProductWeight 20 set ProductOperations (list "OP0" "OP1" "OP3" "OP9" "OP11")]
    if (productType = "DD") [set ProductWeight 20 set ProductOperations (list "OP0" "OP1" "OP4" "OP6" "OP8" "OP11")]
    if (productType = "EE") [set ProductWeight 20 set ProductOperations (list "OP0" "OP2" "OP5" "OP6" "OP9" "OP11")]
    if (productType = "FF") [set ProductWeight 30 set ProductOperations (list "OP0" "OP1" "OP5" "OP7" "OP11")]
    if (productType = "GG") [set ProductWeight 30 set ProductOperations (list "OP0" "OP2" "OP5" "OP8" "OP11")]
    if (productType = "HH") [set ProductWeight 30 set ProductOperations (list "OP0" "OP3" "OP5" "OP9" "OP11")]
    if (productType = "II") [set ProductWeight 30 set ProductOperations (list "OP0" "OP3" "OP4" "OP6" "OP10" "OP11")]
    if (productType = "JJ") [set ProductWeight 30 set ProductOperations (list "OP0" "OP3" "OP5" "OP7" "OP10" "OP11")]
; ProductOperations as integer
;    if (productType = "AA") [set ProductWeight 20 set ProductOperations (list 0 1 4 7 11)]
;    if (productType = "BB") [set ProductWeight 20 set ProductOperations (list 0 1 5 8 11)]
;    if (productType = "CC") [set ProductWeight 20 set ProductOperations (list 0 1 3 9 11)]
;    if (productType = "DD") [set ProductWeight 20 set ProductOperations (list 0 1 4 6 8 11)]
;    if (productType = "EE") [set ProductWeight 20 set ProductOperations (list 0 2 5 6 9 11)]
;    if (productType = "FF") [set ProductWeight 30 set ProductOperations (list 0 1 5 7 11)]
;    if (productType = "GG") [set ProductWeight 30 set ProductOperations (list 0 2 5 8 11)]
;    if (productType = "HH") [set ProductWeight 30 set ProductOperations (list 0 3 5 9 11)]
;    if (productType = "II") [set ProductWeight 30 set ProductOperations (list 0 3 4 6 10 11)]
;    if (productType = "JJ") [set ProductWeight 30 set ProductOperations (list 0 3 5 7 10 11)]
    set ProductState "To-be-released"
    set ProductReleaseOrder #3
    set ProductDueDate #4
    set ProductCurrentOperation "-"
    set ProductNextOperation 0
    set ProductStartOperation[]
    set ProductCompletionOperation[]
    set ProductInVehicle "-"
    set ProductInMachine "-"
  ]

end

to L-CreatingVehiclesFleet [#1]     ; #1 List of Type of Vehicles (T1, T2, T3). Order give order of loading. Length give number of vehicles
                                    ;
  let NumberVehicles length #1

  let i 0
  repeat NumberVehicles [
    create-vehicles 1 [

      let CurretVehicles count vehicles with [xcor >= 5 and xcor <= 30 and ycor >= 20 and ycor <= 110]

      if(CurretVehicles = 0) [setxy 24 105 set heading 90]
      if(CurretVehicles = 1) [setxy 17 105 set heading 90]
      if(CurretVehicles = 2) [setxy 10 105 set heading 90]
      if(CurretVehicles > 2)[setxy 10 105 - 7 * (CurretVehicles - 2) set heading 0]
      set color Red
      set size 8
      set VehicleID (word "AGV-" (i + 1) )
      set VehicleType item i #1
      set VehicleState "WaitingOutside"
      if (VehicleType = "T1") [set VehicleBattery 21 set shape "t1" set VehicleBatteryCharge 21]
      if (VehicleType = "T2") [set VehicleBattery 42 set shape "t2" set VehicleBatteryCharge 42]
      if (VehicleType = "T3") [set VehicleBattery 63 set shape "t3" set VehicleBatteryCharge 63]
      set VehicleDestinationNode 0
      set VehicleDestinationEntity "LoadingStation"
      set VehicleSpeed-X 0.8
      set VehicleSpeed-Y 0
      set VehicleSpeed-Total 0.8
      set VehicleWithProduct "None"
    ]
    set i i + 1
  ]

end

to M-ChangeSpeedVehicle [#1 #2 #3] ; #1: Which Vehicle, #2: Speed in X-Axis, #3: Speed in Y-Axis

  ask vehicle #1 [
    set VehicleSpeed-X #2
    set VehicleSpeed-Y #3
  ]

end


to N-UpdateBateryDecharging

  ask vehicles with [VehicleState = "Moving" or VehicleState ="WaitingOutside"][

    let loaded ""
    ifelse(VehicleWithProduct = "None") [set loaded 0][set loaded 1]

    set VehicleBatteryCharge VehicleBatteryCharge - ((0.00434 * VehicleSpeed-Total) / 20) - ((0.00434 * 0.5 * Loaded) / 20)   ; Check if it is ok the tick as it is divided by 20
    set VehicleBatteryCharge precision VehicleBatteryCharge 6

  ]

end

to O-MovingToChargers

  ask vehicles with [VehicleState = "GoingCharger"][
    set heading precision heading 3
    if (count vehicles in-cone 10 40 < 2) [forward VehicleSpeed-Total]                                     ; Change according to speed
    set xcor  precision xcor 3
    set ycor  precision ycor 3
    set VehicleSpeed-Total 0.8
    set VehicleSpeed-X VehicleSpeed-Total * cos W-HeadingToAngle heading
    set VehicleSpeed-Y VehicleSpeed-Total * sin W-HeadingToAngle heading
    set VehicleSpeed-X precision VehicleSpeed-X 3
    set VehicleSpeed-Y precision VehicleSpeed-Y 3
    set VehicleSpeed-Total 0.8
  ]

end

to P-EnteringChargers

  ask recharge-stations [
    let tempRechargerStationVar who
    let dischargelevel ""
    let full ""
    let TempVehicleEntering ""
    if(count vehicles in-radius 2 with [VehicleState = "GoingCharger"] = 1)[
      ask vehicles in-radius 2 [
        set TempVehicleEntering who
        move-to recharge-station tempRechargerStationVar
        set VehicleState "Charging"
        set dischargelevel ((100 - (VehicleBatteryCharge / VehicleBattery))/ 100)
        set Full VehicleBattery
      ]
      set Rech.WithVehicle TempVehicleEntering
      set Rech.State "StationBusy"
      set Rech.NextCompletion SimulationTime + (121 * exp(2.7 * dischargelevel) * (Full / 21))
    ]
  ]



end

to R-ExitingChargers

  ask recharge-stations [
    let tempVehicle ""
    if (Rech.NextCompletion <= SimulationTime) [

      ask vehicle  Rech.WithVehicle [
        set VehicleState "Moving"
        face turtle 22
        set VehicleBatteryCharge VehicleBattery
      ]
      set Rech.State "StationIdle"
      set Rech.NextCompletion 1000000000



    ]
  ]

end

to V-MovementVehicleOutside

  ask vehicles with [VehicleState = "WaitingOutside"][
    ifelse(count vehicles in-cone 12 60 <= 1) [
      forward 0.8
      if (heading = 0) [set VehicleSpeed-X 0 set VehicleSpeed-Y 0.8 set VehicleSpeed-Total 0.8]
      if (heading = 90) [set VehicleSpeed-X 0.8 set VehicleSpeed-Y 0 set VehicleSpeed-Total 0.8]
      if (heading = 270) [set VehicleSpeed-X -0.8 set VehicleSpeed-Y 0 set VehicleSpeed-Total 0.8]
      set xcor  precision xcor 3
      set ycor  precision ycor 3
    ][
      set VehicleSpeed-X 0
      set VehicleSpeed-Y 0
      set VehicleSpeed-Total 0
    ]
  ]

  ask vehicles with [xcor = 10 and ycor >= 104.5 and ycor <= 105.5] [move-to turtle 20 set heading 90]  ; turn
  ask vehicles with [xcor >= 9.5 and xcor <= 10.5 and ycor = 15] [move-to turtle 21 set heading 0]      ; turn


  ask vehicles with [xcor >= 33.5 and xcor <= 34.5 and ycor = 105] [move-to turtle 19 set VehicleState "Stand-By" face turtle 0 set VehicleSpeed-X 0 set VehicleSpeed-Y 0 set VehicleSpeed-Total 0]      ; Entering
  ask vehicles with [xcor >= 33.5 and xcor <= 34.5 and ycor >= 14.5 and ycor <= 15.5] [move-to turtle 22 set heading 270 set VehicleState "WaitingOutside"]      ; Exiting


  let TempVehiclesInTransit count vehicles with [xcor >= 32 and xcor <= 36 and ycor >= 70.5 and ycor <= 102]
  let TempProductsToBeReleased count products with [ProductState = "To-be-released"]

  ask vehicles with [xcor = 34 and ycor = 105] [if (TempProductsToBeReleased > TempVehiclesInTransit)[set VehicleState "Moving"]]

  ask vehicles with [xcor = 34 and ycor >= 69.5 and ycor <= 70.5] [move-to turtle 0 set VehicleState "WaitingLoading"]

end



to-report W-HeadingToAngle [#1]
  report (90 - #1) mod 360
end

to X-SetupMachines

  ask machine 1 [set MachineID "M1" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP1")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 2 [set MachineID "M2" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP2")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 3 [set MachineID "M3" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP3")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 4 [set MachineID "M4" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP4")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 5 [set MachineID "M5" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP5")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]

  ask machine 6 [set MachineID "M6" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP6")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 7 [set MachineID "M7" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP7")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 8 [set MachineID "M8" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP8")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 9 [set MachineID "M9" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP9")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]
  ask machine 10 [set MachineID "M10" set MachineType "Normal" set MachineState "MachineIdle" set MachinePossibleOperations  (list "OP10")  set MachineOperProcessingTime  (list 30) set MachineNextCompletion  100000000 set MachineProcessingProduct "-"]


end

to Y-Setup-Corridor

  ask patches with [pxcor > 5 and pxcor < 15 and pycor > 10 and pycor < 110] [set pcolor 29.5]       ; Vehicle Corridor
  ask patches with [pxcor > 14 and pxcor < 29 and pycor > 100 and pycor < 110] [set pcolor 29.5]     ; Vehicle Corridor
  ask patches with [pxcor > 27 and pxcor < 30 and pycor > 100 and pycor < 110] [set pcolor green + 4]; Vehicle Corridor
  ask patches with [pxcor = 30 and pycor > 100 and pycor < 110] [set pcolor green + 2]; Vehicle Corridor
  ask patches with [pxcor > 14 and pxcor < 29 and pycor > 10 and pycor < 20] [set pcolor 29.5]       ; Vehicle Corridor
  ask patches with [pxcor > 27 and pxcor < 30 and pycor > 10 and pycor < 20] [set pcolor red + 4]                   ; Vehicle Corridor
  ask patches with [pxcor = 30 and pycor > 10 and pycor < 20] [set pcolor red + 2]

  create-turtles 1 [setxy 34 105 set shape "circle" set size 0.5 set color green set heading 0]     ; Loading AGVs
  create-turtles 1 [setxy 10 105 set shape "circle" set size 0.5 set color orange set heading 0]     ; Node
  create-turtles 1 [setxy 10 15 set shape "circle" set size 0.5 set color orange set heading 0]      ; Node
  create-turtles 1 [setxy 34 15 set shape "circle" set size 0.5 set color red set heading 0]        ; Un-Loading AGVs

  ask turtle 22 [create-link-to turtle 21] ask link 22 21 [set color orange + 3]
  ask turtle 21 [create-link-to turtle 20] ask link 21 20 [set color orange + 3]
  ask turtle 20 [create-link-to turtle 19] ask link 20 19 [set color orange + 3]

  ask patches with [pxcor = 5 and pycor >= 10 and pycor <= 110][ifelse pycor mod 2 = 0[set pcolor 2][set pcolor 28]]  ; Left border
  ask patches with [pxcor = 15 and pycor >= 20 and pycor <= 100][ifelse pycor mod 2 = 0[set pcolor 2][set pcolor 28]] ; Left border
  ask patches with [pxcor > 5 and pxcor < 30 and pycor = 10][ifelse pxcor mod 2 = 0[set pcolor 28][set pcolor 2]]    ; Bottom border
  ask patches with [pxcor > 15 and pxcor < 30 and pycor = 20][ifelse pxcor mod 2 = 0[set pcolor 28][set pcolor 2]]    ; Bottom border
  ask patches with [pxcor > 15 and pxcor < 30 and pycor = 100][ifelse pxcor mod 2 = 0[set pcolor 28][set pcolor 2]]   ; Upper border
  ask patches with [pxcor > 5 and pxcor < 30 and pycor = 110][ifelse pxcor mod 2 = 0[set pcolor 28][set pcolor 2]]   ; Upper border


end

to Z-Layout

  ask patches [set pcolor 9.9]
  ask patches with [pxcor > 30 and pxcor < 260 and pycor > 10 and pycor < 110] [set pcolor 99]

  ask patches with [pxcor = 30 and pycor >= 10 and pycor <= 110][ifelse pycor mod 2 = 0[set pcolor 3][set pcolor 48]]  ; Left border
  ask patches with [pxcor = 260 and pycor >= 10 and pycor <= 110][ifelse pycor mod 2 = 0[set pcolor 3][set pcolor 48]] ; Right border
  ask patches with [pxcor > 30 and pxcor < 260 and pycor = 10][ifelse pxcor mod 2 = 0[set pcolor 3][set pcolor 48]]    ; Bottom border
  ask patches with [pxcor > 30 and pxcor < 260 and pycor = 110][ifelse pxcor mod 2 = 0[set pcolor 3][set pcolor 48]]   ; Upper border

  ask patches with [pxcor > 30 and pxcor <= 38 and pycor >= 66 and pycor <= 74] [set pcolor 98] ; Loading-position
  ask patches with [pxcor > 30 and pxcor <= 38 and pycor >= 46 and pycor <= 54] [set pcolor 98] ; Uploading-position

  ask patches with [pxcor >= 252 and pxcor < 260 and pycor >= 76 and pycor <= 84] [set pcolor 68] ; Charging station R1
  ask patches with [pxcor >= 252 and pxcor < 260 and pycor >= 66 and pycor <= 74] [set pcolor 68] ; Charging station R2
  ask patches with [pxcor >= 252 and pxcor < 260 and pycor >= 56 and pycor <= 64] [set pcolor 68] ; Charging station R3
  ask patches with [pxcor >= 252 and pxcor < 260 and pycor >= 46 and pycor <= 54] [set pcolor 68] ; Charging station R4
  ask patches with [pxcor >= 252 and pxcor < 260 and pycor >= 36 and pycor <= 44] [set pcolor 68] ; Charging station R5

  ask patches with [pxcor >= 101 and pxcor < 109 and pycor >= 102 and pycor < 110] [set pcolor 49]  ; M1-position
  ask patches with [pxcor >= 131 and pxcor < 139 and pycor >= 102 and pycor < 110] [set pcolor 49]  ; M2-position
  ask patches with [pxcor >= 161 and pxcor < 169 and pycor >= 102 and pycor < 110] [set pcolor 49]  ; M3-position
  ask patches with [pxcor >= 191 and pxcor < 199 and pycor >= 102 and pycor < 110] [set pcolor 49]  ; M4-position
  ask patches with [pxcor >= 221 and pxcor < 229 and pycor >= 102 and pycor < 110] [set pcolor 49]  ; M5-position

  ask patches with [pxcor >= 101 and pxcor < 109 and pycor > 10 and pycor <= 18] [set pcolor 49]  ; M6-position
  ask patches with [pxcor >= 131 and pxcor < 139 and pycor > 10 and pycor <= 18] [set pcolor 49]  ; M7-position
  ask patches with [pxcor >= 161 and pxcor < 169 and pycor > 10 and pycor <= 18] [set pcolor 49]  ; M8-position
  ask patches with [pxcor >= 191 and pxcor < 199 and pycor > 10 and pycor <= 18] [set pcolor 49]  ; M9-position
  ask patches with [pxcor >= 221 and pxcor < 229 and pycor > 10 and pycor <= 18] [set pcolor 49]  ; M10-position



  create-turtles 1 [setxy 34 70 set shape "circle" set size 1 set color black set heading 0]          ; Loading Node

  create-machines 1 [setxy 104.5 105.5 set shape "circle" set size 1 set color black set heading 0]    ; Processing Node M1
  create-machines 1 [setxy 134.5 105.5 set shape "circle" set size 1 set color black set heading 0]    ; Processing Node M2
  create-machines 1 [setxy 164.5 105.5 set shape "circle" set size 1 set color black set heading 0]    ; Processing Node M3
  create-machines 1 [setxy 194.5 105.5 set shape "circle" set size 1 set color black set heading 0]    ; Processing Node M4
  create-machines 1 [setxy 224.5 105.5 set shape "circle" set size 1 set color black set heading 0]    ; Processing Node M5

  create-machines 1 [setxy 104.5 14.5 set shape "circle" set size 1 set color black set heading 0]     ; Processing Node M6
  create-machines 1 [setxy 134.5 14.5 set shape "circle" set size 1 set color black set heading 0]     ; Processing Node M7
  create-machines 1 [setxy 164.5 14.5 set shape "circle" set size 1 set color black set heading 0]     ; Processing Node M8
  create-machines 1 [setxy 194.5 14.5 set shape "circle" set size 1 set color black set heading 0]     ; Processing Node M9
  create-machines 1 [setxy 224.5 14.5 set shape "circle" set size 1 set color black set heading 0]     ; Processing Node M10

  create-turtles 1 [setxy 34 50 set shape "circle" set size 1 set color black set heading 0]          ; Unloading Node


  create-Recharge-Stations 1 [setxy 256 80 set shape "circle" set size 1 set color black set heading 0 set Rech.ReservedForVehicle "None" set Rech.State "StationIdle" set Rech.NextCompletion 1000000000]         ; Recharging Node R1
  create-Recharge-Stations 1 [setxy 256 70 set shape "circle" set size 1 set color black set heading 0 set Rech.ReservedForVehicle "None" set Rech.State "StationIdle" set Rech.NextCompletion 1000000000]         ; Recharging Node R2
  create-Recharge-Stations 1 [setxy 256 60 set shape "circle" set size 1 set color black set heading 0 set Rech.ReservedForVehicle "None" set Rech.State "StationIdle" set Rech.NextCompletion 1000000000]         ; Recharging Node R3
  create-Recharge-Stations 1 [setxy 256 50 set shape "circle" set size 1 set color black set heading 0 set Rech.ReservedForVehicle "None" set Rech.State "StationIdle" set Rech.NextCompletion 1000000000]         ; Recharging Node R4
  create-Recharge-Stations 1 [setxy 256 40 set shape "circle" set size 1 set color black set heading 0 set Rech.ReservedForVehicle "None" set Rech.State "StationIdle" set Rech.NextCompletion 1000000000]         ; Recharging Node R5

  create-turtles 1 [setxy 23 70 set shape "Circle" set size 8 set color green + 2 set heading 0]
  create-turtles 1 [setxy 23 50 set shape "Circle" set size 8 set color red + 2 set heading 0]
  ask turtle 17 [create-link-to turtle 0]
  ask turtle 18 [create-link-from turtle 11]


end
@#$#@#$#@
GRAPHICS-WINDOW
127
10
1259
503
-1
-1
4.0
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
280
0
120
0
0
1
ticks
24.0

BUTTON
11
18
77
51
Setup
A-setup
NIL
1
T
OBSERVER
NIL
A
NIL
NIL
1

BUTTON
11
54
78
87
Step
B-go
NIL
1
T
OBSERVER
NIL
S
NIL
NIL
1

BUTTON
11
91
79
124
Play
B-go
T
1
T
OBSERVER
NIL
D
NIL
NIL
1

SWITCH
9
278
112
311
Default
Default
0
1
-1000

BUTTON
12
128
75
161
10x
repeat 10 [B-go]
NIL
1
T
OBSERVER
NIL
Z
NIL
NIL
1

MONITOR
8
318
114
363
Time (s)
SimulationTime
1
1
11

BUTTON
19
380
82
413
Up
up
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
1
418
56
451
Left
Left-Arrow
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
60
418
115
451
Right
right-arrow
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
19
456
85
489
Down
down
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

newsquare-t1
false
0
Polygon -7500403 true true 30 150 30 60 60 30 240 30 270 60 270 240 240 270 60 270 30 240 30 150
Polygon -1 true false 60 30 60 60 120 60 120 30
Circle -13791810 true false 45 45 210

newsquare-t2
false
0
Polygon -7500403 true true 30 150 30 60 60 30 240 30 270 60 270 240 240 270 60 270 30 240 30 150
Polygon -1 true false 120 30 120 60 180 60 180 30
Circle -13791810 true false 45 45 210

newsquare-t3
false
0
Polygon -7500403 true true 30 150 30 60 60 30 240 30 270 60 270 240 240 270 60 270 30 240 30 150
Polygon -1 true false 180 30 180 60 240 60 240 30
Circle -13791810 true false 45 45 210

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

t1
false
0
Polygon -7500403 true true 30 60 30 240 60 270 240 270 270 240 270 60 240 30 60 30 30 60
Polygon -1 true false 60 30 60 60 120 60 120 30

t2
false
0
Polygon -7500403 true true 30 60 30 240 60 270 240 270 270 240 270 60 240 30 60 30 30 60
Polygon -1 true false 120 30 120 60 180 60 180 30

t3
false
0
Polygon -7500403 true true 30 60 30 240 60 270 240 270 270 240 270 60 240 30 60 30 30 60
Polygon -1 true false 180 30 180 60 240 60 240 30

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

wall
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
@#$#@#$#@
0
@#$#@#$#@

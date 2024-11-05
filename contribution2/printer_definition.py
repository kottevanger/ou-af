# structure of the laser printer
structure_laserprinter = {
    "name":"structure_laserprinter",
    "components": {
        "1":{
            "name":"LaserDiode",
            "type":"LaserDiode"
        },
        "2":{
            "name":"Mirror6Sided",
            "type":"Mirror6Sided"           
        },
        "3":{
            "name":"AcrylicLens",
            "type":"AcrylicLens"           
        }          
    },
    "connections":{
        "1":{
            "name":"Beam1",
            "type":"Beam1",
            "startComponent":"LaserDiode",
            "endComponent":"Mirror6Sided"
        },
        "2":{
            "name":"Beam2",
            "type":"Beam2",
            "startComponent":"Mirror6Sided",
            "endComponent":"AcrylicLens"
        }
    }
}

# connections of the laser printer
beam1 = {
    "type":"Beam1",
    "start":"PresentLaserBeamOutputs",
    "typeStart":"LaserDiode",
    "end":"PresentLaserBeamInputs",
    "typeEnd":"Mirror6Sided",
    "Healths":{
        "1":{
            "modality":"Health",
            "property":"health",
            "propertyvalues":["ok","broken"],
            "priorprobability":[0.9,0.1]
        }
    },
    "Behavior":{
        "normal": {
            'PresentLaserBeamOutputs' :   ["yes", "no"],
            'PresentLaserBeamInputs'  :   ["yes", "no"],
            'health'                  :   ["ok",  "ok"]
        }
    }
}

beam2 = {
    "type":"Beam2",
    "start":"PresentLaserBeamOutputs",
    "typeStart":"Mirror6Sided",
    "end":"PresentLaserBeamInputs",
    "typeEnd":"AcrylicLens",
    "Healths":{
        "1":{
            "modality":"Health",
            "property":"health",
            "propertyvalues":["ok","broken"],
            "priorprobability":[0.9,0.1]
        }
    },
    "Behavior":{
        "normal": {
            'PresentLaserBeamOutputs' :   ["yes", "no"],
            'PresentLaserBeamInputs'  :   ["yes", "no"],
            'health'                  :   ["ok",  "ok"]
        }
    }
}

# components of the laser printer.
laser_diode = {
    "type":"LaserDiode",
    "Inputs":{
        "1":{
            "modality":"Power", 
            "property":"Present",
            "propertyvalues":["yes", "no"],
            "priorprobability":[0.99,0.01]        }
    },
    "Outputs":{
        "1":{
            "modality":"LaserBeam",
            "property":"Present",
            "propertyvalues":["yes", "no"]
        }
    },
    "Healths":{
        "1":{
            "modality":"Health",
            "property":"health",
            "propertyvalues":["ok","broken"],
            "priorprobability":[0.98,0.02]
        }
    },
    "Decisions":{
        "1":{
            "name":"Replace",
            "values":["yes", "no"],
            "replacementcosts": 150,
            "incorrectreplacementcosts": 150,
            "failuretorepaircosts": 800
            }
    },
    "Behavior":{
        "normal": {
            'PresentPowerInputs':      ["yes", "no"], 
            'PresentLaserBeamOutputs': ["yes", "no"],
            'health':                  ["ok",  "ok"]
        }
    }
}

mirror_6_sided = {
    "type":"Mirror6Sided",
    "Inputs":{
        "1":{
            "modality":"LaserBeam",
            "property":"Present",
            "propertyvalues":["yes", "no"],
            "priorprobability":[0.99,0.01]        }
    },
    "Outputs":{
        "1":{
            "modality":"LaserBeam",
            "property":"Present",
            "propertyvalues":["yes", "no"]
        }
    },
    "Healths":{
        "1":{
            "modality":"Health",
            "property":"health",
            "propertyvalues":["ok","broken"],
            "priorprobability":[0.98,0.02]
        }
    },
    "Decisions":{
        "1":{
            "name":"Replace",
            "values":["yes", "no"],
            "replacementcosts": 151,
            "incorrectreplacementcosts": 150,
            "failuretorepaircosts": 800
            }
    },
    "Behavior":{
        "normal": {
            'PresentLaserBeamInputs':  ["yes", "no"], 
            'PresentLaserBeamOutputs': ["yes", "no"],
            'health':                  ["ok",  "ok"]
        }
    }
}

acrylic_lens = {
    "type":"AcrylicLens",
    "Inputs":{
        "1":{
            "modality":"LaserBeam",
            "property":"Present",
            "propertyvalues":["yes", "no"],
            "priorprobability":[0.99,0.01]        }
    },
    "Outputs":{
        "1":{
            "modality":"LaserBeam",
            "property":"Present",
            "propertyvalues":["yes", "no"]
        }
    },
    "Healths":{
        "1":{
            "modality":"Health",
            "property":"health",
            "propertyvalues":["ok","broken"],
            "priorprobability":[0.98,0.02]
        }
    },
    "Decisions":{
        "1":{
            "name":"Replace",
            "values":["yes", "no"],
            "replacementcosts": 152,
            "incorrectreplacementcosts": 150,
            "failuretorepaircosts": 800
            }
    },
    "Behavior":{
        "normal": {
            'PresentLaserBeamInputs':  ["yes", "no"], 
            'PresentLaserBeamOutputs': ["yes", "no"],
            'health':                  ["ok",  "ok"]
        }
    }
}

testObserveHealth = {
        "name":"TestObserveHealth",
        "typeUndertest":"AcrylicLens",
        "decisionvalues":["yes", "no"],
        "testoutcomevalues":["clean","dirty", "notdone"],
        "testcosts": 100,
        "testoutcomecpt":{
            'health':                    ["ok",     "broken" , "ok"     ,"broken"],
            'DecisionTestObserveHealth': ["no",     "no"     , "yes"    ,"yes"   ],
            "TestObserveHealth":         ["notdone","notdone", "clean"  ,'dirty']
        }
    }

testmapping3 = {
    "1":{
        "test":"TestObserveHealth",
        "target":"AcrylicLens"
    }
}
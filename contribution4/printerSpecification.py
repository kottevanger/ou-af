states = [
    {'id' : 1, 'value' : 'yes'},  
    {'id' : 2, 'value' : 'no'},
    {'id' : 3, 'value' : 'high'},   
    {'id' : 4, 'value' : 'low'},
    {'id' : 5, 'value' : 'ok'}, 
    {'id' : 6, 'value' : 'broken'} 
]

modalities = [
    {'id' : 1, 'name' : 'power', 'states' : [3, 4]},
    {'id' : 2, 'name' : 'control_signal', 'states' : [1, 2]},
    {'id' : 3, 'name' : 'movement', 'states' : [1, 2]},
    {'id' : 4, 'name' : 'power', 'states' : [3, 4]},
    {'id' : 5, 'name' : 'laser_beam', 'states' : [1, 2]},
    {'id' : 6, 'name' : 'image_in_toner', 'states' : [1, 2]},
    {'id' : 7, 'name' : 'moving_beam', 'states' : [1, 2]},
    {'id' : 8, 'name' : 'toner_particles', 'states' : [1, 2]},
    {'id' : 9, 'name' : 'moving_toner_particles', 'states' : [1, 2]},
    {'id' : 10, 'name' : 'electrical_charge', 'states' : [3, 4]},
    {'id' : 11, 'name' : 'focussed_laser_beam', 'states' : [1, 2]}
]

behaviours = [
        # Behaviour of wiper blade. Input is power and control signal, output is movement.
        {
            'id' : 1, 
            'name' : 'wiper_blade_behaviour', 
            'input' : [
                1, {'prior' : [0.98, 0.02]},
                2, {'prior' : [0.98, 0.02]}],
            'output' : 3,
            'normal' : [
                ['high', 'yes', 'yes'],
                {'else' : 'no'}]
        },
        # Behaviour of lens. Input is laser beam, output is focussed laser beam.
        {
            'id' : 2, 
            'name' : 'lens_behaviour', 
            'input' : [
                5, {'prior' : [0.98, 0.02]}],
            'output' : 11,
            'normal' : [
                ['yes', 'yes'],
                {'else' : 'no'}]
        },  
        # Behaviour of tilted mirror. Input is laser beam, power and control signal, output is moving laser beam.
        {
            'id' : 3, 
            'name' : 'tilted_mirror_behaviour', 
            'input' : [
                11, {'prior' : [0.98, 0.02]},
                1, {'prior' : [0.98, 0.02]},
                2, {'prior' : [0.98, 0.02]}],
            'output' : 7,
            'normal' : [
                ['yes', 'high', 'yes', 'yes'],
                {'else' : 'no'}]
        },
        # Behaviour of developer roll. Input is power and toner particles, output is moving toner particles.
        {
            'id' : 4, 
            'name' : 'developer_roll_behaviour', 
            'input' : [
                1, {'prior' : [0.98, 0.02]},
                8, {'prior' : [0.98, 0.02]}],
            'output' : 9,
            'normal' : [
                ['high', 'yes', 'yes'],
                {'else' : 'no'}]
        },
        # Behaviour of charge roll. Input is power, output is electrical charge.
        {
            'id' : 5, 
            'name' : 'charge_roll_behaviour', 
            'input' : [
                1, {'prior' : [0.98, 0.02]}],
            'output' : 10,
            'normal' : [
                ['high', 'high'],
                {'else' : 'no'}]
        },
        # Behaviour of photo conductor drum. Input is wiper movement, moving beam, moving toner particles, electrical charge. Output is an image in toner particals on the drum.
        {
            'id' : 6, 
            'name' : 'drum_behaviour',
            'input' : [
                3, None,
                7, None,
                9, None,
                10, None],
            'output' : 6,
            'normal' : [
                ['yes', 'yes'],
                {'else' : 'no'}]
        }
    ]

components = [
        # Wiper blade with health ok or broken.
        {
            'id' : 1, 
            'name' : 'wiper_blade', 
            'behaviours' : [1],
            'health' :  { 
                'states' :  [5, 6],
                'prior' :   [0.99, 0.01]
            } 
        },
        # Lens with health ok or broken.
        {
            'id' : 2, 
            'name' : 'lens', 
            'behaviours' : [2],
            'health' :  { 
                'states' :  [5, 6],
                'prior' :   [0.99, 0.01]
            }
        },
        # Tilted mirror with health ok or broken.
        {
            'id' : 3, 
            'name' : 'tilted_mirror', 
            'behaviours' : [3],
            'health' :  { 
                'states' :  [5, 6],
                'prior' :   [0.99, 0.01]
            } 
        },
        # Developer roll with health ok or broken.
        {
            'id' : 4, 
            'name' : 'developer_roll', 
            'behaviours' : [4],
            'health' :  { 
                'states' :  [5, 6],
                'prior' :   [0.99, 0.01]
            } 
        },
        # Charge roll with health ok or broken.
        {
            'id' : 5, 
            'name' : 'charge_roll', 
            'behaviours' : [5],
            'health' :  { 
                'states' :  [5, 6],
                'prior' :   [0.99, 0.01]
            } 
        },
        # Photo conductor drum with health ok or broken.
        {
            'id' : 6, 
            'name' : 'drum', 
            'behaviours' : [6],
            'health' :  { 
                'states' :  [5, 6],
                'prior' :   [0.99, 0.01]
            }
        }        
    ]

assembly = [
        {'from' : ['wiper_blade','wiper_blade_behaviour','movement'], 'to' : ['drum','drum_behaviour','movement']},
        {'from' : ['lens','lens_behaviour','laser_beam'], 'to' : ['tilted_mirror','tilted_mirror_behaviour','focussed_laser_beam']},
        {'from' : ['tilted_mirror','tilted_mirror_behaviour','moving_beam'], 'to' : ['drum','drum_behaviour','moving_beam']},
        {'from' : ['developer_roll','developer_roll_behaviour','moving_toner_particles'], 'to' : ['drum','drum_behaviour','moving_toner_particles']},
        {'from' : ['charge_roll','charge_roll_behaviour','electrical_charge'], 'to' : ['drum','drum_behaviour','electrical_charge']}
    ]

test = [
        # Observe; is the mirror bright and clean?
        {
            'id' : 1,
            'test_type' : 1,
            'description' : 'Is the tilted mirror bright and clear.',
            'costs' : 200,
            'functional_chain' : ['tilted_mirror']
        },
        # Change input for the developer roll component.
        {
            'id' : 2,
            'test_type' : 2,
            'description' : 'Use a different type of toner.',
            'costs' : 1000,
            'functional_chain' : ['developer_roll']
        },
        # Replace the charge roller.
        {
            'id' : 3,
            'test_type' : 3,
            'description' : 'Replace the charge roller with a brand new one.',
            'costs' : 2000,
            'functional_chain' : ['charge_roll']
        },
        # Clean the drum by hand and print paper.
        {
            'id' : 4,
            'test_type' : 4,
            'description' : 'Clean drum by hand and print paper.',
            'costs' : 1000,
            'functional_chain' : ['wiper_blade']
        },
        # Manually project a laser beam on the drum.
        {
            'id' : 5,
            'test_type' : 4,
            'description' : 'Manually project a laser beam on the drum.',
            'costs' : 1000,
            'functional_chain' : ['lens', 'tilted_mirror']
        }
    ]
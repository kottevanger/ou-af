# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 22:54:02 2024

@author: KOTTEV
"""
import os

from pylab import *
import matplotlib.pyplot as plt
import math
import pyAgrum as gum
from itertools import product
import printerSpecification as spec
import xml.etree.ElementTree as ET
import pandas as pd

from problem3.assemblies import *
from problem3.components import *
from problem3.tests import *
from problem3.oopnclasses import Component
from problem3.oopnclasses import Tests

from importlib import reload
reload(spec)

def truncate_logfile():
    # Open the file in write mode to truncate it
    with open('logfile.txt', 'w') as file:
        # Truncate the file to zero bytes
        file.truncate()
truncate_logfile()
        
def write_to_logfile(log_line):
    # Open a file in write mode
    with open('logfile.txt', 'a') as file:
        # Write a single line
        file.write(log_line + '\n')
        file.flush()

def create_components():
    created_components = []
    component_types = [component["type"] for component in assembly["components"].values()]
    for component_type in component_types:
        new_component = Component(component_type, components[component_type], [])
        created_components.append(Component(component_type, components[component_type], []))
    return created_components   
        
def link_created_components(created_components):
    created_connections = []
    
    connections = [connection for connection in assembly["connections"].values()]
    for connection in connections:
        start = next((component for component in created_components if component.getName() == connection["startComponent"]), None)
        end = next((component for component in created_components if component.getName() == connection["endComponent"]), None)
        
        if start and end:
            end.getInputComponents().append(start)
            start.getOutputComponents().append(end)

    # Add connections between the different components.
    for component in created_components:
        output_node = [node for node in component.getNodes() if node.getType() == 'Output'][0]
        
        for output_component in component.getOutputComponents():
            output_node_next_component = [node for node in output_component.getNodes() if node.getType() == 'Output'][0]
            
            if (output_node and output_node_next_component):
                created_connections.append((output_node.getVariable().name(), output_node_next_component.getVariable().name()))
                break
            
    return created_connections

def create_influence_diagram(diagram):
    
    # Create the components.
    created_components = create_components()

    # Link the created components to one another.
    created_connections = link_created_components(created_components)
           
    for component in created_components:
        component.createInputNodes()
        component.setInternalConnections()      
        component.setPriorOutput()              
        component.setPriorHealth()              
        component.setPriorInputs()                  

    # Create the change nodes in the pyagrum diagram.
    for component in created_components:
        for node in component.getNodes():
            diagram.addChanceNode(node.getVariable())

        for connection in component.getInternalConnections():
            diagram.addArc(connection[0], connection[1])
    
    # add connections between components.
    for connection in created_connections:
        diagram.addArc(connection[0], connection[1])

    # fill health and Inputs probability tables.
    for component in created_components:
        for node in component.getNodes():
            potential_table = node.getPrior()
            cpt_table =  diagram.cpt(node.getName())
            cpt_table.fillWith((potential_table))
    
    # Add the decision node with tests.
    testUtil = Tests(tests)
    for component in created_components:
        testUtil.createUtilityNode(component)
    testUtil.createDecisionVar()
    diagram.addDecisionNode(testUtil.decision_var)

    # add connection between decision node and utility nodes.
    for component in created_components:
        utility_node = component.getUtilityNode()
        if utility_node is None:
            continue
        diagram.addUtilityNode(utility_node.getVariable())
        diagram.addArc(component.getHealthNode().getVariable().name(), utility_node.getVariable().name())
        diagram.addArc(testUtil.decision_var.name(), utility_node.getVariable().name())

    # set probability table.
    for component in created_components:
            utility_node = component.getUtilityNode()
            if utility_node is None:
                continue
            priors = testUtil.GetPriors(component)

            for prior in priors:
                diagram.utility(utility_node.getName())[prior[0]]=prior[1]
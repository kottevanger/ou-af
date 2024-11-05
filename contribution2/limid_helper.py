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

# Returns all decisions within the provided influence diagram (ID) and produces a list of dictionaries.
# Each dictionary has all decisions in the ID, where the decision variable is the key and the corresponding 
# value indicates whether to test or replace (‘yes’) or not (‘no’).
# Each dictionary is structured to have only one variable set to ‘yes,’ while the others are marked as ‘no.’.
# An example dictionary would be: {'replace_battery': 'yes', 'replace_bulb': 'no'}.
def get_decision_sequences(influence_diagram, previous_decisions):
    
    # Helper function to find a group of decisions. For example all relace decisions.
    def find_decisions_with_keyword(influence_diagram, keyword, previous_decisions, variables_list):
        for variable_name in influence_diagram.names():
            if keyword in variable_name.lower() and influence_diagram.isDecisionNode(variable_name) and variable_name not in previous_decisions:
                variables_list.append(variable_name)
    
    # Helper function to get a dictionary with all decisions having value 'no', except for the selected_variable.
    def generate_replacement_data(variables_list, selected_variable):
        data = {variable: 'yes' if variable == selected_variable else 'no' for variable in variables_list}
        return data

    variables_list = []
    # Find the replace decisions.
    find_decisions_with_keyword(influence_diagram, "replace", previous_decisions, variables_list)
    # Find the test decisions.
    find_decisions_with_keyword(influence_diagram, "test", previous_decisions, variables_list)
            
    decision_policies = []
    for selected_variable in variables_list:
        decision_policies.append(generate_replacement_data(variables_list, selected_variable))

    return decision_policies
    
# Run the inference for each decision sequence. Return the resulting inference list.
# This list has the decision_sequence used plus the calculated MEU.
def run_inference(gum, influence_diagram, decision_sequences, previous_decisons, final_node):
    
    # Helper function to filter a dictionary by key.
    def filter_dict_by_keyword(input_dict, keyword):
        return {key: value for key, value in input_dict.items() if keyword in key.lower()}
    
    # Helper function to filter a dictionary by value.
    def filter_dict_by_value(input_dict, target_value):
        return {key: value for key, value in input_dict.items() if value.lower() == target_value.lower()}

    inference = gum.ShaferShenoyLIMIDInference(influence_diagram)
    inference_list = []
    for decision_sequence in decision_sequences:
        
        decisions_made = {}
        # Find the replace decisions made and add extra evidence. The health is 100% ok, after a replace.
        previous_replacements = filter_dict_by_value(filter_dict_by_keyword(previous_decisons, 'replace'), 'yes')
        for key, value in previous_replacements.items():
            new_key = key.replace('DecisionReplace', 'health')
            decisions_made[new_key] = 'ok'
            decisions_made[key] = value     

        # Find the test decisions made. the ID will calculate a propability for each test result.
        previous_tests = filter_dict_by_value(filter_dict_by_keyword(previous_decisons, 'test'), 'yes')    
        for key, value in previous_tests.items(): 
            decisions_made[key] = value        
        
        temp_sequence = {**decision_sequence, **decisions_made} 
        if (len(decision_sequence) > 1):
            temp_sequence[final_node] = 'no'

        inference.eraseAllEvidence()
        inference.setEvidence(temp_sequence)
        inference.makeInference()

        inference_list.append({'sequence' : decision_sequence, 'MEU' : inference.MEU()["mean"]})
    return inference_list;
 
# Returns the optimal plan as a list. Each element in the list is a dictionary with the decision
# and its MEU and the second best decision and its MEU.
def determine_optimal_plan(gum, influence_diagram, final_node):

    # Helper function to find the decision with option is 'yes'.
    def find_yes_decision(dictionary):
        try:
            return next((key, value) for key, value in dictionary.items() if value == 'yes')
        except StopIteration:
            # If no matching key-value pair is found, return a default value or handle it accordingly.
            return None
        
    # Find all possible decision sequences in the influence diagram.
    decision_sequences = get_decision_sequences(influence_diagram, {})

    # Run for each decision sequence an inference.
    inference_list = run_inference(gum, influence_diagram, decision_sequences, {}, final_node)
    
    found_plan = []
    previous_decisions = {}
    while (len(inference_list) > 0):
        # Find the decison with the highest MEU.
        best_option = max(inference_list, key=lambda x: x['MEU'])
        best_decision_sequence = best_option['sequence']
        
        # Find the decision with the second highest MEU.
        sorted_list = sorted(inference_list, key=lambda x: x['MEU'], reverse=True)
        second_best_option = sorted_list[1] if len(sorted_list) > 1 else None
        second_best_decision_sequence = second_best_option['sequence'] if second_best_option != None else None;
        
        # Only one decision has a yes 'value'
        yes_pair = find_yes_decision(best_decision_sequence)
        if (second_best_decision_sequence != None):
            yes_pair_second = find_yes_decision(second_best_decision_sequence)
            # found_plan.append({'Decision' : yes_pair[0], 'MEU' : best_option['MEU'], 'Second best decision' : yes_pair_second[0], 'Second MEU' : second_best_option['MEU']})
            found_plan.append({'Test Decision' : yes_pair[0], 'MEU' : best_option['MEU']})
        else:
            found_plan.append({'Test Decision' : yes_pair[0], 'MEU' : best_option['MEU']})
            
        # Remember the previous decisions.
        previous_decisions[yes_pair[0]] = yes_pair[1]
        decision_sequences = get_decision_sequences(influence_diagram, previous_decisions)
        inference_list = run_inference(gum, influence_diagram, decision_sequences, previous_decisions, final_node)
        
    return found_plan

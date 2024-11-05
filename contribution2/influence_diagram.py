
# class assembly contains objects for all part of the system: components, connections, tests
class Assembly:
    def __init__(self, name, components, connections, tests):
        self.name = name
        self.components = components
        self.connections = connections
        self.tests = tests
    def getComponents(self):
        return self.components
    def getConnections(self):
        return self.connections
    def getTests(self):
        return self.tests
        
        
# MAIN method to build objects and create a system definition
def readAssembly(assembly):
    name = assembly['structure']["name"]
    print("building system: " + name)

    componentslist = getComponents(assembly)
    print("number of components: " + str(len(componentslist)))

    connectionslist = getConnections(assembly, componentslist)
    print("number of connections: " + str(len(componentslist)))

    testslist = getTests(assembly, componentslist)
    print("number of tests: " + str(len(testslist)))
    
    return Assembly(name, componentslist, connectionslist, testslist)
    
def get_value_health_variable(cpt_dict):    
    for key in cpt_dict:
        if key.lower().startswith('health'):
            return cpt_dict[key]
            
def get_value_output_variable(cpt_dict):    
    for key in cpt_dict:
        if 'outputs' in key.lower():
            return cpt_dict[key]  
            
def get_value_input_variable(cpt_dict):    
    for key in cpt_dict:
        if 'inputs' in key.lower():
            return cpt_dict[key]
            
def get_value_decision_test_variable(cpt_dict):    
    for key in cpt_dict:
        if 'decisiontest' in key.lower():
            return cpt_dict[key]

def get_value_test_outcome_variable(cpt_dict):    
    for key in cpt_dict:
        if 'testoutcome' in key.lower():
            return cpt_dict[key]            

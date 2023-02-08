class BNVariable:
    name = None
    parents = []

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        return "{} - Number of parents: {}".format(self.name, len(self.parents))


class BNetwork:
    probs = {}
    variables = []

    def add_variable(self, variable_name: str):
        new_variable = BNVariable(variable_name)
        self.variables.append(new_variable)

    def add_probability(self, probability_string: str, probability_value: float):
        self.probs[probability_string] = probability_value
        if probability_string[0] == "-":
            self.probs[probability_string[1:]] = 1 - probability_value
        else:
            self.probs["-" + probability_string] = 1 - probability_value

    def set_parents_to_variable(self, variable_name: str, parent_variable_names: [str]):
        var = None
        parents = []

        for variable in self.variables:
            if variable_name == variable.name:
                var = variable
                break
        if var is None:
            raise Exception("Could not find variable. Please be sure to create it first with add_variable")

        for variable in self.variables:
            for p_var_name in parent_variable_names:
                if variable.name == p_var_name:
                    parents.append(variable)

        if len(parents) is not len(parent_variable_names):
            raise Exception("Could not find all the specified parent variables. Please be sure to create them with "
                            "add_variable")
        var.parents = parents

    def inference(self, query: {str: bool}, observed_values: {str: bool}):
        o = observed_values.copy()
        evidence_prob = self.enumeration_ask(o, {})
        dis_prob = self.enumeration_ask(query, observed_values)
        return dis_prob / evidence_prob

    def enumeration_ask(self, query: {str: bool}, observed_values: {str: bool}):
        expanded = {}

        expanded.update(query)
        expanded.update(observed_values)
        qx = self.enumerate_all(self.variables, expanded)

        return qx

    def enumerate_all(self, variables: [BNVariable], observed_values: {str: bool}) -> float:
        cloned_vars: [BNVariable] = variables.copy()
        if len(cloned_vars) == 0:
            return 1
        first: BNVariable = cloned_vars.pop(0)
        prob_string: str = first.name
        if len(first.parents) > 0:
            prob_string += "|"
            for p in first.parents:
                prob_string += p.name

        for (observed_name, observed_value) in observed_values.items():
            if not observed_value:
                prob_string = prob_string.replace(observed_name, "-"+observed_name)

        observed_values_contain_first = False
        for name in observed_values.keys():
            if name == first.name:
                observed_values_contain_first = True

        if observed_values_contain_first:
            prob = self.probs[prob_string]
            return prob * self.enumerate_all(cloned_vars, observed_values)
        else:
            extended_1 = observed_values.copy()
            extended_1[first.name] = True
            extended_2 = observed_values.copy()
            extended_2[first.name] = False
            prob_1 = self.probs[prob_string]
            prob_2 = self.probs[prob_string.replace(first.name, "-" + first.name)]

            return prob_1 * self.enumerate_all(cloned_vars, extended_1) \
                   + prob_2 * self.enumerate_all(cloned_vars, extended_2)

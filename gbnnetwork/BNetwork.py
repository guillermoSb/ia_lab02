from prettytable import PrettyTable
class BNVariable:
    name = None
    parents = []

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        s = self.name
        if len(self.parents) > 0:
            s += "|"
            for p in self.parents:
                s += p.name
        return s


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

    def calculate_sorted(self):
        sorted_variables: [BNVariable] = []
        sorted_count = 0
        while len(self.variables) > sorted_count:
            for v in self.variables:

                if self.list_contains(v, sorted_variables):
                    break
                if len(v.parents) == 0:
                    sorted_variables.append(v)
                    sorted_count += 1
                else:
                    all_parents_present = False
                    for p in v.parents:
                        if not self.list_contains(p, sorted_variables):
                            break
                        all_parents_present = True
                    if all_parents_present:
                        sorted_variables.append(v)
                        sorted_count += 1
        return sorted_variables

    def set_parents_to_variable(self, variable_name: str, parent_variable_names: [str]):
        var = None
        parents = []

        for variable in self.variables:
            if variable_name == variable.name:
                var = variable
                break
        if var is None:
            raise Exception("Could not find variable. Please be sure to create it first with add_variable")
        for p_var_name in parent_variable_names:
            for variable in self.variables:
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
        sorted_variables = self.calculate_sorted()

        qx = self.enumerate_all(sorted_variables, expanded)

        return qx

    def list_contains(self, value: BNVariable, list: [BNVariable]) -> bool:
        for l_var in list:
            if l_var.name == value.name:
                return True
        return False

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

    def compact_string(self):
        sorted_variables = self.calculate_sorted()
        compact_string = ""
        for v in sorted_variables:
            v_s = "P(" + v.name
            if len(v.parents) > 0:
                v_s += "|"
                for p in v.parents:
                    v_s += p.name
            v_s += ")"
            compact_string += v_s
        return compact_string

    def factor_string(self):
        return self.probs.__str__()

    def __str__(self):
        return self.compact_string()
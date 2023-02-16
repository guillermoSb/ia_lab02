from gbnnetwork import BNetwork
network = BNetwork() 


network.add_variable("B")
network.add_variable("E")
network.add_variable("A")
network.add_variable("J")
network.add_variable("M")

network.set_parents_to_variable("A", ["B", "E"])
network.set_parents_to_variable("J", ["A"])
network.set_parents_to_variable("M", ["A"])

network.add_probability("B", 0.001)
network.add_probability("E", 0.002)
network.add_probability("A|BE", 0.95)
network.add_probability("A|-BE", 0.29)
network.add_probability("A|B-E", 0.94)
network.add_probability("A|-B-E", 0.001)
network.add_probability("M|A", 0.7)
network.add_probability("M|-A", 0.01)
network.add_probability("J|A", 0.9)
network.add_probability("J|-A", 0.05)


p = network.inference({'B': False}, {'J': True, 'M': True})  
defined = network.compact_string()

## Check if the burglgary not happening given that johns calls is true and mary calls is true
assert round(p, 2) == 0.72
## Check correct compact string
assert defined == 'P(B)P(E)P(A|BE)P(J|A)P(M|A)'



from BNetwork import  BNetwork

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    network = BNetwork()

    network.add_variable("C")
    network.add_variable("E")
    network.add_variable("M")


    network.set_parents_to_variable("C", ["E", "M"])

    network.add_probability("E", 0.1)
    network.add_probability("M", 0.2)
    network.add_probability("C|-E-M", 0.0)
    network.add_probability("C|-EM", 0.5)
    network.add_probability("C|E-M", 1.0)
    network.add_probability("C|EM", 1.0)


    p2 = network.inference({'E': True}, {'C': True,})
    print(p2)



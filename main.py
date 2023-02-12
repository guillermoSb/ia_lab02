from gbnnetwork import BNetwork

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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




    # Probabilidad que haya habido un robo dado que los dos vecinos llamaron
    p = network.inference({'B': True}, {'J': True, 'M': True})

    # Version compacta
    print(network.compact_string())
    
    print("Resultado de la query (Probabilidad de Robo dado que ambos vecinos llaman): ", p)
    print("La red esta totalmente definida?", network.validate_defined_state())
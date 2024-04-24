class Automata:
    def __init__(self):
        # Define los estados posibles del AFD
        self.estadosPosibles = ["q0 " "q1" "q2" "q3" "q4" "q5"]

        self.estadoInicial = "q0"
        self.estadoFinal = ["q2","q5"]
        self.transiciones = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q3",
            ("q0", "c"): "q3",
            ("q1", "c"): "q2",
            ("q1", "b"): "q5",
            ("q1", "a"): "q4",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
            ("q2", "c"): "q2",
            ("q3", "b"): "q3",
            ("q3", "c"): "q3",
            ("q3", "a"): "q4",
            ("q4", "a"): "q4", 
            ("q4", "c"): "q3", 
            ("q4", "b"): "q5", 
            ("q5", "a"): "q4",
            ("q5", "b"): "q3",
            ("q5", "c"): "q3",
            
            
        }

    def Automata(self, a):
        Actual = self.estadoInicial

        for symbol in a:
            Actual = self.transiciones.get((Actual, symbol))
            print(Actual)
            print(symbol)
            if Actual is None:
                return False

        if Actual in self.estadoFinal:
            print(self.estadoFinal)
            return True
        else:
            return False


automata = Automata()

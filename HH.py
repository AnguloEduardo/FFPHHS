# Provides the methods to create and use hyper-heuristics for the FFP
# This is a class you must extend it to provide the actual implementation
class HyperHeuristic:

    # Constructor
    #   features = A list with the names of the features to be used by this hyper-heuristic
    #   heuristics = A list with the names of the heuristics to be used by this hyper-heuristic
    def __init__(self, features, heuristics):
        if features:
            self.features = features.copy()
        else:
            print("=====================")
            print("Critical error at HyperHeuristic.__init__.")
            print("The list of features cannot be empty.")
            print("The system will halt.")
            print("=====================")
            exit(0)
        if heuristics:
            self.heuristics = heuristics.copy()
        else:
            print("=====================")
            print("Critical error at HyperHeuristic.__init__.")
            print("The list of heuristics cannot be empty.")
            print("The system will halt.")
            print("=====================")
            exit(0)

    # Returns the next heuristic to use
    # problem = The FFP instance being solved
    def nextHeuristic(self, problem):
        print("=====================")
        print("Critical error at HyperHeuristic.nextHeuristic.")
        print("The method has not been overriden by a valid subclass.")
        print("The system will halt.")
        print("=====================")
        exit(0)

    # Returns the string representation of this hyper-heuristic
    def __str__(self):
        print("=====================")
        print("Critical error at HyperHeuristic.__str__.")
        print("The method has not been overriden by a valid subclass.")
        print("The system will halt.")
        print("=====================")
        exit(0)

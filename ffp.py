from HH import HyperHeuristic


# Provides the methods to create and solve the firefighter problem
class FFP:

    # Constructor
    #   fileName = The name of the file that contains the FFP instance
    def __init__(self, fileName):
        file = open(fileName, "r")
        text = file.read()
        tokens = text.split()
        seed = int(tokens.pop(0))
        self.n = int(tokens.pop(0))  # no. of nodes in the graph
        model = int(tokens.pop(0))
        int(tokens.pop(0))  # Ignored
        # self.state contains the state of each node
        #    -1 On fire
        #     0 Available for analysis
        #     1 Protected
        self.state = [0] * self.n  # Initialization of nodes in "Available for analysis"
        nbBurning = int(tokens.pop(0))  # Node(s) where the fire starts
        for i in range(nbBurning):
            b = int(tokens.pop(0))
            self.state[b] = -1
        self.graph = []
        for i in range(self.n):  # Matrix of adjacency of nXn
            self.graph.append([0] * self.n)
        while tokens:  # Filling the matrix with the connection between nodes
            x = int(tokens.pop(0))
            y = int(tokens.pop(0))
            self.graph[x][y] = 1
            self.graph[y][x] = 1

    #   Solves the FFP by using a given method and a number of firefighters
    #   method = Either a string with the name of one available heuristic or an object of class HyperHeuristic
    #   nbFighters = The number of available firefighters per turn
    #   debug = A flag to indicate if debugging messages are shown or not
    def solve(self, method, nbFighters, debug=False):
        spreading = True
        if debug:
            print("Initial state:" + str(self.state))
        t = 0
        while spreading:
            if debug:
                print("Features")
                print("")
                print("Graph density: %1.4f" % (self.getFeature("EDGE_DENSITY")))
                print("Average degree: %1.4f" % (self.getFeature("AVG_DEGREE")))
                print("Burning nodes: %1.4f" % self.getFeature("BURNING_NODES"))
                print("Burning edges: %1.4f" % self.getFeature("BURNING_EDGES"))
                print("Nodes in danger: %1.4f" % self.getFeature("NODES_IN_DANGER"))
            # It protects the nodes (based on the number of available firefighters)
            for i in range(nbFighters):
                heuristic = method
                if isinstance(method, HyperHeuristic):
                    heuristic = method.nextHeuristic(self)
                node = self.__nextNode(heuristic)
                if node >= 0:
                    # The node is protected
                    self.state[node] = 1
                    # The node is disconnected from the rest of the graph
                    for j in range(len(self.graph[node])):
                        self.graph[node][j] = 0
                        self.graph[j][node] = 0
                    if debug:
                        print("\tt" + str(t) + ": A firefighter protects node " + str(node))
                        # It spreads the fire among the unprotected nodes
            spreading = False
            state = self.state.copy()
            for i in range(len(state)):
                # If the node is on fire, the fire propagates among its neighbors
                if state[i] == -1:
                    for j in range(len(self.graph[i])):
                        if self.graph[i][j] == 1 and state[j] == 0:
                            spreading = True
                            # The neighbor is also on fire
                            self.state[j] = -1
                            # The edge between the nodes is removed (it will no longer be used)
                            self.graph[i][j] = 0
                            self.graph[j][i] = 0
                            if debug:
                                print("\tt" + str(t) + ": Fire spreads to node " + str(j))
            t = t + 1
            if debug:
                print("---------------")
        if debug:
            print("Final state: " + str(self.state))
            print("Solution evaluation: " + str(self.getFeature("BURNING_NODES")))
        return self.getFeature("BURNING_NODES")

    # Selects the next node to protect by a firefighter
    # heuristic = A string with the name of one available heuristic
    def __nextNode(self, heuristic):
        index = -1
        best = -1
        for i in range(len(self.state)):
            if self.state[i] == 0:
                index = i
                break
        value = -1
        for i in range(len(self.state)):
            if self.state[i] == 0:
                if heuristic == "LDEG":
                    # It prefers the node with the largest degree, but it only considers
                    # the nodes directly connected to a node on fire
                    for j in range(len(self.graph[i])):
                        if self.graph[i][j] == 1 and self.state[j] == -1:
                            value = sum(self.graph[i])
                            break
                elif heuristic == "GDEG":
                    value = sum(self.graph[i])
                else:
                    print("=====================")
                    print("Critical error at FFP.__nextNode.")
                    print("Heuristic " + heuristic + " is not recognized by the system.")
                    print("The system will halt.")
                    print("=====================")
                    exit(0)
            if value > best:
                best = value
                index = i
        return index

    # Returns the value of the feature provided as argument
    # feature = A string with the name of one available feature
    def getFeature(self, feature):
        f = 0
        if feature == "EDGE_DENSITY":
            n = len(self.graph)
            for i in range(len(self.graph)):
                f = f + sum(self.graph[i])
            f = f / (n * (n - 1))
        elif feature == "AVG_DEGREE":
            n = len(self.graph)
            count = 0
            for i in range(len(self.state)):
                if self.state[i] == 0:
                    f += sum(self.graph[i])
                    count += 1
            if count > 0:
                f /= count
                f /= (n - 1)
            else:
                f = 0
        elif feature == "BURNING_NODES":
            for i in range(len(self.state)):
                if self.state[i] == -1:
                    f += 1
            f = f / len(self.state)
        elif feature == "BURNING_EDGES":
            n = len(self.graph)
            for i in range(len(self.graph)):
                for j in range(len(self.graph[i])):
                    if self.state[i] == -1 and self.graph[i][j] == 1:
                        f += 1
            f = f / (n * (n - 1))
        elif feature == "NODES_IN_DANGER":
            for j in range(len(self.state)):
                for i in range(len(self.state)):
                    if self.state[i] == -1 and self.graph[i][j] == 1:
                        f += 1
                        break
            f /= len(self.state)
        else:
            print("=====================")
            print("Critical error at FFP._getFeature.")
            print("Feature " + feature + " is not recognized by the system.")
            print("The system will halt.")
            print("=====================")
            exit(0)
        return f

    # Returns the string representation of this problem
    def __str__(self):
        text = "n = " + str(self.n) + "\n"
        text += "state = " + str(self.state) + "\n"
        for i in range(self.n):
            for j in range(self.n):
                if self.graph[i][j] == 1 and i < j:
                    text += "\t" + str(i) + " - " + str(j) + "\n"
        return text

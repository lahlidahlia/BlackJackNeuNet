import math

class Perceptron():
    """
    Defines a single perceptron.
    """
    def __init__(self):
        self.input_list = []  # Received from other perceptrons.
        # self.output_destination = []  # Which perceptrons will this perceptron place its output in.  
        

class NeuralNetwork():
    """
    Defines a neural network, made up of perceptrons.
    """
    
    def __init__(self, layer_size_list):
        """
        Create a neural network.
        
        layer_size_list: defines the size of each layer of perceptrons.
            Ex: [2, 3, 1] means 2 input perceptrons, 3 hidden and 1 output.
        """
        self.layer_size_list = layer_size_list
        # Perceptron list contains a list of perceptron layers that contains individual perceptrons.
        # For example: [[input_p1, input_p2], [hidden_p1, hidden_p2, hidden_p3], [output_p1]]
        # This class is implemented with this structure in mind.
        self.perceptron_layer_list = []
        for i in layer_size_list:
            layer = []
            for _ in range(i):
                layer.append(Perceptron())
            self.perceptron_layer_list.append(layer)
            
    def run(self, input_list, weight_list):
        """
        Runs the neural network with the given inputs and weights.
        
        input_list: the list of inputs to be placed in the input layer. Requires as many
            values as the amount of perceptrons in the input layer.
        weight_list: list of weights, including bias. Use the get_weight_amount function to 
            calculate the amount of weights required in the list.
            
        Returns a list of outputs from the output layer.
        """
        # Are there enough inputs?
        if len(input_list) != self.layer_size_list[0]:  
            raise Exception(
                "There are not enough inputs ({} required, {} found)".format(
                    self.layer_size_list[0], len(input_list)))
        # Are there enough weights?
        if len(weight_list) != self.get_weight_amount():  
            raise Exception(
                "There are not enough weights ({} required, {} found)".format(
                    self.get_weight_amount(), len(weight_list)))
        ret = []
        for layer_index, layer in enumerate(self.perceptron_layer_list):
            for perceptron in layer:
                if layer_index == 0:  # If input layer:
                    perceptron.input_list.append(input_list.pop())  # Grab inputs from the input list.
                # sigmoid(sum of all input*weight - bias)
                # Sums all (input*weight) together.
                sum = 0
                for input in perceptron.input_list:
                    sum += input * weight_list.pop(0)
                # Form output.
                output = self.sigmoid(sum - weight_list.pop(0))  # Weight.pop() here is bias.
                if layer_index == len(self.perceptron_layer_list) - 1:  # If in output layer:
                    ret.append(output)
                else:
                    # Use the output as next layer's perceptrons' inputs.
                    for next_layer_perceptron in self.perceptron_layer_list[layer_index+1]:
                        next_layer_perceptron.input_list.append(output)
                        
        # Clean up, i.e. clear all perceptron's input list.
        for layer in self.perceptron_layer_list:
            for perceptron in layer:
                perceptron.input_list = []
        return ret
                              
    def get_weight_amount(self):
        """
        Returns the amount of weight required to run the neural network.
        """
        ret = 0
        ret += self.layer_size_list[0]*2
        for i in range(1, len(self.layer_size_list)):
            ret += (self.layer_size_list[i-1] + 1) * self.layer_size_list[i]
        return ret
    
    def sigmoid(self, x):
        return 1/(1 + math.exp(-x))
           
    
if __name__ == '__main__':
    import pprint
    
    print "Neural network init, get_weight_amount and sigmoid"
    neuNet = NeuralNetwork([3, 3, 3])
    print "3, 3, 3:"
    pprint.pprint(neuNet.perceptron_layer_list)
    print "Get weight amount:"
    print neuNet.get_weight_amount() == 30
    print "Sigmoid function:"
    print neuNet.sigmoid(0) == 0.5
    print "-------------------------"
    
    print "Running the neural network"
    neuNet = NeuralNetwork([3,3,3])
    weights = []
    for i in range(neuNet.get_weight_amount()):
        weights.append(i)
    print "All results should be close to 0:"
    print neuNet.run([1,1,1], weights)
    weights = []
    for i in range(neuNet.get_weight_amount()):
        weights.append(i)
    print "All results should be close to 1:"
    print neuNet.run([2,2,2], weights)
    
    

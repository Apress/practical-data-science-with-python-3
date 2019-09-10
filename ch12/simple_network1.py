import numpy as np


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights to small random values using Normal distribution.
        self.weights_input_to_hidden = np.random.normal(
            scale = self.input_nodes ** -0.5, 
            size = (self.input_nodes, self.hidden_nodes))
        self.weights_hidden_to_output = np.random.normal(
            scale = self.hidden_nodes ** -0.5, 
            size = (self.hidden_nodes, self.output_nodes))

        self.lr = learning_rate
        self.activation_function = lambda x : 1 / (1 + np.exp(-x)) # sigmoid                   

    def train(self, features, targets):
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)

        for X, y in zip(features, targets):
            y_hat, hidden_outputs = self.__forward(X)
            delta_weights_i_h, delta_weights_h_o = self.__backward(
                y_hat, hidden_outputs, 
                X, y,
                delta_weights_i_h, delta_weights_h_o)
        self.__update_weights(delta_weights_i_h, delta_weights_h_o)

    def run(self, X):
        return self.__forward(X)[0]

    def __forward(self, X):
        hidden_inputs = np.dot(X, self.weights_input_to_hidden)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output)
        y_hat = final_inputs
        return y_hat, hidden_outputs
    
    def __backward(self, y_hat, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        error = y - y_hat
        hidden_error = np.dot(self.weights_hidden_to_output, error)
        output_error_term = error
        hidden_error_term = hidden_error * hidden_outputs * (1 - hidden_outputs)
        delta_weights_i_h += np.dot(
            X[:, np.newaxis], hidden_error_term[np.newaxis, :])
        delta_weights_h_o += np.dot(
            hidden_outputs[:, np.newaxis], output_error_term[np.newaxis, :])
        return delta_weights_i_h, delta_weights_h_o

    def __update_weights(self, delta_weights_i_h, delta_weights_h_o):
        self.weights_hidden_to_output += self.lr * delta_weights_h_o
        self.weights_input_to_hidden += self.lr * delta_weights_i_h


#########################################################
# Set your hyperparameters here
##########################################################
iterations = 1000
learning_rate = 0.005
hidden_nodes = 20
output_nodes = 1

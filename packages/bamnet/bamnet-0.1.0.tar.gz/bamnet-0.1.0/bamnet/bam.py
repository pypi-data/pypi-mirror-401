import numpy as np

class BAM:
    def __init__(self):
        self.W = None

    def train(self, X, Y):
        """
        X: 2D numpy array of input patterns
        Y: 2D numpy array of associated output patterns
        """
        self.W = np.zeros((X.shape[1], Y.shape[1]))
        for i in range(X.shape[0]):
            self.W += np.outer(X[i], Y[i])
        return self.W

    def recall_Y(self, X_input):
        """
        Recall Y from X
        """
        if self.W is None:
            raise ValueError("Train the network first!")
        Y_output = np.sign(np.dot(X_input, self.W))
        return Y_output

    def recall_X(self, Y_input):
        """
        Recall X from Y
        """
        if self.W is None:
            raise ValueError("Train the network first!")
        X_output = np.sign(np.dot(Y_input, self.W.T))
        return X_output

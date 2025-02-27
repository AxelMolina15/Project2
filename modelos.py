import numpy as np

class KalmanFilterReg():
    def __init__(self):
        self.w = np.array([1, 1])
        self.A = np.eye(2)
        self.Q = np.eye(2) * 1
        self.R = np.array([[1]]) * 10
        self.P = np.eye(2)

    def predict(self):
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, x, y):
        C = np.array([[1, x]])
        S = C @ self.P @ C.T + self.R
        K = self.P @ C.T @ np.linalg.inv(S)
        self.P = (np.eye(2) - K @ C) @ self.P
        self.w = self.w + K @ (y - C @ self.w)

    def params(self):
        return self.w[0], self.w[1]

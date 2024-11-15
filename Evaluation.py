import numpy as np

# Define arrays with correct shapes
x = np.zeros((2, 11))
u = np.zeros((1, 10))
uhat = np.zeros((1, 10))
y = np.zeros((1, 10))
xhat = np.zeros((2, 11))
yhat = np.zeros((1, 10))
r = np.zeros((1, 10))

# Define parameters as specified
a_u = np.array([x * 1000 for x in [0.2570, 0.0068, 0.0011, -0.0021, -0.0034, -0.0100, 0.0032, -0.0025, -0.0018, 1.123]])
a_y = np.array([-1.2822, -3.8838, -6.5325, -9.1790, -11.8007, -14.3584, -16.8851, -19.4185, -21.9335, -30.0617])
A = np.array([[1, 0.1], [0, 1]])
B = np.array([[0.005], [0.1]])
C = np.array([1, 0])

# Known variable values
h = 0.1
K = np.array([16.0302, 5.6622])
L = np.array([[1.8721], [9.6532]])

# Set initial conditions
t = 9
x[:, 0] = np.array([0.65, 0.78])
xhat[:, 0] = np.array([0.65, 0.78])
u[0,0]=-K@xhat[:,0]
uhat[0,0]=u[0,0]+a_u[0]
# Update x, y, and yhat using the specified equations
#Without Skip
for i in range(1, t + 1):
    x[:, i] = (A @ x[:, i - 1]).flatten() + (B.flatten() * uhat[0, i - 1])
    y[0, i] = C @ x[:, i] + a_y[i-1]
    yhat[0, i] = C @ (A @ xhat[:, i - 1] + B.flatten() * u[0, i - 1])

    r[0,i]=yhat[0,i]-y[0,i]
    xhat[:,i]=A@xhat[:,i-1] + B.flatten()*u[0,i-1] + L.flatten()*r[0,i]
    u[0,i]=-K@xhat[:,i]
    uhat[0,i]=u[0,i]+a_u[i]
p=x[0,:9].copy()
#With skip Control sequence given from algo
skip='1'*2+'0'*4+'1'*3
for i in range(1, t + 1):
    x[:, i] = (A @ x[:, i - 1]).flatten() + (B.flatten() * uhat[0, i - 1])
    if(skip[i-1]!='0'):

        y[0, i] = C @ x[:, i] + a_y[i-1]
        yhat[0, i] = C @ (A @ xhat[:, i - 1] + B.flatten() * u[0, i - 1])

        r[0,i]=yhat[0,i]-y[0,i]
        xhat[:,i]=A@xhat[:,i-1] + B.flatten()*u[0,i-1] + L.flatten()*r[0,i]
        u[0,i]=-K@xhat[:,i]
        uhat[0,i]=u[0,i]+a_u[i]
    else:
        uhat[0,i]=uhat[0,i-1]

z=x[0,:9].copy()

import numpy as np
import matplotlib.pyplot as plt

# Generate sample data for the x-axis
x = list(range(0, 9))  # 100 points from 0 to 8
# p = [18.8834,21.14,22.61,22.67,21.59,20.9,25.99,20.26,45.013] Another state representation for different control pattern
# z=[18.8834,21.14,22.61,22.67,22.019,20.64,19.49,19.43,25.89]  

# Create the plot
plt.plot(x, p, label='Periodic Execution',color='blue')
plt.plot(x, z, label='aperiodic Execution',color='green')
plt.axhline(0, color='black',linewidth=0.8)  # Horizontal axis
plt.axvline(0, color='black',linewidth=0.8)  # Vertical axis
# Set the x and y axis limits
plt.xlim(0, 8)
plt.ylim(-35, 35)
plt.axhline(30, color='red', linestyle='--', linewidth=1)  # Line at y = 30
plt.axhline(-30, color='red', linestyle='--', linewidth=1)  # Line at y = -30
# Add labels and a title
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Plot of deviation vs time')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
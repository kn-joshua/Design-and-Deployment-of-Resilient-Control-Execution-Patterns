from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import scipy.io


mat_data = scipy.io.loadmat('attack_vectors.mat') #Load with attack vectors synthesized from library

x=mat_data['dataset'][:,:13,:]
x=x.transpose(1,0,2)
x=x.reshape(x.shape[2],-1)
# print(x.shape)


num_samples = 100

y = np.random.randint(0, 2, num_samples) #Load with actual labels obtained from the algo





X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32),  
    activation='tanh',           
    solver='adam',               
    learning_rate_init=0.001,    
    max_iter=500,                
    random_state=42
)

# Train the model
mlp.fit(X_train, y_train)

# Make predictions
y_pred = mlp.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

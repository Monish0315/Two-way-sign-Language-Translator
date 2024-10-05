from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Example: Create a simple model (replace this with your actual model)
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(32,)))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy')

# Save the model
model.save('model.h5')
print("Model saved as model.h5")

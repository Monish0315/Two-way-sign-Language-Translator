from keras.models import load_model

model = load_model(r"C:\Users\pmoni\two-way-sign-language-translator\model.h5")
model.summary()  # This will display the architecture of the model

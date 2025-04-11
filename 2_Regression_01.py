import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import LSTM ,Dense, Conv1D, MaxPooling1D, Flatten, Embedding, Activation , Dropout, Conv2D, MaxPooling2D
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.constraints import max_norm
from keras.metrics import RootMeanSquaredError as rmse
from keras.layers import LeakyReLU
from keras.constraints import max_norm
from tensorflow.keras.layers import BatchNormalization
from keras.callbacks import ModelCheckpoint

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=100):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), :]
        dataX.append(a)
        dataY.append(dataset[i + look_back, :])
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print  ((numpy.array(dataX)).shape , (numpy.array(dataY)).shape)    
    return numpy.array(dataX), numpy.array(dataY)
# fix random seed for reproducibility
numpy.random.seed(7)
# load the dataset
dataframe = pandas.read_csv('1_main.csv',engine= 'python')
dataset = dataframe.values
dataset = dataset.astype( 'float32' )
print(dataset.shape)
# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))
# reshape dataset
look_back = 100
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
# reshape input to be [samples, time steps, features]
print((trainX.shape ))

trainX = numpy.reshape(trainX, (trainX.shape[0], 20,20,1))
testX = numpy.reshape(testX, (testX.shape[0], 20,20,1))

#dataset shape
print("##########################")
print((trainX[0] ))
print((trainX[0].shape ))
print((trainX[1] ))
print((trainX[1].shape ))
print(trainX.shape[1])
print("##########################")
print(trainX.shape)
print(trainY.shape)
print(testX.shape)
print(testY.shape)
input()
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu',padding = 'same',input_shape=(20,20,1)))
model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu'))
#model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu'))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(4, activation='sigmoid'))
model.compile(optimizer='adam', loss= 'mse' , metrics = [rmse()])
#_________________________________
# checkpoint
filepath="4_REGR_001-weights-improvement.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor= 'val_loss' , verbose=1, save_best_only=True,mode= min )
callbacks_list = [checkpoint]
#____________________________________

# model training for 300 epochs
history = model.fit(trainX, trainY, epochs =1000 , validation_data = (testX,testY), batch_size=32, verbose=2 ,callbacks=callbacks_list)
print(model.summary())
# evaluate training data
train_loss, train_rmse = model.evaluate(trainX,trainY, batch_size = 32)
print(f"train_loss={train_loss:.8f}")
print(f"train_rmse={train_rmse:.8f}")

# evaluate testing data
test_loss, test_rmse = model.evaluate(testX,testY, batch_size = 32)
print(f"test_loss={test_loss:.8f}")
print(f"test_rmse={test_rmse:.8f}")
#_________________________________
# Make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
print(testPredict.shape)

trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)

testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
print( 'Train Score: %.6f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY, testPredict))
print( 'Test Score: %.6f RMSE' % (testScore))
testVariance = numpy.var(testY - testPredict)
print('Test Variance: %.6f' % (testVariance))
# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict


# serialize model to JSON
model_json = model.to_json()
with open("4_model_forex.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("4_REGR_001-weights-improvement.hdf5")
print("Saved model to disk")
# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()


from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

def get_forecast(b, d, q, v):
    series = read_csv('lines.csv', header=0, index_col=0, squeeze=True)

    l = []
    X = v
    history = [x for x in X]
    predictions = list()
    for t in range(6):
        model = ARIMA(history, order=(b,d,q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        l.append(yhat)
      
    pyplot.plot(predictions, color='red')
    pyplot.show()

    print (history)
    print (l)

#get_forecast([1.,2.,3.,20.,10.,11.,12.,30.,21.,22.,23.,40.,31.,32.,33., 50., 41., 42.])



def evaluate_arima_model(X, arima_order):
    # prepare training dataset
    train_size = int(len(X) * 0.90)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    return error

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    best_score, best_cfg = float("inf"), None
    bp = 1
    bd = 1
    bq = 1
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    mse = evaluate_arima_model(dataset, order)
                    if mse < best_score:
                        best_score, best_cfg = mse, order
                        bp = p, bd = d, bq = q
                    print('ARIMA%s MSE=%.3f' % (order,mse))
                except:
                    continue
    return [bp, bd, bq]


import datetime
p_values = [6,7,8]
d_values = [1,2]
q_values = [2,3,4]
#warnings.filterwarnings("ignore")
train = [1.,2.,3.,20.,10.,11.,12.,30.,21.,22.,23.,40.,31.,32.,33., 50., 41., 42.]
[bp, bd, bq] = evaluate_models(train, p_values, d_values, q_values)
get_forecast(bp, bd, bq, [1.,2.,3.,20.,10.,11.,12.,30.,21.,22.,23.,40.,31.,32.,33., 50., 41., 42.])

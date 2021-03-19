'''
Analyze a stock's historical records of dividends.

NOTE: Currently set up to analyze Toronto-Dominion dividend history 
obtained from Yahoo Finance.

TODO: Generalize this to work with different companies. Possiblly make a 
text file for each company containing custom inputs.
'''

import numpy as np
import plotly.graph_objects as go
import pandas as pd
from sklearn.linear_model import LinearRegression
pd.options.plotting.backend = "plotly"

def clean_data(data):
    '''
    Cleans the historical dividends data obtained from Yahoo Finance.
    The issues are 
     - Yahoo Finance gives data that is unsorted
    '''
    data = data.sort_values(by='Date')
    return data

def get_best_fit(data, verbose=False):
    '''
    Gets a curve of best fit with the given data. It is assumed that 
    companies generally increase their dividend every period over time.

    From this assumption the data is fitted to an exponential curve.
    '''
    X = (data.index - data.index[0]).days # NOTE: Compounding period is in days
    Y = np.log(data.Dividends)

    X = np.array(X).reshape(-1,1) # Regressor requires data to be '2-D'
    Y = np.array(Y).reshape(-1,1) # That is, it likes to see one column and 
                                  # many rows.

    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    
    Y_pred = np.exp(Y_pred)
    Y_pred = Y_pred.flatten() # plotly doesn't like dealing with a list of lists

    if verbose:
        print(f'Best Fit Equation: Y_pred = {np.exp(linear_regressor.intercept_)}exp({linear_regressor.coef_}X')

    return Y_pred

def get_cagr(begin_value, end_value, num_years):
    '''
    Calculate the cumulative annual growth rate
    '''
    return pow((end_value/begin_value), (1/num_years)) - 1

def main():
    # Retrieve the historical dividend data.
    path = './data/dividends/TD.TO.csv'
    data = pd.read_csv(path, index_col='Date', parse_dates=True)

    # Clean the data
    data = clean_data(data)
    
    # Check that the data looks right
    data.info()
    print(data.head())
    
    # Calculate best fit curves.
    domains = [['Apr 2011', 'Jan 2021'], 
               ['Mar 1995', 'Mar 2001'], 
               ['Sep 2003', 'Oct 2008']]
    X = []
    Y_pred = []
    for domain in domains:
        X.append(data[domain[0]:domain[1]].index)
        Y_pred.append(get_best_fit(data[domain[0]:domain[1]]))
    
    # Calculate the annual growth rate
    growth=get_cagr(data.loc['Jan 2020'].values[0], data.loc['Jan 2021'].values[0], 1)
    print(f'Cumulative Annual Growth Rate: {growth*100} percent')

    # Plot the data.
    fig = go.Figure()
    fig.update_yaxes(type='log')
    fig.add_trace(go.Scatter(x=data.index, y=data.Dividends, mode='markers', name='Dividends (dB)'))
    for i in range(len(Y_pred)):
        fig.add_trace(go.Scatter(x=X[i], y=Y_pred[i], mode='lines', name=f'fit{i}'))
    fig.show()

if __name__ == "__main__":
    main()
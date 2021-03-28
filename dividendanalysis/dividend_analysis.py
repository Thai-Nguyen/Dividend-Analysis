'''
Analyze a stock's historical records of dividends.

NOTE: Currently set up to analyze Toronto-Dominion dividend history 
obtained from Yahoo Finance.

TODO: Generalize this to work with different companies. Possiblly make a 
text file for each company containing custom inputs.
TODO: If ticker data is not available in the folder, find a way of 
downloading it from Yahoo Finance or another site. 
'''
import analyze

import pandas as pd
from pathlib import Path
import argparse
import yaml
# Load config file containing all paths.
with open('config.yml', 'r') as stream:
    try:
        paths = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def clean_data(data):
    '''
    Cleans the historical dividends data obtained from Yahoo Finance.
    The issues with data obtained from Yahoo Finance are
     - Yahoo Finance gives data that is unsorted
    '''
    data = data.sort_values(by='Date')
    return data

def check_ticker(ticker):
    '''
    Check if historical dividend data is available for that 
    ticker symbol.  
    '''
    
    ticker_list = get_tickers()
    if ticker in ticker_list:
        return ticker
    else:
        raise argparse.ArgumentError('Ticker symbol not available')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Looks at a company's historical record of dividend payouts.")
    parser.add_argument('ticker', type=check_ticker, help='The ticker symbol for the company under analysis')
    
    args = parser.parse_args()
    return args

def get_tickers():
    '''
    Returns a list of strings containing all the available ticker symbols 
    '''
    path = Path(paths['dividend_data_path'])
    files = path.glob('*.csv')
    return [x.stem for x in files if x.is_file()]

def main():
    # Parse arguments from user.
    args = parse_arguments()
    ticker_symbol = args.ticker
    # ticker_symbol = 'TD.TO'
    
    path = Path(paths['dividend_data_path'] + ticker_symbol + '.csv')
    data = pd.read_csv(path, index_col='Date', parse_dates=True)

    # Clean the data
    data = clean_data(data)

    # Analyze the data
    analyze.analyze(data) 

if __name__ == "__main__":

    main()

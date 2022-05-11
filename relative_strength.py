#!/usr/bin/python

# Required Libraries
import json, os

# Variables
basedir = "/path/to/your/base/directory"    # Base directory, edit as needed
json_file = os.path.join(basedir, 'daily_ohlc.json')  # Input json file
outperforming_stocks = []	# List of outperforming stocks (to sell puts)
underperforming_stocks = []	# List of underperforming stocks (to sell calls)

# Number of candles before latest candle to calculate ratios
long = 55	# Long period in days
short = 34	# Short period in days

# Fancy stuff for text color
CRED = '\33[31m'
CGREEN = '\33[32m'
CEND = '\033[0m'

# Read json file
with open(json_file, 'r') as fo:
	data = json.load(fo)

# Function to get close on a particular day for a particular symbol
def get_day_close(symbol, index):
	date = list(data[symbol].keys())[index]
	close = float(data[symbol][date]['close'])
	return close

# Calculate ratios for a symbol = Current close to close N days ago, for two periods long and short
def get_ratios(sym):
	latest_date = list(data['NIFTY'].keys())[-1]
	idx_latest = list(data[sym].keys()).index(latest_date)
	idx_long = idx_latest - long
	idx_short = idx_latest - short

	close_long = get_day_close(sym, idx_long)
	close_short = get_day_close(sym, idx_short)
	close_latest = get_day_close(sym, idx_latest)

	long_ratio = round(close_latest / close_long,2)
	short_ratio = round(close_latest / close_short,2)

	return(latest_date,close_latest,long_ratio,short_ratio)

latest_date_nifty,nifty_close,nifty_long_ratio,nifty_short_ratio = get_ratios("NIFTY")

# Header of the table
print("=" * 105)
print("{0:^18} {1:^8} {2:^12} {3:^10} {4:^10} {5:^10} {6:^10} {7:^13}".format("Symbol", "Date", "Close", "Stock-"+ str(long)+ "d", "Stock-" + str(short) + "d", "Nifty-" + str(long), "Nifty-" + str(short), "RelativeStrength"))
print("_" * 105)

# Iterate through all symbols, get the ratios and print the information
# Relatively strong only if both the ratios for a stock are greater than those for Nifty
for sym in sorted(data.keys()):
	latest_date,close,long_ratio,short_ratio = get_ratios(sym)
	if (long_ratio > nifty_long_ratio) and (short_ratio > nifty_short_ratio):
		rs = CGREEN + "Outperforming" + CEND
		outperforming_stocks.append(sym)
	elif (long_ratio < nifty_long_ratio) and (short_ratio < nifty_short_ratio):
		rs = CRED + "Underperforming" + CEND
		underperforming_stocks.append(sym)
	else:
		rs = "Sideways"

	if rs == "Outperforming Nifty":
		print("{0:^18} {1:^8} {2:^12} {3:^10} {4:^10} {5:^10} {6:^10} {7:^13}".format(sym, latest_date, close, long_ratio,short_ratio,nifty_long_ratio,nifty_short_ratio,rs))
	elif rs == "Underperforming Nifty":
		print("{0:^18} {1:^8} {2:^12} {3:^10} {4:^10} {5:^10} {6:^10} {7:^13}".format(sym, latest_date, close, long_ratio,short_ratio,nifty_long_ratio,nifty_short_ratio,rs))
	else:
		print("{0:^18} {1:^8} {2:^12} {3:^10} {4:^10} {5:^10} {6:^10} {7:^13}".format(sym, latest_date, close, long_ratio,short_ratio,nifty_long_ratio,nifty_short_ratio,rs))

print("=" * 105)

print(CGREEN + "Outperforming Nifty: " + CEND + ", ".join(outperforming_stocks))
print(CRED + "Underperforming Nifty: " + CEND + ", ".join(underperforming_stocks))

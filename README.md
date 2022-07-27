# EMA-Crossover-Backtester
Moving Average Crossovers are a widely used trading strategy characterised by their conceptual simplicity and ease of execution. It consists of setting values for two moving averages on the adjusted close prices time series of the security we're interested in trading and keeping track of their values. A buy signal will be generated when the short MA crosses the long MA and a sell signal will be generated when the long MA crosses the short MA.

When deploying a trading strategy it is of crucial importance to have previously backtested it. A backtest is a simulation of a trading strategy on past price data in order to analyse its performance and risk, which are then advantageous to decide whether to use it or not using real money.

The script takes the following variables as inputs: `ticker` (which is the string of the ticker of the security we want to backtest the strategy on), `years` (which is an integer and denotes the number of years' worth of data we want to perform the backtest on), `small_ma` (an integer, which is the small MA), `large_ma` (an integer, which is the large MA) and `initial_capital` (an integer, which is the amount of capital we want to deploy into the strategy). We must mention that this is a long-only backtester.

I shall explain my logic and rationale for the script before proceeding to outline the output metrics. We first import the standard data science modules and define the `Moving_Average_Crossover_Backtest` function, which takes the aforementioned inputs. Once we have set the basic parameters, we want to gather our data from Yahoo Finance using the `DataReader` function and remove all columns but the `'Adj Close'`, since it is the one that we will use. Note that we obtain the data from `years` years ago until today. Afterwards, we create the EMA colums in our dataframe, using a convenient pandas function, and delete the indexes in which information may be missing. We now want to know when the signals will happen. To do this, we create a `'Signal'` and `'Position'` columns. Looking at the position column, a value of 1 is a buy signal and a -1 is a sell signal.

Having prepared the data, we now create a new dataframe, `trade_history`, in which we will compile the trades that the strategy executes. We begin by compiling the days we buy and sell each position and their respective prices, by using the condition of the `'Position'` described above. Notice that if a given pair of EMA values would have a position open at the time the backtest is performed, there will be one sell day less. To overcome this, we run the backtest assumming that the position would have closed at the last trading day's `'Adj Close'` price.

Let's discuss the other properties of the trades. We are assumming that we are placing sufficiently large trades using Interactive Broker's Fixed - IB SmartRouting service in the United Kingdom, which charges 0.05% of trade value	as commission. The amount of shares that we buy when deploying capital to start a position is specifically selected so that the purchase price and the buying commission equals the totality of available capital. Gross PnL is computed by multiplying the difference of the sell and buy prices times the amount of shares. To compute the total commission, we must add the buying commissions to the selling commissions, namely 0.05% of the amount of shares times the sell price. We obtain net PnL by substracting total commissions from gross PnL. Equity is the sum of the previous final capital plus the net PnL. Once we have calculated these values for all trades, we create columns with said information and append them to our dataframe. We round the values in the `'trade_history'` dataframe for visualisation purposes, albeit we will perform all calculations with the actual values. 

We now print the parameters of the backtest and, if at least one trade is executed, we calculate the maximum loss (if there is at least one trade resulting in a loss), since it will be one of the output metrics, and the holding CAGR, namely, the CAGR of the traded asset from the beginning of the backtest period, which we will later use to inquire whether out strategy generates alpha or not. The majority of output metrics are fairly self-explanatory, except for `'CAGR Alpha'`, which is actually one of the most important ones. Alpha is the excess return a trading strategy or a portfolio generates in comparison to a benchmark, in our case, buying and holding our stock. It is very important to an investor because it informs of whether deploying a strategy will result in higher returns compared to the benchmark, and thus whether it is worth the effort. Larger alpha is better, although one must keep in mind that it can be as a result of overfitting and thus not generate such a significant alpha when deployed. The `'trade_history_rounded'` is also displayed, in case the user finds it useful. 

Below are the results of an example backtest:

**EMA Crossover Backtest Results**

**Parameters**
- Small MA: 25
- Large MA: 35
- Ticker: GOOG
- Period: 10 Year(s)
- Date: 2022-07-27
- Initial Capital: $18000

**Metrics**
- Number of Trades: 21
- Shares Traded: 16589.26
- Commissions Paid: $735.35

**Performance**
- Total Net PnL: $58343.75
- Total Net PnL Perc: 324.13%
- Indiv Net PnL Perc Mean: 8.24%
- Indiv Net PnL Perc SD: 17.63%
- CAGR: 15.54%
- CAGR Alpha: -6.03%
- Win Perc 57.14%
- Max Loss Perc: -9.65%

This material has been prepared for informational purposes only, and is not intended to provide, and should not be relied on for, financial tax, legal or accounting advice. You should consult your own financial, tax, legal and accounting advisors before engaging in any transaction.

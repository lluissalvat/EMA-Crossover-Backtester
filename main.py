import numpy as np 
import pandas as pd
import datetime
import pandas_datareader.data as web

def Moving_Average_Crossover_Backtest (ticker, years, small_ma, large_ma, initial_capital):

  start = (date.today()-timedelta(years*365))
  end = date.today()
  df = web.DataReader(ticker, 'yahoo', start, end)
  df = df.drop(['High','Low','Open','Close','Volume'], axis=1)

  df['Small MA'] = df['Adj Close'].ewm(span = small_ma, adjust = False).mean()
  df['Large MA'] = df['Adj Close'].ewm(span = large_ma, adjust = False).mean()
  df = df[df['Large MA'].notna()]

  df['Signal'] = 0 
  df['Signal'] = np.where(df['Small MA'] > df['Large MA'], 1, 0) 
  df['Position'] = df['Signal'].diff()
  df = df[df['Position'].notna()]

  trade_history = pd.DataFrame()

  buy_days = []
  sell_days = []
  buy_prices = []
  sell_prices = []

  for day in range(len(df)):

    if df['Position'][day] == 1:

      buy_days.append(df.index[day])
      buy_prices.append(df['Adj Close'][day])

    elif df['Position'][day] == -1:

      sell_days.append(df.index[day])
      sell_prices.append(df['Adj Close'][day])

  if len(buy_days) != len(sell_days):

    sell_days.append(df.index[-1])
    sell_prices.append(df['Adj Close'][-1])

  trade_history['Date Bought'] = buy_days
  trade_history['Date Sold'] = sell_days
  trade_history['Price Bought ($)'] = buy_prices
  trade_history['Price Sold ($)'] = sell_prices    
    
  gross_pnl = []
  shares = []
  commissions = []
  net_pnl = []
  net_pnl_perc = []
  equity = []

  equity.append(initial_capital)

  for trade in range(len(trade_history)):

    if trade == 0:

      trade_shares = equity[0]/(1.0005*trade_history['Price Bought ($)'][0])
      trade_gross_pnl = trade_shares*(trade_history['Price Sold ($)'][0]-trade_history['Price Bought ($)'][0])
      trade_commissions = equity[0]*0.0005+trade_history['Price Sold ($)'][0]*trade_shares*0.0005
      trade_net_pnl = trade_gross_pnl-trade_commissions
      trade_net_pnl_perc = trade_net_pnl/equity[0]*100
      trade_equity = trade_net_pnl+equity[0]

      shares.append(trade_shares)
      gross_pnl.append(trade_gross_pnl)
      commissions.append(trade_commissions)
      net_pnl.append(trade_net_pnl)
      net_pnl_perc.append(trade_net_pnl_perc)
      equity.append(trade_equity)

    elif trade > 0:

      trade_shares = equity[trade]/(1.0005*trade_history['Price Bought ($)'][trade])
      trade_gross_pnl = trade_shares*(trade_history['Price Sold ($)'][trade]-trade_history['Price Bought ($)'][trade])
      trade_commissions = equity[trade]*0.0005+trade_history['Price Sold ($)'][trade]*trade_shares*0.0005
      trade_net_pnl = trade_gross_pnl-trade_commissions
      trade_net_pnl_perc = trade_net_pnl/equity[trade] * 100
      trade_equity = trade_net_pnl+equity[trade]

      shares.append(trade_shares)
      gross_pnl.append(trade_gross_pnl)
      commissions.append(trade_commissions)
      net_pnl.append(trade_net_pnl)
      net_pnl_perc.append(trade_net_pnl_perc)
      equity.append(trade_equity)

  equity.pop(0)

  trade_history['Shares'] = shares
  trade_history['Gross PnL ($)'] = gross_pnl
  trade_history['Commissions ($)'] = commissions
  trade_history['Net PnL ($)'] = net_pnl
  trade_history['Net PnL (%)'] = net_pnl_perc
  trade_history['Equity ($)'] = equity

  trade_history_rounded = trade_history.round(decimals = {'Price Bought ($)':2,'Price Sold ($)':2,'Gross PnL ($)':2,'Net PnL (%)':2,'Equity ($)':2})
  
  print('EMA Crossover Backtest Results')
  print('')
  print('Parameters')
  print('- Small MA: '+str(small_ma))
  print('- Large MA: '+str(large_ma))
  print('- Ticker: '+ticker)
  print('- Period: '+str(years)+' Year(s)')
  print('- Date: '+str(end))
  print('- Initial Capital: $'+str(initial_capital))

  if len(trade_history) > 0:

    if len(trade_history[trade_history['Net PnL ($)']<0]) == 0:

      max_loss = 'There were no losses'

    else:

      max_loss = str(round(trade_history['Net PnL (%)'].min(),2)) + '%'

    holding_cagr = ((df['Adj Close'][-1]/df['Adj Close'][0])**(1/years)-1)*100

    print('')
    print('Metrics')
    print('- Number of Trades: '+str(len(trade_history)))
    print('- Shares Traded: '+str(round(trade_history['Shares'].sum(),2)))
    print('- Commissions Paid: $'+str(round(trade_history['Commissions ($)'].sum(),2)))
    print('')
    print('Performance')
    print('- Total Net PnL: $'+str(round(trade_history['Equity ($)'].iloc[-1]-initial_capital,2)))
    print('- Total Net PnL Perc: '+str(round((trade_history['Equity ($)'].iloc[-1]-initial_capital)/initial_capital*100,2))+'%')
    print('- Indiv Net PnL Perc Mean: '+str(round(trade_history['Net PnL (%)'].mean(),2))+'%')
    print('- Indiv Net PnL Perc SD: '+str(round(trade_history['Net PnL (%)'].std(),2))+'%')
    print('- CAGR: '+str(round(((trade_history['Equity ($)'].iloc[-1]/initial_capital)**(1/years)-1)*100,2))+'%')
    print('- CAGR Alpha: '+str(round(((trade_history['Equity ($)'].iloc[-1]/initial_capital)**(1/years)-1)*100-holding_cagr,2))+'%')
    print('- Win Perc '+str(round(len(trade_history[trade_history['Net PnL ($)']>0])/len(trade_history)*100,2))+'%')
    print('- Max Loss Perc: '+max_loss)
    print('')

  else:

    print('The specified parameters did not yield any positions')

  return trade_history_rounded

Moving_Average_Crossover_Backtest (ticker='GOOG', years=10, small_ma=25, large_ma=35, initial_capital=18000)

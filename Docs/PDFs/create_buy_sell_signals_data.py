#!/usr/bin/env python
# coding: utf-8

# # Rule:
# * Buy or sell with weekly chart gives me a 3 arrows at the same direction. 
# * Exit with when the day stockastic arrows gives me a opposit direction. 

# In[1]:


import pandas as pd


# In[17]:


day = pd.read_csv('day.csv')
three_day = pd.read_csv('3d.csv')
week = pd.read_csv('wk.csv')


# In[18]:


day['Date'] = pd.to_datetime(day['Date'])
three_day['Date'] = pd.to_datetime(three_day['Date'])
week['Date'] = pd.to_datetime(week['Date'])


# In[4]:


three_day.head(1)


# In[5]:


week = three_day
buy_date = []
action_type = []
buy_prices = []

for i in range(len(week)):
    if week.loc[i, 'SMA_Arrow'] == "UP" and week.loc[i, "MACD_Arrow"] == "UP" and week.loc[i, "Sto_Arrow"] == "UP":
        if week.loc[i-1, 'SMA_Arrow'] == "UP" and week.loc[i-1, "MACD_Arrow"] == "UP" and week.loc[i-1, "Sto_Arrow"] == "DOWN" or week.loc[i-1, 'SMA_Arrow'] == "UP" and week.loc[i-1, "MACD_Arrow"] == "DOWN" and week.loc[i-1, "Sto_Arrow"] == "UP" or week.loc[i-1, 'SMA_Arrow'] == "DOWN" and week.loc[i-1, "MACD_Arrow"] == "UP" and week.loc[i-1, "Sto_Arrow"] == "UP":
            date = week.loc[i, 'Date']
            buy_date.append(date)
            action = "BUY CALL"
            action_type.append(action)
            price = week.loc[i, 'Adj Close']
            buy_prices.append(price)
    if week.loc[i, 'SMA_Arrow'] == "DOWN" and week.loc[i, "MACD_Arrow"] == "DOWN" and week.loc[i, "Sto_Arrow"] == "DOWN":
        if week.loc[i-1, 'SMA_Arrow'] == "DOWN" and week.loc[i-1, "MACD_Arrow"] == "DOWN" and week.loc[i-1, "Sto_Arrow"] == "UP" or week.loc[i-1, 'SMA_Arrow'] == "DOWN" and week.loc[i-1, "MACD_Arrow"] == "UP" and week.loc[i-1, "Sto_Arrow"] == "DOWN" or week.loc[i-1, 'SMA_Arrow'] == "UP" and week.loc[i-1, "MACD_Arrow"] == "DOWN" and week.loc[i-1, "Sto_Arrow"] == "DOWN":
            date = week.loc[i, 'Date']
            buy_date.append(date)
            action = "BUY PUT"
            action_type.append(action)
            price = week.loc[i, 'Adj Close']
            buy_prices.append(price)


# In[29]:


from price_data import Data, DataMin

def set_buy_signals(df):
    """
    Detect all the buy signals I set up. 
        Buy signal: SMA, MACD, and Stockastic gives all UP or DOWN signals. 
    df: df.add_arrows
    """
    buy_date = []
    action_type = []
    buy_prices = []
    
    for i in range(len(df)):
        try:
        
            if df.loc[i, 'SMA_Arrow'] == "UP" and df.loc[i, "MACD_Arrow"] == "UP" and df.loc[i, "Sto_Arrow"] == "UP":
                if df.loc[i-1, 'SMA_Arrow'] == "UP" and df.loc[i-1, "MACD_Arrow"] == "UP" and df.loc[i-1, "Sto_Arrow"] == "DOWN" or df.loc[i-1, 'SMA_Arrow'] == "UP" and df.loc[i-1, "MACD_Arrow"] == "DOWN" and df.loc[i-1, "Sto_Arrow"] == "UP" or df.loc[i-1, 'SMA_Arrow'] == "DOWN" and df.loc[i-1, "MACD_Arrow"] == "UP" and df.loc[i-1, "Sto_Arrow"] == "UP":
                    date = df.loc[i, 'Date']
                    buy_date.append(date)
                    action = "BUY CALL"
                    action_type.append(action)
                    price = df.loc[i, 'Adj Close']
                    buy_prices.append(price)
            if df.loc[i, 'SMA_Arrow'] == "DOWN" and df.loc[i, "MACD_Arrow"] == "DOWN" and df.loc[i, "Sto_Arrow"] == "DOWN":
                if df.loc[i-1, 'SMA_Arrow'] == "DOWN" and df.loc[i-1, "MACD_Arrow"] == "DOWN" and df.loc[i-1, "Sto_Arrow"] == "UP" or df.loc[i-1, 'SMA_Arrow'] == "DOWN" and df.loc[i-1, "MACD_Arrow"] == "UP" and df.loc[i-1, "Sto_Arrow"] == "DOWN" or df.loc[i-1, 'SMA_Arrow'] == "UP" and df.loc[i-1, "MACD_Arrow"] == "DOWN" and df.loc[i-1, "Sto_Arrow"] == "DOWN":
                    date = df.loc[i, 'Date']
                    buy_date.append(date)
                    action = "BUY PUT"
                    action_type.append(action)
                    price = df.loc[i, 'Adj Close']
                    buy_prices.append(price)
                
        except:
            pass
        
    return pd.DataFrame({"Date Enter": buy_date, "Action": action_type, "Enter Price": buy_prices})


# In[27]:


df = Data("AMD", 50, freq="1D")
day = df.add_arrow
buy_data_d= set_buy_signals(day)


# In[28]:


pd.set_option('display.max_rows', 500)
buy_data_d


# In[10]:


buy_data_3d.to_csv('buy_data_3d.csv')


# In[26]:


day.head(1)


# In[30]:


def set_sell_signal(day):
    """
    Detect all the sell signals I set up. 
        Sell signal: Stockastic cross the lines. 
    best result so far is the Day signal. 
    day: df.add_arrows (day means df.)
    """
    sell_date = []
    action_type = []
    sell_prices = []

    for i in range(len(day)):
        try: 
            if day.loc[i, "Sto_Arrow"] == "UP":
                if day.loc[i-1, "SMA_Arrow"] == "DOWN" and day.loc[i-1, "MACD_Arrow"] == "DOWN" and day.loc[i-1, "Sto_Arrow"] == "DOWN":
                    date = day.loc[i, "Date"]
                    sell_date.append(date)
                    action = "SELL PUT"
                    action_type.append(action)
                    price = day.loc[i, "High"]
                    sell_prices.append(price)
            elif day.loc[i, "Sto_Arrow"] == "DOWN":
                if day.loc[i-1, "SMA_Arrow"] == "UP" and day.loc[i-1, "MACD_Arrow"] == "UP" and day.loc[i-1, "Sto_Arrow"] == "UP":
                    date = day.loc[i, "Date"]
                    sell_date.append(date)
                    action = "SELL CALL"
                    action_type.append(action)
                    price = day.loc[i, "Low"]
                    sell_prices.append(price)
        except:
            pass
        
    return pd.DataFrame({"Date Exit": sell_date, "Action": action_type, "Exit Price": sell_prices})


# In[31]:


df = Data("AMD", 50, freq='1D')
day_sell = df.add_arrow
sell_data = set_sell_signal(day_sell)
sell_data


# In[39]:


sell_data.to_csv("sell_data.csv")


# In[40]:


week = pd.read_csv("3d.csv")
buy_date = []
action_type = []
buy_prices = []

for i in range(len(week)):
    if week.loc[i, 'SMA_Arrow'] == "UP" and week.loc[i, "MACD_Arrow"] == "UP" and week.loc[i, "Sto_Arrow"] == "UP":
        if week.loc[i-1, 'SMA_Arrow'] == "UP" and week.loc[i-1, "MACD_Arrow"] == "UP" and week.loc[i-1, "Sto_Arrow"] == "DOWN" or week.loc[i-1, 'SMA_Arrow'] == "UP" and week.loc[i-1, "MACD_Arrow"] == "DOWN" and week.loc[i-1, "Sto_Arrow"] == "UP" or week.loc[i-1, 'SMA_Arrow'] == "DOWN" and week.loc[i-1, "MACD_Arrow"] == "UP" and week.loc[i-1, "Sto_Arrow"] == "UP":
            date = week.loc[i, 'Date']
            buy_date.append(date)
            action = "BUY CALL"
            action_type.append(action)
            price = week.loc[i, 'Adj Close']
            buy_prices.append(price)
    if week.loc[i, 'SMA_Arrow'] == "DOWN" and week.loc[i, "MACD_Arrow"] == "DOWN" and week.loc[i, "Sto_Arrow"] == "DOWN":
        if week.loc[i-1, 'SMA_Arrow'] == "DOWN" and week.loc[i-1, "MACD_Arrow"] == "DOWN" and week.loc[i-1, "Sto_Arrow"] == "UP" or week.loc[i-1, 'SMA_Arrow'] == "DOWN" and week.loc[i-1, "MACD_Arrow"] == "UP" and week.loc[i-1, "Sto_Arrow"] == "DOWN" or week.loc[i-1, 'SMA_Arrow'] == "UP" and week.loc[i-1, "MACD_Arrow"] == "DOWN" and week.loc[i-1, "Sto_Arrow"] == "DOWN":
            date = week.loc[i, 'Date']
            buy_date.append(date)
            action = "BUY PUT"
            action_type.append(action)
            price = week.loc[i, 'Adj Close']
            buy_prices.append(price)


# In[42]:


buy_data = pd.DataFrame({"Date Enter": buy_date, "Action": action_type, "Enter Price": buy_prices})
buy_data.to_csv("3days_buy.csv")


# In[48]:


day = pd.read_csv('3d.csv')
sell_date = []
action_type = []
sell_prices = []

for i in range(len(day)):
    try: 
        if day.loc[i, "Sto_Arrow"] == "UP":
            if day.loc[i-1, "SMA_Arrow"] == "DOWN" and day.loc[i-1, "MACD_Arrow"] == "DOWN" and day.loc[i-1, "Sto_Arrow"] == "DOWN":
                date = day.loc[i, "Date"]
                sell_date.append(date)
                action = "SELL PUT"
                action_type.append(action)
                price = day.loc[i, "High"]
                sell_prices.append(price)
        elif day.loc[i, "Sto_Arrow"] == "DOWN":
            if day.loc[i-1, "SMA_Arrow"] == "UP" and day.loc[i-1, "MACD_Arrow"] == "UP" and day.loc[i-1, "Sto_Arrow"] == "UP":
                date = day.loc[i, "Date"]
                sell_date.append(date)
                action = "SELL CALL"
                action_type.append(action)
                price = day.loc[i, "Low"]
                sell_prices.append(price)
    except:
        pass


# In[50]:


sell_data = pd.DataFrame({"Date Exit": sell_date, "Action": action_type, "Exit Price": sell_prices})
sell_data.to_csv("3days_sell.csv")


# In[ ]:





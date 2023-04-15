import datetime as dt
import pandas_datareader as pdr
import yfinance as yf
import talib as ta
from talib import MA_Type


class Data:
    def __init__(self, symbol, length):
        self.symbol = symbol
        self.length = length
        self.df = self.get_data()

    # function of obtaining data
    def get_data(self):
        now = dt.datetime.now()
        start = now.replace(now.year - self.length).strftime("%Y-%m-%d")
        end = now.strftime("%Y-%m-%d")

        yf.pdr_override()
        df = pdr.data.get_data_yahoo(self.symbol, start=start, end=end)
        return df

    def preprocess_data_1(self, data_for="Adj Close", SMA=True, sma5=5, sma10=10, sma20=20,
                        MACD=True, short_span=8, long_span=17, macd_span=9,
                        RSI=True, timeperiod=14, SOI=True, slowk_period=3, fastk_period=14,
                        Bband=False):
        """
        data_for: pick one of them ["Adj Close", "Open", "high", "Low"]
        """
        df = self.df.copy()
        # Fill the zero value on open price to previous closing price
        for i, open_price in enumerate(df["Open"]):
            if open_price == 0.0:
                df["Open"].iloc[i] = df["Adj Close"].iloc[i - 1]

        df["DiffClose$"] = df["Adj Close"].diff()
        df["DiffOpen$"] = df["Open"].diff()
        df["DiffHigh$"] = df["High"].diff()
        df["DiffLow$"] = df["Low"].diff()

        closeps = []
        openps = []
        highs = []
        lows = []
        for i in range(len(df)):
            closep = df["DiffClose$"].iloc[i] / df["Adj Close"].iloc[i - 1]
            closeps.append(closep)

        for i in range(len(df)):
            openp = df["DiffOpen$"].iloc[i] / df["Open"].iloc[i - 1]
            openps.append(openp)

        for i in range(len(df)):
            highp = df["DiffHigh$"].iloc[i] / df["High"].iloc[i - 1]
            highs.append(highp)

        for i in range(len(df)):
            lowp = df["DiffLow$"].iloc[i] / df["Low"].iloc[i - 1]
            lows.append(lowp)

        df["Closep"] = closeps
        df["Openp"] = openps
        df["Highp"] = highs
        df["Lowp"] = lows

        if data_for == "Adj Close":
            percent = "Closep"
        elif data_for == "Open":
            percent = "Openp"
        elif data_for == "High":
            percent = "Highp"
        else:
            percent = "Lowp"

        # SMA
        if SMA:
            df["SMA5"] = df[data_for].rolling(sma5).mean()
            df["SMA10"] = df[data_for].rolling(sma10).mean()
            df["SMA20"] = df[data_for].rolling(sma20).mean()

            df["smap5"] = df[percent].rolling(sma5).mean()
            df["smap10"] = df[percent].rolling(sma10).mean()
            df["smap20"] = df[percent].rolling(sma20).mean()

        # MACD
        if MACD:
            # Calculate the short term exponential moving average
            shortEMA = df[data_for].ewm(span=short_span, adjust=False).mean()
            # Calculate the long term exponential moving average
            longEMA = df[data_for].ewm(span=long_span, adjust=False).mean()
            # Calculate MACD line
            MACD = shortEMA - longEMA
            # calculate the signal line
            signal = MACD.ewm(span=macd_span, adjust=False).mean()
            # Add to the DataFrame
            df["MACD"] = MACD
            df["Signal Line"] = signal

            # Calculate the short term exponential moving average with stationary data
            shortEMA = df[percent].ewm(span=short_span, adjust=False).mean()
            # Calculate the long term exponential moving average
            longEMA = df[percent].ewm(span=long_span, adjust=False).mean()
            # Calculate MACD line
            MACD = shortEMA - longEMA
            # calculate the signal line
            signal = MACD.ewm(span=macd_span, adjust=False).mean()
            # Add to the DataFrame
            df["macdp"] = MACD
            df["signal_linep"] = signal

        # RSI
        if RSI:
            df["RSI"] = ta.RSI(df[data_for], timeperiod=timeperiod)

            df["rsip"] = ta.RSI(df[percent], timeperiod=timeperiod)

        # Stochastic
        if SOI:
            df["SlowK"], df["SlowD"] = ta.STOCH(high=df["High"],
                                                low=df["Low"],
                                                close=df["Adj Close"],
                                                slowk_period=slowk_period,
                                                fastk_period=fastk_period)

            df["slowKp"], df["slowDp"] = ta.STOCH(high=df["Highp"],
                                                  low=df["Lowp"],
                                                  close=df["Closep"],
                                                  slowk_period=slowk_period,
                                                  fastk_period=fastk_period)

        # Bollinger Band
        if Bband:
            df["Bband_upper"], df["Bband_mid"], df["Bband_lower"] = ta.BBANDS(df[data_for], matype=MA_Type.T3)

            df["BBuperp"], df["BBmidp"], df["BBlowp"] = ta.BBANDS(df[percent], matype=MA_Type.T3)

        return df

    def process_data_2(self, OBV=True, SMA=True, sma_short=10, sma_long=50,
                      MACD=True, short_span=8, long_span=17, macd_span=9,
                      RSI=True, timeperiod=14, SOI=True, fastk_period=14):
        """
        Add the indicators for later data manupulation.

        Args:
            symbol: Company simbol you want to obtain the data. (dtype=str)
            data_length: The length of the data you want to get. (e.g. 10 mean 10 years of data).

        All the indicator's default is True. If you don't want to get the data, set for False.
            OBV: On-Balance-Volume indicator.
            SMA: Simple Moving Average.
            sma_short: Short period of SMA. Default is 15.
            sma_long: Long period of SMA. Default is 50.
            MACD: MACD indicator.
            short_span: EMA short span for MACD.
            long_span: EMA long span for MACD.
            macd_span: MACD signal span.
                default (9, 12, 26) - (macd_span, short_span, long_span)
            RSI: RSI indicator.
            timeperiod: RSI time period. default is 14
            SOI: Stochastic Oscillator indicator.
            fastk_period: %K period. default is 14.
        """
        # Get the dataset and make a copy of it.

        df = self.df.copy()

        # Difference in the closing price each day
        df["Change"] = df["Close"].diff()
        # Show the direction of the movement
        df = df.dropna()
        df.reset_index(inplace=True)
        df["Direction"] = None
        for i in range(len(df)):
            if df["Change"][i] > 0:
                df.loc[i, "Direction"] = "UP"
            elif df["Change"][i] < 0:
                df.loc[i, "Direction"] = "DOWN"
            else:
                df.loc[i, "Direction"] = "SAME"

            # OBV
        if OBV:
            df["OBV"] = 0
            for i in range(len(df)):
                try:
                    if df["Direction"][i] == "UP":
                        df.loc[i, "OBV"] = df["Volume"][i] + df["OBV"][i - 1]
                    elif df["Direction"][i] == "DOWN":
                        df.loc[i, "OBV"] = df["OBV"][i - 1] - df["Volume"][i]
                    else:
                        df.loc[i, "OBV"] = 0 + df["OBV"][i - 1]
                except:
                    df.loc[i, "OBV"] = df["Volume"][i]

        # SMA
        if SMA:
            df["SMA/short"] = df["Close"].rolling(sma_short).mean()
            df["SMA/long"] = df["Close"].rolling(sma_long).mean()

        # MACD
        if MACD:
            # Calculate the short term exponential moving average
            shortEMA = df["Close"].ewm(span=short_span, adjust=False).mean()
            # Calculate the long term exponential moving average
            longEMA = df["Close"].ewm(span=long_span, adjust=False).mean()
            # Calculate MACD line
            MACD = shortEMA - longEMA
            # calculate the signal line
            signal = MACD.ewm(span=macd_span, adjust=False).mean()
            # Add to the DataFrame
            df["MACD"] = MACD
            df["Signal Line"] = signal

        # RSI
        if RSI:
            df["RSI"] = ta.RSI(df["Close"], timeperiod=timeperiod)

        # Stochastic
        if SOI:
            df["SlowK"], df["SlowD"] = ta.STOCH(high=df["High"],
                                                low=df["Low"],
                                                close=df["Close"],
                                                fastk_period=fastk_period)
        return df.dropna()




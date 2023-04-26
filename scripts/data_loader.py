from price_data import *
import pandas as pd
import os
import finnhub
from financial_data import FinancialDataFinnHub, FinancialDataYahoo
from dotenv import load_dotenv
load_dotenv()

# Obtain price history data from Yahoo Finance and add indicators
nvda = Data("NVDA", 50)
#df = nvda.preprocess_data_1()
df2 = nvda.process_data_2()
df2 = df2[-100:]
df2.to_csv(".\\Docs\\CSV_files\\nvda_data.csv", index=False)

# Obtain financial data from Finnhub
#finnhub_api_key = os.getenv("FINHUB_API_KEY")
#finnhub_client = finnhub.Client(api_key=finnhub_api_key)

#nvda_fin = FinancialDataFinnHub("NVDA", finnhub_api_key)
#print(nvda_fin.company_news)



# Obtain financial data from Yahoo finance
nvda_yahoo = FinancialDataYahoo("NVDA")
validation = nvda_yahoo.validation
quote_table = nvda_yahoo.quote_table
stats = nvda_yahoo.stats
analyst_info = nvda_yahoo.analyst_info

print(f"Validation: \n{validation}")
print(f"Quote table: \n{quote_table}")
print(f"Stats: \n{stats}")
print(f"Analyst info: \n{analyst_info}")


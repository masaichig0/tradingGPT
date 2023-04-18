import finnhub
from datetime import datetime, timedelta
import pandas as pd
import yahoo_fin.stock_info as si
from dotenv import load_dotenv
load_dotenv()


# From finnhub
class FinancialDataFinnHub:
    def __init__(self, symbol, api_key):
        self.today = datetime.now().date()
        self.symbol = symbol
        self.api_key = api_key
        self.bs_list_a, self.ic_list_a, self.fc_list_a = self._get_reports("annual")
        self.bs_list_q, self.ic_list_q, self.fc_list_q = self._get_reports("quarterly")

    @property
    def set_client(self): # Setup client
        return finnhub.Client(api_key=self.api_key)

    @property
    def company_info(self):
        company_info = self.set_client.company_profile2(symbol=self.symbol)
        return pd.DataFrame({"Attribute": company_info.keys(),
                            "Values": company_info.values()})

    @property
    def company_news(self):
        """
        Last 5 days of news.
        :return: List of dict Recent News
        """
        new_date = self.today - timedelta(days=1)
        _from = new_date.strftime("%Y-%m-%d")
        news =  self.set_client.company_news(self.symbol, _from=_from, to=self.today)
        dataframe = []
        for i in range(len(news)):
            single_data = pd.DataFrame({"News Number": news[i].keys(),
                                        0: news[i].values()})
            single_data = single_data.T
            header = single_data.iloc[0]
            single_data.columns = [header]
            single_data.drop(index="News Number", inplace=True)
            dataframe.append(single_data)
        index = pd.Index(range(len(dataframe)))
        return pd.concat(dataframe).set_index(index)

    @property
    def insiders(self):
        """
        Last 1 year of insider trading.
        :return:
        """
        new_date = self.today - timedelta(days=365)
        _from = new_date.strftime("%Y-%m-%d")
        # Insider Trading information
        insider = self.set_client.stock_insider_transactions(self.symbol, _from, self.today)
        insider_dict = insider["data"]
        dataframe = []
        for i in range(len(insider_dict)):
            single_data = pd.DataFrame({"Transaction Number": insider_dict[i].keys(),
                                        0: insider_dict[i].values()})
            single_data = single_data.T
            header = single_data.iloc[0]
            single_data.columns = [header]
            single_data.drop(index="Transaction Number", inplace=True)
            dataframe.append(single_data)
        index = pd.Index(range(len(dataframe)))
        return pd.concat(dataframe).set_index(index)

    @property
    def basic_financials(self):
        # Basic financials
        return pd.DataFrame(self.set_client.company_basic_financials(self.symbol, 'all'))

    @property
    def earning_surprises(self):
        # Earnings surprises
        return pd.DataFrame(self.set_client.company_earnings(self.symbol, limit=5))

    def _get_reports(self, freq):
        """
        Retrieve reports for the given frequency ('annual' or 'quarterly').
        :param freq: Frequency of reports ('annual' or 'quarterly').
        :return: Tuple of report lists for balance sheet, income statement, and cash flow.
        """
        report = self.set_client.financials_reported(symbol=self.symbol, freq=freq)

        years = [str(report['data'][i]['year']) for i in range(len(report['data']))]
        bss = [report['data'][i]['report']['bs'] for i in range(len(report['data']))]
        ics = [report['data'][i]['report']['ic'] for i in range(len(report['data']))]
        cfs = [report['data'][i]['report']['cf'] for i in range(len(report['data']))]

        bs_docs = {years[i]: bss[i] for i in range(len(years))}
        ic_docs = {years[i]: ics[i] for i in range(len(years))}
        cf_docs = {years[i]: cfs[i] for i in range(len(years))}

        bs_dfs = [pd.DataFrame(bs_docs[years[i]]) for i in range(len(years))]
        ic_dfs = [pd.DataFrame(ic_docs[years[i]]) for i in range(len(years))]
        cf_dfs = [pd.DataFrame(cf_docs[years[i]]) for i in range(len(years))]

        return bs_dfs, ic_dfs, cf_dfs


# Yahoo data
class FinancialDataYahoo:
    def __init__(self, symbol):
        self.symbol = symbol

    @property
    def quote_table(self):
        return si.get_quote_table(self.symbol, dict_result=False)

    @property
    def validation(self):
        return si.get_stats_valuation(self.symbol)

    @property
    def stats(self):
        return si.get_stats(self.symbol)

    @property
    def holders(self):
        """
        0: Major holders,
        1: Direct Holders,
        2: Top Institutional Holders,
        :return: list of holders DataFrame
        """
        holders_list = []
        holders = si.get_holders(self.symbol)
        for key in holders:
            holders_list.append(holders[key])
        return holders_list

    @property
    def analyst_info(self):
        """
        Earnings Estimate
            0: Earning Estimate
            1: Revenue Estimate
            2: Earnings History
            3: EPS Trend
            4: EPS Revisions
            5: Growth Estimates
        :return: List of Analyst info DataFrame
        """
        a_info_list = []
        analyst_info =  si.get_analysts_info(self.symbol)
        for key in analyst_info:
            a_info_list.append(analyst_info[key])
        return a_info_list

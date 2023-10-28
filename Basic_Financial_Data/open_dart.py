#%%
import OpenDartReader
import FinanceDataReader as fdr
import numpy as np
import pandas as pd
from tabulate import tabulate as tb

# from IPython.display import display

def GetStockPrice(sp_data, date):
    sp_data.reset_index(inplace=True) #HAVE TO DO THIS CUZ THE sp_data returns Date as default index. So changing it back to column
    date = pd.to_datetime(date)

    #If the there isn't any stock value equivalent
    #NOTE: we are assuming that the date inputed is NEVER a weekend.

    if sp_data['Date'].max() < date:
        return np.nan
    else:
        while True:
            if sum(sp_data['Date'] == date) > 0:
                value = sp_data[sp_data['Date'] == date]
                value = sp_data['Close'].iloc[0]
                break
            else:
                date += pd.to_timedelta(1, 'day')
        return value

def GetReport(dart, corp_code: str, year: int) -> dict:
    key_info = {
        'EPS': {'current_EPS':0,'previous_EPS':0,'sprevious_EPS':0,}
    }
    report = dart.report(corp_code, "배당", year, "11012")

    if report is None:
        key_info = {
            'EPS': np.nan
        }
    else:
        # print(tb(report, headers='keys'))

        #GETTING THE EPS
        EPS = report[(report['se'].str.contains('주당순이익'))]
        key_info['EPS']['current_EPS'] = EPS['thstrm'].str.replace(",","").astype(float).values[0]
        key_info['EPS']['previous_EPS'] = EPS['frmtrm'].str.replace(",","").astype(float).values[0]
        key_info['EPS']['sprevious_EPS'] = EPS['lwfr'].str.replace(",","").astype(float).values[0]

    return key_info

def GetFinState(dart, corp_code: str, year: int) -> dict:
    BasicInfo = {
        'Debt_Equity_Ratio' : 0,
        'Total_Assets' : 0,
        'Total_Equity':0,
        'Total_Debt':0,
        'Operating_Income': {'3month':0, 'add':0},
        'Net_Income':{'3month':0, 'add':0}
    }
    finstate = dart.finstate(corp_code, year, "11012")

    #getting the total assets
    finstate_debt = finstate.loc[(finstate["account_nm"] == "자산총계") & (finstate["fs_nm"] == '재무제표')]
    finstate_debt = finstate_debt[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'thstrm_dt', 'thstrm_amount']]
    BasicInfo['Total_Assets'] = finstate_debt['thstrm_amount'].str.replace(",","").astype(float).values[0]
    
    #getting the total debt
    finstate_debt = finstate.loc[(finstate["account_nm"] == "부채총계") & (finstate["fs_nm"] == '재무제표')]
    finstate_debt = finstate_debt[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'thstrm_dt', 'thstrm_amount']]
    BasicInfo['Total_Debt'] = finstate_debt['thstrm_amount'].str.replace(",","").astype(float).values[0]

    #getting the total equity
    finstate_equity = finstate.loc[(finstate["account_nm"] == "자본총계") & (finstate["fs_nm"] == '재무제표')]
    finstate_equity = finstate_equity[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'thstrm_dt', 'thstrm_amount']]
    BasicInfo['Total_Equity'] = finstate_equity['thstrm_amount'].str.replace(",","").astype(float).values[0]

    debt_equity_ratio = finstate_debt['thstrm_amount'].str.replace(",","").astype(float).values / finstate_equity['thstrm_amount'].str.replace(",","").astype(float).values * 100
    #The .values at the end only extracts the value from the df into an array. Cuz without it it would return a df with an index, and a value, like this
    #   5    1.060509e+13
    #Then this return an ARRAY. the real float value is in the [0]
    BasicInfo['Debt_Equity_Ratio'] = debt_equity_ratio[0]

    #getting the total assets
    finstate_OI = finstate.loc[(finstate["account_nm"] == "영업이익") & (finstate["fs_nm"] == '재무제표')]
    finstate_OI = finstate_OI[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'frmtrm_add_amount', 'thstrm_dt', 'thstrm_amount', 'thstrm_add_amount']]
    BasicInfo['Operating_Income']['3month'] = finstate_OI['thstrm_amount'].str.replace(",","").astype(float).values[0]
    BasicInfo['Operating_Income']['add'] = finstate_OI['thstrm_add_amount'].str.replace(",","").astype(float).values[0]

    #getting the total assets
    finstate_debt = finstate.loc[(finstate["account_nm"] == "당기순이익") & (finstate["fs_nm"] == '재무제표')]
    finstate_debt = finstate_debt[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'frmtrm_add_amount', 'thstrm_dt', 'thstrm_amount', 'thstrm_add_amount']]
    BasicInfo['Net_Income']['3month'] = finstate_debt['thstrm_amount'].str.replace(",","").astype(float).values[0]
    BasicInfo['Net_Income']['add'] = finstate_debt['thstrm_add_amount'].str.replace(",","").astype(float).values[0]


    return BasicInfo

def main():
    #INITIALIZING THE API KEY.
    my_api = "d846275c00eff1f16dc3b0b724da1327a00141b8" #PUT YOU OWN API KEY HERE
    dart = OpenDartReader(my_api)
    
    #GETTING THE LIST OF NAMES AND THEIR CORPORATE CODES IN THE KOSPI
    KOP_list = fdr.StockListing('KOSPI')
    KOP_list = KOP_list.loc[0:100, ['Code', 'Name']]
    name_code = dict(zip(KOP_list['Name'], KOP_list['Code']))

    GetFinState(dart, name_code['삼성전자'], 2023)
    GetReport(dart, name_code['삼성전자'], 2023)

    sp_data = fdr.DataReader("005380", "2020-10-01", "2023-10-28")
    print(GetStockPrice(sp_data, "2023-10-25"))

    return 0

if __name__ == "__main__":
    main()
# %%

#%%
import OpenDartReader
import FinanceDataReader as fdr
import numpy as np
import pandas as pd
from tabulate import tabulate as tb
from datetime import datetime
from datetime import date

# from IPython.display import display

def GetDateToday():
    today = date.today()
    x = today.weekday()
    today = pd.to_datetime(today)
    while x > 4:
        today -= pd.to_timedelta(1, 'D')
        x -= 1
    return today

def GetStockPrice(sp_data, date):
    sp_data.reset_index(inplace=True) #HAVE TO DO THIS CUZ THE sp_data returns Date as default index. So changing it back to column
    date = pd.to_datetime(date)

    #If the there isn't any stock value equivalent
    #NOTE: we are assuming that the date inputed is NEVER a weekend.
    if sp_data['Date'].max() < date:
        print(sp_data['Date'].max())
        return np.nan
    else:
        while True:
            if sum(sp_data['Date'] == date) > 0:
                sp_data = sp_data[sp_data['Date'] == date]
                value = sp_data['Close'].iloc[0]
                break
            else:
                date += pd.to_timedelta(1, 'day')
        return value

def GetReport(dart, corp_code: str, year: int, today) -> dict:
    key_info = {
        'EPS': {'current_EPS':0,'previous_EPS':0,'sprevious_EPS':0,}
    }
    try:
        report = dart.report(corp_code, "배당", year, "11012")
        sp_data = fdr.DataReader(corp_code, "2020-10-01", today)
    except:
        key_info = {
            'EPS': np.nan,
            'PER': np.nan
        }
        return key_info

    # print(tb(report, headers='keys'))

    if report.empty:
        key_info = {
            'EPS': np.nan
        }
    else:
        #GETTING THE EPS
        EPS = report[(report['se'].str.contains('주당순이익'))]
        try:
            key_info['EPS']['current_EPS'] = EPS['thstrm'].str.replace(",","").astype(float).values[0]
            key_info['EPS']['previous_EPS'] = EPS['frmtrm'].str.replace(",","").astype(float).values[0]
            key_info['EPS']['sprevious_EPS'] = EPS['lwfr'].str.replace(",","").astype(float).values[0]
            key_info['PER'] = GetStockPrice(sp_data, today) / key_info['EPS']['current_EPS']
        except:
            key_info = {
                'EPS': np.nan,
                'PER': np.nan
            }


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
    try:
        finstate = dart.finstate(corp_code, year, "11012")
    except:
        key_info = {
            'Debt_Equity_Ratio' : np.nan,
            'Total_Assets' : np.nan,
            'Total_Equity':np.nan,
            'Total_Debt':np.nan,
            'Operating_Income': {'3month':np.nan, 'add':np.nan},
            'Net_Income':{'3month':np.nan, 'add':np.nan}
        }
        return key_info

    if finstate.empty:
        key_info = {
            'Debt_Equity_Ratio' : np.nan,
            'Total_Assets' : np.nan,
            'Total_Equity':np.nan,
            'Total_Debt':np.nan,
            'Operating_Income': {'3month':np.nan, 'add':np.nan},
            'Net_Income':{'3month':np.nan, 'add':np.nan}
        }
        return key_info

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

    #getting the total Operating Income
    finstate_OI = finstate.loc[(finstate["account_nm"] == "영업이익") & (finstate["fs_nm"] == '재무제표')]
    finstate_OI = finstate_OI[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'frmtrm_add_amount', 'thstrm_dt', 'thstrm_amount', 'thstrm_add_amount']]
    BasicInfo['Operating_Income']['3month'] = finstate_OI['thstrm_amount'].str.replace(",","").astype(float).values[0]
    BasicInfo['Operating_Income']['add'] = finstate_OI['thstrm_add_amount'].str.replace(",","").astype(float).values[0]

    #getting the total Net_Income
    finstate_debt = finstate.loc[(finstate["account_nm"] == "당기순이익") & (finstate["fs_nm"] == '재무제표')]
    finstate_debt = finstate_debt[['fs_nm', 'frmtrm_dt', 'frmtrm_amount', 'frmtrm_add_amount', 'thstrm_dt', 'thstrm_amount', 'thstrm_add_amount']]
    try:
        BasicInfo['Net_Income']['3month'] = finstate_debt['thstrm_amount'].str.replace(",","").astype(float).values[0]
        BasicInfo['Net_Income']['add'] = finstate_debt['thstrm_add_amount'].str.replace(",","").astype(float).values[0]
    except:
        BasicInfo['Net_Income']['3month'] = np.nan
        BasicInfo['Net_Income']['add'] = np.nan

    return BasicInfo

def main():
    #INITIALIZING THE API KEY.
    my_api = "" #PUT YOU OWN API KEY HERE
    dart = OpenDartReader(my_api)

    today = GetDateToday()

    #GETTING THE LIST OF NAMES AND THEIR CORPORATE CODES IN THE KOSPI
    KOP_list = fdr.StockListing('KOSPI')
    KOP_list = KOP_list.loc[0:100, ['Code', 'Name']]
    name_code = dict(zip(KOP_list['Name'], KOP_list['Code']))

    #AN PRACTICAL EXAMPLE:
    #I WANT THE LIST OF ALL THE COMPANIES WITH DEBT_EQUITY_RATIO OF OVER 400%
    companies_with_DER_bigger_than_400 = {
        # 'Name':dbr
    }

    count = 1
    for names in name_code:
        # print(f"count: {count}")
        # print(names)
        finstate = GetFinState(dart, name_code[names], 2023)
        # GetReport(dart, name_code[names], 2023)
        count += 1
        try:
            if finstate['Debt_Equity_Ratio'] > 400:
                companies_with_DER_bigger_than_400[names] = finstate['Debt_Equity_Ratio']
        except:
            pass
    print(companies_with_DER_bigger_than_400)
    return 0

if __name__ == "__main__":
    main()
# %%

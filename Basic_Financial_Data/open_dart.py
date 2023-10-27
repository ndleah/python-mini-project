#%%
import OpenDartReader
import FinanceDataReader as fdr
import numpy as np
from tabulate import tabulate as tb
from IPython.display import display

def GetReport(dart, corp_code: str, year: int) -> dict:
    key_info = {
        'EPS': {'current_EPS':0,'previous_EPS':0,'sprevious_EPS':0,}
    }
    report = dart.report(corp_code, "배당", year, "11012")
    if report is None:
        key_info = {
            'EPS': np.nan #EPS 주당순이익
        }
    else:
        # print(tb(report, headers='keys'))

        #GETTING THE EPS
        EPS = report[(report['se'].str.contains('주당순이익'))]
        key_info['EPS']['current_EPS'] = EPS['thstrm'].str.replace(",","").astype(float).values[0]
        key_info['EPS']['previous_EPS'] = EPS['frmtrm'].str.replace(",","").astype(float).values[0]
        key_info['EPS']['sprevious_EPS'] = EPS['lwfr'].str.replace(",","").astype(float).values[0]

    return key_info

def GetFinState(dart, corp_code: str) -> dict:
    BasicInfo = {
        'Debt_Equity_Ratio' : 0,
        'Total_Assets' : 0,
        'Total_Equity':0,
        'Total_Debt':0,
        'Operating_Income':0,
        'Net_Income':0
    }

    finstate = dart.finstate(corp_code, 2023, "1102")

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

    return BasicInfo

def main():
    my_api = "d846275c00eff1f16dc3b0b724da1327a00141b8"
    dart = OpenDartReader(my_api)
    
    KOP_list = fdr.StockListing('KOSPI')
    KOP_list = KOP_list.loc[0:100, ['Code', 'Name']]
    name_code = dict(zip(KOP_list['Name'], KOP_list['Code']))
    # print(GetFinState(dart, "035720"))
    # print(GetReport(dart, "035720", 2023))

    return 0

if __name__ == "__main__":
    main()
# %%

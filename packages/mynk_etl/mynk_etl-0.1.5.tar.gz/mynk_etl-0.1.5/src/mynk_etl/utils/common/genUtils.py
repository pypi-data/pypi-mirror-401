
from typing import Any
from mynk_etl.utils.common.constants import Constants


def param_init(key: str) -> Any:

    conf_key = key.split('.')[0]
    prop_key = key.split('.')[1]
    conf_dict = Constants.INFRA_CFG.value[conf_key]
    prop_dict = Constants.TBL_CFG.value[conf_key][prop_key]

    return prop_key, conf_dict, prop_dict


def fetch_db_dtl(db_type: str) -> dict[str, str | int]:
    db_dtl = Constants.INFRA_CFG.value[db_type]
    return db_dtl


'''@logtimer
@staticmethod
def niftySymbols(url: str) -> list[str]:
    
    session = requests.Session()
    r = session.get(BASE_URL, headers=HEADERS, timeout=5)
    cookies = dict(r.cookies)
    
    response = session.get(url, timeout=5, headers=HEADERS, cookies=cookies)
    content = response.content.decode('utf-8')

    columns=['Company Name', 'Industry', 'Symbol', 'Series', 'ISIN Code']
    data_lst = [x.strip().split(',') for x in content.splitlines() if x.strip().split(',') != columns]              

    df=pd.DataFrame(data_lst, columns=columns)
    symbols_lst = df['Symbol'].tolist()
    
    return symbols_lst'''

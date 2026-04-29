import requests, json, sys

url = 'https://np-anotice-stock.eastmoney.com/api/security/ann'
params = {
    'sr': -1,
    'page_size': 50,
    'page_index': 1,
    'ann_type': 'A',
    'stock_list': '002371',
    'f_node': '0',
    's_node': '0',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://data.eastmoney.com/',
}

try:
    r = requests.get(url, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)

found = False
if data.get('data') and data['data'].get('list'):
    for item in data['data']['list']:
        title = item.get('title', '')
        date = item.get('notice_date', '')[:10] if item.get('notice_date') else ''
        keywords = ['业绩预', '快报', '一季报', '半年报', '三季报', '年报', '业绩预告']
        if any(k in title for k in keywords):
            print(f'{date} | {title}')
            found = True

if not found:
    print('未找到业绩相关公告')

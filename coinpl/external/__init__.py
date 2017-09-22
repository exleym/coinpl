import requests

def download_qr_code_from_google(wallet, size=250):
    base = 'https://chart.googleapis.com/chart?'
    base_path = '/coinpl/coinpl/static/img/qrcodes/'
    url = base + 'chs={}&cht=qr&chl={}'.format(
        '{}x{}'.format(size, size),
        wallet.address
    )
    path = base_path + 'wallet_qr_{}.png'.format(wallet.id)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    return 0
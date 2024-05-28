import glob
import re

import httpx
from tqdm import tqdm


def download():
    pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}) \[download 4k\]\((https[^\)]+)\)')
    months = glob.glob('picture/*/README.md')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'}
    with httpx.Client(headers=headers) as client:
        tqdm_months = tqdm(months)
        for month in tqdm_months:
            tqdm_months.set_description(f'Handling {month}')
            content = open(month, 'r', encoding='utf-8').read()
            urls = pattern.findall(content)

            tqdm_urls = tqdm(urls, desc='Downloading')
            for name, url in tqdm_urls:
                tqdm_urls.set_description(f'Downloading {name}')

                for _ in range(3):
                    try:
                        with open(f'download/{name}.jpg', 'wb') as file:
                            file.write(client.get(url).read())
                    except:
                        pass
                    finally:
                        break

if __name__ == '__main__':
    download()

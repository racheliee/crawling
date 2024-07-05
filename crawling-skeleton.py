import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the header for the request
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# List URLs that we want to crawl
urls = [
    'https://www.investing.com/equities/nike',
    'https://www.investing.com/equities/coca-cola-co',
    'https://www.investing.com/equities/microsoft-corp',
    'https://www.investing.com/equities/3m-co',
    'https://www.investing.com/equities/american-express',
    'https://www.investing.com/equities/amgen-inc',
    'https://www.investing.com/equities/apple-computer-inc',
    'https://www.investing.com/equities/boeing-co',
    'https://www.investing.com/equities/cisco-sys-inc',
    'https://www.investing.com/equities/goldman-sachs-group',
    'https://www.investing.com/equities/ibm',
    'https://www.investing.com/equities/intel-corp',
    'https://www.investing.com/equities/jp-morgan-chase',
    'https://www.investing.com/equities/mcdonalds',
    'https://www.investing.com/equities/salesforce-com',
    'https://www.investing.com/equities/verizon-communications',
    'https://www.investing.com/equities/visa-inc',
    'https://www.investing.com/equities/wal-mart-stores',
    'https://www.investing.com/equities/disney',
]

# Loop through the URLs and get the data
all_data = []
for url in urls:
    try:
        # TODO: response 가져오기 & soup 만들기
        
        
        # TODO: Find and extract the data (필요하면 error handling 추가)

    except AttributeError:
        print(f"Change the Element id for URL: {url}")
    except Exception as e:
        print(f"An error occurred for URL: {url} - {e}")

# TODO: 데이터가 수집되었는지 확인하기
if all_data:
    # TODO: Store the data in a DataFrame
    
    # TODO: Save the data to an Excel file
else:
    print("No data was collected.")

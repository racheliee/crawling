import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the header for the request to avoid being blocked
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
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        # soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find and extract the data
        # Example of the elements to extract: company
        # <h1 class="mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr">Nike Inc (NKE)</h1>
        
        company = soup.find('h1', {'class': 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'})
        price = soup.find('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]', 'data-test': 'instrument-price-last'})
        price_change = soup.find('span', {'data-test': 'instrument-price-change'})
        volume_label = soup.find('span', text='Volume')
        volume = volume_label.find_next('span') if volume_label else None
        
        # Check if all elements are found
        if company and price and price_change and volume:
            company_text = company.text.strip()
            price_text = price.text.strip()
            change_text = price_change.text.strip()
            volume_text = volume.text.strip()
            
            print(f"Company: {company_text}, Price: {price_text}, Change: {change_text}, Volume: {volume_text}")
            all_data.append([company_text, price_text, change_text, volume_text])
        else:
            print(f"Missing data in URL: {url}")
    except AttributeError:
        print(f"Change the Element id for URL: {url}")
    except Exception as e:
        print(f"An error occurred for URL: {url} - {e}")

# Check if data was collected
if all_data:
    # Store the data in a DataFrame
    column_names = ['Company', 'Price', 'Price Change', 'Volume']
    df = pd.DataFrame(all_data, columns=column_names)
    
    # Save the data to an Excel file
    df.to_excel('stock_data.xlsx', index=False)
    print("Data successfully saved to 'stock_data.xlsx'.")
else:
    print("No data was collected.")

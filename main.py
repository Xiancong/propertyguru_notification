from crawler.config import load_config, get_config
from crawler.crawler import PropertyGuruCrawler
import os
import pandas as pd

def main():
    config = load_config()

    csv_path = get_config(config,"csv_path","Please provide the path to the output CSV")
    api_url = get_config(config,"api_url","Please provide the API endpoint")
    headers = get_config(config,"headers","No headers provided",True)
    base_params = [[k,v] for k, v in get_config(config,"base_params","Base params not provided",True).items()]
    map_areas = get_config(config,"map_areas","No coordinates provided",True)

    crawler = PropertyGuruCrawler()
    crawler.crawl(csv_path, api_url, headers, base_params, map_areas)

    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
    else:
        existing_df = pd.DataFrame(columns=['property ID', 'date'])

    new_properties = crawler.detect_new_properties(existing_df)
    crawler.save_properties(new_properties, existing_df)
    crawler.print_new_links(new_properties)

if __name__ == "__main__":
    main()

from crawler.config import load_config, get_config
from crawler.crawler import PropertyGuruCrawler
from telegram import telegram_notification
import os
import pandas as pd

def main():
    config = load_config()

    csv_path = get_config(config,"csv_path","Please provide the path to the output CSV")
    api_url = get_config(config,"api_url","Please provide the API endpoint")
    token = get_config(config,"token","Please provide the API endpoint")
    chat_id = get_config(config,"chat_id","Please provide the API endpoint")
    headers = get_config(config,"headers","No headers provided",True)
    base_params = [[k,v] for k, v in get_config(config,"base_params","Base params not provided",True).items()]
    map_areas = get_config(config,"map_areas","No coordinates provided",True)

    crawler = PropertyGuruCrawler()
    crawler.crawl(api_url, headers, base_params, map_areas)

    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
    else:
        existing_df = pd.DataFrame(columns=['property ID', 'date'])

    new_properties, property_count = crawler.detect_new_properties(existing_df)
    crawler.save_properties(new_properties, existing_df, csv_path)
    crawler.print_new_links(new_properties)

    alerts = telegram_notification(token, chat_id)
    alerts.new_properties_notification(new_properties, property_count)

if __name__ == "__main__":
    main()

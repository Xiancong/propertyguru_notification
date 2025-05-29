from datetime import datetime
from dataclasses import dataclass, field
from typing import Set, List
import requests
import pandas as pd
import time

@dataclass
class PropertyGuruCrawler:
    collected_ids: Set[int] = field(default_factory=set)

    def fetch_clusters(self, api_url, headers, base_params, params: List[tuple]) -> None:
        query_params = base_params + params
        print(headers)
        response = requests.get(api_url, params=query_params, headers=headers)
        time.sleep(1)

        if response.status_code != 200:
            print(f"Failed to fetch data with status code {response.status_code}")
#             print(query_params)
#             print(response.json())
            return

        data = response.json()
        for cluster in data.get('clusters', []):
            self.collected_ids.update(cluster.get('ids', []))

    def crawl(self, api_url, headers, base_params, map_areas):
        for area in map_areas:
            print(f"Fetching area: {area}")
            self.fetch_clusters(api_url, headers, base_params, area)

    def detect_new_properties(self, existing_df: pd.DataFrame) -> pd.DataFrame:
        new_df = pd.DataFrame(self.collected_ids, columns=['property ID'])
        merged_df = new_df.merge(existing_df, how='left', on='property ID')
        new_props = merged_df[merged_df['date'].isnull()].copy()
        new_props['date'] = datetime.now().strftime('%Y-%m-%d')
        return new_props

    def save_properties(self, new_df: pd.DataFrame, existing_df: pd.DataFrame) -> None:
        combined = pd.concat([existing_df, new_df], ignore_index=True)
        combined.to_csv(csv_path, index=False)
        print(f"Saved updated dataset with {len(new_df)} new properties.")

    def print_new_links(self, new_df: pd.DataFrame) -> None:
        for property_id in new_df['property ID']:
            print(property_url_template.format(property_id=property_id))

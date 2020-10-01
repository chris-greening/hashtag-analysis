#Author: Chris Greening
#Date: 08/30/2020
#Purpose: Data analysis regarding instagram hashtags

import matplotlib.pyplot as plt
import pandas as pd

CSV_FPATH = r'D:\Programming\pythonstuff\InstagramScraper\hashtags.csv'
SECONDS_PER_HR = 3600

class HashtagAnalyzer:
    """Analyze hashtag data collected for a collection of hashtags"""
    def __init__(self, csv_fpath):
        self.csv_fpath = csv_fpath
        self._load_dataframes()
        self._total_changes()

    def _load_dataframes(self):
        """Load DataFrame's from the total csv"""
        self.total_df = pd.read_csv(self.csv_fpath)

        hashtag_names = self.total_df['hashtag'].unique()
        self.hashtags = {}
        for tag in hashtag_names:
            tag_df = self.total_df[self.total_df['hashtag'] == tag]
            self.hashtags[tag] = Hashtag(hashtag=tag, df=tag_df)

    def _total_changes(self):
        """Construct a DataFrame of all hashtags total changes"""
        all_data = []
        for tag in self.hashtags.values():
            tag_data = tag.total_change.copy()
            tag_data['hashtag'] = tag.hashtag
            all_data.append(tag_data)
        self.total_change_df = pd.DataFrame(all_data)

        #Dynamically reorder columns so that hashtag is first no matter what
        columns = [tag for tag in self.total_change_df.columns if tag != 'hashtag']
        columns[0] = 'hashtag'
        self.total_change_df = self.total_change_df[columns]

class Hashtag:
    """Data collection and analysis from a single hashtag"""
    def __init__(self, hashtag, df):
        self.hashtag = hashtag
        self.df = df

        self._clean_up_dataframe()
        self._calculate_total_change()

    def _clean_up_dataframe(self):
        """Clean up DataFrame to a more presentable, usable format"""
        self.df = self.df.reset_index(drop=True)
        self.df = self.df.drop(columns=['hashtag'])  #this column is irrelevant
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df['datetime'] = self.df['datetime'].astype('datetime64[s]')

    def change_between(self, i=0, j=-1):
        """
        Returns a DataFrame with analysis regarding
        how a hashtag has changed over time.
        """
        if j < 0:
            j = len(self.df) + j
        delta_data = []
        while i < j:
            if i == j:
                break
            else:
                delta_data.append(self.row_delta(i, i+1))
            i += 1
        return pd.DataFrame(delta_data)

    def row_delta(self, i, j):
        """Return change in data between two indices"""
        first_row = self.df.iloc[i]
        second_row = self.df.iloc[j]
        time_diff = self.calculate_timedelta_in_hours(i, j)
        data_dict = {}
        data_dict['post_diff'] = second_row['posts'] - first_row['posts']
        data_dict['time'] = second_row['datetime']
        data_dict['time_diff_in_hrs'] = time_diff
        data_dict['avg_posts_per_hr'] = data_dict['post_diff']/time_diff
        data_dict['percent_rate_of_change'] = (data_dict['avg_posts_per_hr']/first_row['posts'])*100
        return data_dict

    def _calculate_total_change(self):
        """Get difference between newest and oldest data entries"""
        self.delta_df = self.change_between()
        self.total_change = self.row_delta(0, -1)

    def calculate_timedelta_in_hours(self, i, j):
        """Returns how many hours passed between the start index and the end index"""
        start_time = self.df['datetime'].iloc[i]
        end_time = self.df['datetime'].iloc[j]
        diff = end_time - start_time
        return diff.total_seconds()/SECONDS_PER_HR

    def plot_df(self, x_axis: str, y_axis: str):
        plt.plot(self.df[x_axis], self.df[y_axis])

    def plot_delta_df(self, x_axis: str, y_axis: str):
        plt.plot(self.delta_df[x_axis], self.delta_df[y_axis])

    def __repr__(self):
        return f'<Hashtag: {self.hashtag}>'

def main():
    """Main driver function"""
    analyzer = HashtagAnalyzer(csv_fpath=CSV_FPATH)
    return analyzer

if __name__ == '__main__':
    ANALYZER = main()

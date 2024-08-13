import pandas as pd

country_df = pd.read_csv('../../PycharmProjects/travel_pare/datasets/countries of the world.csv', header=0)

# Strip whitespace from values
country_df = country_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

def unique_regions():
    return country_df['Region'].unique()


def filter_for_population_in_between(min_pop, max_pop):
    return ((country_df['Population'] > min_pop) & (country_df['Population'] < max_pop))


def countries_in_region(region):
    return country_df[country_df['Region'] == region]['Country'].tolist()


if __name__ == '__main__':
    country_df = pd.read_csv('../../PycharmProjects/travel_pare/datasets/countries of the world.csv', header=1)

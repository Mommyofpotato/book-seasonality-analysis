import pandas as pd

df = pd.read_csv("/Users/laurensisson/Downloads/best sellin books total.csv", encoding='latin1')

# clean publishing date text first
df['Publishing date'] = df['Publishing date'].astype(str).str.replace(
    r'(\d+)(st|nd|rd|th)', r'\1', regex=True
)

df['Publishing Date Clean'] = pd.to_datetime(
    df['Publishing date'],
    errors='coerce',
    dayfirst=True
)

df_long = df.melt(
    id_vars=['Book name', 'Genre', 'Publishing Date Clean'],
    value_vars=['id_2023', 'id_2024', 'id_2025'],
    var_name='year',
    value_name='rank'
)

df_long['year'] = df_long['year'].str.replace('id_', '', regex=False).astype(int)

# safe rank cleaning
df_long['rank_clean'] = pd.to_numeric(
    df_long['rank'].astype(str).str.replace('#', '', regex=False).str.strip(),
    errors='coerce'
)

df_long = df_long.dropna(subset=['rank_clean'])

df_long['rank_clean'] = df_long['rank_clean'].astype(int)

def rank_group(rank):
    if rank <= 10:
        return 'Top 10'
    elif rank <= 50:
        return 'Top 50'
    else:
        return 'Top 100'

df_long['rank_group'] = df_long['rank_clean'].apply(rank_group)

# add month + season for Tableau
df_long['month'] = df_long['Publishing Date Clean'].dt.month
df_long['month_name'] = df_long['Publishing Date Clean'].dt.month_name()

def get_season(month):
    if pd.isna(month):
        return None
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df_long['season'] = df_long['month'].apply(get_season)

df_long.to_csv("/Users/laurensisson/Downloads/books_long_format.csv", index=False)

print(df_long.head())
print(df_long.columns)
# %%
import polars as pl
import numpy as np
import requests
import time
from typing import Tuple

# %%
df = pl.read_csv("sps-elementary-schools.csv")

# %%
df = df.with_columns(
    (100*(pl.col("Enrollment") / pl.col("Capacity"))).alias("Percent Utilization"),
    ((pl.col("Building Condition") - pl.col("Building Condition").mean()) / pl.col("Building Condition").std()).alias("Normalized Building Condition"),
    (pl.col("Building Condition").rank(method="random", descending=True)).alias("Building Condition Rank"),
    ((pl.col("Capacity") - pl.col("Capacity").mean()) / pl.col("Capacity").std()).alias("Normalized Capacity"),
    (pl.col("Capacity").rank(method="random", descending=True)).alias("Capacity Rank"),
    ((pl.col("Learning Environment") - pl.col("Learning Environment").mean()) / pl.col("Learning Environment").std()).alias("Normalized Learning Environment"),
    (pl.col("Learning Environment").rank(method="random", descending=False)).alias("Learning Environment Rank"),
    (5 - pl.col("Learning Environment")).alias("learning_environment_rev"),
    ((pl.col("Total Budget") - pl.col("Total Budget").mean()) / pl.col("Total Budget").std()).alias("Normalized Total Budget"),
    (pl.col("Total Budget") / pl.col("P223 K5 Count")).alias("Budget per K5 Student"),
    (pl.col("Total Budget") / pl.col("P223 K8 Count")).alias("Budget per K8 Student"),
    (pl.col("Total Budget") / pl.col("PK8 Count")).alias("Budget per PK8 Student")
)


# %%
def clean_column_names(df: pl.DataFrame) -> pl.DataFrame:
    """
    Convert all column names to lowercase and replace spaces with underscores.
    
    Args:
    df (pl.DataFrame): Input Polars DataFrame
    
    Returns:
    pl.DataFrame: DataFrame with cleaned column names
    """
    return df.rename({
        col: col.lower().replace(' ', '_')
        for col in df.columns
    })


# %%
def calculate_nearest_schools(df: pl.DataFrame) -> pl.DataFrame:
    def haversine_distance(lat1, lon1, lat2, lon2):
        # R = 6371000  # Earth's radius in meters
        R = 3959  # Earth's radius in miles
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        return R * c

    schools = df['school'].to_list()
    n_schools = len(schools)
    
    nearest_school_df = pl.DataFrame({
        'school': schools,
        'nearest_school': [''] * n_schools,
        'distance_to_nearest_school': [float('inf')] * n_schools
    })

    for i, school in enumerate(schools):
        distances = [
            haversine_distance(
                df['latitude'][i], df['longitude'][i],
                df['latitude'][j], df['longitude'][j]
            ) if i != j else float('inf')
            for j in range(n_schools)
        ]
        nearest_idx = min(range(n_schools), key=lambda j: distances[j])
        nearest_school_df = nearest_school_df.with_columns([
            pl.when(pl.col('school') == school)
              .then(pl.lit(schools[nearest_idx]))
              .otherwise(pl.col('nearest_school'))
              .alias('nearest_school'),
            pl.when(pl.col('school') == school)
              .then(pl.lit(distances[nearest_idx]))
              .otherwise(pl.col('distance_to_nearest_school'))
              .alias('distance_to_nearest_school')
        ])

    return nearest_school_df


# %%
cleaned_df = clean_column_names(df)

# %%
cleaned_df.describe()

# %%
nearest_schools = calculate_nearest_schools(cleaned_df)

# %%
nearest_schools.filter(pl.col("school") == "Thurgood Marshall")

# %%
nearest_schools

# %%
cleaned_df = cleaned_df.join(nearest_schools, coalesce = True, on='school', how='left')

# %%
# Write to CSV
cleaned_df.write_csv("sps-elementary-schools-clean.csv")

# %%
cleaned_df["budget_per_k8_student"].median()

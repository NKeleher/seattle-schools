# %%
import polars as pl

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
    (pl.col("Total Budget") / pl.col("P223 Total Count")).alias("Budget per Student")
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
cleaned_df = clean_column_names(df)

# %%
cleaned_df.describe()

# %%
# Write to CSV
cleaned_df.write_csv("sps-elementary-schools-clean.csv")

# %%

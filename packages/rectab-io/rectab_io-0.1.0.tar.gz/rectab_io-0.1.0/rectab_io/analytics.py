import pandas as pd
from tabulate import tabulate
from .auth import validate_auth

def recommenders_analytics(df: pd.DataFrame, user_col: str = "user_id", item_col: str = "item_id", rating_col: str = None):
    """
    Generate advanced analytics for recommendation systems from pandas dataframe
    
    Args:
        df: Input pandas dataframe containing user-item interactions
        user_col: Name of the column containing user IDs
        item_col: Name of the column containing item IDs
        rating_col: Optional name of the column containing ratings (if applicable)
    """
    # First validate authentication
    validate_auth()

    # Calculate core metrics
    analytics = []

    # Dataset Overview
    total_rows = len(df)
    total_users = df[user_col].nunique()
    total_items = df[item_col].nunique()
    
    analytics.extend([
        ["Total Rows", total_rows],
        ["Unique Users", total_users],
        ["Unique Items", total_items]
    ])

    # Interaction Matrix Sparsity
    possible_interactions = total_users * total_items
    sparsity = 100 - (total_rows / possible_interactions) * 100
    analytics.append(["Interaction Matrix Sparsity", f"{sparsity:.2f}%"])

    # User Behavior Metrics
    user_interactions = df.groupby(user_col)[item_col].count()
    analytics.extend([
        ["Avg. Interactions per User", f"{user_interactions.mean():.2f}"],
        ["Max Interactions per User", user_interactions.max()],
        ["Min Interactions per User", user_interactions.min()]
    ])

    # Item Behavior Metrics
    item_interactions = df.groupby(item_col)[user_col].count()
    analytics.extend([
        ["Avg. Interactions per Item", f"{item_interactions.mean():.2f}"],
        ["Max Interactions per Item", item_interactions.max()],
        ["Min Interactions per Item", item_interactions.min()]
    ])

    # Cold Start Analysis
    cold_users = len(user_interactions[user_interactions == 1])
    cold_items = len(item_interactions[item_interactions == 1])
    analytics.extend([
        ["% Cold Start Users (1 interaction)", f"{(cold_users/total_users)*100:.2f}%"],
        ["% Cold Start Items (1 interaction)", f"{(cold_items/total_items)*100:.2f}%"]
    ])

    # Rating Metrics (if applicable)
    if rating_col and rating_col in df.columns:
        analytics.extend([
            ["Average Rating", f"{df[rating_col].mean():.2f}"],
            ["Rating Range", f"{df[rating_col].min()} - {df[rating_col].max()}"],
            ["Most Common Rating", df[rating_col].mode()[0]]
        ])

    # Generate professional table with tabulate
    print("📊 Rectab.io - Recommendation Systems Analytics Report")
    print("="*70)
    table = tabulate(analytics, headers=["Metric", "Value"], tablefmt="fancy_grid")
    print(table)

    # Add custom footers with love icon
    print("\n" + "="*70)
    print("❤️  Made With Love By Louati Mahdi ❤️")
    print("Book Your demo by visiting : https://louati.setmore.com")
    print("="*70)
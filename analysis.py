"""
analysis.py

Beginner-friendly Facebook engagement analysis using a CSV dataset.
"""

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = "dataset_Facebook.csv"


def load_and_prepare_data(file_path=DATA_FILE):
    """
    Load the dataset, clean it, and create useful columns.

    This project uses the provided Facebook dataset file. That dataset uses
    semicolons as separators and has column names like Type, like, comment,
    share, Post Month, and Post Hour.
    """
    df = pd.read_csv(file_path, sep=";")

    # Rename original dataset columns into simpler beginner-friendly names.
    df = df.rename(
        columns={
            "Type": "post_type",
            "like": "likes",
            "comment": "comments",
            "share": "shares",
            "Post Month": "post_month",
            "Post Weekday": "post_weekday",
            "Post Hour": "posting_hour",
            "Paid": "paid",
            "Category": "category",
            "Total Interactions": "total_interactions",
        }
    )

    # Fill missing text values with 'Unknown'.
    df["post_type"] = df["post_type"].fillna("Unknown")

    # Fill missing numeric values with 0.
    numeric_columns = [
        "likes",
        "comments",
        "shares",
        "post_month",
        "post_weekday",
        "posting_hour",
        "paid",
        "category",
        "total_interactions",
    ]
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Convert the columns to numbers safely.
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    # Create a total engagement column.
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]
    df["likes"] = df["likes"].astype(int)
    df["comments"] = df["comments"].astype(int)
    df["shares"] = df["shares"].astype(int)
    df["post_month"] = df["post_month"].astype(int)
    df["post_weekday"] = df["post_weekday"].astype(int)
    df["posting_hour"] = df["posting_hour"].astype(int)
    df["paid"] = df["paid"].astype(int)
    df["category"] = df["category"].astype(int)
    df["total_interactions"] = df["total_interactions"].astype(int)

    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    weekday_names = {
        1: "Sun",
        2: "Mon",
        3: "Tue",
        4: "Wed",
        5: "Thu",
        6: "Fri",
        7: "Sat",
    }
    df["month_name"] = df["post_month"].map(month_names).fillna("Unknown")
    df["weekday_name"] = df["post_weekday"].map(weekday_names).fillna("Unknown")
    df["paid_label"] = df["paid"].map({1: "Paid", 0: "Organic"}).fillna("Unknown")

    return df


def analyze_data(df):
    """
    Print useful beginner-friendly analysis results.
    """
    print("\nDATASET PREVIEW")
    print(
        df[
            [
                "post_type",
                "likes",
                "comments",
                "shares",
                "post_month",
                "posting_hour",
                "engagement",
            ]
        ].head()
    )

    # Best post type by average engagement.
    engagement_by_post_type = (
        df.groupby("post_type")["engagement"].mean().sort_values(ascending=False)
    )

    best_post_type = engagement_by_post_type.idxmax()

    # Best posting hour by average engagement.
    engagement_by_hour = (
        df.groupby("posting_hour")["engagement"].mean().sort_values(ascending=False)
    )
    best_posting_hour = engagement_by_hour.idxmax()

    # Correlation between likes, comments, and shares.
    correlation_matrix = df[["likes", "comments", "shares"]].corr()

    print("\nAVERAGE ENGAGEMENT BY POST TYPE")
    print(engagement_by_post_type)

    print(f"\nBest post type based on engagement: {best_post_type}")
    print(f"Best posting hour based on engagement: {best_posting_hour}:00")

    print("\nCORRELATION BETWEEN LIKES, COMMENTS, AND SHARES")
    print(correlation_matrix)

    return engagement_by_post_type, engagement_by_hour, correlation_matrix


def create_visualizations(df):
    """
    Create and save beginner-friendly charts.
    """
    # Bar chart: average engagement by post type
    engagement_by_post_type = df.groupby("post_type")["engagement"].mean()

    plt.figure(figsize=(8, 5))
    engagement_by_post_type.plot(kind="bar", color="skyblue")
    plt.title("Average Engagement by Post Type")
    plt.xlabel("Post Type")
    plt.ylabel("Average Engagement")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("engagement_by_post_type.png")
    plt.close()

    # Line chart: average engagement by posting hour
    engagement_by_hour = df.groupby("posting_hour")["engagement"].mean().sort_index()

    plt.figure(figsize=(10, 5))
    plt.plot(engagement_by_hour.index, engagement_by_hour.values, marker="o", color="green")
    plt.title("Average Engagement by Posting Hour")
    plt.xlabel("Posting Hour")
    plt.ylabel("Average Engagement")
    plt.tight_layout()
    plt.savefig("engagement_by_posting_hour.png")
    plt.close()

    print("\nCharts saved:")
    print("- engagement_by_post_type.png")
    print("- engagement_by_posting_hour.png")


def explain_why_dataset_is_used():
    """
    Explain why a dataset is used instead of real Facebook scraping.
    """
    print("\nWHY USE A DATASET INSTEAD OF REAL FACEBOOK SCRAPING?")
    print(
        "- Facebook pages often require login, permission, and API access.\n"
        "- Scraping real Facebook content may break platform rules or privacy expectations.\n"
        "- A CSV dataset is safer, faster, and better for learning analysis basics.\n"
        "- It lets beginners focus on pandas, charts, and dashboard building."
    )


if __name__ == "__main__":
    facebook_df = load_and_prepare_data()
    analyze_data(facebook_df)
    create_visualizations(facebook_df)
    explain_why_dataset_is_used()

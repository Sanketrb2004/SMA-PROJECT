"""
app.py

Clean and simple Streamlit dashboard for Facebook engagement analysis.

Run with:
streamlit run app.py
"""

import matplotlib.pyplot as plt
import streamlit as st

from analysis import load_and_prepare_data


st.set_page_config(page_title="Facebook Engagement Dashboard", layout="wide")


@st.cache_data
def get_data():
    """Load the cleaned dataset once and reuse it."""
    return load_and_prepare_data()


def format_hour(hour_value):
    """Convert 24-hour values into easy AM/PM text."""
    hour_value = int(hour_value)
    if hour_value == 0:
        return "12:00 AM"
    if hour_value < 12:
        return f"{hour_value}:00 AM"
    if hour_value == 12:
        return "12:00 PM"
    return f"{hour_value - 12}:00 PM"


df = get_data()

st.title("Facebook Engagement Dashboard")
st.write(
    "This dashboard shows which post type performs best and what posting time "
    "gets the highest average engagement in the dataset. All insights below are "
    "based only on real columns from the CSV file."
)

with st.sidebar:
    st.header("Filters")
    post_types = sorted(df["post_type"].unique().tolist())
    selected_post_types = st.multiselect(
        "Choose post types",
        options=post_types,
        default=post_types,
    )
    selected_paid = st.selectbox(
        "Choose post promotion type",
        options=["All", "Organic", "Paid"],
        index=0,
    )

filtered_df = df[df["post_type"].isin(selected_post_types)].copy()

if selected_paid != "All":
    filtered_df = filtered_df[filtered_df["paid_label"] == selected_paid]

if filtered_df.empty:
    st.warning("No data matches your filters. Please change the filters.")
    st.stop()

engagement_by_post_type = (
    filtered_df.groupby("post_type")["engagement"].mean().sort_values(ascending=False)
)
engagement_by_hour = (
    filtered_df.groupby("posting_hour")["engagement"].mean().sort_values(ascending=False)
)
engagement_by_month = (
    filtered_df.groupby("month_name")["engagement"].mean().reindex(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)
engagement_by_month = engagement_by_month.dropna()
engagement_by_paid = filtered_df.groupby("paid_label")["engagement"].mean().sort_values(
    ascending=False
)

best_post_type = engagement_by_post_type.idxmax()
best_hour = int(engagement_by_hour.idxmax())
best_hour_text = format_hour(best_hour)
average_engagement = round(filtered_df["engagement"].mean(), 1)
total_posts = int(len(filtered_df))
best_month = engagement_by_month.idxmax() if not engagement_by_month.empty else "N/A"
best_promotion_type = engagement_by_paid.idxmax()

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("Total Posts", total_posts)
metric_col2.metric("Average Engagement", average_engagement)
metric_col3.metric("Best Post Type", best_post_type)
metric_col4.metric("Best Posting Time", best_hour_text)

st.subheader("Main Insight")
st.info(
    f"From the current data, **{best_post_type}** posts have the highest average engagement. "
    f"The best posting time is **{best_hour_text}**, which is the hour where posts got the "
    f"highest average engagement. The best month in this dataset view is **{best_month}**, "
    f"and **{best_promotion_type}** posts perform better on average."
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Best Post Type")
    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    bars = ax1.bar(
        engagement_by_post_type.index,
        engagement_by_post_type.values,
        color="#4f46e5",
    )
    ax1.set_title("Average Engagement by Post Type")
    ax1.set_xlabel("Post Type")
    ax1.set_ylabel("Average Engagement")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    for bar in bars:
        value = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            value + 5,
            f"{value:.0f}",
            ha="center",
            va="bottom",
        )
    st.pyplot(fig1, clear_figure=True)
    st.caption("The tallest bar shows the post type with the best average engagement.")

with chart_col2:
    st.subheader("Best Posting Time")
    hour_data = engagement_by_hour.sort_index()
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    ax2.plot(
        hour_data.index,
        hour_data.values,
        marker="o",
        color="#059669",
        linewidth=2.5,
    )
    ax2.scatter([best_hour], [hour_data.loc[best_hour]], color="#dc2626", s=80, zorder=5)
    ax2.annotate(
        best_hour_text,
        xy=(best_hour, hour_data.loc[best_hour]),
        xytext=(8, 10),
        textcoords="offset points",
        fontsize=10,
    )
    ax2.set_title("Average Engagement by Posting Time")
    ax2.set_xlabel("Posting Time")
    ax2.set_ylabel("Average Engagement")
    ax2.set_xticks(hour_data.index)
    ax2.set_xticklabels(
        [format_hour(hour).replace(":00", "") for hour in hour_data.index],
        rotation=45,
        ha="right",
    )
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    st.pyplot(fig2, clear_figure=True)
    st.caption("The highest point shows the time with the best average engagement.")

extra_col1, extra_col2 = st.columns(2)

with extra_col1:
    st.subheader("Best Month")
    fig3, ax3 = plt.subplots(figsize=(7, 4.5))
    ax3.bar(engagement_by_month.index, engagement_by_month.values, color="#0ea5e9")
    ax3.set_title("Average Engagement by Month")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Average Engagement")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    st.pyplot(fig3, clear_figure=True)
    st.caption("This compares average engagement across the months in the dataset.")

with extra_col2:
    st.subheader("Paid vs Organic")
    fig4, ax4 = plt.subplots(figsize=(7, 4.5))
    bars = ax4.bar(engagement_by_paid.index, engagement_by_paid.values, color=["#f59e0b", "#6366f1"])
    ax4.set_title("Average Engagement by Promotion Type")
    ax4.set_xlabel("Promotion Type")
    ax4.set_ylabel("Average Engagement")
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    for bar in bars:
        value = bar.get_height()
        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            value + 5,
            f"{value:.0f}",
            ha="center",
            va="bottom",
        )
    st.pyplot(fig4, clear_figure=True)
    st.caption("This shows whether paid or organic posts get better average engagement.")

st.subheader("Top Posting Times")
top_hours_table = (
    engagement_by_hour.head(5).reset_index().rename(
        columns={"posting_hour": "Hour", "engagement": "Average Engagement"}
    )
)
top_hours_table["Posting Time"] = top_hours_table["Hour"].apply(format_hour)
top_hours_table = top_hours_table[["Posting Time", "Average Engagement"]]
st.dataframe(top_hours_table, use_container_width=True, hide_index=True)

st.subheader("What The Dashboard Is Based On")
st.write(
    "This dashboard uses only real dataset columns: `Type`, `like`, `comment`, "
    "`share`, `Post Hour`, `Post Month`, and `Paid`. It does not use any artificial "
    "date or generated timeline."
)

st.subheader("Dataset Preview")
preview_df = filtered_df[
    [
        "post_type",
        "month_name",
        "paid_label",
        "likes",
        "comments",
        "shares",
        "posting_hour",
        "engagement",
    ]
].copy()
preview_df["posting_time"] = preview_df["posting_hour"].apply(format_hour)
preview_df = preview_df[
    [
        "post_type",
        "month_name",
        "paid_label",
        "likes",
        "comments",
        "shares",
        "posting_time",
        "engagement",
    ]
]
st.dataframe(preview_df, use_container_width=True, hide_index=True)

with st.expander("Correlation between likes, comments, and shares"):
    correlation_matrix = filtered_df[["likes", "comments", "shares"]].corr()
    st.dataframe(correlation_matrix.style.format("{:.2f}"), use_container_width=True)
    st.write(
        "Values closer to 1 mean the two engagement metrics tend to increase together."
    )

st.subheader("Why Use a Dataset Instead of Real Facebook Scraping?")
st.write(
    "A dataset is used because real Facebook scraping may involve login restrictions, "
    "privacy issues, and platform rules. Using a dataset is safer and better for learning."
)

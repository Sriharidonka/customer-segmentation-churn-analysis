import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="European Banking Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .kpi-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        text-align: center;
        min-height: 130px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .kpi-icon {
        font-size: 28px;
        margin-bottom: 5px;
    }

    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #555555;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #1f2937;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# PLOTLY CHART STYLE
# ==================================================

def style_chart(fig):

    fig.update_layout(
        font=dict(size=13),
        title_font=dict(size=18),
        margin=dict(t=70, b=50, l=50, r=30),
        legend_title_text="",
        hovermode="x unified"
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="lightgray"
    )

    return fig

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv(
            "../Dataset/Bank_Churn_Risk_Segmented.csv"
        )

        return df

    except FileNotFoundError:
        st.error(
            "❌ Dataset file not found. "
            "Please check that Bank_Churn_Risk_Segmented.csv "
            "is inside the Dataset folder."
        )
        return None

    except Exception as e:
        st.error(
            f"❌ Error while loading the dataset: {e}"
        )
        return None


df = load_data()
if df is None:
    st.stop()
# ==================================================
# DATA VALIDATION
# ==================================================
required_columns = [
    "CustomerId",
    "Geography",
    "AgeGroup",
    "CreditScoreBand",
    "TenureGroup",
    "BalanceSegment",
    "CustomerValue",
    "EngagementStatus",
    "ChurnRiskSegment",
    "RiskScore",
    "Exited",
    "Balance",
    "CreditScore",
    "Age",
    "Gender",
    "Tenure",
    "NumOfProducts",
    "HasCrCard",
    "EstimatedSalary",
    "IsActiveMember"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "❌ Dataset is missing required columns:"
    )

    st.write(missing_columns)

    st.stop()
# ==================================================
# HEADER
# ==================================================

st.title("🏦 European Banking Churn Analytics")

st.markdown(
    """
    ### Customer Segmentation & Churn Pattern Analytics

    Explore customer churn across **geography, demographics,
    engagement, financial profile, and risk segments**.
    """
)

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:10px 0 20px 0;
    ">
        <div style="font-size:42px;">🏦</div>
        <h2 style="margin:0;">Banking Analytics</h2>
        <p style="font-size:13px; opacity:0.7;">
            Customer Churn Intelligence
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.markdown("### 🔎 Dashboard Filters")

# Default filter values
default_geography = sorted(df["Geography"].unique())
default_age = list(df["AgeGroup"].unique())
default_engagement = sorted(df["EngagementStatus"].unique())
default_value = sorted(df["CustomerValue"].unique())


# ==================================================
# RESET FILTER FUNCTION
# ==================================================

def reset_filters():

    st.session_state["geography_filter"] = default_geography
    st.session_state["age_filter"] = default_age
    st.session_state["engagement_filter"] = default_engagement
    st.session_state["value_filter"] = default_value


# ==================================================
# FILTERS
# ==================================================

# Geography
geography_filter = st.sidebar.multiselect(
    "🌍 Geography",
    options=default_geography,
    default=default_geography,
    key="geography_filter"
)


# Age Group
age_filter = st.sidebar.multiselect(
    "👥 Age Group",
    options=default_age,
    default=default_age,
    key="age_filter"
)


# Engagement Status
engagement_filter = st.sidebar.multiselect(
    "📱 Engagement Status",
    options=default_engagement,
    default=default_engagement,
    key="engagement_filter"
)


# Customer Value
value_filter = st.sidebar.multiselect(
    "💰 Customer Value",
    options=default_value,
    default=default_value,
    key="value_filter"
)


# ==================================================
# RESET BUTTON
# ==================================================

st.sidebar.divider()

st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True,
    on_click=reset_filters
)


# ==================================================
# FILTER DATA
# ==================================================

filtered_df = df[
    (df["Geography"].isin(geography_filter)) &
    (df["AgeGroup"].isin(age_filter)) &
    (df["EngagementStatus"].isin(engagement_filter)) &
    (df["CustomerValue"].isin(value_filter))
]


# ==================================================
# EMPTY FILTER CHECK
# ==================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No customers match the selected filters. "
        "Please select at least one option from each filter."
    )

    st.stop()


st.sidebar.divider()

st.sidebar.metric(
    "👥 Customers in Selection",
    f"{len(filtered_df):,}"
)
# ==================================================
# DASHBOARD TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🌍 Demographics",
    "🎯 Risk Analysis",
    "💰 Customer Value",
    "🔎 Customer Explorer"
])
# ==================================================
# EXECUTIVE KPIs
# ==================================================
with tab1:

    st.subheader("📊 Executive Overview")

    # Total customers after filters
    total_customers = len(filtered_df)

    # Churned customers
    churned_customers = filtered_df["Exited"].sum()

    # Churn rate
    churn_rate = (
        churned_customers / total_customers * 100
        if total_customers > 0 else 0
    )

    # Total balance associated with selected customers
    total_balance = filtered_df["Balance"].sum()

    # Balance associated with churned customers
    churned_balance = filtered_df.loc[
        filtered_df["Exited"] == 1,
        "Balance"
    ].sum()

    # ==================================================
    # KPI CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-title">Total Customers</div>
                <div class="kpi-value">{total_customers:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">🚨</div>
                <div class="kpi-title">Churned Customers</div>
                <div class="kpi-value">{churned_customers:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">📉</div>
                <div class="kpi-title">Churn Rate</div>
                <div class="kpi-value">{churn_rate:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">💰</div>
                <div class="kpi-title">Churn-Associated Balance</div>
                <div class="kpi-value">{churned_balance / 1e6:.2f}M</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    # ==================================================
    # CHURN DISTRIBUTION
    # ==================================================

    with col1:

        st.subheader("📌 Customer Churn Distribution")

        churn_distribution = (
            filtered_df["Exited"]
            .value_counts()
            .rename({
                0: "Retained",
                1: "Churned"
            })
            .reset_index()
        )

        churn_distribution.columns = [
            "Status",
            "Customers"
        ]

        fig = px.pie(
            churn_distribution,
            names="Status",
            values="Customers",
            hole=0.55,
            title="Retained vs Churned Customers"
        )
        fig = style_chart(fig)
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # ==================================================
    # GEOGRAPHY-WISE CHURN
    # ==================================================

    with col2:

        st.subheader("🌍 Geography-wise Churn")

        geo_analysis = (
            filtered_df
            .groupby("Geography")
            .agg(
                Customers=("Exited", "size"),
                Churned=("Exited", "sum"),
                ChurnRate=("Exited", "mean")
            )
            .reset_index()
        )

        geo_analysis["ChurnRate"] = (
            geo_analysis["ChurnRate"] * 100
        )

        fig = px.bar(
            geo_analysis,
            x="Geography",
            y="ChurnRate",
            text="ChurnRate",
            title="Churn Rate by Geography"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            yaxis_title="Churn Rate (%)",
            xaxis_title="Geography"
        )
        fig = style_chart(fig)
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # ==================================================
    # EXECUTIVE INSIGHTS
    # ==================================================

    st.subheader("💡 Executive Insights")

    # Highest churn geography
    highest_churn_geo = geo_analysis.loc[
        geo_analysis["ChurnRate"].idxmax()
    ]

    # Highest churn age group
    age_analysis = (
        filtered_df
        .groupby("AgeGroup", observed=True)
        .agg(
            Customers=("Exited", "size"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    age_analysis["ChurnRate"] = (
        age_analysis["ChurnRate"] * 100
    )

    highest_churn_age = age_analysis.loc[
        age_analysis["ChurnRate"].idxmax()
    ]

    # Highest churn risk segment
    risk_analysis_insight = (
        filtered_df
        .groupby("ChurnRiskSegment", observed=True)
        .agg(
            Customers=("Exited", "size"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    risk_analysis_insight["ChurnRate"] = (
        risk_analysis_insight["ChurnRate"] * 100
    )

    highest_risk = risk_analysis_insight.loc[
        risk_analysis_insight["ChurnRate"].idxmax()
    ]

    # Inactive vs Active churn
    engagement_analysis = (
        filtered_df
        .groupby("EngagementStatus", observed=True)
        .agg(
            Customers=("Exited", "size"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    engagement_analysis["ChurnRate"] = (
        engagement_analysis["ChurnRate"] * 100
    )

    inactive_rate = engagement_analysis.loc[
        engagement_analysis["EngagementStatus"] == "Inactive",
        "ChurnRate"
    ]

    active_rate = engagement_analysis.loc[
        engagement_analysis["EngagementStatus"] == "Active",
        "ChurnRate"
    ]

    # Display insights
    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.info(
            f"🌍 **Geography:** "
            f"{highest_churn_geo['Geography']} has the highest observed "
            f"churn rate at **{highest_churn_geo['ChurnRate']:.2f}%** "
            f"within the current selection."
        )

        st.info(
            f"👥 **Age Group:** "
            f"{highest_churn_age['AgeGroup']} has the highest observed "
            f"churn rate at **{highest_churn_age['ChurnRate']:.2f}%**."
        )

    with insight_col2:

        st.info(
            f"🎯 **Risk Segment:** "
            f"{highest_risk['ChurnRiskSegment']} has the highest observed "
            f"churn rate at **{highest_risk['ChurnRate']:.2f}%**."
        )

        if not inactive_rate.empty and not active_rate.empty:

            st.info(
                f"📱 **Engagement:** "
                f"Inactive customers show an observed churn rate of "
                f"**{inactive_rate.iloc[0]:.2f}%**, compared with "
                f"**{active_rate.iloc[0]:.2f}%** for active customers."
            )
# ==================================================
# TAB 2 — DEMOGRAPHICS
# ==================================================

with tab2:

    st.subheader("🌍 Demographic & Financial Analysis")
    # ==================================================
    # AGE × GEOGRAPHY CHURN
    # ==================================================

    st.subheader("👥 Age & Geography Churn Analysis")

    geo_age_analysis = (
        filtered_df
        .groupby(
            ["Geography", "AgeGroup"],
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            Churned=("Exited", "sum"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    geo_age_analysis["ChurnRate"] = (
        geo_age_analysis["ChurnRate"] * 100
    )

    fig = px.bar(
        geo_age_analysis,
        x="AgeGroup",
        y="ChurnRate",
        color="Geography",
        barmode="group",
        title="Churn Rate by Age Group and Geography",
        text="ChurnRate"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Age Group"
    )
    fig = style_chart(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==================================================
    # AGE × ENGAGEMENT CHURN
    # ==================================================

    st.subheader("📈 Age & Engagement Churn Analysis")

    age_engagement_analysis = (
        filtered_df
        .groupby(
            ["AgeGroup", "EngagementStatus"],
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            Churned=("Exited", "sum"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    age_engagement_analysis["ChurnRate"] = (
        age_engagement_analysis["ChurnRate"] * 100
    )

    fig = px.bar(
        age_engagement_analysis,
        x="AgeGroup",
        y="ChurnRate",
        color="EngagementStatus",
        barmode="group",
        title="Churn Rate by Age Group and Engagement",
        text="ChurnRate"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Age Group"
    )
    fig = style_chart(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==================================================
    # TENURE ANALYSIS
    # ==================================================

    st.subheader("⏳ Tenure & Churn Analysis")

    tenure_analysis = (
        filtered_df
        .groupby(
            "TenureGroup",
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            Churned=("Exited", "sum"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    tenure_analysis["ChurnRate"] = (
        tenure_analysis["ChurnRate"] * 100
    )

    fig = px.bar(
        tenure_analysis,
        x="TenureGroup",
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Tenure Group"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Tenure Group"
    )
    fig = style_chart(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==================================================
    # CREDIT SCORE ANALYSIS
    # ==================================================

    st.subheader("📊 Credit Score & Churn")

    credit_analysis = (
        filtered_df
        .groupby(
            "CreditScoreBand",
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            Churned=("Exited", "sum"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    credit_analysis["ChurnRate"] = (
        credit_analysis["ChurnRate"] * 100
    )

    fig = px.bar(
        credit_analysis,
        x="CreditScoreBand",
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Credit Score Band"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Credit Score Band"
    )
    fig = style_chart(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==================================================
    # BALANCE SEGMENT ANALYSIS
    # ==================================================

    st.subheader("💳 Balance Segment & Churn")

    balance_analysis = (
        filtered_df
        .groupby(
            "BalanceSegment",
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            Churned=("Exited", "sum"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    balance_analysis["ChurnRate"] = (
        balance_analysis["ChurnRate"] * 100
    )

    fig = px.bar(
        balance_analysis,
        x="BalanceSegment",
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Balance Segment"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Balance Segment"
    )
    fig = style_chart(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ==================================================
# TAB 3 — RISK ANALYSIS
# ==================================================

with tab3:

    st.subheader("🎯 Risk Analysis")
    col1, col2 = st.columns(2)
    # ==================================================
    # RISK SEGMENTATION
    # ==================================================
    with col1:
        st.subheader("🎯 Churn Risk Segmentation")
        risk_analysis = (
            filtered_df
            .groupby(
                "ChurnRiskSegment",
                observed=True
            )
            .agg(
                Customers=("Exited", "size"),
                Churned=("Exited", "sum"),
                ChurnRate=("Exited", "mean")
            )
            .reset_index()
        )
    
        risk_analysis["ChurnRate"] = (
            risk_analysis["ChurnRate"] * 100
        )
        fig = px.bar(
            risk_analysis,
            x="ChurnRiskSegment",
            y="ChurnRate",
            text="ChurnRate",
            title="Observed Churn Rate by Risk Segment"
        )
        
        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )
        
        fig.update_layout(
            yaxis_title="Churn Rate (%)",
            xaxis_title="Risk Segment"
        )
        fig = style_chart(fig)
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
    # ==================================================
    # FINANCIAL EXPOSURE BY RISK
    # ==================================================
        risk_balance = (
                filtered_df[filtered_df["Exited"] == 1]
                .groupby(
                    "ChurnRiskSegment",
                    observed=True
                )
                .agg(
                    ChurnedCustomers=("Exited", "size"),
                    ChurnedBalance=("Balance", "sum")
                )
                .reset_index()
        )
        
        fig = px.bar(
                risk_balance,
                x="ChurnRiskSegment",
                y="ChurnedBalance",
                text="ChurnedBalance",
                title="Churn-Associated Balance by Risk Segment"
        )
        
        fig.update_traces(
                texttemplate="%{text:.2s}",
                textposition="outside"
        )
        
        fig.update_layout(
                yaxis_title="Churn-Associated Balance",
                xaxis_title="Risk Segment"
        )
        fig = style_chart(fig)
        st.plotly_chart(
                fig,
                use_container_width=True
        )

    # ==================================================
    # RISK SEGMENT SUMMARY
    # ==================================================

    st.subheader("📋 Risk Segment Summary")

    risk_summary = (
        filtered_df
        .groupby(
            "ChurnRiskSegment",
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            ChurnedCustomers=("Exited", "sum"),
            ChurnRate=("Exited", "mean"),
            AverageBalance=("Balance", "mean"),
            TotalBalance=("Balance", "sum")
        )
        .reset_index()
    )

    risk_summary["ChurnRate"] = (
        risk_summary["ChurnRate"] * 100
    )

    risk_summary["AverageBalance"] = (
        risk_summary["AverageBalance"].round(2)
    )

    risk_summary["TotalBalance"] = (
        risk_summary["TotalBalance"].round(2)
    )

    st.dataframe(
        risk_summary,
        use_container_width=True,
        hide_index=True
    )
    # ==================================================
    # PRIORITY RETENTION SEGMENT
    # ==================================================

    st.subheader("🚨 Priority Retention Segment")

    priority_df = filtered_df[
        (filtered_df["ChurnRiskSegment"] == "Critical Risk") &
        (filtered_df["CustomerValue"] == "High Value")
    ]

    priority_customers = len(priority_df)

    priority_churned = priority_df["Exited"].sum()

    priority_churn_rate = (
        priority_churned / priority_customers * 100
        if priority_customers > 0 else 0
    )

    priority_balance = priority_df.loc[
        priority_df["Exited"] == 1,
        "Balance"
    ].sum()

    # ==================================================
    # PRIORITY RETENTION KPI CARDS
    # ==================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-title">Critical + High Value Customers</div>
                <div class="kpi-value">{priority_customers:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">🚨</div>
                <div class="kpi-title">Observed Churn Rate</div>
                <div class="kpi-value">{priority_churn_rate:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">💰</div>
                <div class="kpi-title">Churned Balance</div>
                <div class="kpi-value">{priority_balance / 1e6:.2f}M</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.info(
        "💡 This segment represents customers who combine "
        "high churn risk with high customer value and may "
        "warrant targeted retention attention."
    )
# ==================================================
# TAB 4 — CUSTOMER VALUE
# ==================================================

with tab4:

    st.subheader("💰 Customer Value & Financial Analysis")
    # ==================================================
    # HIGH-VALUE CUSTOMER ANALYSIS
    # ==================================================

    st.subheader("💰 High-Value Customer Analysis")

    high_value_df = filtered_df[
        filtered_df["CustomerValue"] == "High Value"
    ]

    high_value_customers = len(high_value_df)

    high_value_churned = high_value_df["Exited"].sum()

    high_value_churn_rate = (
        high_value_churned / high_value_customers * 100
        if high_value_customers > 0 else 0
    )

    high_value_churned_balance = high_value_df.loc[
        high_value_df["Exited"] == 1,
        "Balance"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">💎</div>
                <div class="kpi-title">High-Value Customers</div>
                <div class="kpi-value">{high_value_customers:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">🚨</div>
                <div class="kpi-title">High-Value Churned</div>
                <div class="kpi-value">{high_value_churned:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">📉</div>
                <div class="kpi-title">High-Value Churn Rate</div>
                <div class="kpi-value">{high_value_churn_rate:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">💰</div>
                <div class="kpi-title">Churned High-Value Balance</div>
                <div class="kpi-value">{high_value_churned_balance / 1e6:.2f}M</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==================================================
    # CUSTOMER VALUE × RISK
    # ==================================================

    st.subheader("🎯 Customer Value × Risk Analysis")
    value_risk_analysis = (
        filtered_df
        .groupby(
            ["ChurnRiskSegment", "CustomerValue"],
            observed=True
        )
        .agg(
            Customers=("Exited", "size"),
            Churned=("Exited", "sum"),
            ChurnRate=("Exited", "mean")
        )
        .reset_index()
    )

    value_risk_analysis["ChurnRate"] = (
        value_risk_analysis["ChurnRate"] * 100
    )

    fig = px.bar(
        value_risk_analysis,
        x="ChurnRiskSegment",
        y="ChurnRate",
        color="CustomerValue",
        barmode="group",
        text="ChurnRate",
        title="Churn Rate by Risk Segment and Customer Value"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Risk Segment"
    )
    fig = style_chart(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.info(
        "💡 This analysis helps identify whether high-value customers "
        "are concentrated in higher-risk segments, supporting targeted "
        "customer-retention analysis."
    )
# ==================================================
# TAB 5 — CUSTOMER EXPLORER
# ==================================================

with tab5:

    st.subheader("🔎 Customer Explorer")

    st.markdown(
        "Select a customer to view their profile and churn-risk information."
    )

    # Customer selection
    customer_ids = filtered_df["CustomerId"].astype(str).tolist()

    selected_customer = st.selectbox(
        "Select Customer ID",
        options=customer_ids
    )
    # Get selected customer
    customer = filtered_df[
    filtered_df["CustomerId"].astype(str) == selected_customer
    ].iloc[0]
    # ==================================================
    # CUSTOMER PROFILE
    # ==================================================

    st.markdown("### 👤 Customer Profile")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Customer ID",
        str(customer["CustomerId"])
    )

    col2.metric(
        "Geography",
        customer["Geography"]
    )

    col3.metric(
        "Gender",
        customer["Gender"]
    )

    col4.metric(
        "Age",
        int(customer["Age"])
    )
    st.markdown("### 💳 Financial & Banking Profile")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Credit Score",
        int(customer["CreditScore"])
    )

    col2.metric(
        "Balance",
        f"{customer['Balance']:,.2f}"
    )

    col3.metric(
        "Estimated Salary",
        f"{customer['EstimatedSalary']:,.2f}"
    )

    col4.metric(
        "Tenure",
        f"{int(customer['Tenure'])} years"
    )
    st.markdown("### 📱 Engagement & Products")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Products",
        int(customer["NumOfProducts"])
    )

    col2.metric(
        "Credit Card",
        "Yes" if customer["HasCrCard"] == 1 else "No"
    )

    col3.metric(
        "Engagement",
        customer["EngagementStatus"]
    )

    col4.metric(
        "Customer Value",
        customer["CustomerValue"]
    )
    st.markdown("### 🎯 Risk Assessment")

    col1, col2, col3 = st.columns(3)

    churn_status = (
        "Churned"
        if customer["Exited"] == 1
        else "Retained"
    )

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-title">Risk Score</div>
                <div class="kpi-value">{int(customer["RiskScore"])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">⚠️</div>
                <div class="kpi-title">Risk Segment</div>
                <div class="kpi-value">{customer["ChurnRiskSegment"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">📌</div>
                <div class="kpi-title">Current Status</div>
                <div class="kpi-value">{churn_status}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if customer["Exited"] == 1:
        st.warning(
            "🚨 This customer is recorded as churned in the dataset."
        )
    elif customer["RiskScore"] >= 7:
        st.warning(
            "⚠️ This customer has a relatively high calculated risk score."
        )
    else:
        st.info(
            "ℹ️ This customer is currently recorded as retained."
        )

    
    # ==================================================
    # FILTERED CUSTOMER DATA
    # ==================================================

    st.subheader("📋 Filtered Customer Details")

    display_columns = [
        "CustomerId",
        "Geography",
        "Age",
        "Gender",
        "CreditScore",
        "Balance",
        "NumOfProducts",
        "IsActiveMember",
        "CustomerValue",
        "RiskScore",
        "ChurnRiskSegment",
        "Exited"
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )
    # ==================================================
    # DOWNLOAD FILTERED DATA
    # ==================================================

    csv_data = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Filtered Customer Data",
        data=csv_data,
        file_name="filtered_customer_data.csv",
        mime="text/csv"
    )   
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go

st.set_page_config(
    page_title="GoBorong Dashboard",
    page_icon="🛒",
    layout="wide"
)

@st.cache_data
def load_data():
    transactions = pd.read_csv("data/transactions.csv", parse_dates=["Tanggal Order"])
    customers = pd.read_csv("data/customers.csv")
    products = pd.read_csv("data/products.csv")
    product_recommendation = pd.read_csv("data/product_recommendation.csv")
    customer_cluster = pd.read_csv("data/customer_cluster_dashboard.csv")
    target_market = pd.read_csv("data/target_market_dashboard.csv")
    geo = pd.read_csv("data/geo_dashboard.csv")

    return (
        transactions,
        customers,
        products,
        product_recommendation,
        customer_cluster,
        target_market,
        geo
    )


( transactions, customers, products, product_recommendation, customer_cluster, target_market, geo ) = load_data()

@st.cache_data
def load_geojson():
    with open(
        "data/goborong_wilayah.geojson",
        "r",
        encoding="utf-8"
    ) as f:
        wilayah_geojson = json.load(f)

    with open(
        "data/goborong_background_wilayah.geojson",
        "r",
        encoding="utf-8"
    ) as f:
        background_geojson = json.load(f)

    return wilayah_geojson, background_geojson


wilayah_geojson, background_geojson = load_geojson()

# Warna dashboard
st.markdown("""
<style>

    /* Background utama */
    .stApp {
        background-color: #FFFFFF;
        color: #3A2F2A;
    }

    /* Top bar */
    header[data-testid="stHeader"] {
        background-color: #eb5642;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F77D25;
    }

    /* Judul halaman */
    h1, h2, h3 {
        color: #3A2F2A;
    }

    /* Text sidebar */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    /* Tombol menu sidebar */
    section[data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        text-align: left;
        border: none;
        background-color: transparent;
        color: #FFFFFF;
        padding: 10px 14px;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] div.stButton > button p {
        color: #FFFFFF;
    }

    /* Hover menu */
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #eb5642;
        color: #FFFFFF;
    }

    /* Header dropdown */
    section[data-testid="stSidebar"] details summary {
        background-color: #eb5642;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 8px 12px;
    }

    section[data-testid="stSidebar"] details summary p {
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] details summary svg {
        fill: #FFFFFF;
        color: #FFFFFF;
    }

   .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-top: 5px solid #EB5642;
        border-radius: 12px;
        padding: 18px;
        min-height: 130px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        box-sizing: border-box;
    }

    .kpi-title {
        font-size: 14px;
        color: #777777;
        margin-bottom: 8px;
        white-space: nowrap;
    }

    .kpi-value {
        font-size: 25px;
        font-weight: 700;
        color: #3A2F2A;
    }

    .kpi-value-money {
        font-size: 18px;
        font-weight: 700;
        color: #3A2F2A; 
        white-space: nowrap;
    }

    .highlight-card {
        background-color: #FFF8F5;
        border-left: 5px solid #F77D25;
        border-radius: 10px;
        padding: 18px;
        min-height: 115px;
    }

    .highlight-title {
        color: #777777;
        font-size: 14px;
    }

    .highlight-value {
        color: #3A2F2A;
        font-size: 18px;
        font-weight: 650;
        margin-top: 6px;
    }

    .product-main-card {
        background: linear-gradient(135deg, #EB5642, #F77D25);
        border-radius: 12px;
        padding: 22px;
        min-height: 150px;
        color: white;
    }

    .product-main-title {
        font-size: 14px;
        opacity: 0.9;
    }

    .product-main-name {
        font-size: 22px;
        font-weight: 700;
        margin-top: 8px;
    }

    .product-main-detail {
        font-size: 14px;
        margin-top: 10px;
    }

    .recommendation-card {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-left: 5px solid #FFDA75;
        border-radius: 10px;
        padding: 16px;
        min-height: 145px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .recommendation-rank {
        font-size: 13px;
        color: #F77D25;
        font-weight: 700;
    }

    .recommendation-name {
        font-size: 16px;
        color: #3A2F2A;
        font-weight: 650;
        margin-top: 6px;
    }

    .recommendation-detail {
        font-size: 13px;
        color: #777777;
        margin-top: 8px;
    }

</style>
""", unsafe_allow_html=True)

# Halaman default
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# Logo
st.sidebar.image(
    "assets/logo_goborong.png",
    width=190
)

st.sidebar.markdown("### Main")

if st.sidebar.button("🏠  Overview"):
    st.session_state.page = "Overview"

with st.sidebar.expander("📊  Dashboards", expanded=True):
    if st.button("📦  Product Analysis"):
        st.session_state.page = "Product Analysis"

    if st.button("👥  Customer Analysis"):
        st.session_state.page = "Customer Analysis"

    if st.button("🌍  Geographic Analysis"):
        st.session_state.page = "Geographic Analysis"

st.sidebar.markdown("### Elements")

with st.sidebar.expander("▦  Tables"):
    if st.button("🧾  Transactions"):
        st.session_state.page = "Transactions"

    if st.button("👤  Customers / Clients"):
        st.session_state.page = "Customers"

    if st.button("🛍️  Product Data"):
        st.session_state.page = "Product Data"


# Isi halaman sementara
page = st.session_state.page

if page == "Overview":

    st.title("Overview")
    st.write(
        "Ringkasan performa transaksi, customer, produk, "
        "dan wilayah GoBorong."
    )

    # KPI utama
    total_spending = transactions["Total Transaction"].sum()
    total_orders = transactions["Nomor Order"].nunique()
    total_customers = transactions["Customer ID"].nunique()
    total_quantity = transactions["Jumlah Beli"].sum()

    average_order_value = (
        total_spending / total_orders
        if total_orders > 0
        else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Spending</div>
                <div class="kpi-value-money">
                    Rp {total_spending:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">
                    {total_orders:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Customers</div>
                <div class="kpi-value">
                    {total_customers:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Quantity</div>
                <div class="kpi-value">
                    {total_quantity:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Average Order Value</div>
                <div class="kpi-value-money">
                    Rp {average_order_value:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### About the Dashboard")

    start_date = transactions["Tanggal Order"].min()
    end_date = transactions["Tanggal Order"].max()
    total_products = transactions["SKU Produk"].nunique()
    total_regions = transactions["City (Shipping)"].nunique()

    st.write(
        f"Dashboard ini menggunakan data transaksi GoBorong "
        f"periode **{start_date.strftime('%d %B %Y')} sampai "
        f"{end_date.strftime('%d %B %Y')}**. "
        f"Data mencakup **{total_products} produk** dan "
        f"**{total_regions} wilayah**, dengan analisis utama "
        f"meliputi Product Purchase Pattern, Customer Segmentation, "
        f"dan Geographic Analysis."
    )

    st.markdown("### Business Highlights")

    # Wilayah dengan spending tertinggi
    top_region = (
        geo.sort_values("Total_Spending", ascending=False)
        .iloc[0]
    )

    # Kategori dengan spending tertinggi
    top_category = (
        transactions
        .groupby("Kategori Produk")["Total Transaction"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    # Cluster dengan kontribusi spending tertinggi
    top_cluster = (
        customer_cluster
        .sort_values(
            "Spending_Contribution_%",
            ascending=False
        )
        .iloc[0]
    )

    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown(
            f"""
            <div class="highlight-card">
                <div class="highlight-title">
                    Top Spending Region
                </div>
                <div class="highlight-value">
                    {top_region["City (Shipping)"]}
                </div>
                <div>
                    Rp {top_region["Total_Spending"]:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h2:
        st.markdown(
            f"""
            <div class="highlight-card">
                <div class="highlight-title">
                    Dominant Product Category
                </div>
                <div class="highlight-value">
                    {top_category}
                </div>
                <div>
                    Berdasarkan total spending
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h3:
        st.markdown(
            f"""
            <div class="highlight-card">
                <div class="highlight-title">
                    Highest Spending Customer Cluster
                </div>
                <div class="highlight-value">
                    {top_cluster["Cluster Label"]}
                </div>
                <div>
                    {top_cluster["Spending_Contribution_%"]:.1f}% kontribusi spending
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

elif page == "Product Analysis":

    st.title("Product Analysis")
    st.write(
        "Analisis pola pembelian produk dan rekomendasi produk "
        "yang sering dibeli secara bersamaan."
    )

    # Produk yang masuk clustering
    clustered_products = (
        products
        .dropna(subset=["Cluster"])
        .copy()
    )

    clustered_products["Cluster"] = (
        clustered_products["Cluster"].astype(int)
    )

    # Filter
    f1, f2, f3 = st.columns(3)

    with f1:
        selected_cluster = st.selectbox(
            "Product Cluster",
            sorted(clustered_products["Cluster"].unique())
        )

    cluster_products = clustered_products[
        clustered_products["Cluster"] == selected_cluster
    ]

    category_options = (
        ["All Categories"]
        + sorted(
            cluster_products["Kategori Produk"]
            .dropna()
            .unique()
        )
    )

    with f2:
        selected_category = st.selectbox(
            "Product Category",
            category_options
        )

    if selected_category != "All Categories":
        filtered_products = cluster_products[
            cluster_products["Kategori Produk"]
            == selected_category
        ]
    else:
        filtered_products = cluster_products.copy()

    with f3:
        selected_product = st.selectbox(
            "Main Product",
            sorted(filtered_products["Item Name"].unique())
        )

    selected_row = filtered_products[
        filtered_products["Item Name"] == selected_product
    ].iloc[0]

    selected_sku = selected_row["SKU Produk"]

    # Cari order yang memiliki produk utama
    order_product = (
        transactions[
            ["Nomor Order", "SKU Produk"]
        ]
        .drop_duplicates()
    )

    main_orders = order_product[
        order_product["SKU Produk"] == selected_sku
    ]["Nomor Order"].unique()

    # Hitung co-purchase
    copurchase = (
        order_product[
            order_product["Nomor Order"].isin(main_orders)
            & (order_product["SKU Produk"] != selected_sku)
        ]
        .groupby("SKU Produk")["Nomor Order"]
        .nunique()
        .sort_values(ascending=False)
        .head(3)
        .reset_index(name="Jumlah_Order_Bersama")
    )

    copurchase["Persentase_CoPurchase"] = (
        copurchase["Jumlah_Order_Bersama"]
        / len(main_orders)
        * 100
    )

    copurchase = copurchase.merge(
        products[
            [
                "SKU Produk",
                "Item Name",
                "Kategori Produk"
            ]
        ],
        on="SKU Produk",
        how="left"
    )

    # KPI
    jumlah_produk_cluster = (
        cluster_products["SKU Produk"].nunique()
    )

    jumlah_order_produk = len(main_orders)

    strongest_copurchase = (
        copurchase["Persentase_CoPurchase"].max()
        if not copurchase.empty
        else 0
    )

    kategori_dominan = (
        cluster_products["Kategori Produk"]
        .mode()
        .iloc[0]
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Products in Cluster</div>
                <div class="kpi-value">
                    {jumlah_produk_cluster}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Main Product Orders</div>
                <div class="kpi-value">
                    {jumlah_order_produk:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Strongest Co-Purchase</div>
                <div class="kpi-value">
                    {strongest_copurchase:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Dominant Category</div>
                <div class="kpi-value" style="font-size:20px;">
                    {kategori_dominan}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Co-Purchase Recommendation")

    # Produk utama
    st.markdown(
        f"""
        <div class="product-main-card">
            <div class="product-main-title">
                Main Product
            </div>
            <div class="product-main-name">
                {selected_product}
            </div>
            <div class="product-main-detail">
                SKU: {selected_sku}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Category: {selected_row["Kategori Produk"]}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Orders: {jumlah_order_produk:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Top 3 recommendation
    recommendation_cols = st.columns(3)

    for i, (_, row) in enumerate(copurchase.iterrows()):
        with recommendation_cols[i]:
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <div class="recommendation-rank">
                        TOP {i + 1} CO-PURCHASE
                    </div>
                    <div class="recommendation-name">
                        {row["Item Name"]}
                    </div>
                    <div class="recommendation-detail">
                        {row["Kategori Produk"]}<br>
                        {row["Jumlah_Order_Bersama"]:.0f} shared orders
                        &nbsp;•&nbsp;
                        {row["Persentase_CoPurchase"]:.1f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Purchase Pattern")

    chart1, chart2 = st.columns(2)

    # Co-purchase chart
    with chart1:
        
        fig_copurchase = px.bar(
            copurchase.sort_values(
                "Persentase_CoPurchase",
                ascending=True
            ),
            x="Persentase_CoPurchase",
            y="Item Name",
            orientation="h",
            text="Persentase_CoPurchase",
            title="Top 3 Co-Purchase Products"
        )

        fig_copurchase.update_traces(
            marker_color="#EB5642",
            texttemplate="%{text:.1f}%",
            textposition="outside",
            textfont=dict(color="#3A2F2A")
        )

        fig_copurchase.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Co-Purchase (%)",
            yaxis_title="",
            showlegend=False,
            margin=dict(l=10, r=30, t=50, b=20),
            font=dict(color="#3A2F2A"),
            title_font=dict(color="#3A2F2A", size=20),
            xaxis=dict(
                title_font=dict(color="#3A2F2A"),
                tickfont=dict(color="#3A2F2A")
            ),
            yaxis=dict(
                title_font=dict(color="#3A2F2A"),
                tickfont=dict(color="#3A2F2A")
            )
        )

        st.plotly_chart(
            fig_copurchase,
            use_container_width=True
        )

    # Category composition
    with chart2:

        category_composition = (
            cluster_products
            .groupby("Kategori Produk")
            .size()
            .reset_index(name="Jumlah Produk")
        )

        fig_category = px.pie(
            category_composition,
            names="Kategori Produk",
            values="Jumlah Produk",
            hole=0.55,
            title="Category Composition in Cluster",
            color_discrete_sequence=[
                "#EB5642",
                "#F77D25",
                "#FFDA75",
                "#F3A683",
                "#F8C291"
            ]
        )

        fig_category.update_traces(
            textfont=dict(color="#3A2F2A")
        )

        fig_category.update_layout(
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=50, b=20),
            font=dict(color="#3A2F2A"),
            title_font=dict(color="#3A2F2A", size=20),
            legend=dict(
                font=dict(color="#3A2F2A")
            )
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    st.markdown("### Co-Purchase Detail")

    copurchase_table = copurchase[
        [
            "Item Name",
            "Kategori Produk",
            "Jumlah_Order_Bersama",
            "Persentase_CoPurchase"
        ]
    ].copy()

    copurchase_table.columns = [
        "Recommended Product",
        "Category",
        "Shared Orders",
        "Co-Purchase (%)"
    ]

    copurchase_table["Co-Purchase (%)"] = (
        copurchase_table["Co-Purchase (%)"]
        .round(2)
    )

    st.dataframe(
        copurchase_table,
        use_container_width=True,
        hide_index=True
    )

elif page == "Customer Analysis":

    st.title("Customer Analysis")
    st.write(
        "Analisis segmentasi customer berdasarkan karakteristik "
        "demografis dan perilaku transaksi."
    )

    segmented_customers = (
        customers
        .dropna(subset=["Cluster", "Cluster Label"])
        .copy()
    )

    segmented_customers["Cluster"] = (
        segmented_customers["Cluster"].astype(int)
    )

    age_order = [
        "Remaja",
        "Dewasa Muda",
        "Dewasa",
        "Dewasa Matang",
        "Lansia"
    ]

    # Filter
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        cluster_options = (
            ["All Clusters"]
            + sorted(
                segmented_customers["Cluster Label"]
                .dropna()
                .unique()
            )
        )

        selected_customer_cluster = st.selectbox(
            "Customer Cluster",
            cluster_options
        )

    with f2:
        gender_options = (
            ["All Genders"]
            + sorted(
                segmented_customers["Gender"]
                .dropna()
                .unique()
            )
        )

        selected_gender = st.selectbox(
            "Gender",
            gender_options
        )

    with f3:
        age_options = (
            ["All Age Groups"]
            + [
                age for age in age_order
                if age in segmented_customers[
                    "Age Group"
                ].dropna().unique()
            ]
        )

        selected_age = st.selectbox(
            "Age Group",
            age_options
        )

    with f4:
        preference_options = (
            ["All Preferences"]
            + sorted(
                segmented_customers[
                    "Product Preference"
                ]
                .dropna()
                .unique()
            )
        )

        selected_preference = st.selectbox(
            "Product Preference",
            preference_options
        )

    filtered_customer = segmented_customers.copy()

    if selected_customer_cluster != "All Clusters":
        filtered_customer = filtered_customer[
            filtered_customer["Cluster Label"]
            == selected_customer_cluster
        ]

    if selected_gender != "All Genders":
        filtered_customer = filtered_customer[
            filtered_customer["Gender"]
            == selected_gender
        ]

    if selected_age != "All Age Groups":
        filtered_customer = filtered_customer[
            filtered_customer["Age Group"]
            == selected_age
        ]

    if selected_preference != "All Preferences":
        filtered_customer = filtered_customer[
            filtered_customer["Product Preference"]
            == selected_preference
        ]

    # KPI
    segmented_count = filtered_customer[
        "Customer ID"
    ].nunique()

    total_customer_spending = (
        filtered_customer["Total_Spending"].sum()
    )

    average_customer_spending = (
        filtered_customer["Total_Spending"].mean()
        if len(filtered_customer) > 0
        else 0
    )

    average_frequency = (
        filtered_customer["Frequency"].mean()
        if len(filtered_customer) > 0
        else 0
    )

    average_customer_aov = (
        filtered_customer[
            "Average_Order_Value"
        ].mean()
        if len(filtered_customer) > 0
        else 0
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Segmented Customers
                </div>
                <div class="kpi-value">
                    {segmented_count:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Total Spending
                </div>
                <div class="kpi-value-money">
                    Rp {total_customer_spending:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Average Spending
                </div>
                <div class="kpi-value-money">
                    Rp {average_customer_spending:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Average Frequency
                </div>
                <div class="kpi-value">
                    {average_frequency:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Average Order Value
                </div>
                <div class="kpi-value-money">
                    Rp {average_customer_aov:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Customer Profile")

    chart1, chart2 = st.columns(2)

    # Gender distribution
    with chart1:

        gender_summary = (
            filtered_customer
            .groupby("Gender")["Customer ID"]
            .nunique()
            .reset_index(name="Jumlah Customer")
        )

        fig_gender = px.pie(
            gender_summary,
            names="Gender",
            values="Jumlah Customer",
            hole=0.55,
            title="Customer Distribution by Gender",
            color_discrete_sequence=[
                "#EB5642",
                "#F77D25",
                "#FFDA75"
            ]
        )

        fig_gender.update_layout(
            paper_bgcolor="white",
            font=dict(color="#3A2F2A"),
            title_font=dict(
                color="#3A2F2A",
                size=20
            ),
            legend=dict(
                font=dict(color="#3A2F2A")
            ),
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=20
            )
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True
        )

    # Product preference
    with chart2:

        preference_summary = (
            filtered_customer
            .groupby("Product Preference")[
                "Customer ID"
            ]
            .nunique()
            .reset_index(name="Jumlah Customer")
        )

        fig_preference = px.pie(
            preference_summary,
            names="Product Preference",
            values="Jumlah Customer",
            hole=0.55,
            title="Customer Product Preference",
            color_discrete_sequence=[
                "#EB5642",
                "#F77D25",
                "#FFDA75",
                "#F3A683",
                "#F8C291",
                "#C44536",
                "#FFB347",
                "#E59866"
            ]
        )

        fig_preference.update_layout(
            paper_bgcolor="white",
            font=dict(color="#3A2F2A"),
            title_font=dict(
                color="#3A2F2A",
                size=20
            ),
            legend=dict(
                font=dict(color="#3A2F2A")
            ),
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=20
            )
        )

        st.plotly_chart(
            fig_preference,
            use_container_width=True
        )

    st.markdown("### Customer Segmentation")

    cluster_summary = (
        filtered_customer
        .groupby("Cluster Label")
        .agg(
            Jumlah_Customer=("Customer ID", "nunique"),
            Total_Spending=("Total_Spending", "sum")
        )
        .reset_index()
    )

    total_customer_cluster = cluster_summary["Jumlah_Customer"].sum()
    total_spending_cluster = cluster_summary["Total_Spending"].sum()

    cluster_summary["Customer Contribution"] = (
        cluster_summary["Jumlah_Customer"] / total_customer_cluster * 100
    )

    cluster_summary["Spending Contribution"] = (
        cluster_summary["Total_Spending"] / total_spending_cluster * 100
    )

    cluster_summary = cluster_summary.sort_values(
        "Spending Contribution",
        ascending=True
    )

    cluster_compare = pd.melt(
        cluster_summary,
        id_vars="Cluster Label",
        value_vars=["Customer Contribution", "Spending Contribution"],
        var_name="Metric",
        value_name="Percentage"
    )

    fig_cluster_compare = px.bar(
        cluster_compare,
        x="Percentage",
        y="Cluster Label",
        color="Metric",
        barmode="group",
        orientation="h",
        text="Percentage",
        title="Customer vs Spending Contribution by Cluster",
        color_discrete_map={
            "Customer Contribution": "#EB5642",
            "Spending Contribution": "#F77D25"
        }
    )

    fig_cluster_compare.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont=dict(color="#3A2F2A", size=12)
    )

    fig_cluster_compare.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#3A2F2A"),
        title_font=dict(color="#3A2F2A", size=20),
        xaxis_title="Contribution (%)",
        yaxis_title="",
        height=520,
        margin=dict(l=10, r=40, t=60, b=20),
        legend=dict(
            title="Metric",
            font=dict(color="#3A2F2A", size=12),
            title_font=dict(color="#3A2F2A", size=12),
            x=1.02,
            y=1,
            bgcolor="rgba(255,255,255,0.7)"
        )
    )

    fig_cluster_compare.update_xaxes(
        title_font=dict(color="#3A2F2A"),
        tickfont=dict(color="#3A2F2A"),
        showgrid=False
    )

    fig_cluster_compare.update_yaxes(
        title_font=dict(color="#3A2F2A"),
        tickfont=dict(color="#3A2F2A")
    )

    st.plotly_chart(fig_cluster_compare, use_container_width=True)

    st.markdown("### Customer Behavior")

    # Average Spending by Age Group
    age_summary = (
        filtered_customer
        .groupby("Age Group", observed=True)
        .agg(
            Average_Spending=("Total_Spending", "mean"),
            Average_Frequency=("Frequency", "mean")
        )
        .reset_index()
    )

    age_summary["Age Group"] = pd.Categorical(
        age_summary["Age Group"],
        categories=age_order,
        ordered=True
    )

    age_summary = age_summary.sort_values("Age Group")

    fig_age = px.line(
        age_summary,
        x="Age Group",
        y="Average_Spending",
        markers=True,
        title="Average Spending by Age Group"
    )

    fig_age.update_traces(
        line_color="#EB5642",
        marker_color="#F77D25",
        line_width=3,
        marker_size=9
    )

    fig_age.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#3A2F2A"),
        title_font=dict(color="#3A2F2A", size=20),
        xaxis_title="Age Group",
        yaxis_title="Average Spending",
        height=500,
        margin=dict(l=10, r=20, t=60, b=20)
    )

    fig_age.update_xaxes(
        title_font=dict(color="#3A2F2A"),
        tickfont=dict(color="#3A2F2A"),
        showgrid=False
    )

    fig_age.update_yaxes(
        title_font=dict(color="#3A2F2A"),
        tickfont=dict(color="#3A2F2A"),
        gridcolor="rgba(58,47,42,0.15)"
    )

    st.plotly_chart(fig_age, use_container_width=True)

    # Age Group vs Product Preference
    heatmap_data = pd.crosstab(
        filtered_customer["Age Group"],
        filtered_customer["Product Preference"]
    )

    heatmap_data = heatmap_data.reindex(
        age_order
    ).fillna(0)

    # Hilangkan preference yang tidak memiliki customer
    heatmap_data = heatmap_data.loc[
        :,
        heatmap_data.sum(axis=0) > 0
    ]

    fig_heatmap = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        title="Age Group vs Product Preference",
        labels={
            "x": "Product Preference",
            "y": "Age Group",
            "color": "Customers"
        },
        color_continuous_scale=[
            [0.00, "#FFF7F2"],
            [0.35, "#FFDA75"],
            [0.70, "#F77D25"],
            [1.00, "#EB5642"]
        ]
    )

    fig_heatmap.update_traces(
        textfont=dict(
            color="#3A2F2A",
            size=13
        )
    )

    fig_heatmap.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#3A2F2A"),
        title_font=dict(
            color="#3A2F2A",
            size=20
        ),
        height=520,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        coloraxis_colorbar=dict(
            title="Customers",
            tickfont=dict(color="#3A2F2A"),
            title_font=dict(color="#3A2F2A")
        )
    )

    fig_heatmap.update_xaxes(
        title_font=dict(color="#3A2F2A"),
        tickfont=dict(color="#3A2F2A"),
        tickangle=-30
    )

    fig_heatmap.update_yaxes(
        title_font=dict(color="#3A2F2A"),
        tickfont=dict(color="#3A2F2A")
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

    st.markdown("### Target Market by Product Category")

    target_table = target_market.copy()

    if selected_gender != "All Genders":
        target_table = target_table[
            target_table["Target_Gender"]
            == selected_gender
        ]

    if selected_age != "All Age Groups":
        target_table = target_table[
            target_table["Target_Age_Group"]
            == selected_age
        ]

    st.dataframe(
        target_table[
            [
                "Kategori Produk",
                "Target_Segment",
                "Jumlah_Customer",
                "Total_Quantity",
                "Total_Spending"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Customer Cluster Profile")

    cluster_profile_table = customer_cluster.copy()

    if selected_customer_cluster != "All Clusters":
        cluster_profile_table = (
            cluster_profile_table[
                cluster_profile_table[
                    "Cluster Label"
                ] == selected_customer_cluster
            ]
        )

    st.dataframe(
        cluster_profile_table,
        use_container_width=True,
        hide_index=True
    )

elif page == "Geographic Analysis":

    st.title("Geographic Analysis")
    st.write(
        "Analisis performa transaksi GoBorong berdasarkan wilayah."
    )

    metric_labels = {
        "Total_Spending": "Total Spending",
        "Jumlah_Customer": "Jumlah Customer",
        "Jumlah_Order": "Jumlah Order",
        "Total_Quantity": "Total Quantity",
        "Average_Order_Value": "Average Order Value",
        "Order_per_Customer": "Order per Customer"
    }

    # Filter
    f1, f2 = st.columns(2)

    with f1:
        selected_metric = st.selectbox(
            "Map Metric",
            list(metric_labels.keys()),
            format_func=lambda x: metric_labels[x]
        )

    with f2:
        region_options = (
            ["All Regions"]
            + sorted(geo["City (Shipping)"].unique())
        )

        selected_region = st.selectbox(
            "Region",
            region_options
        )

    # Filter transaksi
    if selected_region == "All Regions":
        geo_transactions = transactions.copy()
        map_data = geo.copy()
    else:
        geo_transactions = transactions[
            transactions["City (Shipping)"]
            == selected_region
        ].copy()

        map_data = geo[
            geo["City (Shipping)"]
            == selected_region
        ].copy()

    # KPI
    geo_spending = geo_transactions[
        "Total Transaction"
    ].sum()

    geo_orders = geo_transactions[
        "Nomor Order"
    ].nunique()

    geo_customers = geo_transactions[
        "Customer ID"
    ].nunique()

    geo_quantity = geo_transactions[
        "Jumlah Beli"
    ].sum()

    geo_aov = (
        geo_spending / geo_orders
        if geo_orders > 0
        else 0
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Spending</div>
                <div class="kpi-value-money">
                    Rp {geo_spending:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Customers</div>
                <div class="kpi-value">
                    {geo_customers:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">
                    {geo_orders:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Quantity</div>
                <div class="kpi-value">
                    {geo_quantity:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Average Order Value</div>
                <div class="kpi-value-money">
                    Rp {geo_aov:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Regional Performance Map")

    # Background map
    background_ids = [
        feature["properties"]["GID_2"]
        for feature in background_geojson["features"]
    ]

    fig_geo = go.Figure()

    fig_geo.add_trace(
        go.Choropleth(
            geojson=background_geojson,
            locations=background_ids,
            featureidkey="properties.GID_2",
            z=[1] * len(background_ids),
            colorscale=[
                [0, "#E8E8E8"],
                [1, "#E8E8E8"]
            ],
            showscale=False,
            marker_line_color="white",
            marker_line_width=0.6,
            hoverinfo="skip"
        )
    )

    # 15 wilayah utama
    fig_geo.add_trace(
        go.Choropleth(
            geojson=wilayah_geojson,
            locations=map_data["City (Shipping)"],
            featureidkey="properties.City_Key",
            z=map_data[selected_metric],

            zmin=geo[selected_metric].min(),
            zmax=geo[selected_metric].max(),

            colorscale=[
                [0.00, "#FFDA75"],
                [0.50, "#F77D25"],
                [1.00, "#EB5642"]
            ],

            customdata=map_data[
                [
                    "Jumlah_Customer",
                    "Jumlah_Order",
                    "Total_Spending",
                    "Total_Quantity",
                    "Average_Order_Value",
                    "Order_per_Customer",
                    "Kategori_Dominan"
                ]
            ],

            hovertemplate=(
                "<b>%{location}</b><br>"
                "Customer: %{customdata[0]:,.0f}<br>"
                "Order: %{customdata[1]:,.0f}<br>"
                "Spending: Rp %{customdata[2]:,.0f}<br>"
                "Quantity: %{customdata[3]:,.0f}<br>"
                "AOV: Rp %{customdata[4]:,.0f}<br>"
                "Order / Customer: %{customdata[5]:.2f}<br>"
                "Dominant Category: %{customdata[6]}"
                "<extra></extra>"
            ),

            marker_line_color="white",
            marker_line_width=1,

            colorbar=dict(
                title=metric_labels[selected_metric],
                tickfont=dict(color="#3A2F2A"),
                title_font=dict(color="#3A2F2A")
            )
        )
    )

    fig_geo.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="white"
    )

    fig_geo.update_layout(
        paper_bgcolor="white",
        font=dict(color="#3A2F2A"),
        height=620,
        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        )
    )

    st.plotly_chart(
        fig_geo,
        use_container_width=True
    )

    st.markdown("### Regional Ranking")

    ranking_data = geo.sort_values(
        selected_metric,
        ascending=True
    ).copy()

    ranking_colors = [
        "#EB5642"
        if (
            selected_region != "All Regions"
            and city == selected_region
        )
        else "#F77D25"
        for city in ranking_data["City (Shipping)"]
    ]

    fig_ranking = px.bar(
        ranking_data,
        x=selected_metric,
        y="City (Shipping)",
        orientation="h",
        text=selected_metric,
        title=f"Regional Ranking by {metric_labels[selected_metric]}"
    )

    fig_ranking.update_traces(
        marker_color=ranking_colors,
        textposition="outside",
        textfont=dict(
            color="#3A2F2A"
        )
    )

    fig_ranking.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#3A2F2A"),
        title_font=dict(
            color="#3A2F2A",
            size=20
        ),
        xaxis_title=metric_labels[selected_metric],
        yaxis_title="",
        height=600,
        margin=dict(
            l=10,
            r=80,
            t=60,
            b=20
        )
    )

    fig_ranking.update_xaxes(
        tickfont=dict(color="#3A2F2A"),
        title_font=dict(color="#3A2F2A"),
        showgrid=False
    )

    fig_ranking.update_yaxes(
        tickfont=dict(color="#3A2F2A")
    )

    st.plotly_chart(
        fig_ranking,
        use_container_width=True
    )

    # Kategori dominan
    dominant_category = (
        geo_transactions
        .groupby("Kategori Produk")[
            "Total Transaction"
        ]
        .sum()
        .sort_values(ascending=False)
    )

    if not dominant_category.empty:
        top_geo_category = dominant_category.index[0]
        top_geo_category_spending = dominant_category.iloc[0]
    else:
        top_geo_category = "-"
        top_geo_category_spending = 0

    st.markdown("### Regional Highlight")

    st.markdown(
        f"""
        <div class="highlight-card">
            <div class="highlight-title">
                Dominant Product Category
            </div>
            <div class="highlight-value">
                {top_geo_category}
            </div>
            <div>
                Rp {top_geo_category_spending:,.0f} spending
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Regional Detail")

    geo_detail = geo[
        [
            "City (Shipping)",
            "Jumlah_Customer",
            "Jumlah_Order",
            "Total_Spending",
            "Total_Quantity",
            "Average_Order_Value",
            "Order_per_Customer",
            "Kategori_Dominan",
            "Spending_Contribution_%",
            "Customer_Contribution_%"
        ]
    ].copy()

    if selected_region != "All Regions":
        geo_detail = geo_detail[
            geo_detail["City (Shipping)"]
            == selected_region
        ]

    st.dataframe(
        geo_detail,
        use_container_width=True,
        hide_index=True
    )

elif page == "Transactions":

    st.title("Transactions")
    st.write(
        "Detail seluruh transaksi yang digunakan dalam analisis GoBorong."
    )

    transaction_data = transactions.copy()

    f1, f2, f3 = st.columns(3)

    with f1:
        search_order = st.text_input(
            "Search Order / Customer",
            placeholder="Order number or Customer ID"
        )

    with f2:
        transaction_city = st.selectbox(
            "City",
            ["All Cities"]
            + sorted(
                transaction_data["City (Shipping)"]
                .dropna()
                .unique()
            )
        )

    with f3:
        transaction_category = st.selectbox(
            "Product Category",
            ["All Categories"]
            + sorted(
                transaction_data["Kategori Produk"]
                .dropna()
                .unique()
            )
        )

    if search_order:
        search_text = search_order.lower()

        transaction_data = transaction_data[
            transaction_data["Nomor Order"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
            |
            transaction_data["Customer ID"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
        ]

    if transaction_city != "All Cities":
        transaction_data = transaction_data[
            transaction_data["City (Shipping)"]
            == transaction_city
        ]

    if transaction_category != "All Categories":
        transaction_data = transaction_data[
            transaction_data["Kategori Produk"]
            == transaction_category
        ]

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Rows",
        f"{len(transaction_data):,}"
    )

    k2.metric(
        "Orders",
        f"{transaction_data['Nomor Order'].nunique():,}"
    )

    k3.metric(
        "Total Spending",
        f"Rp {transaction_data['Total Transaction'].sum():,.0f}"
    )

    st.dataframe(
        transaction_data,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Transactions CSV",
        transaction_data.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="goborong_transactions.csv",
        mime="text/csv"
    )

elif page == "Customers":

    st.title("Customers / Clients")
    st.write(
        "Profil customer dan ringkasan perilaku transaksi."
    )

    customer_data = customers.copy()

    f1, f2, f3 = st.columns(3)

    with f1:
        search_customer = st.text_input(
            "Search Customer",
            placeholder="Customer ID or name"
        )

    with f2:
        customer_gender = st.selectbox(
            "Gender",
            ["All Genders"]
            + sorted(
                customer_data["Gender"]
                .dropna()
                .unique()
            )
        )

    with f3:
        member_options = (
            ["All Member Status"]
            + sorted(
                customer_data["Member Status"]
                .dropna()
                .unique()
            )
        )

        customer_member = st.selectbox(
            "Member Status",
            member_options
        )

    if search_customer:
        search_text = search_customer.lower()

        customer_mask = (
            customer_data["Customer ID"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
        )

        if "Name" in customer_data.columns:
            customer_mask = (
                customer_mask
                |
                customer_data["Name"]
                .astype(str)
                .str.lower()
                .str.contains(search_text)
            )

        customer_data = customer_data[
            customer_mask
        ]

    if customer_gender != "All Genders":
        customer_data = customer_data[
            customer_data["Gender"]
            == customer_gender
        ]

    if customer_member != "All Member Status":
        customer_data = customer_data[
            customer_data["Member Status"]
            == customer_member
        ]

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Customers",
        f"{customer_data['Customer ID'].nunique():,}"
    )

    k2.metric(
        "Total Spending",
        f"Rp {customer_data['Total_Spending'].sum():,.0f}"
    )

    k3.metric(
        "Average Frequency",
        f"{customer_data['Frequency'].mean():.2f}"
    )

    customer_columns = [
        "Customer ID",
        "Name",
        "Age",
        "Age Group",
        "Gender",
        "Product Preference",
        "Member Status",
        "Frequency",
        "Total_Spending",
        "Total_Quantity",
        "Average_Order_Value",
        "Cluster",
        "Cluster Label"
    ]

    customer_columns = [
        col for col in customer_columns
        if col in customer_data.columns
    ]

    st.dataframe(
        customer_data[customer_columns],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Customers CSV",
        customer_data.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="goborong_customers.csv",
        mime="text/csv"
    )

elif page == "Product Data":

    st.title("Product Data")
    st.write(
        "Ringkasan performa produk dan hasil product clustering."
    )

    product_data = products.copy()

    f1, f2, f3 = st.columns(3)

    with f1:
        search_product = st.text_input(
            "Search Product",
            placeholder="SKU or product name"
        )

    with f2:
        product_category = st.selectbox(
            "Category",
            ["All Categories"]
            + sorted(
                product_data["Kategori Produk"]
                .dropna()
                .unique()
            )
        )

    with f3:
        cluster_values = sorted(
            product_data["Cluster"]
            .dropna()
            .astype(int)
            .unique()
        )

        product_cluster_filter = st.selectbox(
            "Product Cluster",
            ["All Clusters"] + cluster_values
        )

    if search_product:
        search_text = search_product.lower()

        product_data = product_data[
            product_data["SKU Produk"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
            |
            product_data["Item Name"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
        ]

    if product_category != "All Categories":
        product_data = product_data[
            product_data["Kategori Produk"]
            == product_category
        ]

    if product_cluster_filter != "All Clusters":
        product_data = product_data[
            product_data["Cluster"]
            == product_cluster_filter
        ]

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Products",
        f"{product_data['SKU Produk'].nunique():,}"
    )

    k2.metric(
        "Total Orders",
        f"{product_data['Jumlah_Order'].sum():,.0f}"
    )

    k3.metric(
        "Total Spending",
        f"Rp {product_data['Total_Spending'].sum():,.0f}"
    )

    st.dataframe(
        product_data,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Product Data CSV",
        product_data.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="goborong_products.csv",
        mime="text/csv"
    )
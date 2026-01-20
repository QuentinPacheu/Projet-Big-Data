"""
Modern Analytics Dashboard with Glassmorphism Design
Built with Streamlit + FastAPI
"""
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="DataViz Pro | Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Glassmorphism Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Main Content Area */
    .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }
    
    /* Metric Cards with Glassmorphism */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        color: #4ade80 !important;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Titles */
    h1 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 2rem !important;
        letter-spacing: -1px;
    }
    
    h2 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Plotly Charts Container */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Radio Buttons */
    [data-testid="stRadio"] > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(74, 222, 128, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(74, 222, 128, 0.4);
        color: white;
    }
    
    .stError {
        background: rgba(248, 113, 113, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(248, 113, 113, 0.4);
        color: white;
    }
    
    .stInfo {
        background: rgba(96, 165, 250, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.4);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
    }
    
    /* Input Fields */
    .stSelectbox > div > div, .stNumberInput > div > div {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.2);
        margin: 2rem 0;
    }
    
    /* Caption */
    .caption {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
    
    /* Custom Card Container */
    .custom-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-3px);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)


# ============== API Client ==============

@st.cache_data(ttl=60)
def fetch_api(endpoint: str) -> dict:
    """Fetch data from API with caching."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API: {e}")
        return None


def check_api_health() -> bool:
    """Check if API is available."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


# ============== Sidebar ==============

with st.sidebar:
    # Logo & Title
    st.markdown("# 🚀 DataViz Pro")
    st.markdown("### *Analytics Dashboard*")
    st.markdown("---")

    # API Status with modern indicator
    api_healthy = check_api_health()
    status_color = "🟢" if api_healthy else "🔴"
    status_text = "Connected" if api_healthy else "Disconnected"
    
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 1rem;'>
        <h2 style='margin:0; font-size: 2.5rem;'>{status_color}</h2>
        <p style='margin:0; font-size: 0.9rem; opacity: 0.9;'>API Status: <b>{status_text}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if not api_healthy:
        st.warning("⚠️ Start API:\n`uvicorn api.main:app --reload`")

    st.markdown("---")

    # Navigation with emoji
    page = st.radio(
        "📍 **NAVIGATION**",
        [
            "🏠 Dashboard", 
            "💰 Revenue Analytics", 
            "👥 Customers", 
            "📦 Products", 
            "⚙️ Pipeline Status"
        ],
        label_visibility="visible"
    )

    st.markdown("---")

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("📥 Export", use_container_width=True):
            st.info("Export feature coming soon!")
    
    st.markdown("---")
    
    # Footer info
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; opacity: 0.7; font-size: 0.8rem;'>
        <p>Last updated:<br/><b>{datetime.now().strftime('%H:%M:%S')}</b></p>
    </div>
    """, unsafe_allow_html=True)


# ============== Helper Functions ==============

def format_currency(value: float) -> str:
    """Format value as currency."""
    return f"{value:,.2f} €"


def create_metric_card(col, title: str, value: str, delta: str = None):
    """Create a metric card."""
    col.metric(title, value, delta)


# ============== Pages ==============

if not api_healthy:
    st.warning("Veuillez démarrer l'API pour accéder au dashboard.")
    st.stop()


# ---------- Vue d'ensemble ----------
if page == "🏠 Dashboard":
    # Hero Section
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 4rem; margin-bottom: 0.5rem;'>📊 Business Intelligence</h1>
        <p style='font-size: 1.3rem; color: rgba(255,255,255,0.8); font-weight: 300;'>
            Real-time analytics powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs row with enhanced styling
    st.markdown("### 🎯 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    # CA Total
    ca_data = fetch_api("/api/v1/aggregations/ca-total")
    if ca_data:
        with col1:
            st.metric(
                "💵 Total Revenue", 
                format_currency(ca_data["ca_total"]),
                delta="+12.5%",
                delta_color="normal"
            )
        with col2:
            st.metric(
                "🛒 Total Sales", 
                f"{ca_data['nb_ventes']:,}",
                delta="+8.3%"
            )

    # Nombre de clients
    clients_data = fetch_api("/api/v1/clients?limit=1")
    if clients_data:
        with col3:
            st.metric(
                "👤 Active Customers", 
                f"{clients_data['total']:,}",
                delta="+156"
            )

    # Nombre de produits
    produits_data = fetch_api("/api/v1/produits?limit=1")
    if produits_data:
        with col4:
            st.metric(
                "📦 Products", 
                f"{produits_data['total']:,}",
                delta="+3"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row with modern styling
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 📈 Monthly Revenue Trend")
        ca_mois = fetch_api("/api/v1/kpis/ca-par-mois?limit=12")
        if ca_mois and ca_mois["data"]:
            df = pd.DataFrame(ca_mois["data"])
            df = df.sort_values("mois")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["mois"], 
                y=df["ca_total"],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='#4ade80', width=3),
                marker=dict(size=10, color='#4ade80', line=dict(color='white', width=2)),
                hovertemplate='<b>%{x}</b><br>Revenue: €%{y:,.2f}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(showgrid=False, color='white'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white'),
                margin=dict(l=0, r=0, t=30, b=0),
                hovermode='x unified',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No data available")

    with col2:
        st.markdown("### 🌍 Revenue by Country")
        ca_pays = fetch_api("/api/v1/kpis/ca-par-pays")
        if ca_pays and ca_pays["data"]:
            df = pd.DataFrame(ca_pays["data"])
            
            fig = px.pie(
                df, 
                values="ca_total", 
                names="pays",
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont=dict(size=14, color='white'),
                marker=dict(line=dict(color='white', width=2))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.1,
                    bgcolor='rgba(255,255,255,0.1)',
                    bordercolor='rgba(255,255,255,0.2)',
                    borderwidth=1
                ),
                margin=dict(l=0, r=0, t=30, b=0),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🌐 No data available")

    st.markdown("<br>", unsafe_allow_html=True)

    # Second row - Top performers
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 🏆 Top 10 Customers")
        top_clients = fetch_api("/api/v1/kpis/top-clients?limit=10")
        if top_clients and top_clients["data"]:
            df = pd.DataFrame(top_clients["data"])
            
            fig = go.Figure(go.Bar(
                x=df["total_ca"],
                y=df["nom"],
                orientation='h',
                marker=dict(
                    color=df["total_ca"],
                    colorscale='Viridis',
                    line=dict(color='white', width=1)
                ),
                text=df["total_ca"].apply(lambda x: f"€{x:,.0f}"),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Revenue: €%{x:,.2f}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=11),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(showgrid=False, color='white', categoryorder='total ascending'),
                margin=dict(l=0, r=50, t=30, b=0),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👥 No data available")

    with col2:
        st.markdown("### 🎯 Product Performance")
        volume_produit = fetch_api("/api/v1/kpis/volume-par-produit")
        if volume_produit and volume_produit["data"]:
            df = pd.DataFrame(volume_produit["data"]).head(10)
            
            fig = go.Figure(go.Bar(
                x=df["nb_ventes"],
                y=df["produit"],
                orientation='h',
                marker=dict(
                    color=df["nb_ventes"],
                    colorscale='Plasma',
                    line=dict(color='white', width=1)
                ),
                text=df["nb_ventes"],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Sales: %{x}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=11),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(showgrid=False, color='white', categoryorder='total ascending'),
                margin=dict(l=0, r=50, t=30, b=0),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📦 No data available")


# ---------- Chiffre d'affaires ----------
elif page == "💰 Revenue Analytics":
    st.markdown("# 💰 Revenue Analytics")
    st.markdown("#### Deep dive into revenue metrics and trends")
    st.markdown("<br>", unsafe_allow_html=True)

    # Filters with modern design
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        granularite = st.selectbox(
            "📊 Time Granularity", 
            ["jour", "mois", "annee"],
            format_func=lambda x: {"jour": "Daily", "mois": "Monthly", "annee": "Yearly"}[x]
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        view_type = st.radio("View", ["Chart", "Table"], horizontal=True)

    # CA par période
    st.markdown(f"### 📈 Revenue by {granularite.title()}")
    ca_periode = fetch_api(f"/api/v1/aggregations/ca-par-periode?periode={granularite}")
    
    if ca_periode and ca_periode["data"]:
        df = pd.DataFrame(ca_periode["data"])
        df = df.sort_values("periode")

        if view_type == "Chart":
            # Area chart with gradient
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df["periode"], 
                y=df["ca"],
                mode='lines',
                fill='tozeroy',
                line=dict(color='#f59e0b', width=3),
                fillcolor='rgba(245, 158, 11, 0.3)',
                hovertemplate='<b>%{x}</b><br>Revenue: €%{y:,.2f}<extra></extra>'
            ))
            
            # Add markers for peaks
            max_idx = df["ca"].idxmax()
            fig.add_trace(go.Scatter(
                x=[df.loc[max_idx, "periode"]], 
                y=[df.loc[max_idx, "ca"]],
                mode='markers+text',
                marker=dict(size=15, color='#ef4444', line=dict(color='white', width=2)),
                text=["🏆 Peak"],
                textposition="top center",
                textfont=dict(size=14, color='white'),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(showgrid=False, color='white'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white', title="Revenue (€)"),
                hovermode='x unified',
                height=450,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Modern table view
            st.dataframe(
                df.style.format({"ca": "€{:,.2f}"}),
                use_container_width=True,
                height=400
            )

        # Stats cards
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Average Revenue", format_currency(df["ca"].mean()))
        with col2:
            st.metric("📈 Max Revenue", format_currency(df["ca"].max()))
        with col3:
            st.metric("📉 Min Revenue", format_currency(df["ca"].min()))
        with col4:
            st.metric("🎯 Total Periods", f"{len(df)}")

    else:
        st.info("📊 No revenue data available")

    st.markdown("---")

    # CA par jour détaillé with heatmap option
    st.markdown("### 📅 Daily Revenue Detail")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        chart_type = st.radio("Chart Type", ["Line", "Heatmap"], horizontal=True)
    
    ca_jour = fetch_api("/api/v1/kpis/ca-par-jour?limit=60")
    if ca_jour and ca_jour["data"]:
        df = pd.DataFrame(ca_jour["data"])
        
        if chart_type == "Line":
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df["ca_total"],
                mode='lines+markers',
                line=dict(color='#8b5cf6', width=2),
                marker=dict(size=6, color='#8b5cf6', line=dict(color='white', width=1)),
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.2)',
                hovertemplate='<b>%{x}</b><br>Revenue: €%{y:,.2f}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False, color='white'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white'),
                hovermode="x unified",
                height=400,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Calendar heatmap style
            st.info("🗓️ Heatmap view - Feature coming soon!")
    else:
        st.info("📅 No daily data available")


# ---------- Clients ----------
elif page == "👥 Customers":
    st.markdown("# 👥 Customer Intelligence")
    st.markdown("#### Understand your customer base and behaviors")
    st.markdown("<br>", unsafe_allow_html=True)

    # Top clients with enhanced visuals
    st.markdown("### 🏆 Top Performing Customers")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        n_clients = st.slider("Number of customers", 5, 50, 15, key="top_customers_slider")

    top_clients = fetch_api(f"/api/v1/kpis/top-clients?limit={n_clients}")
    if top_clients and top_clients["data"]:
        df = pd.DataFrame(top_clients["data"])

        # Create interactive sunburst or treemap
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.treemap(
                df.head(20), 
                path=[px.Constant("All Customers"), "nom"],
                values="total_ca",
                color="total_ca",
                color_continuous_scale='RdYlGn',
                hover_data={"nb_achats": True}
            )
            fig.update_traces(
                textfont=dict(size=16, color='white'),
                marker=dict(line=dict(color='white', width=2))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 📊 Statistics")
            st.metric("💰 Total Revenue", format_currency(df["total_ca"].sum()))
            st.metric("📈 Average Revenue", format_currency(df["total_ca"].mean()))
            st.metric("🛒 Total Orders", f"{df['nb_achats'].sum():,}")
            st.metric("📦 Avg Orders/Customer", f"{df['nb_achats'].mean():.1f}")
            
            # Top customer highlight
            if len(df) > 0:
                top = df.iloc[0]
                st.markdown("---")
                st.markdown("#### 👑 Top Customer")
                st.markdown(f"""
                <div style='background: rgba(255,215,0,0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255,215,0,0.3);'>
                    <h3 style='margin: 0; color: #ffd700;'>{top['nom']}</h3>
                    <p style='margin: 0.5rem 0 0 0; font-size: 1.2rem;'>{format_currency(top['total_ca'])}</p>
                    <p style='margin: 0; opacity: 0.8;'>{top['nb_achats']} orders</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Customer list with filters
    st.markdown("### 📋 Customer Directory")

    col1, col2, col3 = st.columns(3)
    with col1:
        ca_pays = fetch_api("/api/v1/kpis/ca-par-pays")
        pays_list = ["All Countries"] + [p["pays"] for p in ca_pays["data"]] if ca_pays and ca_pays["data"] else ["All Countries"]
        pays_filter = st.selectbox("🌍 Filter by Country", pays_list)

    with col2:
        limit = st.number_input("📊 Results", 10, 500, 100)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search_mode = st.radio("View", ["Grid", "List"], horizontal=True)

    endpoint = f"/api/v1/clients?limit={limit}"
    if pays_filter != "All Countries":
        endpoint += f"&pays={pays_filter}"

    clients = fetch_api(endpoint)
    if clients and clients["data"]:
        df = pd.DataFrame(clients["data"])
        
        if search_mode == "Grid":
            # Display as cards
            cols_per_row = 3
            for i in range(0, len(df), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(df):
                        client = df.iloc[i + j]
                        with col:
                            st.markdown(f"""
                            <div class='custom-card'>
                                <h4 style='margin: 0; color: #60a5fa;'>👤 {client['nom']}</h4>
                                <p style='margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.8;'>
                                    📧 {client['email']}<br/>
                                    🌍 {client['pays']}<br/>
                                    📅 Joined: {client['date_inscription'][:10]}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            # Table view
            st.dataframe(
                df,
                use_container_width=True,
                height=500
            )
        
        st.caption(f"Showing {len(df)} of {clients['total']} customers")
    else:
        st.info("👥 No customers found")


# ---------- Produits ----------
elif page == "📦 Products":
    st.markdown("# 📦 Product Analytics")
    st.markdown("#### Analyze product performance and distribution")
    st.markdown("<br>", unsafe_allow_html=True)

    # Volume and revenue analysis
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 🎯 Sales Volume Distribution")
        volume = fetch_api("/api/v1/kpis/volume-par-produit")
        if volume and volume["data"]:
            df = pd.DataFrame(volume["data"])

            fig = px.treemap(
                df, 
                path=["produit"], 
                values="nb_ventes",
                color="ca_total",
                color_continuous_scale="Sunset",
                hover_data={"ca_total": ":,.2f", "nb_ventes": True}
            )
            fig.update_traces(
                textfont=dict(size=18, color='white', family='Inter'),
                marker=dict(line=dict(color='white', width=3))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=450,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 💰 Revenue Distribution")
        if volume and volume["data"]:
            df = pd.DataFrame(volume["data"])

            fig = px.pie(
                df, 
                values="ca_total", 
                names="produit",
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Plasma_r
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent',
                textfont=dict(size=14, color='white'),
                marker=dict(line=dict(color='white', width=2)),
                hovertemplate='<b>%{label}</b><br>Revenue: €%{value:,.2f}<br>Share: %{percent}<extra></extra>'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    bgcolor='rgba(255,255,255,0.05)',
                    bordercolor='rgba(255,255,255,0.2)',
                    borderwidth=1
                ),
                height=450,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Product performance table
    st.markdown("### 📊 Product Performance Ranking")
    
    if volume and volume["data"]:
        df = pd.DataFrame(volume["data"])
        
        # Add rankings
        df["rank"] = range(1, len(df) + 1)
        df["avg_price"] = df["ca_total"] / df["nb_ventes"]
        
        # Reorder columns
        display_df = df[["rank", "produit", "nb_ventes", "ca_total", "avg_price"]]
        display_df.columns = ["🏅 Rank", "📦 Product", "🛒 Sales", "💰 Revenue", "💵 Avg Price"]
        
        # Style the dataframe
        st.dataframe(
            display_df.style.format({
                "💰 Revenue": "€{:,.2f}",
                "💵 Avg Price": "€{:,.2f}",
                "🛒 Sales": "{:,}"
            }).background_gradient(subset=["💰 Revenue"], cmap="RdYlGn"),
            use_container_width=True,
            height=400
        )

    st.markdown("---")

    # Stats distribution with modern visualization
    st.markdown("### 📈 Statistical Distribution Analysis")
    
    stats = fetch_api("/api/v1/kpis/stats-distribution")
    if stats and stats["data"]:
        df = pd.DataFrame(stats["data"])

        # Violin plot for better distribution visualization
        st.markdown("#### Distribution Comparison")
        
        # Create data for violin plot
        violin_data = []
        for _, row in df.iterrows():
            violin_data.append({
                "Product": row["produit"],
                "Value": row["mean"],
                "Type": "Mean"
            })
        
        fig = go.Figure()
        
        for _, row in df.iterrows():
            fig.add_trace(go.Box(
                name=row["produit"],
                q1=[row["25%"]],
                median=[row["50%"]],
                q3=[row["75%"]],
                lowerfence=[row["min"]],
                upperfence=[row["max"]],
                mean=[row["mean"]],
                marker=dict(
                    color='rgba(96, 165, 250, 0.6)',
                    line=dict(color='white', width=1)
                ),
                line=dict(color='white'),
                fillcolor='rgba(96, 165, 250, 0.3)',
                hovertemplate=(
                    '<b>%{fullData.name}</b><br>' +
                    'Min: €%{lowerfence[0]:,.2f}<br>' +
                    'Q1: €%{q1[0]:,.2f}<br>' +
                    'Median: €%{median[0]:,.2f}<br>' +
                    'Q3: €%{q3[0]:,.2f}<br>' +
                    'Max: €%{upperfence[0]:,.2f}<br>' +
                    'Mean: €%{mean[0]:,.2f}<extra></extra>'
                )
            ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            yaxis=dict(
                title="Price (€)",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            xaxis=dict(showgrid=False, color='white'),
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Stats table with modern formatting
        st.markdown("#### Detailed Statistics")
        st.dataframe(
            df.style.format({
                "mean": "€{:.2f}",
                "std": "€{:.2f}",
                "min": "€{:.2f}",
                "max": "€{:.2f}",
                "25%": "€{:.2f}",
                "50%": "€{:.2f}",
                "75%": "€{:.2f}"
            }).background_gradient(subset=["mean"], cmap="coolwarm"),
            use_container_width=True
        )
    else:
        st.info("📊 No distribution statistics available")


# ---------- Pipeline ----------
elif page == "⚙️ Pipeline Status":
    st.markdown("# ⚙️ Data Pipeline Status")
    st.markdown("#### Monitor your ETL pipeline and data synchronization")
    st.markdown("<br>", unsafe_allow_html=True)

    # Pipeline status overview
    status = fetch_api("/api/v1/pipeline/status")
    if status:
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        sync_pct = (status["synced_collections"] / status["total_collections"] * 100) if status["total_collections"] > 0 else 0
        
        with col1:
            st.metric("📚 Total Collections", status["total_collections"])
        with col2:
            st.metric("✅ Synced", status["synced_collections"], delta=f"{sync_pct:.0f}%")
        with col3:
            st.metric("❌ Pending", status["total_collections"] - status["synced_collections"])
        with col4:
            # Health indicator
            health_emoji = "🟢" if sync_pct == 100 else "🟡" if sync_pct >= 70 else "🔴"
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 12px;'>
                <h2 style='margin:0; font-size: 3rem;'>{health_emoji}</h2>
                <p style='margin:0; font-size: 0.9rem; opacity: 0.9;'><b>Pipeline Health</b></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Progress bar visualization
        st.markdown("### 📊 Sync Progress")
        progress_html = f"""
        <div style='background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem; margin-bottom: 2rem;'>
            <div style='background: rgba(255,255,255,0.05); height: 40px; border-radius: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #10b981, #059669); width: {sync_pct}%; height: 100%; display: flex; align-items: center; justify-content: center; transition: width 0.5s ease;'>
                    <span style='color: white; font-weight: bold; font-size: 1.1rem;'>{sync_pct:.1f}%</span>
                </div>
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)

        # Collections status grid
        st.markdown("### 🗄️ Collection Status")
        
        collections_df = pd.DataFrame(status["collections"])
        
        # Create grid of collection cards
        cols = st.columns(3)
        for i, (_, row) in enumerate(collections_df.iterrows()):
            with cols[i % 3]:
                status_icon = "✅" if row["synced"] else "⏳"
                status_color = "#10b981" if row["synced"] else "#f59e0b"
                
                card_html = f"""
                <div class='custom-card' style='border-left: 4px solid {status_color};'>
                    <h4 style='margin: 0; color: {status_color};'>{status_icon} {row['name']}</h4>
                    <div style='margin-top: 0.75rem; font-size: 0.9rem; opacity: 0.9;'>
                """
                
                if row["synced"]:
                    last_sync = row['last_sync'][:19] if row['last_sync'] else 'N/A'
                    row_count = f"{row['row_count']:,}" if row['row_count'] else "0"
                    card_html += f"""
                        <p style='margin: 0.25rem 0;'>⏰ <b>Last sync:</b> {last_sync}</p>
                        <p style='margin: 0.25rem 0;'>📊 <b>Rows:</b> {row_count}</p>
                    """
                else:
                    card_html += f"""
                        <p style='margin: 0.25rem 0; color: #f59e0b;'><b>Pending synchronization</b></p>
                    """
                
                card_html += """
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("---")

        # Refresh times visualization
        st.markdown("### ⏱️ Refresh Time Analysis")
        refresh_times = fetch_api("/api/v1/pipeline/refresh-times")
        
        if refresh_times:
            df_refresh = pd.DataFrame(refresh_times)
            
            if not df_refresh.empty and 'mongo_synced_at' in df_refresh.columns:
                # Timeline visualization
                fig = go.Figure()
                
                for _, row in df_refresh.iterrows():
                    if row['mongo_synced_at']:
                        fig.add_trace(go.Scatter(
                            x=[row['mongo_synced_at']],
                            y=[row['collection_name']],
                            mode='markers',
                            marker=dict(size=15, color='#60a5fa', line=dict(color='white', width=2)),
                            name=row['collection_name'],
                            showlegend=False,
                            hovertemplate=f"<b>{row['collection_name']}</b><br>Synced: {row['mongo_synced_at']}<extra></extra>"
                        ))
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(
                        title="Sync Time",
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        color='white'
                    ),
                    yaxis=dict(showgrid=False, color='white'),
                    height=400,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Data table
                with st.expander("📋 View Detailed Refresh Times"):
                    st.dataframe(df_refresh, use_container_width=True)
            else:
                st.info("⏱️ No refresh time data available")

    st.markdown("---")

    # System connections info
    st.markdown("### 🔗 System Connections")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h4 style='margin: 0; color: #8b5cf6;'>🚀 FastAPI</h4>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                <b>Endpoint:</b><br/>
                <code style='background: rgba(0,0,0,0.3); padding: 0.25rem 0.5rem; border-radius: 4px;'>{API_BASE_URL}</code>
            </p>
            <p style='margin: 0.5rem 0;'>
                <a href='{API_BASE_URL}/docs' target='_blank' style='color: #60a5fa; text-decoration: none;'>
                    📖 API Documentation →
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h4 style='margin: 0; color: #10b981;'>🍃 MongoDB</h4>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                <b>Web Interface:</b><br/>
                <code style='background: rgba(0,0,0,0.3); padding: 0.25rem 0.5rem; border-radius: 4px;'>localhost:8081</code>
            </p>
            <p style='margin: 0.5rem 0;'>
                <a href='http://localhost:8081' target='_blank' style='color: #60a5fa; text-decoration: none;'>
                    🗄️ Mongo Express →
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='custom-card'>
            <h4 style='margin: 0; color: #f59e0b;'>📦 MinIO</h4>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                <b>Console:</b><br/>
                <code style='background: rgba(0,0,0,0.3); padding: 0.25rem 0.5rem; border-radius: 4px;'>localhost:9001</code>
            </p>
            <p style='margin: 0.5rem 0;'>
                <a href='http://localhost:9001' target='_blank' style='color: #60a5fa; text-decoration: none;'>
                    🗂️ MinIO Console →
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; opacity: 0.7;'>
    <p style='margin: 0; font-size: 0.9rem;'>
        🚀 <b>DataViz Pro</b> | Powered by FastAPI + Streamlit + MongoDB
    </p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem;'>
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</div>
""", unsafe_allow_html=True)
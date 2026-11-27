"""UI and BI Dashboard styling utilities for Streamlit."""
import streamlit as st


def apply_bi_theme():
    """Injects modern, executive Business Intelligence (BI) CSS styling."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc;
        }

        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }

        /* Top header banner */
        .bi-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 12px;
            padding: 20px 26px;
            color: #ffffff;
            margin-bottom: 18px;
            border: 1px solid #334155;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
        }
        .bi-banner h1 {
            color: #ffffff !important;
            font-size: 1.65rem;
            font-weight: 700;
            margin: 0 0 4px 0;
        }
        .bi-banner p {
            color: #94a3b8 !important;
            font-size: 0.9rem;
            margin: 0;
        }

        /* KPI Metric Card with Left Accent Stripe */
        .bi-metric-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px 18px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            margin-bottom: 12px;
        }
        .bi-metric-card.accent-info { border-left: 4px solid #2563eb; }
        .bi-metric-card.accent-success { border-left: 4px solid #10b981; }
        .bi-metric-card.accent-danger { border-left: 4px solid #ef4444; }
        .bi-metric-card.accent-warning { border-left: 4px solid #f59e0b; }

        .bi-metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
        }
        .bi-metric-title {
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .bi-metric-value {
            font-size: 1.65rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.15;
            margin-bottom: 6px;
        }
        .bi-metric-sub {
            font-size: 0.78rem;
            color: #64748b;
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }

        /* Badges */
        .bi-badge-success {
            background-color: #dcfce7;
            color: #166534;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
        }
        .bi-badge-danger {
            background-color: #fee2e2;
            color: #991b1b;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
        }
        .bi-badge-warning {
            background-color: #fef3c7;
            color: #92400e;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
        }
        .bi-badge-info {
            background-color: #dbeafe;
            color: #1e40af;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
        }

        /* Section containers */
        .bi-panel {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
        }

        /* Active Filter Strip */
        .bi-filter-strip {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px 14px;
            margin-bottom: 14px;
            font-size: 0.82rem;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        /* Callout notification */
        .bi-callout {
            border-left: 4px solid #2563eb;
            background-color: #eff6ff;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin: 12px 0;
            font-size: 0.88rem;
            color: #1e3a8a;
        }

        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
            color: #0f172a !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, subtext: str = "", badge_text: str = "", badge_type: str = "info"):
    """Renders an executive BI metric card with left accent stripe."""
    badge_html = f'<span class="bi-badge-{badge_type}">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
    <div class="bi-metric-card accent-{badge_type}">
        <div class="bi-metric-title">{label}</div>
        <div class="bi-metric-value">{value}</div>
        <div class="bi-metric-sub">{badge_html} <span>{subtext}</span></div>
    </div>
    """, unsafe_allow_html=True)


def render_banner(title: str, subtitle: str, badge: str = "NYC 311 Open Data"):
    """Renders an executive BI header banner."""
    st.markdown(f"""
    <div class="bi-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div>
                <span style="background: #2563eb; color: #ffffff; border-radius: 16px; font-size: 0.82rem; font-weight: 600; padding: 6px 14px; white-space: nowrap;">{badge}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_active_filter_strip(filtered_count: int, total_count: int):
    """Displays active slicer summary pills across every page."""
    yr = st.session_state.get("slicer_year", "All Years")
    langs = st.session_state.get("slicer_langs", [])
    period = st.session_state.get("slicer_period", "All Periods")
    dow = st.session_state.get("slicer_dow", "All Days")
    tier = st.session_state.get("slicer_tier", "All Calls")
    month = st.session_state.get("action_month")

    lang_lbl = ", ".join(langs[:3]) + (f" (+{len(langs)-3})" if len(langs) > 3 else "") if langs else "All 112 Languages"
    month_badge = f'<span class="bi-badge-danger">Month Action: {month}</span>' if month else ""
    st.markdown(f"""
    <div class="bi-filter-strip">
        <strong>Active Slicers:</strong>
        <span class="bi-badge-info">Year: {yr}</span>
        {month_badge}
        <span class="bi-badge-info">Languages: {lang_lbl}</span>
        <span class="bi-badge-info">Window: {period}</span>
        <span class="bi-badge-info">Day: {dow}</span>
        <span class="bi-badge-warning">Tier: {tier}</span>
        <span style="margin-left: auto; font-weight: 600; color: #0f172a;">{filtered_count:,} / {total_count:,} calls</span>
    </div>
    """, unsafe_allow_html=True)

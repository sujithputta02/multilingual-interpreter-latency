"""UI and BI Dashboard styling utilities for Streamlit."""
import streamlit as st


def apply_bi_theme():
    """Injects modern, executive Business Intelligence (BI) CSS styling."""
    st.markdown("""
    <style>
        /* Import clean modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top header banner */
        .bi-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 12px;
            padding: 24px 28px;
            color: #ffffff;
            margin-bottom: 24px;
            border: 1px solid #334155;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        .bi-banner h1 {
            color: #ffffff !important;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .bi-banner p {
            color: #94a3b8 !important;
            font-size: 0.95rem;
            margin-bottom: 0px;
        }

        /* KPI Metric Card */
        .bi-metric-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 18px 20px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            margin-bottom: 14px;
        }
        .bi-metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        }
        .bi-metric-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .bi-metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.1;
            margin-bottom: 6px;
        }
        .bi-metric-sub {
            font-size: 0.8rem;
            color: #64748b;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Badges */
        .bi-badge-success {
            background-color: #dcfce7;
            color: #166534;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .bi-badge-danger {
            background-color: #fee2e2;
            color: #991b1b;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .bi-badge-info {
            background-color: #e0f2fe;
            color: #0369a1;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Section containers */
        .bi-panel {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        }

        /* Callout notification */
        .bi-callout {
            border-left: 4px solid #3b82f6;
            background-color: #eff6ff;
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            font-size: 0.9rem;
            color: #1e3a8a;
        }
        .bi-callout strong {
            color: #1d4ed8;
        }

        /* Streamlit metric overrides */
        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
            color: #0f172a !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, subtext: str = "", badge_text: str = "", badge_type: str = "info"):
    """Renders an executive BI metric card."""
    badge_html = f'<span class="bi-badge-{badge_type}">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
    <div class="bi-metric-card">
        <div class="bi-metric-title">{label}</div>
        <div class="bi-metric-value">{value}</div>
        <div class="bi-metric-sub">{badge_html} <span>{subtext}</span></div>
    </div>
    """, unsafe_allow_html=True)


def render_banner(title: str, subtitle: str, badge: str = "NYC 311 Open Data"):
    """Renders an executive BI header banner."""
    st.markdown(f"""
    <div class="bi-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div>
                <span class="bi-badge-info" style="font-size: 0.85rem; padding: 6px 12px;">{badge}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

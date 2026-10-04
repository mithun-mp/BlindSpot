"""
BlindSpot Technical Design System & Styling Tokens.
Provides dual-theme (Dark Workstation & High-Contrast Light) theme injection,
cohesive color tokens, typography rules, accessibility guards, and responsive CSS for Streamlit.
"""
import streamlit as st
from typing import Dict, Any, Optional


DARK_THEME_TOKENS: Dict[str, str] = {
    "bg": "#0b0e14",
    "bg_dark": "#0b0e14",
    "surface_1": "#141824",
    "surface_2": "#1a2030",
    "surface_3": "#232b40",
    "border_subtle": "#1e2638",
    "border_card": "#26334d",
    "border_focus": "#38bdf8",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "accent": "#38bdf8",
    "accent_hover": "#0ea5e9",
    "accent_active": "#0284c7",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    "purple": "#a855f7",
    "teal": "#14b8a6",
}

LIGHT_THEME_TOKENS: Dict[str, str] = {
    "bg": "#f8fafc",
    "bg_dark": "#f8fafc",
    "surface_1": "#ffffff",
    "surface_2": "#f1f5f9",
    "surface_3": "#e2e8f0",
    "border_subtle": "#e2e8f0",
    "border_card": "#cbd5e1",
    "border_focus": "#0284c7",
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_muted": "#64748b",
    "accent": "#0284c7",
    "accent_hover": "#0369a1",
    "accent_active": "#075985",
    "success": "#059669",
    "warning": "#d97706",
    "error": "#dc2626",
    "info": "#2563eb",
    "purple": "#9333ea",
    "teal": "#0d9488",
}

# Retain module-level THEME_COLORS for strict backwards compatibility
THEME_COLORS: Dict[str, str] = dict(DARK_THEME_TOKENS)
THEME_COLORS["bg_light"] = LIGHT_THEME_TOKENS["bg"]


def get_workstation_css(theme: str = "dark") -> str:
    """
    Generates cohesive workstation CSS rules calibrated for the requested theme
    ('dark', 'light', or 'auto').
    """
    is_light = (theme == "light")

    # Primary token definitions based on active theme
    bg = "#f8fafc" if is_light else "#0b0e14"
    surface_1 = "#ffffff" if is_light else "#141824"
    surface_2 = "#f1f5f9" if is_light else "#1a2030"
    surface_3 = "#e2e8f0" if is_light else "#232b40"
    border = "#cbd5e1" if is_light else "#26334d"
    border_subtle = "#e2e8f0" if is_light else "#1e2638"
    text_primary = "#0f172a" if is_light else "#f1f5f9"
    text_secondary = "#475569" if is_light else "#94a3b8"
    text_muted = "#64748b" if is_light else "#64748b"
    accent = "#0284c7" if is_light else "#38bdf8"
    accent_hover = "#0369a1" if is_light else "#0ea5e9"
    accent_active = "#075985" if is_light else "#0284c7"

    btn_sec_bg = "#ffffff" if is_light else "#141824"
    btn_sec_border = "#cbd5e1" if is_light else "#334155"
    btn_sec_text = "#1e293b" if is_light else "#e2e8f0"

    input_bg = "#ffffff" if is_light else "#141824"
    input_border = "#cbd5e1" if is_light else "#26334d"

    grid_container_bg = "#ffffff" if is_light else "#0f131d"
    table_th_bg = "#f8fafc" if is_light else "#141926"
    table_hover_bg = "#f1f5f9" if is_light else "#151c2c"
    card_shadow = "0 1px 3px rgba(0, 0, 0, 0.05)" if is_light else "0 1px 3px rgba(0, 0, 0, 0.2)"
    grid_shadow = "0 4px 16px rgba(0, 0, 0, 0.06)" if is_light else "0 4px 20px rgba(0, 0, 0, 0.4)"

    sidebar_bg = "#f1f5f9" if is_light else "#080b10"
    sidebar_border = "#cbd5e1" if is_light else "#1e2638"

    return f"""<style>
/* Root CSS Variables */
:root, .stApp {{
    --bs-bg: {bg};
    --bs-bg-dark: {bg};
    --bs-surface-1: {surface_1};
    --bs-surface-2: {surface_2};
    --bs-surface-3: {surface_3};
    --bs-border: {border};
    --bs-border-subtle: {border_subtle};
    --bs-text-primary: {text_primary};
    --bs-text-secondary: {text_secondary};
    --bs-text-muted: {text_muted};
    --bs-accent: {accent};
    --bs-accent-hover: {accent_hover};
    --bs-accent-active: {accent_active};
    --bs-success: #10b981;
    --bs-warning: #f59e0b;
    --bs-error: #ef4444;
    --bs-card-shadow: {card_shadow};
    --bs-grid-shadow: {grid_shadow};
}}

@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* App Shell Background & Base Typography */
.stApp, [data-testid="stAppViewContainer"], .main {{
    background-color: {bg} !important;
    color: {text_primary} !important;
}}

html, body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: {text_primary} !important;
    background-color: {bg} !important;
}}

/* Sidebar Container */
[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {sidebar_border} !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {{
    color: {text_primary} !important;
}}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
    color: {text_muted} !important;
}}

/* Material Symbols & Streamlit Icon Typography Guard */
[data-testid*="stIcon"],
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons,
[class*="material-symbols"],
[class*="material-icons"],
.stIcon,
span[data-testid="stIconMaterial"] {{
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-feature-settings: 'liga' 1 !important;
    -webkit-font-feature-settings: 'liga' 1 !important;
    text-rendering: optimizeLegibility !important;
    -webkit-font-smoothing: antialiased !important;
    display: inline-block !important;
    line-height: 1 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    word-wrap: normal !important;
    white-space: nowrap !important;
    direction: ltr !important;
}}

/* Custom Scrollbars */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: {bg};
}}
::-webkit-scrollbar-thumb {{
    background: {surface_3};
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {accent};
}}

/* Technical Monospace Elements */
code, pre, .stCode, .terminal-text {{
    font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", Consolas, monospace !important;
}}

/* Workstation Header Styles */
.workstation-header {{
    background: {surface_1} !important;
    border: 1px solid {border} !important;
    border-radius: 6px;
    padding: 12px 18px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: {card_shadow};
}}

.workstation-header-title {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: {text_primary} !important;
    margin: 0;
}}

.workstation-header-sub {{
    font-size: 0.8rem;
    color: {text_secondary} !important;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}}

.telemetry-badge {{
    display: inline-flex;
    align-items: center;
    background: {surface_2} !important;
    border: 1px solid {border} !important;
    border-radius: 4px;
    padding: 3px 8px;
    font-size: 0.75rem;
    font-family: monospace;
    color: {text_primary} !important;
    margin-left: 6px;
}}

/* Technical Metric Cards */
.tech-card {{
    background: {surface_1} !important;
    border: 1px solid {border} !important;
    border-radius: 6px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: {card_shadow};
}}

.tech-card:hover {{
    border-color: {accent} !important;
}}

.tech-card-selected {{
    background: {surface_2} !important;
    border: 1px solid {accent} !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
}}

.tech-badge {{
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: monospace;
    display: inline-block;
}}

/* Workstation Terminal Logs Box */
.terminal-window {{
    background-color: {"#080b10" if not is_light else "#1e293b"} !important;
    border: 1px solid {"#1e2638" if not is_light else "#334155"} !important;
    border-radius: 4px;
    padding: 10px 12px;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 0.82rem;
    line-height: 1.45;
    color: #f8fafc !important;
    overflow-y: auto;
    max-height: 480px;
}}

.terminal-line {{
    margin: 2px 0;
    white-space: pre-wrap;
    word-break: break-all;
}}

/* Container spacing */
.main .block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 96% !important;
}}

/* Primary Buttons */
.stButton > button[kind="primary"] {{
    background-color: {accent} !important;
    border-color: {accent} !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    letter-spacing: 0.03em !important;
}}

.stButton > button[kind="primary"]:hover {{
    background-color: {accent_hover} !important;
    border-color: {accent_hover} !important;
}}

/* Secondary Buttons */
.stButton > button[kind="secondary"] {{
    background-color: {btn_sec_bg} !important;
    border: 1px solid {btn_sec_border} !important;
    color: {btn_sec_text} !important;
    border-radius: 4px !important;
    transition: all 0.15s ease !important;
}}

.stButton > button[kind="secondary"]:hover {{
    border-color: {accent} !important;
    color: {accent} !important;
    background-color: {surface_2} !important;
}}

/* Input fields & Selectboxes */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {{
    background-color: {input_bg} !important;
    border-color: {input_border} !important;
    color: {text_primary} !important;
    border-radius: 4px !important;
}}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 1px {accent} !important;
}}

/* Top Navigation Bars */
.top-nav-bar {{
    display: flex;
    gap: 6px;
    background: {surface_1} !important;
    border: 1px solid {border} !important;
    border-radius: 6px;
    padding: 6px 10px;
    margin-bottom: 16px;
    align-items: center;
    overflow-x: auto;
    box-shadow: {card_shadow};
}}

.top-subnav-bar {{
    display: flex;
    gap: 8px;
    background: {surface_2} !important;
    border: 1px solid {border_subtle} !important;
    border-radius: 4px;
    padding: 4px 10px;
    margin-bottom: 14px;
    align-items: center;
}}

/* Matrix Grid & Tables */
.bs-grid-container {{
    width: 100%;
    overflow-x: auto;
    border: 1px solid {border} !important;
    border-radius: 8px;
    background: {grid_container_bg} !important;
    margin: 14px 0 24px 0;
    box-shadow: {grid_shadow};
}}

.bs-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 0.83rem;
    color: {text_primary} !important;
    text-align: left;
}}

.bs-table th {{
    background: {table_th_bg} !important;
    color: {text_secondary} !important;
    font-size: 0.73rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 10px 12px;
    border-bottom: 2px solid {border} !important;
    border-right: 1px solid {border_subtle} !important;
    white-space: nowrap;
    position: sticky;
    top: 0;
    z-index: 2;
}}

.bs-table td {{
    padding: 9px 12px;
    border-bottom: 1px solid {border_subtle} !important;
    border-right: 1px solid {border_subtle} !important;
    vertical-align: middle;
}}

.bs-table tr:hover {{
    background: {table_hover_bg} !important;
}}

.bs-col-sticky {{
    position: sticky;
    left: 0;
    background: {grid_container_bg} !important;
    z-index: 1;
    border-right: 2px solid {border} !important;
}}

.bs-table tr:hover .bs-col-sticky {{
    background: {table_hover_bg} !important;
}}

/* Cell-Level Deviation Indicators */
.cell-badge {{
    display: inline-flex;
    flex-direction: column;
    width: 100%;
    padding: 6px 8px;
    border-radius: 5px;
    font-family: monospace;
    font-size: 0.76rem;
    line-height: 1.3;
    box-sizing: border-box;
    transition: all 0.15s ease;
}}

/* Match */
.cell-match {{
    background: {"#ecfdf5" if is_light else "rgba(16, 185, 129, 0.08)"} !important;
    border: 1px solid {"#a7f3d0" if is_light else "rgba(16, 185, 129, 0.35)"} !important;
    color: {"#065f46" if is_light else "#34d399"} !important;
}}
.cell-match:hover {{
    background: {"#d1fae5" if is_light else "rgba(16, 185, 129, 0.16)"} !important;
    border-color: #10b981 !important;
}}

/* Deviation */
.cell-deviation {{
    background: {"#fffbeb" if is_light else "rgba(245, 158, 11, 0.12)"} !important;
    border: 1.5px solid {"#fde68a" if is_light else "#f59e0b"} !important;
    color: {"#92400e" if is_light else "#fbbf24"} !important;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.15);
}}
.cell-deviation:hover {{
    background: {"#fef3c7" if is_light else "rgba(245, 158, 11, 0.22)"} !important;
}}

/* Failure (Blind) */
.cell-failure {{
    background: {"#fef2f2" if is_light else "rgba(239, 68, 68, 0.14)"} !important;
    border: 1.5px solid {"#fecaca" if is_light else "#ef4444"} !important;
    color: {"#991b1b" if is_light else "#f87171"} !important;
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.15);
}}
.cell-failure:hover {{
    background: {"#fee2e2" if is_light else "rgba(239, 68, 68, 0.25)"} !important;
}}

/* Misweighted (Violet / Purple) */
.cell-misweighted {{
    background: {"#faf5ff" if is_light else "rgba(168, 85, 247, 0.14)"} !important;
    border: 1.5px solid {"#d8b4fe" if is_light else "#a855f7"} !important;
    color: {"#6b21a8" if is_light else "#c084fc"} !important;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.2);
}}
.cell-misweighted:hover {{
    background: {"#f3e8ff" if is_light else "rgba(168, 85, 247, 0.25)"} !important;
}}

/* Misweighted with Expected Behavior Met (Lighter Neon Green) */
.cell-misweighted-match {{
    background: {"#f0fdf4" if is_light else "rgba(34, 197, 94, 0.16)"} !important;
    border: 1.5px solid {"#4ade80" if is_light else "#22c55e"} !important;
    color: {"#15803d" if is_light else "#4ade80"} !important;
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.25);
}}
.cell-misweighted-match:hover {{
    background: {"#dcfce7" if is_light else "rgba(34, 197, 94, 0.26)"} !important;
}}

/* Spurious (Orange) */
.cell-spurious {{
    background: {"#fff7ed" if is_light else "rgba(249, 115, 22, 0.14)"} !important;
    border: 1.5px solid {"#fdba74" if is_light else "#f97316"} !important;
    color: {"#c2410c" if is_light else "#fb923c"} !important;
    box-shadow: 0 0 10px rgba(249, 115, 22, 0.2);
}}
.cell-spurious:hover {{
    background: {"#ffedd5" if is_light else "rgba(249, 115, 22, 0.25)"} !important;
}}

/* Undetermined */
.cell-undetermined {{
    background: {"#f8fafc" if is_light else "rgba(148, 163, 184, 0.08)"} !important;
    border: 1px solid {"#cbd5e1" if is_light else "#64748b"} !important;
    color: {"#334155" if is_light else "#cbd5e1"} !important;
}}

/* Not Run */
.cell-notrun {{
    background: {"#f1f5f9" if is_light else "rgba(30, 41, 59, 0.4)"} !important;
    border: 1px dashed {"#cbd5e1" if is_light else "#475569"} !important;
    color: {text_muted} !important;
}}

/* Invalid */
.cell-invalid {{
    background: {"#faf5ff" if is_light else "rgba(168, 85, 247, 0.12)"} !important;
    border: 1.5px dashed {"#d8b4fe" if is_light else "#a855f7"} !important;
    color: {"#6b21a8" if is_light else "#c084fc"} !important;
}}

/* Status Tag Pills */
.status-pill {{
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-top: 3px;
    width: fit-content;
}}

.pill-match {{
    background: {"#d1fae5" if is_light else "#064e3b"} !important;
    color: {"#065f46" if is_light else "#6ee7b7"} !important;
    border: 1px solid {"#a7f3d0" if is_light else "transparent"} !important;
}}
.pill-dev {{
    background: {"#fef3c7" if is_light else "#78350f"} !important;
    color: {"#92400e" if is_light else "#fde68a"} !important;
    border: 1px solid {"#fde68a" if is_light else "transparent"} !important;
}}
.pill-fail {{
    background: {"#fee2e2" if is_light else "#7f1d1d"} !important;
    color: {"#991b1b" if is_light else "#fca5a5"} !important;
    border: 1px solid {"#fecaca" if is_light else "transparent"} !important;
}}
.pill-misweighted {{
    background: {"#f3e8ff" if is_light else "#581c87"} !important;
    color: {"#6b21a8" if is_light else "#e9d5ff"} !important;
    border: 1px solid {"#d8b4fe" if is_light else "rgba(168, 85, 247, 0.4)"} !important;
}}
.pill-misweighted-match {{
    background: {"#dcfce7" if is_light else "rgba(34, 197, 94, 0.22)"} !important;
    color: {"#15803d" if is_light else "#4ade80"} !important;
    border: 1px solid {"#86efac" if is_light else "rgba(74, 222, 128, 0.5)"} !important;
}}
.pill-spurious {{
    background: {"#ffedd5" if is_light else "#7c2d12"} !important;
    color: {"#9a3412" if is_light else "#fdba74"} !important;
    border: 1px solid {"#fed7aa" if is_light else "rgba(249, 115, 22, 0.4)"} !important;
}}
.pill-undet {{
    background: {"#e2e8f0" if is_light else "#1e293b"} !important;
    color: {"#334155" if is_light else "#cbd5e1"} !important;
    border: 1px solid {"#cbd5e1" if is_light else "transparent"} !important;
}}
.pill-notrun {{
    background: {"#f1f5f9" if is_light else "#0f172a"} !important;
    color: {text_muted} !important;
    border: 1px solid {"#e2e8f0" if is_light else "transparent"} !important;
}}
.pill-invalid {{
    background: {"#f3e8ff" if is_light else "#581c87"} !important;
    color: {"#6b21a8" if is_light else "#e9d5ff"} !important;
}}

/* Transition Badges */
.trans-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 6px;
    border-radius: 3px;
    background: {surface_2} !important;
    border: 1px solid {border_subtle} !important;
    font-family: monospace;
    font-size: 0.72rem;
    font-weight: 600;
    color: {accent} !important;
    white-space: nowrap;
}}

/* Model Completeness Banner */
.model-completeness-banner {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: {surface_1} !important;
    border: 1px solid {border} !important;
    border-left: 4px solid {accent} !important;
    border-radius: 6px;
    padding: 10px 16px;
    margin-bottom: 16px;
    font-family: monospace;
    font-size: 0.82rem;
    box-shadow: {card_shadow};
}}

.model-completeness-warning {{
    border-left-color: #f59e0b !important;
    background: {"#fffbeb" if is_light else "rgba(120, 53, 15, 0.15)"} !important;
}}

/* Failure Summary Metric Cards */
.failure-summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}}

.failure-metric-card {{
    background: {surface_1};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 12px 14px;
    font-family: monospace;
    box-shadow: {card_shadow};
    transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.18s ease, border-color 0.18s ease;
    position: relative;
    overflow: hidden;
}}

.failure-metric-card:hover {{
    transform: translateY(-2px);
}}

.failure-metric-card-val {{
    font-size: 1.85rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 4px 0 2px 0;
    font-family: "JetBrains Mono", Menlo, Consolas, monospace;
    letter-spacing: -0.02em;
}}

/* Failure Metric Card Specific Color Themes */
.failure-card-blind {{
    background: {"linear-gradient(135deg, rgba(239, 68, 68, 0.10) 0%, rgba(255, 255, 255, 0.95) 100%)" if is_light else "linear-gradient(135deg, rgba(239, 68, 68, 0.14) 0%, rgba(17, 22, 34, 0.95) 100%)"} !important;
    border: 1px solid {"rgba(239, 68, 68, 0.35)" if is_light else "rgba(239, 68, 68, 0.45)"} !important;
    border-left: 4px solid #ef4444 !important;
    box-shadow: 0 4px 14px -2px rgba(239, 68, 68, {"0.12" if is_light else "0.22"}) !important;
}}
.failure-card-blind:hover {{
    border-color: #ef4444 !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.32) !important;
}}
.val-blind, .failure-card-blind .failure-metric-card-val {{
    color: {"#dc2626" if is_light else "#f87171"} !important;
    text-shadow: 0 0 16px rgba(239, 68, 68, {"0.25" if is_light else "0.45"});
}}

.failure-card-spurious {{
    background: {"linear-gradient(135deg, rgba(249, 115, 22, 0.10) 0%, rgba(255, 255, 255, 0.95) 100%)" if is_light else "linear-gradient(135deg, rgba(249, 115, 22, 0.14) 0%, rgba(17, 22, 34, 0.95) 100%)"} !important;
    border: 1px solid {"rgba(249, 115, 22, 0.35)" if is_light else "rgba(249, 115, 22, 0.45)"} !important;
    border-left: 4px solid #f97316 !important;
    box-shadow: 0 4px 14px -2px rgba(249, 115, 22, {"0.12" if is_light else "0.22"}) !important;
}}
.failure-card-spurious:hover {{
    border-color: #f97316 !important;
    box-shadow: 0 6px 20px rgba(249, 115, 22, 0.32) !important;
}}
.val-spurious, .failure-card-spurious .failure-metric-card-val {{
    color: {"#ea580c" if is_light else "#fb923c"} !important;
    text-shadow: 0 0 16px rgba(249, 115, 22, {"0.25" if is_light else "0.45"});
}}

.failure-card-misweighted {{
    background: {"linear-gradient(135deg, rgba(168, 85, 247, 0.10) 0%, rgba(255, 255, 255, 0.95) 100%)" if is_light else "linear-gradient(135deg, rgba(168, 85, 247, 0.14) 0%, rgba(17, 22, 34, 0.95) 100%)"} !important;
    border: 1px solid {"rgba(168, 85, 247, 0.35)" if is_light else "rgba(168, 85, 247, 0.45)"} !important;
    border-left: 4px solid #a855f7 !important;
    box-shadow: 0 4px 14px -2px rgba(168, 85, 247, {"0.12" if is_light else "0.22"}) !important;
}}
.failure-card-misweighted:hover {{
    border-color: #a855f7 !important;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.32) !important;
}}
.val-misweighted, .failure-card-misweighted .failure-metric-card-val {{
    color: {"#9333ea" if is_light else "#c084fc"} !important;
    text-shadow: 0 0 16px rgba(168, 85, 247, {"0.25" if is_light else "0.45"});
}}

.failure-card-undetermined {{
    background: {"linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(255, 255, 255, 0.95) 100%)" if is_light else "linear-gradient(135deg, rgba(56, 189, 248, 0.10) 0%, rgba(17, 22, 34, 0.95) 100%)"} !important;
    border: 1px solid {"rgba(56, 189, 248, 0.30)" if is_light else "rgba(56, 189, 248, 0.40)"} !important;
    border-left: 4px solid #38bdf8 !important;
    box-shadow: 0 4px 14px -2px rgba(56, 189, 248, {"0.10" if is_light else "0.18"}) !important;
}}
.failure-card-undetermined:hover {{
    border-color: #38bdf8 !important;
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.28) !important;
}}
.val-undetermined, .failure-card-undetermined .failure-metric-card-val {{
    color: {"#0284c7" if is_light else "#38bdf8"} !important;
    text-shadow: 0 0 16px rgba(56, 189, 248, {"0.2" if is_light else "0.4"});
}}

.failure-card-total {{
    background: {"linear-gradient(135deg, rgba(244, 63, 94, 0.08) 0%, rgba(255, 255, 255, 0.95) 100%)" if is_light else "linear-gradient(135deg, rgba(244, 63, 94, 0.12) 0%, rgba(17, 22, 34, 0.95) 100%)"} !important;
    border: 1px solid {"rgba(244, 63, 94, 0.35)" if is_light else "rgba(244, 63, 94, 0.45)"} !important;
    border-left: 4px solid #f43f5e !important;
    box-shadow: 0 4px 14px -2px rgba(244, 63, 94, {"0.12" if is_light else "0.22"}) !important;
}}
.failure-card-total:hover {{
    border-color: #f43f5e !important;
    box-shadow: 0 6px 20px rgba(244, 63, 94, 0.32) !important;
}}
.val-total, .failure-card-total .failure-metric-card-val {{
    color: {"#e11d48" if is_light else "#fb7185"} !important;
    text-shadow: 0 0 16px rgba(251, 113, 133, {"0.2" if is_light else "0.4"});
}}

/* ==============================================================
   LEGACY SURFACE & TEXT REMAPPING FOR COMPLETE LIGHT MODE HARMONY
   ============================================================== */
{"\"\"\"" if not is_light else """
/* Re-map hardcoded dark backgrounds to crisp light cards in light mode */
div[style*="background:#141824"],
div[style*="background: #141824"],
div[style*="background:#0f172a"],
div[style*="background: #0f172a"],
div[style*="background:#0f131d"],
div[style*="background: #0f131d"],
div[style*="background:#111622"],
div[style*="background: #111622"],
div[style*="background:#1a2030"],
div[style*="background: #1a2030"],
div[style*="background:#0b0e14"],
div[style*="background: #0b0e14"] {
    background: #ffffff !important;
    border-color: #cbd5e1 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

/* Sub-card backgrounds */
div[style*="background:#0b0f19"],
div[style*="background: #0b0f19"],
div[style*="background:#080b10"],
div[style*="background: #080b10"],
div[style*="background:#1e293b"],
div[style*="background: #1e293b"] {
    background: #f1f5f9 !important;
    border-color: #e2e8f0 !important;
}

/* Re-map hardcoded light text to dark text in light mode */
span[style*="color:#f1f5f9"],
span[style*="color: #f1f5f9"],
span[style*="color:#ffffff"],
span[style*="color: #ffffff"],
span[style*="color:#e2e8f0"],
span[style*="color: #e2e8f0"],
span[style*="color:#cbd5e1"],
span[style*="color: #cbd5e1"],
div[style*="color:#f1f5f9"],
div[style*="color: #f1f5f9"],
div[style*="color:#ffffff"],
div[style*="color: #ffffff"],
div[style*="color:#e2e8f0"],
div[style*="color: #e2e8f0"],
div[style*="color:#cbd5e1"],
div[style*="color: #cbd5e1"] {
    color: #0f172a !important;
}

/* Muted secondary text */
span[style*="color:#94a3b8"],
span[style*="color: #94a3b8"],
div[style*="color:#94a3b8"],
div[style*="color: #94a3b8"] {
    color: #475569 !important;
}

/* Cyan accent adjustment for light mode contrast */
span[style*="color:#38bdf8"],
span[style*="color: #38bdf8"],
div[style*="color:#38bdf8"],
div[style*="color: #38bdf8"] {
    color: #0284c7 !important;
}

/* Code blocks */
code, pre, .stCode {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border-color: #cbd5e1 !important;
}

/* Streamlit widget labels */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* Streamlit expander */
[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border-color: #cbd5e1 !important;
}

/* Streamlit metric */
[data-testid="stMetricValue"] {
    color: #0f172a !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
}
"""}
</style>
"""


# Static default for direct imports
WORKSTATION_CSS: str = get_workstation_css("dark")


def inject_workstation_theme(theme: Optional[str] = None) -> None:
    """
    Injects workstation CSS tokens into Streamlit document.
    Supports 'dark', 'light', and 'auto' modes with persistent session synchronization.
    """
    if theme is None:
        theme = st.session_state.get("ui_theme", "dark")

    css = get_workstation_css(theme)
    st.markdown(css, unsafe_allow_html=True)

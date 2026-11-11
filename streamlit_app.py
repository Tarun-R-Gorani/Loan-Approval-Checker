import os

import requests
import streamlit as st


st.set_page_config(
    page_title="Lendwise | Loan insights",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #17241f;
        --muted: #78827d;
        --green: #237b5b;
        --mint: #e6f4ec;
        --line: #e8ece8;
        --paper: #f7f8f5;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp {
        background:
            radial-gradient(ellipse at 86% 0%, rgba(221, 241, 228, .55), transparent 34%),
            var(--paper);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"], footer { visibility: hidden; }
    .block-container { max-width: 1240px; padding-top: 2rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] {
        background: #f0f3ef;
        border-right: 1px solid #e4e9e4;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }

    .brand {
        display: flex; align-items: center; gap: 11px;
        color: #23332c; font: 800 17px 'Manrope', sans-serif;
        letter-spacing: -.5px; margin: 0 0 2.4rem;
    }
    .brand-mark {
        display: grid; place-items: center; width: 35px; height: 35px;
        border-radius: 12px; color: white; font-size: 19px;
        background: linear-gradient(145deg, #338b68, #1d654a);
        box-shadow: 0 5px 13px rgba(35, 123, 91, .2);
    }
    .eyebrow {
        color: #328263; font-size: 11px; font-weight: 700;
        letter-spacing: 1.6px; text-transform: uppercase;
    }
    .hero-title {
        color: #1b2b24; font: 800 clamp(34px, 4vw, 49px)/1.1 'Manrope', sans-serif;
        letter-spacing: -2.4px; margin: 10px 0 12px;
    }
    .hero-copy { color: #78827d; font-size: 15px; max-width: 610px; line-height: 1.7; }
    .hero-pill {
        display: inline-flex; align-items: center; gap: 8px;
        border: 1px solid #dcebe1; border-radius: 999px;
        color: #39765c; background: rgba(255,255,255,.72);
        padding: 8px 13px; font-size: 12px; font-weight: 600;
    }
    .hero-pill span { width: 7px; height: 7px; border-radius: 50%; background: #56a87e; }
    .section-heading {
        color: #24352d; font: 700 19px 'Manrope', sans-serif;
        letter-spacing: -.5px; margin: 0;
    }
    .section-copy { color: #87918b; font-size: 13px; margin-top: 5px; }
    .panel {
        background: rgba(255,255,255,.86); border: 1px solid #e7ece7;
        border-radius: 20px; padding: 25px 27px;
        box-shadow: 0 12px 35px rgba(27, 46, 36, .045);
    }
    .result-panel {
        min-height: 255px; background: linear-gradient(145deg, #fff, #f8fbf8);
        border: 1px solid #e5ece6; border-radius: 20px;
        padding: 26px; box-shadow: 0 12px 35px rgba(27, 46, 36, .045);
    }
    .result-number {
        font: 800 48px/1 'Manrope', sans-serif;
        letter-spacing: -2px; color: #237b5b; margin: 22px 0 8px;
    }
    .result-caption { color: #7d8981; font-size: 13px; line-height: 1.6; }
    .empty-icon {
        display: grid; place-items: center; width: 50px; height: 50px;
        border-radius: 16px; background: #eaf4ed; color: #34825f;
        font-size: 23px; margin: 27px 0 15px;
    }
    .empty-title { color: #304139; font: 700 16px 'Manrope', sans-serif; }
    .empty-copy { color: #87918b; font-size: 13px; line-height: 1.6; margin-top: 7px; }
    div[data-testid="stForm"] {
        background: rgba(255,255,255,.86); border: 1px solid #e7ece7;
        border-radius: 20px; padding: 24px 26px 18px;
        box-shadow: 0 12px 35px rgba(27, 46, 36, .045);
    }
    div[data-testid="stForm"] label p { color: #42534a; font-weight: 600; font-size: 13px; }
    div[data-testid="stForm"] input, div[data-testid="stForm"] [data-baseweb="select"] > div {
        border-radius: 10px;
    }
    .stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: #237b5b; color: white; border: 1px solid #237b5b;
        border-radius: 11px; min-height: 47px; font-weight: 700;
        transition: all .2s ease;
    }
    div[data-testid="stFormSubmitButton"] > button { width: 100%; margin-top: 10px; }
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        background: #195f45; border-color: #195f45; color: white;
        box-shadow: 0 6px 16px rgba(35, 123, 91, .2);
    }
    .footnote { color: #929b95; font-size: 11px; line-height: 1.6; margin-top: 13px; }
    hr { border-color: #e5eae5; }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_root(value: str) -> str:
    return value.strip().rstrip("/")


with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">✳</span>lendwise<span '
        'style="color:#8e9b93;font-size:11px;font-weight:600;letter-spacing:1px;'
        'margin-left:2px">STUDIO</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)
    st.markdown("### Loan assessment")
    st.caption("A clean, connected interface for your model API.")
    st.divider()
    st.markdown("**API connection**")
    endpoint = st.text_input(
        "Flask API URL",
        value=os.environ.get("LOAN_API_URL", "http://127.0.0.1:5000"),
        help="Base URL of the running Flask service.",
    )
    if st.button("Check API connection", use_container_width=True):
        try:
            response = requests.get(f"{api_root(endpoint)}/health", timeout=4)
            response.raise_for_status()
            st.success("Flask API is connected.")
        except requests.RequestException as error:
            st.error(f"Could not reach the Flask API: {error}")
    st.divider()
    st.markdown("**About this demo**")
    st.caption(
        "A synthetic model demonstration. It is not a credit assessment, "
        "financial recommendation, or lending decision."
    )
    st.markdown(
        '<div class="footnote">MODEL · LOGISTIC REGRESSION<br>MODE · DEMO ONLY</div>',
        unsafe_allow_html=True,
    )


st.markdown(
    '<div class="hero-pill"><span></span> YOUR MODEL, BEAUTIFULLY CONNECTED</div>'
    '<div class="hero-title">A clearer view of<br>loan applications.</div>'
    '<div class="hero-copy">Explore a sample application and see how your '
    'loan-approval model responds — all in one thoughtful workspace.</div>',
    unsafe_allow_html=True,
)
st.write("")

form_column, result_column = st.columns([1.13, 0.87], gap="large")

with form_column:
    st.markdown(
        '<div style="padding:0 2px 14px"><div class="section-heading">'
        'Applicant profile</div><div class="section-copy">'
        'Enter the details below to request a model prediction.</div></div>',
        unsafe_allow_html=True,
    )
    with st.form("loan_application"):
        income_column, loan_column = st.columns(2, gap="medium")
        with income_column:
            annual_income = st.number_input(
                "Annual income · $", min_value=0, max_value=1_000_000,
                value=75_000, step=1_000,
            )
        with loan_column:
            loan_amount = st.number_input(
                "Requested loan · $", min_value=1, max_value=500_000,
                value=20_000, step=1_000,
            )

        credit_column, employment_column = st.columns(2, gap="medium")
        with credit_column:
            credit_score = st.slider(
                "Credit score", min_value=300, max_value=850, value=720,
            )
        with employment_column:
            employment_years = st.number_input(
                "Employment history · years", min_value=0, max_value=60,
                value=8, step=1,
            )

        debt_to_income = st.slider(
            "Debt-to-income ratio",
            min_value=0,
            max_value=100,
            value=25,
            format="%d%%",
            help="Enter the share of monthly income committed to debt.",
        )
        submitted = st.form_submit_button("✨  Generate demo assessment")

if submitted:
    payload = {
        "features": {
            "annual_income": annual_income,
            "loan_amount": loan_amount,
            "credit_score": credit_score,
            "employment_years": employment_years,
            "debt_to_income": debt_to_income / 100,
        }
    }
    try:
        response = requests.post(
            f"{api_root(endpoint)}/predict",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict):
            st.session_state["loan_error"] = (
                "The API returned an unexpected response format."
            )
            st.session_state.pop("loan_result", None)
        else:
            st.session_state["loan_result"] = result
            st.session_state.pop("loan_error", None)
    except requests.RequestException as error:
        st.session_state["loan_error"] = (
            f"Unable to get a prediction from the Flask API: {error}. "
            "Check that the API is running and the URL is correct."
        )
        st.session_state.pop("loan_result", None)
    except ValueError as error:
        st.session_state["loan_error"] = f"The API returned invalid JSON: {error}."
        st.session_state.pop("loan_result", None)

with result_column:
    st.markdown(
        '<div style="padding:0 2px 14px"><div class="section-heading">'
        'Model response</div><div class="section-copy">'
        'Your result appears here after assessment.</div></div>',
        unsafe_allow_html=True,
    )
    error_message = st.session_state.get("loan_error")
    result = st.session_state.get("loan_result")
    if error_message:
        st.error(error_message)
    elif result:
        approved = result.get("decision") == "demo_approved"
        probability = result.get("approval_probability")
        if not isinstance(probability, (int, float)) or not 0 <= probability <= 1:
            st.error("The API returned an invalid approval probability.")
        else:
            label = "Demo approved" if approved else "Demo not approved"
            color = "#237b5b" if approved else "#b15e48"
            st.markdown(
                f'<div class="result-panel"><div class="eyebrow">PREDICTION '
                f'COMPLETE</div><div class="result-number" '
                f'style="color:{color}">{probability:.0%}</div>'
                f'<div class="result-caption">Illustrative approval '
                f'probability</div><div style="margin-top:22px;padding-top:16px;'
                f'border-top:1px solid #e8ece8;color:{color};font-weight:700">'
                f'{label}</div></div>',
                unsafe_allow_html=True,
            )
            st.progress(float(probability))
            st.caption(
                "This is a synthetic-model output for demonstration only. "
                "It is not a real-world credit decision."
            )
    else:
        st.markdown(
            '<div class="result-panel"><div class="eyebrow">READY WHEN YOU ARE'
            '</div><div class="empty-icon">↗</div><div class="empty-title">'
            'Your insight starts here</div><div class="empty-copy">Complete '
            'the applicant profile and run an assessment to see the model\'s '
            'demo response.</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.info(
    "Demo only. This model uses synthetic training data and is not validated "
    "for real lending, credit eligibility, or financial decisions."
)

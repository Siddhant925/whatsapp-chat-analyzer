import streamlit as st
import pandas as pd
import preprocess, helper
import matplotlib.pyplot as plt
from collections import Counter

# ---------- Page setup ----------
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
)

# ---------- Palette ----------
GREEN_DARK = "#075E54"
GREEN = "#128C7E"
GREEN_LIGHT = "#25D366"
INK = "#1B2B27"
MUTED = "#6B7B76"
PAGE_BG = "#F4F7F6"

# ---------- Global styling ----------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {INK};
    }}
    .stApp {{ background: {PAGE_BG}; }}
    .block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{ background: {GREEN_DARK}; }}
    section[data-testid="stSidebar"] * {{ color: #FFFFFF; }}
    /* Selectbox: white box, dark text, regardless of light/dark theme */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: #FFFFFF;
        border-radius: 10px;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    section[data-testid="stSidebar"] [data-baseweb="select"] input {{
        color: {INK} !important;
        -webkit-text-fill-color: {INK} !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] svg {{ fill: {INK}; }}

    /* Dropdown list (rendered outside the sidebar) */
    div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li {{
        background: #FFFFFF;
        color: {INK};
    }}
    div[data-baseweb="popover"] li:hover {{ background: #E7F5EF; }}

    /* File uploader */
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
        background: rgba(255,255,255,0.08);
        border: 1px dashed rgba(255,255,255,0.4);
        border-radius: 10px;
    }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {{
        background: #FFFFFF;
        border: none;
    }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button * {{
        color: {GREEN_DARK} !important;
    }}

    /* Buttons */
    section[data-testid="stSidebar"] .stButton > button {{
        background: {GREEN_LIGHT};
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        width: 100%;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: #3EE07C;
    }}
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button * {{
        color: {GREEN_DARK} !important;
        font-weight: 600;
    }}

    /* Page header */
    .page-title {{ font-size: 2rem; font-weight: 700; margin: 0; color: {GREEN_DARK}; }}
    .page-sub {{ color: {MUTED}; margin: 0.25rem 0 1.5rem 0; }}

    /* Stat cards */
    .stat-card {{
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        border-left: 5px solid {GREEN_LIGHT};
        box-shadow: 0 1px 3px rgba(7, 94, 84, 0.10);
    }}
    .stat-label {{ font-size: 0.85rem; color: {MUTED}; margin-bottom: 0.2rem; }}
    .stat-value {{ font-size: 2rem; font-weight: 700; color: {GREEN_DARK}; line-height: 1.2; }}

    /* Section headings */
    .section-title {{
        font-size: 1.25rem; font-weight: 600; color: {GREEN_DARK};
        margin: 2rem 0 0.75rem 0;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{ font-weight: 500; }}
    button[data-baseweb="tab"][aria-selected="true"] {{ color: {GREEN}; }}
    div[data-baseweb="tab-highlight"] {{ background-color: {GREEN}; }}

    /* Emoji tiles */
    .emoji-tile {{
        background: #FFFFFF; border-radius: 12px; padding: 0.6rem 0.4rem;
        text-align: center; box-shadow: 0 1px 3px rgba(7, 94, 84, 0.10);
        margin-bottom: 0.6rem;
    }}
    .emoji-tile .e {{ font-size: 1.8rem; }}
    .emoji-tile .n {{ font-size: 0.85rem; color: {MUTED}; font-weight: 500; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Chart styling ----------
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.edgecolor": "#D5DDDA",
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
})


def stat_card(label, value):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# ---------- Sidebar ----------
st.sidebar.title("💬 Chat Analyzer")
st.sidebar.caption("Upload an exported WhatsApp chat (.txt) to get started.")
uploaded_file = st.sidebar.file_uploader("Chat file", type=["txt"])

# ---------- Main ----------
st.markdown('<p class="page-title">WhatsApp Chat Analyzer</p>', unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown(
        '<p class="page-sub">Upload a chat export from the sidebar to see who talks the most, '
        "which words and emojis come up, and more.</p>",
        unsafe_allow_html=True,
    )
    st.info("In WhatsApp, open a chat, tap ⋮ → More → Export chat → Without media.")
else:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocess.preprocess(data)

    st.markdown(
        f'<p class="page-sub">{uploaded_file.name} · {df.shape[0]:,} rows loaded</p>',
        unsafe_allow_html=True,
    )

    with st.expander("View chat data"):
        st.dataframe(df, hide_index=True, use_container_width=True)

    # Fetch unique users
    user_list = df["user"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show analysis"):
        # ----- Top stats -----
        num_messages, words, media_shared, links = helper.fetch_stats(selected_user, df)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            stat_card("Total messages", num_messages)
        with c2:
            stat_card("Total words", len(words))
        with c3:
            stat_card("Media shared", media_shared)
        with c4:
            stat_card("Links shared", len(links))

        # ----- Busiest users (group level) -----
        if selected_user == "Overall":
            section("Most active users")
            x = helper.fetch_most_busy_users(df)

            col1, col2 = st.columns([3, 2])
            with col1:
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.bar(x.index, x.values, color=GREEN, width=0.6)
                ax.set_xlabel("Users")
                ax.set_ylabel("Message count")
                plt.xticks(rotation=60, ha="right")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                pct = (
                    round(100 * (df["user"].value_counts() / df.shape[0]), 2)
                    .reset_index()
                    .rename(columns={"count": "percentage"})
                )
                st.dataframe(
                    pct,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "percentage": st.column_config.ProgressColumn(
                            "Share of messages",
                            format="%.2f%%",
                            min_value=0,
                            max_value=float(pct["percentage"].max()),
                        )
                    },
                )

        # ----- Words and emojis in tabs -----
        tab_wc, tab_words, tab_emoji = st.tabs(["Word cloud", "Common words", "Emojis"])

        with tab_wc:
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)
            plt.close(fig)

        with tab_words:
            mcw = helper.most_common_words(selected_user, df)
            most_common_words = pd.DataFrame(Counter(mcw).most_common(20))
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(most_common_words[0], most_common_words[1], color=GREEN)
            ax.invert_yaxis()  # most frequent word on top
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Words")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with tab_emoji:
            emojis = helper.emoji_analysis(selected_user, df)
            emoji_df = pd.DataFrame(
                Counter(emojis).most_common(), columns=["Emoji", "Frequency"]
            )

            if emoji_df.empty:
                st.info("No emojis found for this selection.")
            else:
                col1, col2 = st.columns([3, 2])

                with col1:
                    top = emoji_df.head(15)
                    cols = st.columns(5)
                    for i, row in enumerate(top.itertuples(index=False)):
                        with cols[i % 5]:
                            st.markdown(
                                f"""
                                <div class="emoji-tile">
                                    <div class="e">{row.Emoji}</div>
                                    <div class="n">{row.Frequency}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                with col2:
                    st.dataframe(emoji_df, hide_index=True, use_container_width=True)
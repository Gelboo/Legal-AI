import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from arabic_support import support_arabic_text

st.set_page_config(layout="wide")
support_arabic_text(all=True)

st.markdown(
    """
    <style>

        /* Move sidebar to the Right */
        [data-testid="stSidebar"] {
            order: 1;
        }

        /* Move collapse button to the right side */
        [data-testid="stExpandSidebarButton"] {
            position: fixed;
            right: 0;
            left: auto !important;
        }

        /* Hide sidebar content when collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] {
            display: none;
        }

        /* Flip collapsed control arrow too */
        /* Not working */
        [data-testid="stExpandSidebarButton"] svg {
            transform: scaleX(-1);
        }

        /* Move scrollbar to the left side of the sidebar */
        [data-testid="stSidebar"] > div:first-child {
            direction: rtl;
        }

        /* Move the resize handle from right to left */
        [data-testid="stSidebar"] > div:last-child {
            right: auto !important;
            left: -6px !important;
        }

        /* Move the resize handle visual bar too */
        [data-testid="stSidebar"] > div:last-child > div {
            right: auto !important;
            left: 0 !important;
        }

        /* Fix slider direction inside sidebar */
        [data-testid="stSidebar"] [data-testid="stSlider"] {
            direction: ltr;
        }

        /* Slider track - filled portion */
        [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"],
        [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
            background-color: purple !important;
            border-color: purple !important;
        }

        /* Slider thumb value - adapts to light/dark theme */
        [data-testid="stSliderThumbValue"] {
            color: #7C3AED !important;                /* purple text - works on both */
        }

        /* Dark mode override */
        [data-theme="dark"] [data-testid="stSliderThumbValue"]{
                color: red !important;            /* lighter purple for dark bg */
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.image(image="cst_legal_logo.svg", caption="نظام القضايا الالكتروني")
    st.divider()
    st.markdown("""<h3 style="text-align: center;"> الفلاتر </h3>""", unsafe_allow_html=True)

    st.multiselect(label="اسم المخالف", placeholder="اختر", options=["STC", "زين", "موبيلي", "التنفيذ المعتمد"])
    st.multiselect(label="رقم القرار", placeholder="اختر رقم القرار", options=["451141261", "18208", "14114", "14114"])
    st.multiselect(label="رقم القضية", placeholder="اختر", options=["STC", "زين", "موبيلي", "التنفيذ المعتمد"])
    st.multiselect(label="رقم الدائره", placeholder="اختر", options=["STC", "زين", "موبيلي", "التنفيذ المعتمد"])

    st.write("درجه التقاضي")
    st.checkbox(label="ابتدائى")
    st.checkbox(label="استئناف")
    st.checkbox(label="عليا")


    penalty = st.slider(
        "مبلغ الغرامه",
        min_value=0,
        max_value=1000000,
        value=(0, 1000000),
        step=1000,
        format="%d ريال"
    )

    case_date = st.slider(
        "تاريخ القضية",
        min_value=datetime(2025,1,1),
        max_value=datetime(2026,1,1),
        value=(datetime(2025,1,1), datetime(2026,1,1)),
        step=timedelta(1),
    )



    with st.expander("فلاتر اخري"):
        st.multiselect(label="صفة المخالف", placeholder="اختر", options=["مقدم خدمة", "اخرين"])

        st.multiselect(label="شكل الحكم", placeholder="اختر", options=["مستلمه", ""])
        st.multiselect(label="نوع الحكم", placeholder="اختر", options=["ضد القرار", "لصالح القرار"])




data = {
    "التوصيات مابعد الغاء القرار": ['', '', '', ''],
    "سبب الالغاء": ['', '', '', ''],
    "تاريخ صدور الحكم": ['', '', '', ''],
    "تاريخه": ["24/10/1446", "12/8/1446", "12/9/1446", "8/1/1447"],
    "شكل الحكم": ["مستلمه", "مستلمه", "مستلمه", "مستلمه"],
    "منطوق": ["رفض الدعوي", "عدم قبول الدعوي", "نقض الحكم وإعادة القضيه الي محكمة الاستئناف", "رفض الدعوي"],
    "نوع الحكم": ["لصالح القرار", "ضد القرار", "لصالح القرار", "لصالح القرار"],
    "مبلغ الغرامه": [100000, 10000, 5000, 5000],
    "درجه التقاضي": ["استئناف", "استئناف", "عليا", "استئناف"],
    "نوع المخالفه": ["اي عمل اخر يخالف احكام النظام", "قطع كيبل", "قطع كيبل", "قطع كيبل"],
    "رقم الدائره": ["استئناف 5", "استئناف 5", "عليا 1", "استئناف مكه 10"],
    "رقم القضيه": [["11225/46", "326/46"], ["8100/46", "2304/45"], ["12975/45", "8294/45", "8137/45"], ["8294/45", "8137/45"]],
    "الشهر": ["ابريل", "فبراير", "مارس", "يوليو"],
    "الاسبوع": ["(24-20) 4/25", "(13-9) 2/25", "(13-9) 3/25", "(3-29) 7/25"],
    "صفه المخالف": ["مقدم خدمه", "اخرين", "اخرين", "اخرين"],
    "رقم القرار": ["451141261", "18208", "14114", "14114"],
    "اسم المخالف": ["STC", "رويفد الصاعدي", "البناء الفاخر", "البناء الفاخر"],
}

df = pd.DataFrame(data)

#### For the sake of more records
df = pd.concat([df, df, df, df, df, df, df, df, df, df, df, df, df, df, df, df, df], ignore_index=True)

st.markdown(
    """
        <h1> نظام القضايا الالكتروني الذكي</h1>
    """,
    unsafe_allow_html=True
)

edited_df = st.data_editor(
    df,
    column_config={
        "رقم القضيه": st.column_config.ListColumn(
            "رقم القضيه",
            help="The sales volume in the last 6 months",
            width="medium",
            disabled=True
        )
    },
    num_rows="fixed",
    disabled=["ID"],
    hide_index=True,
    height="content"
)
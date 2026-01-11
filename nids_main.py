import streamlit as st
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

import seaborn as sns
import matplotlib.pyplot as plt


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI-Based Network Intrusion Detection System", layout="wide"
)

st.title("AI-Based Network Intrusion Detection System (NIDS)")
st.markdown("""
This project implements a **Machine Learning–based Network Intrusion Detection System**
using the **CIC-IDS2017 real-world dataset**.

**Algorithm Used:** Random Forest  
**Goal:** Detect DDoS and malicious traffic
""")


# LOAD REAL CIC-IDS2017 DATASET
@st.cache_data
def load_real_data():
    # Load CSV file
    df = pd.read_csv("Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

    # FIX: Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Drop non-useful columns
    df.drop(
        columns=["Flow ID", "Source IP", "Destination IP", "Timestamp"],
        errors="ignore",
        inplace=True,
    )

    # Replace infinite values & drop missing rows
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    # Convert labels: BENIGN → 0, ATTACK → 1
    if "Label" not in df.columns:
        raise ValueError("Label column not found in dataset")

    df["Label"] = df["Label"].apply(lambda x: 0 if str(x).upper() == "BENIGN" else 1)

    return df


df = load_real_data()


st.sidebar.header("Control Panel")
train_size = st.sidebar.slider("Training Data Size (%)", 60, 90, 80)
n_trees = st.sidebar.slider("Number of Trees (Random Forest)", 50, 200, 100)


features = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Packet Length Mean",
    "Flow Bytes/s",
    "Flow Packets/s",
]

X = df[features]
y = df["Label"]

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=(100 - train_size) / 100, random_state=42, stratify=y
)


st.divider()
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Model Training")

    if st.button("Train Model"):
        model = RandomForestClassifier(n_estimators=n_trees, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        st.session_state["model"] = model
        st.session_state["scaler"] = scaler

        st.success("Model trained successfully using CIC-IDS2017 dataset!")

with col2:
    st.subheader("Model Performance")

    if "model" in st.session_state:
        model = st.session_state["model"]
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)

        m1, m2, m3 = st.columns(3)
        m1.metric("Accuracy", f"{acc * 100:.2f}%")
        m2.metric("Total Records", len(df))
        m3.metric("Detected Attacks", int(y_pred.sum()))

        st.markdown("### Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)

        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Reds", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        st.pyplot(fig)

    else:
        st.warning("Please train the model to view performance metrics.")


st.divider()
st.subheader("Real-Time Network Traffic Analysis")

st.markdown("Enter live network flow parameters to test traffic behavior.")

c1, c2, c3, c4 = st.columns(4)
dest_port = c1.number_input("Destination Port", 1, 65535, 80)
flow_duration = c2.number_input("Flow Duration", 1, 100000, 500)
fwd_packets = c3.number_input("Total Forward Packets", 1, 500, 50)
bwd_packets = c4.number_input("Total Backward Packets", 1, 500, 20)

c5, c6, c7 = st.columns(3)
pkt_len_mean = c5.number_input("Packet Length Mean", 1, 1500, 600)
flow_bytes = c6.number_input("Flow Bytes/s", 0.0, 1e7, 2000.0)
flow_pkts = c7.number_input("Flow Packets/s", 0.0, 1e6, 100.0)

if st.button("Analyze Traffic"):
    if "model" in st.session_state:
        model = st.session_state["model"]
        scaler = st.session_state["scaler"]

        input_data = np.array(
            [
                [
                    dest_port,
                    flow_duration,
                    fwd_packets,
                    bwd_packets,
                    pkt_len_mean,
                    flow_bytes,
                    flow_pkts,
                ]
            ]
        )

        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)

        if prediction[0] == 1:
            st.error("MALICIOUS TRAFFIC DETECTED (DDoS Attack)")
        else:
            st.success("BENIGN TRAFFIC (Normal)")

    else:
        st.warning("Please train the model first.")

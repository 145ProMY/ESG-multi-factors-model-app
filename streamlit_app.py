import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ESG Credit Score Model",layout="wide")
st.title("ESG Multi-Factor Credit Risk Scoring Model")

# Sidebar inputs
st.sidebar.header("Parameter Settings")

#Credit score weight
w1=st.sidebar.slider("Weight of Financial Score (w1)",0.0,1.0,0.7,0.01)
w2=1-w1
st.sidebar.markdown(f"Weight of ESG Score (w2): **{w2:.2f}**")

#ESG weight
st.sidebar.markdown("---")
st.sidebar.subheader("ESG Weight Settings")
alpha=st.sidebar.number_input("E - Environmental (α)", 0.0, 1.0, 0.33, 0.01)
beta=st.sidebar.number_input("S - Social (β)", 0.0, 1.0, 0.33, 0.01)
gamma =st.sidebar.number_input("G - Governance (γ)", 0.0, 1.0, 0.34, 0.01)

if not np.isclose(alpha+beta+gamma, 1.0):
    st.sidebar.error(f"⚠️ The sum of α+β+γ must be 1 (currently {alpha+beta+gamma:.2f})")

st.sidebar.markdown("---")

#Input scores
st.subheader("Input Company Scores")
col1,col2,col3,col4 = st.columns(4)
with col1:
    financial_score = st.number_input("Financial Score",0.0,100.0,80.0)
with col2:
    E_score = st.number_input("E Score",0.0,100.0,80.0)
with col3:
    S_score = st.number_input("S Score",0.0,100.0,80.0)
with col4:
    G_score = st.number_input("G Score",0.0,100.0,80.0)

# Esg Multi Factors Model
esg_score=alpha*E_score+beta*S_score+gamma*G_score
credit_score= w1 *financial_score+w2*esg_score

# Rating classification
def classify(score):
    if score >= 90:
        return "AAA"
    elif score >= 80:
        return "AA"
    elif score >= 70:
        return "A"
    elif score >= 60:
        return "BBB"
    elif score >= 50:
        return "BB"
    elif score >= 40:
        return "B"
    else:
        return "CCC or below"

rating = classify(credit_score)

# Output result
st.markdown("---")
st.subheader("Credit Score Result")
col5, col6 = st.columns(2)
col5.metric("Final Credit Score", f"{credit_score:.2f}", help="Based on weights and input scores")
col6.metric("Credit Rating (S&P Style)", rating)

# Heatmap Visualization
st.markdown("---")
st.subheader("ESG vs Financial Score Sensitivity Heatmap")
heatmap_param=st.selectbox("Choose ESG dimension for Heatmap",["E Score","S Score","G Score", "Same as ESG Weight"])
E_range=np.linspace(0,100,20)
F_range=np.linspace(0,100,20)
Z=np.zeros((len(E_range), len(F_range)))
y_label = []

for i,y in enumerate(E_range):
    for j,F in enumerate(F_range):
        if heatmap_param == "E Score":
            E=y
            S,G=S_score,G_score
        elif heatmap_param=="S Score":
            S=y
            E,G=E_score,G_score
        elif heatmap_param=="G Score":
            G=y
            E,S=E_score,S_score
        else:
            E=S=G=y

        esg=alpha*E+beta*S+gamma*G
        Z[i,j]=w1*F+w2*esg

    y_label.append(f"{int(y)}")

fig=px.imshow(Z,
                x=[f"{int(f)}" for f in F_range],
                y=y_label,
                labels=dict(x="Financial Score", y=heatmap_param, color="Credit Score"),
                aspect="auto",
                color_continuous_scale="RdYlGn")

st.plotly_chart(fig, use_container_width=True)

# Radar chart for ESG
st.markdown("---")
st.subheader("ESG Radar Chart")
esg_factors=["Environmental","Social","Governance"]
esg_scores=[E_score,S_score,G_score]

radar_fig = go.Figure()
radar_fig.add_trace(go.Scatterpolar(
    r=esg_scores,
    theta=esg_factors,
    fill='toself',
    name='ESG Score'))

radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),
                        showlegend=False)

st.plotly_chart(radar_fig,use_container_width=True)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ESG Credit Score Model",layout="wide")
st.title("ESG Multi-Factor Credit Risk Scoring Model")

# Sidebar inputs
st.sidebar.header("🎛Parameter Settings")

#Credit score weight
w1=st.sidebar.slider("Weight of Financial Score (w1)",0.0,1.0,0.7,0.01)
w2=1-w1
st.sidebar.markdown(f"Weight of ESG Score (w2): **{w2:.2f}**")

#ESG weight
st.sidebar.markdown("---")
st.sidebar.subheader("ESG Weight Settings")
alpha=st.sidebar.slider("E - Environmental (α)", 0.0, 1.0, 0.33, 0.01)
beta=st.sidebar.slider("S - Social (β)", 0.0, 1.0 - alpha, 0.33, 0.01)
gamma = 1 - alpha - beta
st.sidebar.markdown(f"G - Governance (γ): **{gamma:.2f}**")

st.sidebar.markdown("---")

#Input scores
st.subheader("Input Company Scores")
col1, col2, col3, col4 = st.columns(4)
with col1:
    financial_score = st.number_input("Financial Score",0.0,100.0,75.0)
with col2:
    E_score = st.number_input("E Score",0.0,100.0,80.0)
with col3:
    S_score = st.number_input("S Score",0.0,100.0,70.0)
with col4:
    G_score = st.number_input("G Score",0.0,100.0, 5.0)

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
st.subheader("📈 Credit Score Result")
col5, col6 = st.columns(2)
col5.metric("Final Credit Score", f"{credit_score:.2f}", help="Based on weights and input scores")
col6.metric("Credit Rating", rating)

# Heatmap Visualization
st.markdown("---")
st.subheader("🌡️ ESG vs Financial Score Sensitivity Heatmap")

E_range=np.linspace(0,100,20)
F_range=np.linspace(0,100,20)
Z=np.zeros((len(E_range), len(F_range)))
for i,E in enumerate(E_range):
    for j,F in enumerate(F_range):
        esg=alpha*E + beta*S_score + gamma*G_score
        Z[i, j] = w1 * F + w2 * esg

fig=px.imshow(Z,
                x=[f"{int(f)}" for f in F_range],
                y=[f"{int(e)}" for e in E_range],
                labels=dict(x="Financial Score", y="E Score", color="Credit Score"),
                aspect="auto",
                color_continuous_scale="Viridis")

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

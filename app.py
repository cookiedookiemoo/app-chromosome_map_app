import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧬 Arabidopsis Chromosome Map")

# Load data
chr_df = pd.read_csv("data/arabidopsis_chromosomes.csv")
gene_df = pd.read_csv("data/genes_of_interest.csv")

# Sidebar gene selection
st.sidebar.header("Select genes")
selected_genes = []
if st.sidebar.button("❌ Uncheck all"):
    for gene in gene_df["gene"]:
        st.session_state[gene] = False

selected_genes = []
for gene in gene_df["gene"]:
    checked = st.sidebar.checkbox(gene, key=gene)
    if checked:
        selected_genes.append(gene)

# Create figure
fig = go.Figure()

# Draw chromosomes
x_positions = list(range(len(chr_df)))

for i, row in chr_df.iterrows():
    chr_name = row["chromosome"]
    length = row["length"]
    centro = row["centromere"]

    # Chromosome line
    fig.add_trace(go.Scatter(
        x=[i, i],
        y=[0, length],
        mode="lines",
        line=dict(width=10, color="black"),
        name=chr_name,
        showlegend=False
    ))

    # Centromere
    fig.add_trace(go.Scatter(
        x=[i],
        y=[centro],
        mode="markers",
        marker=dict(size=12, color="gray"),
        showlegend=False
    ))
    
# Plot selected genes
for gene in selected_genes:
    row = gene_df[gene_df["gene"] == gene].iloc[0]
    chr_index = chr_df.index[chr_df["chromosome"] == row["chromosome"]][0]

    fig.add_trace(go.Scatter(
        x=[chr_index],
        y=[row["position"]],
        mode="markers+text",
        text=[row["gene"]],
        textposition="middle right",
        textfont=dict(size=13),
        marker=dict(
            symbol="line-ew",
            size=8,
            line=dict(color="red", width=2)
        ),
        showlegend=False
    ))

# Layout
fig.update_layout(
    xaxis=dict(
        tickvals=x_positions,
        ticktext=chr_df["chromosome"],
        title=""
    ),
    yaxis=dict(
        title="Physical position (Mb)",
        range=[0, chr_df["length"].max() + 2]
    ),
    height=600
)

st.plotly_chart(fig, use_container_width=True)


























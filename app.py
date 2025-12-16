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
selected_genes = st.sidebar.multiselect(
    "Genes",
    gene_df["gene"].unique(),
    default=[]
)

# Collision avoidance function
def avoid_label_overlap(positions, min_gap=0.5):
    adjusted = []
    for p in positions:
        if not adjusted:
            adjusted.append(p)
        elif p - adjusted[-1] < min_gap:
            adjusted.append(adjusted[-1] + min_gap)
        else:
            adjusted.append(p)
    return adjusted

# Compute label_y per chromosome
gene_df = gene_df.copy()
gene_df["label_y"] = gene_df["position"]

for chr_name in gene_df["chromosome"].unique():
    mask = gene_df["chromosome"] == chr_name
    chr_genes = gene_df[mask].sort_values("position")

    label_y = avoid_label_overlap(chr_genes["position"].values, min_gap=0.4)
    gene_df.loc[chr_genes.index, "label_y"] = label_y

# Create figure
fig = go.Figure()
x_positions = list(range(len(chr_df)))

# Draw chromosomes
for i, row in chr_df.iterrows():
    fig.add_trace(go.Scatter(
        x=[i, i],
        y=[0, row["length"]],
        mode="lines",
        line=dict(width=10, color="black"),
        showlegend=False
    ))

    # Centromere
    fig.add_trace(go.Scatter(
        x=[i],
        y=[row["centromere"]],
        mode="markers",
        marker=dict(size=12, color="gray"),
        showlegend=False
    ))

# Plot selected genes
for gene in selected_genes:
    row = gene_df[gene_df["gene"] == gene].iloc[0]
    chr_index = chr_df.index[chr_df["chromosome"] == row["chromosome"]][0]

    # Connector line
    fig.add_trace(go.Scatter(
        x=[chr_index, chr_index + 0.12],
        y=[row["position"], row["label_y"]],
        mode="lines",
        line=dict(color="gray", width=1),
        showlegend=False
    ))

    # Gene marker + label
    fig.add_trace(go.Scatter(
        x=[chr_index + 0.15],
        y=[row["label_y"]],
        mode="markers+text",
        text=[row["gene"]],
        textposition="middle right",
        textfont=dict(size=11),
        marker=dict(
            symbol="line-ew",
            size=16,
            line=dict(color="blue", width=2)
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
    height=650,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True)

import plotly.express as px
from plotly.graph_objects import Figure
from textwrap import wrap
import streamlit as st

@st.cache(show_spinner=False)
def get_tsne_scatter_figure(x: list, y: list, z: list, sentences: list, labels: list) -> Figure:
    '''
    Returns a plotly figure object.
    input:
        x: list of floats
        y: list of floats
        z: list of floats
        sentences: list of strings
        labels: list of strings
    output:
        fig: plotly figure object
    '''
    hovertext = ['<br>'.join(wrap(sent, width=50)) for sent in sentences]
    labels = [str(label) for label in labels]
    fig = px.scatter_3d(x=x, y=y, z=z, hover_data=[hovertext], color=labels, color_discrete_sequence=px.colors.qualitative.Alphabet, height=800)
    fig.update_layout(scene_xaxis_showticklabels=False,
        scene_yaxis_showticklabels=False,
        scene_zaxis_showticklabels=False,
        margin=dict(r=0, b=0, l=0, t=0))
    return fig

@st.cache(show_spinner=False)
def get_proportions_pie_chart_figure(cluster_proportions: list) -> None:
    '''
    Returns a plotly figure object.
    input:
        cluster_proportions: list of floats
    output:
        fig: plotly figure object
    '''
    fig = px.pie(values=cluster_proportions, names=['Cluster {}'.format(i) for i in range(len(cluster_proportions))])
    fig.update_traces(textposition='inside')
    return fig

@st.cache(show_spinner=False)
def get_affinity_matrix_heatmap_figure(affinity_matrix: list, inference_tokens: list) -> None:
    '''
    Returns a plotly figure object.
    input:
        affinity_matrix: list of floats
        inference_tokens: list of strings
    output:
        fig: plotly figure object
    '''
    return px.imshow(affinity_matrix, x=inference_tokens)

@st.cache(show_spinner=False)
def get_cluster_scores_bar_chart_figure(cluster_scores: list) -> None:
    '''
    Returns a plotly figure object.
    input:
        cluster_scores: list of floats
    output:
        fig: plotly figure object
    '''
    return px.bar(x=range(len(cluster_scores)), y=cluster_scores)
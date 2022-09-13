import plotly.express as px
from plotly.graph_objects import Figure
from textwrap import wrap
import streamlit as st
import numpy as np
import random
from matplotlib.colors import to_hex

#@st.cache(show_spinner=False)
def get_tsne_scatter_figure(x: list, y: list, z: list, sentences: list, labels: list, colors: list) -> Figure:
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
    color_discrete_sequence = [colors[label] for label in labels]
    labels = [str(label) for label in labels]
    #st.write(labels)
    fig = px.scatter_3d(x=x, y=y, z=z, hover_data=[hovertext], color=hovertext, color_discrete_sequence=color_discrete_sequence, height=800, text=labels)
    fig.update_layout(scene_xaxis_showticklabels=False,
        scene_yaxis_showticklabels=False,
        scene_zaxis_showticklabels=False,
        margin=dict(r=0, b=0, l=0, t=0),
        showlegend=False)
    #transparent surface color
    fig.update_scenes(xaxis_showbackground=False, yaxis_showbackground=False, zaxis_showbackground=False, xaxis_gridcolor='rgba(0, 0, 0, 0.2)', yaxis_gridcolor='rgba(0, 0, 0, 0.2)', zaxis_gridcolor='rgba(0, 0, 0, 0.2)')

    for i in range(len(fig.data)):
        fig.data[i].update(hovertemplate=f"{hovertext[i]}")
    return fig

#@st.cache(show_spinner=False)
def get_proportions_pie_chart_figure(cluster_proportions: list, colors: list) -> None:
    '''
    Returns a plotly figure object.
    input:
        cluster_proportions: list of floats
    output:
        fig: plotly figure object
    '''
    fig = px.pie(values=cluster_proportions, names=['Cluster {}'.format(i) for i in range(len(cluster_proportions))], color=colors, color_discrete_sequence=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return fig

#@st.cache(show_spinner=False)
def get_affinity_matrix_heatmap_figure(affinity_matrix: list, inference_tokens: list) -> None:
    '''
    Returns a plotly figure object.
    input:
        affinity_matrix: list of floats
        inference_tokens: list of strings
    output:
        fig: plotly figure object
    '''
    #st.write(inference_tokens)
    #st.write(np.array(affinity_matrix).T)
    return px.imshow(np.array(affinity_matrix).T, aspect="auto", x=inference_tokens, y= ['Cluster {}'.format(i) for i in range(len(np.array(affinity_matrix).T))])

#@st.cache(show_spinner=False)
def get_cluster_scores_bar_chart_figure(cluster_scores: list, colors: list) -> None:
    '''
    Returns a plotly figure object.
    input:
        cluster_scores: list of floats
    output:
        fig: plotly figure object
    '''
    # show the cluster name in the legend
    fig = px.bar(x=range(len(cluster_scores)), y=cluster_scores, color=colors, color_discrete_sequence=colors, text=['Cluster {}'.format(i) for i in range(len(cluster_scores))])
    fig.update_layout(showlegend=False)

    return fig

def get_random_color(pastel_factor = 0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def color_distance(c1,c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

def generate_new_color(existing_colors,pastel_factor = 0.5):
    max_distance = None
    best_color = None
    for i in range(0,100):
        color = get_random_color(pastel_factor = pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color,c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color

def get_n_colors(n_colors):
    colors = []

    for i in range(0, n_colors):
        colors.append(generate_new_color(colors ,pastel_factor = 0.9))

    return [to_hex(color) for color in colors]
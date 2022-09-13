import streamlit as st
from controller import SEEMSController
from controller import TopicController

from utilities.charts import get_tsne_scatter_figure
from utilities.charts import get_affinity_matrix_heatmap_figure
from utilities.charts import get_proportions_pie_chart_figure
from utilities.charts import get_cluster_scores_bar_chart_figure
from utilities.charts import get_n_colors

from utilities.annotations import Annotator

def __change_page(page):
    st.session_state.page = page

def __select_cluster(cluster_label):
    st.session_state.selected_cluster = cluster_label
    st.session_state.page = "dashboard"

def v_spacer(height) -> None:
    for _ in range(height):
        st.write('\n')

def run():
    st.button("Home", on_click=__change_page("home"))

    seems = SEEMSController()
    seems.get_results(st.session_state.reference_text, st.session_state.inference_text, st.session_state.distance_threshold)
    annotator = Annotator(seems.inference_text_tokens, seems.reference_text_sentences, seems.cluster_affinity_matrix, seems.cluster_labels)
    topic_controller = TopicController(
        seems.reference_text_sentences, seems.cluster_labels
    )

    with st.expander("Score", expanded=True):
        st.metric(label="SEEMS SCORE", value=round(seems.seems_score,2))
        st.caption(f"""The reference text contains {len(seems.reference_text_sentences)} sentences and was clustered into {len(seems.cluster_scores)} different clusters. The inference text consists of {len(seems.inference_text_tokens)} tokens. The heatmap below illustrates how different clusters and tokens are related. SEEMS takes into account how well each cluster is represented by the inference text.""")

        heatmap_fig = get_affinity_matrix_heatmap_figure(
            seems.cluster_affinity_matrix, seems.inference_text_tokens
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

    if st.session_state.colors == None:
        st.session_state.colors = get_n_colors(len(seems.cluster_scores))

    with st.expander("Reference Text Clusters", expanded=True):
        st.caption(f"""The reference text was clustered into {len(seems.cluster_scores)} different clusters. The scatter plot below visualizes the clusters in a 3D space, where each sentence in the reference text is represented by a point. The color of each point represents the cluster label. Hovering over a point reveals its text.""")
        tsne_fig = get_tsne_scatter_figure(
            seems.x_tsne,
            seems.y_tsne,
            seems.z_tsne,
            seems.reference_text_sentences,
            seems.cluster_labels,
            st.session_state.colors
        )
        st.plotly_chart(tsne_fig, use_container_width=True)

    with st.expander("Cluster Stats", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.header("Cluster Scores")
            st.caption(
                "The cluster score is an indicator of how well a cluster is represented by the inference text. The higher the score, the better the cluster is represented by the inference text. Clusters with lower scores can be further investigated using the annotation tool below."
            )
            scores_fig = get_cluster_scores_bar_chart_figure(seems.cluster_scores, st.session_state.colors)
            st.plotly_chart(scores_fig, use_container_width=True)

        with col2:
            st.header("Cluster Weights")
            st.caption(
                "The relative size of a cluster (its weight) is used by SEEMS as an indicator of how important a cluster is. The larger the weight, the more important the cluster is."
            )
            proportions_fig = get_proportions_pie_chart_figure(
                seems.cluster_proportions, st.session_state.colors
            )
            st.plotly_chart(proportions_fig, use_container_width=True)

    with st.expander("Annotated Text", expanded=True):
        st.caption("This tool allows to compare reference text clusters with the inference text tokens. It can be used to analyse clusters with low scores. The left column shows the reference text cluster text. The right column shows the inference text tokens, with the color of each token indicating the similarity to the reference text cluster.")

        annotator = Annotator(seems.inference_text_tokens, seems.reference_text_sentences, seems.cluster_affinity_matrix, seems.cluster_labels)

        with st.form("Text Input Form"):
            selected_cluster = st.selectbox("Select Cluster", range(len(seems.cluster_scores)))
            threshold = st.slider("Threshold", 0., 1., 0.4)
            submit = st.form_submit_button("Submit", on_click=__select_cluster, args=[selected_cluster])
            if submit:
                st.session_state.selected_cluster = selected_cluster

        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                st.header("Reference Text")
                annotator.get_annotated_reference_text(st.session_state.selected_cluster, "#FFFF00")

        with col2:
            with st.container():
                st.header("Inference Text")
                annotator.get_annotated_inference_text(st.session_state.selected_cluster, threshold)
                #st.write(annotations)
import streamlit as st
from controller import SEEMSController
from controller import TopicController

from utilities.charts import get_tsne_scatter_figure
from utilities.charts import get_affinity_matrix_heatmap_figure
from utilities.charts import get_proportions_pie_chart_figure
from utilities.charts import get_cluster_scores_bar_chart_figure

from utilities.annotations import Annotator

if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = 0

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
    seems.get_results(st.session_state.reference_text, st.session_state.inference_text)
    annotator = Annotator(seems.inference_text_tokens, seems.reference_text_sentences, seems.cluster_affinity_matrix, seems.cluster_labels)
    topic_controller = TopicController(
        seems.reference_text_sentences, seems.cluster_labels
    )

    with st.expander("Score", expanded=True):
        st.metric(label="SEEMS SCORE", value=seems.seems_score)
        st.caption("Lorem Ipsum is simply dummy text of the printing and typesetting industry.")

    with st.expander("Cluster Stats", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.header("Cluster Scores")
            st.caption(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            )
            scores_fig = get_cluster_scores_bar_chart_figure(seems.cluster_scores)
            st.plotly_chart(scores_fig, use_container_width=True)

        with col2:
            st.header("Cluster Proportions")
            st.caption(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            )
            proportions_fig = get_proportions_pie_chart_figure(
                seems.cluster_proportions
            )
            st.plotly_chart(proportions_fig, use_container_width=True)

    with st.expander("Reference Text Clusters", expanded=True):
        st.caption("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        tsne_fig = get_tsne_scatter_figure(
            seems.x_tsne,
            seems.y_tsne,
            seems.z_tsne,
            seems.reference_text_sentences,
            seems.cluster_labels,
        )
        st.plotly_chart(tsne_fig, use_container_width=True)

    with st.expander("Annotated Text", expanded=True):
        st.caption("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")

        annotator = Annotator(seems.inference_text_tokens, seems.reference_text_sentences, seems.cluster_affinity_matrix, seems.cluster_labels)

        with st.form("Text Input Form"):
            selected_cluster = st.selectbox("Select Cluster", range(len(seems.cluster_scores)))
            submit = st.form_submit_button("Submit", on_click=__select_cluster, args=[selected_cluster])
            if submit:
                st.session_state.selected_cluster = selected_cluster

        col1, col2 = st.columns(2)

        with col1:
            st.header("Inference Text")
            annotator.get_annotated_inference_text(st.session_state.selected_cluster, 0.5)

        with col2:
            st.header("Reference Text")
            annotator.get_annotated_reference_text(st.session_state.selected_cluster)

        v_spacer(height=3)


    with st.expander("Cluster Affinity Matrix", expanded=True):
        st.caption(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        )
        heatmap_fig = get_affinity_matrix_heatmap_figure(
            seems.cluster_affinity_matrix, seems.inference_text_tokens
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)
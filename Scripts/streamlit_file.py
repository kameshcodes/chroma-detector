import streamlit as st
from PIL import Image

st.set_page_config(layout='centered', initial_sidebar_state='collapsed')

st.sidebar.markdown('''
<a href="https://twitter.com/Kameshspeaks" > Twitter </a> <br>
<a href = "https://www.linkedin.com/in/ikameshdubey/"> LinkedIn</a>''' , unsafe_allow_html=True)
page = st.sidebar.radio("Select Page",options=['Home','Generate Chroma'])
st.sidebar.markdown(
    """
    <h1 style='position: fixed; top: 0%; left: 7%; transform: translateX(-50%); color: #316FF6 ;'>Chroma Detector</h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <h5 style='position: fixed; top: 6.5%; left: 10.2%; transform: translateX(-50%); color: #316FF6;'>by Kamesh</h5>
    """,
    unsafe_allow_html=True
)
if page == "Home":
    st.markdown(
        """
        <h2 style='position: fixed; top: 3%; left: 14.5%; transform: translateX(-50%); color: #316FF6 ;'>Chroma Detector</h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h5 style='position: fixed; top: 10.5%; left: 19.7%; transform: translateX(-50%); color: #316FF6;'>by Kamesh</h5>
        """,
        unsafe_allow_html=True
    )
    
    st.write(
    """
    <div class="charcoal-gray-text">
        <h1>Welcome to Chroma Detect!</h1>
        <p>This web app allows you to discover the dominant color present in an image.</p>
    </div>
    <div class="charcoal-gray-text2">
        <p>Simply upload an image using the provided interface, and the app will analyze the image and determine its dominant color.</p>
    </div>
    <div class="charcoal-gray-text4">
        <h6>Give it a try, click on generate schema in sidebar!</h6>
    </div>
    """
    ,unsafe_allow_html=True)
    

    
if page=='Generate Chroma':
    st.markdown(
        """
        <h2 style='position: fixed; top: 3%; left: 14.5%; transform: translateX(-50%); color: #316FF6 ;'>Chroma Detector</h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h5 style='position: fixed; top: 10.5%; left: 19.7%; transform: translateX(-50%); color: #316FF6;'>by Kamesh</h5>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
        <div class="charcoal-gray-text">
            <h1>How it works</h1>
        </div>
        <div class="charcoal-gray-text3">
            <ol>
                <li>Click on the "Browse files" button below.</li>
                <li>Select an image from your device.</li>
                <li>Chroma Detect will process the image and display its dominant color.</li>
            </ol>
        </div>
        <div class="charcoal-gray-text4">
        </div>
        """
        ,unsafe_allow_html=True)


    uploaded_img = st.file_uploader("Upload an image *", type=["jpg", "jpeg", "png"])

    btn = st.button("Analyze")

    if btn:
        if not uploaded_img:
            st.error("Please upload an image.")
        else:
            from utils import *

            img, img_data = load_img(uploaded_img)
            scaled_img_data, scaler = normalise_data(img_data)
            cluster_centers, cluster_labels = get_cluster_centres(scaled_img_data, 5)
            sorted_cluster_centers = sort_by_colour_dominance(cluster_centers, cluster_labels, scaler)
            fig = plot_centre_patches(sorted_cluster_centers)
            st.pyplot(fig)
        
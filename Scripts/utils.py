import pandas as pd
import numpy as np 
from PIL import Image 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

def convert_image_to_rgb_dataframe(img):
    """
    Convert an image into a DataFrame containing RGB values.

    Parameters:
    img (PIL.Image.Image): The input image.

    Returns:
    pd.DataFrame: DataFrame containing pixel values in columns 'R', 'G', and 'B'.
                  If the image is RGBA, the DataFrame contains 'R', 'G', 'B', and 'A'.
    """
    pixels = []
    img_data = img.load()
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            pixel = img_data[x, y]
            pixels.append(pixel) 
            
    try:
        img_data = pd.DataFrame(pixels, columns=["R", "G", "B"]) 
    except ValueError:
        img_data = pd.DataFrame(pixels, columns=["R", "G", "B", "A"])
        img_data = img_data[["R", "G", "B"]]
    
    return img_data


def load_img(uploaded_img):
    """
    Load an image and its pixel data from the specified file path.

    Args:
    - uploaded_img (BytesIO): The uploaded image file.

    Returns:
    - img (PIL.Image.Image): The loaded image object.
    - img_data (PixelAccess): The pixel data of the image.
    """
    img = Image.open(uploaded_img)
    img_data = convert_image_to_rgb_dataframe(img)
    return img, img_data


def imgshow(img, height=3, width=2):
    """
    Display an image using Matplotlib within a Jupyter Notebook.

    Parameters:
    img (PIL.Image.Image): The image to display.
    height (int, optional): Height of the displayed image. Default is 3.
    width (int, optional): Width of the displayed image. Default is 2.
    """
    plt.figure(figsize=(height, width))
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    
def normalise_data(df):
    """
    Normalize the input DataFrame using MinMaxScaler.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be normalized.

    Returns:
    tuple: A tuple containing two elements:
        - np.ndarray: The normalized data.
        - MinMaxScaler: The fitted MinMaxScaler object for possible future transformations.
    """
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    return scaled_data, scaler
  
    
def get_cluster_centres(scaled_img_data, n_clusters):
    """
    Apply K-means clustering to the input data to obtain cluster centers and labels.

    Parameters:
    scaled_img_data (array-like): The scaled data for clustering.
    n_clusters (int): The number of clusters to form.

    Returns:
    tuple: A tuple containing two elements:
        - np.ndarray: Cluster centers of the fitted K-means estimator.
        - np.ndarray: Labels of each data point based on the clustering.
    """
    kmeans = KMeans(n_clusters=n_clusters)
    cluster_labels = kmeans.fit_predict(scaled_img_data)
    cluster_centers = kmeans.cluster_centers_
    return cluster_centers, cluster_labels


def sort_by_colour_dominance(cluster_centers, cluster_labels, scaler):
    """
    Sort cluster centers based on the dominance of colors within each cluster.

    Parameters:
    cluster_centers (np.ndarray): Cluster centers obtained from K-means clustering.
    cluster_labels (np.ndarray): Labels of each data point based on the clustering.
    scaler (MinMaxScaler): The MinMaxScaler used for scaling the data.

    Returns:
    np.ndarray: Cluster centers sorted by color dominance.
    """
    _, label_counts = np.unique(cluster_labels, return_counts=True)
    sorted_indices = np.argsort(label_counts)[::-1]
    sorted_cluster_centers = cluster_centers[sorted_indices]
    rev_sorted_cluster_centers = scaler.inverse_transform(sorted_cluster_centers)
    return rev_sorted_cluster_centers

def plot_centre_patches(cluster_centers):
    fig, ax = plt.subplots(figsize=(10, 1.5))
    num_centers = len(cluster_centers)
    rect_width = 1.0 / num_centers

    for i, cluster_center in enumerate(cluster_centers):
        facecolor = (cluster_center[0] / 255.0, cluster_center[1] / 255.0, cluster_center[2] / 255.0)
        rect = Rectangle((i * rect_width, 0), rect_width, 1, facecolor=facecolor)
        ax.add_patch(rect)
    ax.axis('off')
    fig.savefig(r"artifacts\plots\utils-output")
    return fig


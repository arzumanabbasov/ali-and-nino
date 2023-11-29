import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, filename='downloadimages.log')


def image_downloader(url: str, base_dir) -> None:
    """
    This function downloads an image from a URL and saves it to a local directory.
    It takes two arguments:
    - url: the url of the image to download
    - base_dir: the directory to save the image to

    It has no return value.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a local file in binary write mode
        name = url.split("/")[-1]
        filetype = name.split(".")[-1]
        with open(base_dir + f"{name}.{filetype}", "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        logging.info("Image downloaded successfully.")
    else:
        # Print an error message if the request was not successful
        logging.info(f"Failed to download image. Status code: {response.status_code}")


def download_images(urls: list['str'], base_dir: str = "C:/Users/Admin/Desktop/Projects/Book Price "
                                                       "Prediction/data/images/") -> None:
    """
    This function downloads images from a list of URLs and saves them to a local directory.
    It takes one argument:
    - urls: a list of URLs to download images from

    It has no return value.
    """
    for u in urls:
        image_downloader(u, base_dir=base_dir)


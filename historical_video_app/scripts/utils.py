def download_images_from_wikipedia(page_title, folder_path, image_count=10):
    import wikipediaapi
    import os
    from PIL import Image
    import requests
    from io import BytesIO
    from bs4 import BeautifulSoup

    # Initialize Wikipedia API with a proper user-agent
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent="HistoricalVideoApp/1.0 (milesjoseph747@gmail.com)"
    )

    # Fetch the Wikipedia page
    page = wiki.page(page_title)
    if not page.exists():
        print(f"Page '{page_title}' does not exist.")
        return

    # Use BeautifulSoup to scrape images from the page HTML
    page_url = page.fullurl
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {page_url}")
        return

    # Parse HTML and find image URLs
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [
        "https:" + img['src']
        for img in img_tags if img['src'].startswith("//upload.wikimedia.org")
    ]

    if not img_urls:
        print(f"No images found for {page_title}.")
        return

    # Limit the number of images to download
    img_urls = img_urls[:image_count]

    # Download and save images
    os.makedirs(folder_path, exist_ok=True)
    for i, img_url in enumerate(img_urls):
        try:
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            img_path = os.path.join(folder_path, f"{page_title}_{i}.jpg")
            img.save(img_path)
            print(f"Saved: {img_path}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")


def get_related_links(page_title):
    import wikipediaapi

    # Initialize Wikipedia API
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent="HistoricalVideoApp/1.0 (milesjoseph747@gmail.com)"
    )

    # Fetch the Wikipedia page
    page = wiki.page(page_title)
    if not page.exists():
        print(f"Page '{page_title}' does not exist.")
        return []

    # Return related links
    return [link for link in page.links.keys()]
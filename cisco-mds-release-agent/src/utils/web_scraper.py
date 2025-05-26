def fetch_release_notes(url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def download_file(url, filename):
    import requests

    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    with open(filename, 'wb') as file:
        file.write(response.content)

def extract_links(soup, link_selector):
    return [a['href'] for a in soup.select(link_selector)]

def scrape_release_notes(base_url, link_selector):
    soup = fetch_release_notes(base_url)
    links = extract_links(soup, link_selector)
    return links

def main():
    base_url = "https://www.cisco.com/c/en/us/support/storage-networking/mds-9000-nx-os-san-os-software/products-release-notes-list.html"
    link_selector = "a.release-note-link"  # Example selector, adjust as needed
    release_note_links = scrape_release_notes(base_url, link_selector)

    for link in release_note_links:
        filename = link.split("/")[-1]  # Extract filename from URL
        download_file(link, filename)

if __name__ == "__main__":
    main()
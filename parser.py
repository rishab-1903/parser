import aiohttp
import asyncio
import argparse
from bs4 import BeautifulSoup
import csv
from pathlib import Path

def extract_and_store_content(url, content):
    try:
        # Create a directory to store raw HTML files
        output_dir = Path("raw_html_content")
        output_dir.mkdir(exist_ok=True)

        # Generate a safe filename based on the URL
        safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
        file_name = f"{safe_name}_raw.html"

        # Save raw HTML content to the file
        file_path = output_dir / file_name
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Raw HTML content saved to: {file_path}")

        # Return content as a variable for further processing
        return content

    except Exception as e:
        print(f"Error storing content from {url}: {e}")
        return None
    
async def fetch_and_parse_jobs(session, url):
    try:
        async with session.get(url) as response:
            content = await response.text()
            status = response.status

            print(f"Fetching: {url} | Status: {status}")
            if status == 200:
                # Save raw content and return it
                raw_content = extract_and_store_content(url, content)
                # Placeholder for additional processing with LLMs or parsing logic
                # e.g., parsed_result = llm_api.process_html(raw_content)
            else:
                print(f"Failed to fetch content from {url}, Status: {status}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_parse_jobs(session, url) for url in urls]
        await asyncio.gather(*tasks)

# Entry point for the script
if __name__ == "__main__":
    # Setting up command-line arguments
    parser = argparse.ArgumentParser(description="Async HTTP content fetcher")
    parser.add_argument("urls", metavar="URL", nargs="+", help="One or more URLs to fetch")
    args = parser.parse_args()

    # Run the main function with provided URLs
    asyncio.run(main(args.urls))

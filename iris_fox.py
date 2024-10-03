import requests
from bs4 import BeautifulSoup
import sys
import os

class IrisFoxBrowser:
    def __init__(self):
        self.history = []
        self.user_agent = "Iris Fox/1.0 (Linux)"
        self.favorites_file = "favorites.txt"
        self.favorites = self.load_favorites()

    def load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r") as file:
                return [line.strip() for line in file.readlines()]
        return []

    def save_favorite(self, url):
        if url not in self.favorites:
            self.favorites.append(url)
            with open(self.favorites_file, "a") as file:
                file.write(url + "\n")
            print(f"Saved to favorites: {url}")
        else:
            print(f"{url} is already in favorites.")

    def list_favorites(self):
        if self.favorites:
            print("Favorites:")
            for idx, url in enumerate(self.favorites):
                print(f"[{idx}] {url}")
        else:
            print("No favorite sites saved.")

    def fetch_page(self, url):
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Save URL to history for navigation
            self.history.append(url)
            
            # Parse the page content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def display_text(self, soup):
        if soup:
            text = soup.get_text()
            print(text.strip())
        else:
            print("No content to display.")

    def list_links(self, soup):
        if soup:
            links = soup.find_all('a', href=True)
            for idx, link in enumerate(links):
                print(f"[{idx}] {link.text.strip()}: {link['href']}")
        else:
            print("No links found.")

    def follow_link(self, index, soup):
        try:
            links = soup.find_all('a', href=True)
            if 0 <= index < len(links):
                new_url = links[index]['href']
                # Ensure the URL is absolute
                if new_url.startswith('http'):
                    return new_url
                else:
                    print("Invalid URL format. Skipping.")
            else:
                print("Invalid link index.")
        except Exception as e:
            print(f"Error following link: {e}")
        return None

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()  # Remove current page
            return self.history.pop()  # Return previous page
        else:
            print("No previous page to go back to.")
            return None

    def search_text(self, soup, keyword):
        if soup:
            text = soup.get_text()
            if keyword.lower() in text.lower():
                print(f"Found '{keyword}' in the page!")
            else:
                print(f"'{keyword}' not found in the page.")
        else:
            print("No content to search.")

    def google_search(self, query):
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {'User-Agent': self.user_agent}
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)

            # Display top search results (clean URLs)
            result_links = [link for link in links if "/url?q=" in link['href']]
            if result_links:
                for idx, link in enumerate(result_links[:10]):  # Top 10 results
                    clean_url = link['href'].split("/url?q=")[1].split("&")[0]
                    print(f"[{idx}] {clean_url}")
            else:
                print("No search results found.")
        except requests.exceptions.RequestException as e:
            print(f"Error during Google search: {e}")

if __name__ == "__main__":
    browser = IrisFoxBrowser()
    while True:
        command = input("Iris Fox > ").strip()
        
        # Command to fetch a page
        if command.startswith("open "):
            url = command.split("open ", 1)[1]
            page = browser.fetch_page(url)
            browser.display_text(page)
        
        # Command to list links on the current page
        elif command == "links":
            page = browser.fetch_page(browser.history[-1])
            browser.list_links(page)
        
        # Command to follow a link by index
        elif command.startswith("follow "):
            try:
                index = int(command.split("follow ", 1)[1])
                page = browser.fetch_page(browser.history[-1])
                new_url = browser.follow_link(index, page)
                if new_url:
                    new_page = browser.fetch_page(new_url)
                    browser.display_text(new_page)
            except ValueError:
                print("Invalid link index.")
        
        # Command to go back to the previous page
        elif command == "back":
            previous_url = browser.go_back()
            if previous_url:
                previous_page = browser.fetch_page(previous_url)
                browser.display_text(previous_page)
        
        # Command to search for a keyword on the current page
        elif command.startswith("search "):
            keyword = command.split("search ", 1)[1]
            page = browser.fetch_page(browser.history[-1])
            browser.search_text(page, keyword)
        
        # Command to change user-agent
        elif command.startswith("user-agent "):
            agent = command.split("user-agent ", 1)[1]
            browser.user_agent = agent
            print(f"User-agent changed to: {agent}")
        
        # Command to save current URL to favorites
        elif command == "save favorite":
            if browser.history:
                browser.save_favorite(browser.history[-1])
            else:
                print("No page loaded to save.")
        
        # Command to list favorite sites
        elif command == "favorites":
            browser.list_favorites()
        
        # Command to Google search
        elif command.startswith("google "):
            query = command.split("google ", 1)[1]
            browser.google_search(query)
        
        # Quit the browser
        elif command == "quit":
            print("Exiting Iris Fox.")
            break
        
        else:
            print("Unknown command. Available commands: open <url>, links, follow <index>, back, search <keyword>, save favorite, favorites, google <query>, user-agent <agent>, quit")

New Features Explanation:

    Save Favorite Sites:
        Command: save favorite
        Saves the current page to a favorites list, stored in a favorites.txt file. The command favorites lists all saved favorite sites.
    Google Search:
        Command: google <query>
        Performs a Google search with the given query and displays the top 10 results as clean URLs you can follow.

Example Usage:

bash

Iris Fox > open https://example.com
Iris Fox > save favorite
Iris Fox > favorites
[0] https://example.com
Iris Fox > google Python web scraping
[0] https://realpython.com/python-web-scraping-practical-introduction/
[1] https://scrapy.org/
Iris Fox > follow 0
Iris Fox > back
Iris Fox > quit

1. Low Resource Consumption

    Minimalist: Iris Fox uses very little system memory and processing power. Modern browsers, with their graphical interfaces and heavy background processes, can consume significant system resources, which can be a problem on older or resource-constrained machines. Iris Fox is perfect for those looking to browse text-based content efficiently on low-end hardware or in environments with limited resources.

2. Faster for Simple Tasks

    No Frills: When you just need to quickly grab text content, check some basic info, or perform lightweight browsing (e.g., reading articles or documentation), Iris Fox provides a no-distraction experience, cutting down on page load times that would otherwise be slowed down by rendering images, videos, and ads.

3. Improved Security and Privacy

    Script-Free Browsing: By design, Iris Fox doesn't render JavaScript, images, or other dynamic content. This makes it inherently safer from many web-based attacks like drive-by downloads, malicious ads, or harmful JavaScript injections. It's an excellent choice for security-conscious users who want to avoid potential browser exploits or tracking scripts.
    Minimal Tracking: Without JavaScript or cookies, the ability of websites to track your activity is severely limited. You can also switch user-agents to appear as different browsers or devices, making you more anonymous online.

4. Text-Based Browsing for Terminal Users

    Integration with Terminal Workflows: For users who spend most of their time working in a terminal environment (e.g., developers, system administrators, or hackers), Iris Fox integrates smoothly into command-line workflows. This is ideal for checking references, reading documentation, or performing quick searches without needing to leave the terminal or open a graphical interface.

5. Perfect for Remote or Headless Browsing

    Remote Access: In environments where you might be SSH’ing into a remote server without a graphical interface (headless mode), having a command-line browser like Iris Fox is extremely useful for fetching and reading web content. Modern browsers can't function in such a headless terminal-only environment unless specially configured.

6. Productivity Without Distractions

    Focus on Text: Without videos, images, ads, and pop-ups, Iris Fox helps users focus purely on the text content, making it a great tool for reading without distraction. For users who want to avoid the endless rabbit hole of social media and news sites with interactive elements, Iris Fox keeps browsing simple and to-the-point.

7. Customization and Scriptability

    Custom Features: Since Iris Fox is a script-based tool, users with programming knowledge can easily extend its functionality to suit specific needs (e.g., integrating it into larger automation pipelines, parsing data from web pages, etc.). This level of flexibility and scriptability isn't as easily achievable in modern GUI-based browsers.

8. Accessible in Restricted Environments

    Use in Restricted Networks: Some corporate environments or secure networks restrict the use of modern browsers or disable certain functionality (like JavaScript). Iris Fox can be used in such environments to access basic web information where more complex browsers might be blocked or crippled.

9. Educational Tool

    Learn Web Fundamentals: Using Iris Fox can be a way for developers or learners to better understand how the web works at a lower level, such as HTML structure, networking, and HTTP responses. By stripping away the presentation layer (CSS, JavaScript), it can serve as a tool to help people focus on the underlying mechanics of web pages.

10. Quick and Lightweight Google Searches

    Fast Google Search: If you just need to search for something quickly without opening a full browser, Iris Fox can perform a Google search and return links directly in the terminal. This can be a huge time-saver when performing repetitive research tasks or looking up quick references.

Example Use Cases for Iris Fox:

    Hacker/Researcher Environment: A security researcher who values text-based browsing for investigating web content or gathering intelligence without triggering JavaScript-based tracking.
    Developer Workflow: Developers who are debugging or fetching web content in a server environment may prefer the simplicity and lightweight nature of Iris Fox for reading API documentation or troubleshooting.
    System Administrators: Admins working on remote servers without a graphical environment may use Iris Fox to check web-based services, gather information, or even scrape web content for further analysis.

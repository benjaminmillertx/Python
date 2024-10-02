from selenium import webdriver
import time

# Logger class to log visited URLs and time spent
class WebLogger:
    def __init__(self, log_file='visited_sites.txt'):
        self.log_file = log_file

    def log(self, url, duration):
        with open(self.log_file, 'a') as f:
            f.write(f"Visited: {url}, Time Spent: {duration:.2f} seconds\n")

# Function to set up the browser
def setup_browser():
    # Adjust the path to your ChromeDriver or GeckoDriver if necessary
    driver = webdriver.Chrome()  # Or webdriver.Firefox() for Firefox
    return driver

def main():
    web_logger = WebLogger()

    # Set up the browser
    driver = setup_browser()

    # Open a website
    websites = [
        "https://www.google.com",
        "https://www.example.com",
        "https://www.github.com"
    ]

    for site in websites:
        start_time = time.time()  # Record the start time
        driver.get(site)  # Navigate to the site

        # Simulating time spent on the site (for demonstration)
        time.sleep(5)  # Change this to actual user interaction or input if needed

        end_time = time.time()  # Record the end time
        duration = end_time - start_time  # Calculate time spent

        web_logger.log(site, duration)  # Log the site visited and time spent

    driver.quit()  # Close the browser

if __name__ == "__main__":
    main()

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
import pandas as pd
from io import BytesIO

# Streamlit UI
st.set_page_config(page_title="Flipkart Product Scraper by NexTen Brands", page_icon=":moneybag:", layout="wide")

with st.container():
    st.title('Flipkart Product Scraper by NexTen Brands')

with st.container():
    left_column, right_column = st.columns((2, 1))

    with left_column:

        # Input fields in Streamlit UI
        search_query = st.text_input('Enter the product to search:', '')
        page_count = st.number_input('Enter the number of pages to scrape:', min_value=1, max_value=500, value=2)
        start_scraping = st.button('Start Scraping')

        if start_scraping:
            st.write(f'Starting to scrape {search_query} for {page_count} pages...')

            # Set up Firefox options for headless browsing
            firefox_options = Options()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--disable-gpu')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')

            # Use webdriver_manager to handle the driver installation
            @st.cache_resource
            def get_driver():
                return webdriver.Firefox(
                    service=Service(
                        GeckoDriverManager().install()
                    ),
                    options=firefox_options,
                )

            # Initialize the WebDriver
            browser = get_driver()

            # Load the Flipkart webpage
            browser.get('https://www.flipkart.com/')

            # Close any initial popups (like login popups)
            try:
                close_popup = browser.find_element(By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
                close_popup.click()
            except:
                pass

            # Get the input elements
            input_search = browser.find_element(By.CLASS_NAME, 'Pke_EE')
            search_button = browser.find_element(By.CSS_SELECTOR, '#container > div > div.q8WwEU > div > div > div > div > div:nth-child(1) > div > div > div > div._2nl6Ch > div._2NhoPJ > header > div._3ZqtNW > div._3NorZ0._3jeYYh > form > div > button > svg')

            # Send the input to the webpage
            input_search.send_keys(search_query)
            sleep(2)
            search_button.click()

            # Initialize lists to store product details
            products_title = []
            products_price = []
            products_mrp = []
            products_rating = []
            products_rating_count = []
            products_qty = []

            # Loop through multiple pages based on user input
            for i in range(page_count):
                st.write(f'Scraping page {i+1}...')
                sleep(2)
                
                # Scrape product details on the current page
                titles = browser.find_elements(By.CLASS_NAME, "wjcEIp")
                prices = browser.find_elements(By.CLASS_NAME, "Nx9bqj")
                MRPprices = browser.find_elements(By.CLASS_NAME, "yRaY8j")
                ratings = browser.find_elements(By.CLASS_NAME, "XQDdHH")
                rating_counts = browser.find_elements(By.CLASS_NAME, "Wphh3N")
                qtys = browser.find_elements(By.CLASS_NAME, "NqpwHC")

                # Append the details to the respective lists
                for title, price, mrp, rating, rating_count, qty in zip(titles, prices, MRPprices, ratings, rating_counts, qtys):
                    products_title.append(title.get_attribute('title'))
                    products_price.append(price.text)
                    products_mrp.append(mrp.text)
                    products_rating.append(rating.text)
                    products_rating_count.append(rating_count.text)
                    products_qty.append(qty.text)

                # Click the 'Next' button to go to the next page
                try:
                    next_button = browser.find_element(By.CLASS_NAME, '_9QVEpD')
                    next_button.click()
                    sleep(2)
                except:
                    st.write("No more pages to scrape.")
                    break

            # Close the browser
            browser.quit()

            # Save the scraped data into a DataFrame
            data = pd.DataFrame({
                'Title': products_title,
                'Selling Price': products_price,
                'MRP': products_mrp,
                'Quantity': products_qty,
                'Rating': products_rating,
                'Rating count': products_rating_count
            })

            # Display the data using Streamlit
            st.write("Scraping completed! Here's the data:")
            st.dataframe(data)

            # Use BytesIO to allow file download in Streamlit
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False)
                writer.close()

            # Download button for the data
            st.download_button(
                label="Download data as Excel",
                data=output.getvalue(),
                file_name=f'flipkart_{search_query}_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        with right_column:
            st.image('nexten_logo_2.jpeg')
            st.image('background.png')  # Display an image from a file

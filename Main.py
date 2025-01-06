import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import time
import os
import atexit
import logging
import sys
from dotenv import load_dotenv

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class WebsiteChatbot:
    def __init__(self, api_key):
        self.website_data = ""
        try:
            genai.configure(api_key=api_key)
            
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.8,
                'top_k': 40,
            }
            
            self.model = genai.GenerativeModel(
                model_name='gemini-pro',
                generation_config=generation_config
            )
            
            atexit.register(self.cleanup)
            
            print("Successfully initialized Gemini API")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            raise
    
    def cleanup(self):
        try:
            self.model = None
            import gc
            gc.collect()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def scrape_website(self, url):
        print("\nScraping website content...")
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'meta', 'link']):
                element.decompose()
            
            text_content = []
            
            main_content = soup.find_all(['h1', 'h2', 'h3', 'p'])
            
            for element in main_content:
                text = element.get_text().strip()
                if text and len(text) > 20:  # Filter out very short snippets
                    text_content.append(text)
            
            self.website_data = "\n\n".join(text_content)
            
            if not self.website_data:
                print("Warning: No content extracted from website")
                return False
            
            print(f"Successfully extracted {len(text_content)} content blocks")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error accessing website: {str(e)}")
            return False
        except Exception as e:
            print(f"Error scraping website: {str(e)}")
            return False
    
    def generate_response(self, question):
        if not self.website_data:
            return "No website content available. Please scrape a website first."
        
        try:
            prompt = f"""Based on the following website content, please answer the question.
            
Content:
{self.website_data[:2000]}

Question: {question}

Please provide a concise and relevant answer based only on the website content above."""
            

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(prompt)
                    if response and response.text:
                        return response.text
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(1)  # Wait before retry
            
            return "Sorry, I couldn't generate a response. Please try again."
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error generating response. Please try again."
    
    def start_chat(self):
        self.clear_console()
        print("\n=== Website Chatbot ===")
        print("Commands:")
        print("X - Exit      E - Clear console")
        print("New - Analyze different website")

        
        while True:
            try:
                print("\nEnter a website URL:")
                url = input("> ").strip()
                
                if url.lower() == 'x':
                    print("Goodbye!")
                    return
                elif url.lower() == 'e':
                    self.clear_console()
                    continue
                
 
                if not self.scrape_website(url):
                    continue
                
                print("\nYou can now ask questions about the website")
                print("X - Exit | New - Different website | E - Clear console")
                

                while True:
                    try:
                        print("\nEnter your question:")
                        question = input("> ").strip().lower()
                        
                        if question == 'x':
                            print("Goodbye!")
                            sys.exit(0)
                        elif question == 'new':
                            break
                        elif question == 'e':
                            self.clear_console()
                            continue
                        elif not question:
                            continue
                        
                        print("\nGenerating response...")
                        start_time = time.time()
                        response = self.generate_response(question)
                        end_time = time.time()
                        
                        print(f"\nResponse: {response}")
                        print(f"(Generated in {end_time - start_time:.2f} seconds)")
                        
                    except KeyboardInterrupt:
                        print("\nOperation cancelled by user")
                        continue
                    except Exception as e:
                        logger.error(f"Error in question loop: {str(e)}")
                        print("An error occurred. Please try again.")
                        continue
                        
            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                continue
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                print("An error occurred. Please try again.")
                continue

def main():
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    try:
        chatbot = WebsiteChatbot(API_KEY)
        chatbot.start_chat()
    except KeyboardInterrupt:
        print("\nBot terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
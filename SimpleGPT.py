import openai
from os.path import exists

class SimpleGPT:

    openai.api_key = "<--- add your OpenAI key here, or update to use environment variables specific to your platform --->"

    chat_prompt = []
    cache_responses = False
    cache_directory = ""

    def __init__(self,system_prompt,cache=False,cache_dir=""):
        self.chat_prompt.append({"role": "system", "content": system_prompt})
      
        if cache:
            self.cache_responses = True
            self.cache_directory = cache_dir

    def simple_query(self,query):
        
        gpt_response = ""
        cache_file_name = ""
        full_cache_file_path = ""

        #cache
        if self.cache_responses:
            cache_file_name = ''.join(ch for ch in query if ch.isalnum())
            full_cache_file_path = self.cache_directory + "/" + cache_file_name + ".txt"
        
            if exists(full_cache_file_path):
                cache_file = open(full_cache_file_path,"r")
                gpt_response = cache_file.read()
                cache_file.close()

        if gpt_response == "":

            self.chat_prompt.append({"role": "user", "content": query})

            response = openai.ChatCompletion.create(
                model="gpt-4",
                #model="gpt-3.5-turbo",
                
                messages = self.chat_prompt
            )

            gpt_response = str(response['choices'][0]['message']['content']).strip('\n').strip()

            # cache the response
            if self.cache_responses and exists(self.cache_directory):
                f = open(full_cache_file_path, "w")
                f.write(gpt_response)
                f.close()

        return gpt_response

if __name__ == "__main__":

    # Caching can be enabled on initialization or directly, as in the examples below
    #
    # 1. Set the system prompt on object creation
    # 2. Use simple_query to ask it for stuff

    gpt = SimpleGPT("You are a currency symbol converter. You will extract the from currency symbol, destination currency symbol, and the amount to be converted. The response will be a single statement with no additional information, in the format of (from,to,amount).",cache=True,cache_dir="C:/temp")

    # or turn on cache as needed
    gpt.cache_responses = True
    gpt.cache_directory = "C:/SimpleGPT/"

    response = gpt.simple_query("what is one hundred dollars Australian in us")

    print(response)
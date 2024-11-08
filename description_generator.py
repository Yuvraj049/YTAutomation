import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()
API_TOKEN = os.getenv('HF_TOKEN')
print(f"API Token: {API_TOKEN}")

if __name__ == "__main__":
    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"  
    # Initialize the Hugging Face endpoint with parameters directly
    llm = HuggingFaceEndpoint(
        endpoint_url=f"https://api-inference.huggingface.co/models/{repo_id}",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        max_length=100,  # Pass max_length directly
        temperature=0.7
    )
    
    # Define the context and question
    title = "Exploring Lost Civilizations: The Soul's Journey After Death"
    context = ("The title is for a clip taken from the Joe Rogan Podcast featuring Graham Hancock. "
               "I want to create a description for the video that is engaging and informative.")
    question = ("Using the title and context, please create 2 plain text paragraphs without any headings. "
                "The first paragraph should be a description. The second paragraph should contain keywords "
                "and hashtags for Search Engine Optimization. Both paragraphs should be less than 200 words.")

    prompt = f"{title}\n\n{context}\n\n{question}"

    response = llm.invoke(prompt)
    
    # Print the response
    print(response)

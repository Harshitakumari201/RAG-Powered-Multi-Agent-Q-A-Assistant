from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from model_For_Rag import retrieve_top_k

model_id = "openchat/openchat-3.5-0106"
# model_id = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, device_map="auto", torch_dtype="auto"
)

qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

def answer_question(query):
    relevant_chunks = retrieve_top_k(query)
    context = " ".join(relevant_chunks)  # Concatenate relevant chunks
    question = f"Answer based on the context only and write precisely: {context} \n\nQuestion: {query}"

    answer = qa_pipeline(question, max_new_tokens=200)
    return answer[0]['generated_text']

def calculate(query):
  ans = cal(query)
  return ans

def dictionary(query):
  ans = dic(query)
  return ans

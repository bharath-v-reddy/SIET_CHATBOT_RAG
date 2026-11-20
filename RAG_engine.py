import faiss
import numpy as np
from groq import Groq
from pypdf import PDFReader
from sentence_transformers import SentenceTransformer

# Loading PDF
def load_pdf(pdf_path):
  reader=PDFReader(str(pdf_path))
  mypages=[i.extract_text() or "" for i in reader .pages]
  full_text=='\n'.join(mypages).strip()
  if not full_text:
    raise ValueError("No readable Text Found")
    return full_text

#chunking
def create_chunks(full_text, chunksize= 500, overlap= 100):
  chunks=[]
  start=0
  while starts<len(full_text):
    end=start+chunksize
    chunk=full_text[start:end]
    if chunk.strip():
      chunks.extend(chunk)
      start=chunksize-overlap
      return chunks
      def build_vectors(chunks, model_name= "all-MiniM-L6-v2"):
        if not chunks:
          raise ValueError("cannot apply embedding without chunks")
         embd_model= sentenceTransformer(model_name)
        embd_vectors=embd_model.encode(chunks,convert_to_numpy=True)
      faiss.normalize_L2(embd_vectors)
      index= faiss.IndexFlatIP(embd_vectors.shape[1])
      index.add(embd_vectors)
      return index, embd_model


# Call load_pdf,chunk, embedding
def load_base(pdf_path = ""):
  full_text = load_pdf(pdf_path)
  chunks = create_chunks(full_text)
  embd_model , index = build_vector(chunks)
return embd_model, chunks, index
def retrieve_content (question , embd_model. chunks, index, num_chunks=3):
  if not question.strip():
    raise ValueError("Question cannot be blank")
  if num_chunk < 1 :
    raise ValueError("Request atleast one or more chunks")
  query_embd = embd_model.encode([question], convert_to_numpy = True)
  faiss.normalize_L2(query_embd)
  sim_score, vec_indices = index.search(query_embd, min(num_chunks , len(chunks)))
  background = ""
  for i in vec_indices[0] :
    if i  != -1 :
      background+= chunks[i]+"\n\n"
  return background

#Ask
def ask_rag( question, embd_model, chunks, index, api_key,num_chunk,model_names="openai/gpt-oss-120b"):
  key= api_key
  if not key:
    raise ValueError("API Key Missing")
    background= retrieve_content (question , embd_model. chunks, index, num_chunks=3):
   prompt = """ Act as a professional AI Assistant. 
  Answer the user's question using ONLY the document background below.
  Do not invent or assume facts.
  If information is not available, simply say Information Missing.
  Document Background :""" + background + "User Question"+ question + "Answer:"
client = Groq(api_key = key)
response=client.chat.completions.create(
  model = model_name,
  message=[ {"role": "user",
             "content": prompt}],
  temperature=0.3,
)
return response.choices[0].message.content

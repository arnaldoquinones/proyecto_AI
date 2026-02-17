# Smoke test.

import os
from markitdown import MarkItDown
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

class ProcesadorPDFaRAG:
    def __init__(self, ruta_pdf):
        self.ruta_pdf = ruta_pdf
        self.markitdown = MarkItDown()
        
    def convertir_a_markdown(self):
        """Convierte PDF a Markdown manteniendo estructura"""
        print("🔄 Convirtiendo PDF a Markdown...")
        resultado = self.markitdown.convert(self.ruta_pdf)
        return resultado.text_content
    
    def chunkear_por_estructura(self, texto_markdown):
        """Chunking inteligente usando los headers de Markdown"""
        print("✂️  Chunkeando por estructura...")
        
        splitter = MarkdownHeaderTextSplitter([
            ("#", "titulo_1"),
            ("##", "titulo_2"),
            ("###", "titulo_3"),
        ])
        
        chunks = splitter.split_text(texto_markdown)
        print(f"✅ Creados {len(chunks)} chunks")
        return chunks
    
    def procesar_completo(self):
        """Pipeline completo: PDF → Markdown → Chunks → Embeddings"""
        # Paso 1: PDF a Markdown
        markdown = self.convertir_a_markdown()
        
        # Guardar el markdown por si las moscas
        with open("documento_procesado.md", "w", encoding="utf-8") as f:
            f.write(markdown)
        
        # Paso 2: Chunking semántico
        chunks = self.chunkear_por_estructura(markdown)
        
        # Paso 3: Preparar para embedding (texto limpio de cada chunk)
        textos_para_embedding = [chunk.page_content for chunk in chunks]
        metadatos = [chunk.metadata for chunk in chunks]
        
        return textos_para_embedding, metadatos

# 🎯 USO FINAL:
procesador = ProcesadorPDFaRAG("mi_documento.pdf")
textos, metadatos = procesador.procesar_completo()

# Configuramos Nomic en Ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Creamos la biblioteca con FAISS
print("📦 Creando biblioteca FAISS...")
vectorstore = FAISS.from_texts(textos, embeddings, metadatos=metadatos)

# Guardamos la biblioteca para no tener que procesarla de nuevo
vectorstore.save_local("biblioteca_bi_faiss")
print("✅ Biblioteca guardada en carpeta 'biblioteca_bi_faiss'")

# Ahora texts listo para embedding con Chroma, FAISS, etc.
# Los metadatos contienen la info de los headers (título, sección, etc.)
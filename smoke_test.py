# Smoke test.

import os
from markitdown import MarkItDown
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.embeddings import OpenAIEmbeddings  # o el que uses
from langchain.vectorstores import Chroma

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

# 🎯 USO:
procesador = ProcesadorPDFaRAG("mi_documento.pdf")
textos, metadatos = procesador.procesar_completo()

# Ahora texts listo para embedding con Chroma, FAISS, etc.
# Los metadatos contienen la info de los headers (título, sección, etc.)
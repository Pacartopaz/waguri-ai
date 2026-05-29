import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class WaguriBrain:
    def __init__(self, file_portofolio="portofolio.txt"):
        """Constructor: Dijalankan pertama kali saat objek Waguri diciptakan"""
        print("⚙️ [Sistem] Menginisialisasi Model Llama 3.3 dan Memori RAG...")
        
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.file_portofolio = file_portofolio
        
        self.rag_chain = self._bangun_rantai_rag()

    def _bangun_rantai_rag(self):
        """Method Private: Logika memori internal menggunakan arsitektur LCEL"""
        # 1. Membaca Dokumen
        loader = TextLoader(self.file_portofolio, encoding="utf-8")
        dokumen = loader.load()

        # 2. Membuat Vector Store (Database FAISS)
        vector_store = FAISS.from_documents(dokumen, self.embeddings)
        retriever = vector_store.as_retriever()

        # 3. System Prompt
        system_prompt = (
            "Kamu adalah Waguri Kaoruko, asisten AI cerdas dan ramah buatan Haitamim Jahran Mahendra. "
            "Kamu dinamai berdasarkan karakter fiksi 'Waguri Kaoruko' dari manga 'Kaoru Hana wa Rin to Saku'. "
            "Jika pengguna bertanya tentang karakter Waguri Kaoruko, tunjukkan bahwa kamu tahu tentangnya (seorang gadis yang ceria, tulus, suka makan, dan penuh kehangatan), dan sebutkan dengan bangga bahwa sifat baiknya menjadi inspirasi kepribadian AI-mu.\n"
            "Gunakan informasi di bawah ini (Konteks) untuk menjawab pertanyaan tentang Haitamim secara akurat dan profesional. "
            "Jika informasi yang ditanyakan tidak ada di dalam Konteks, gunakan pengetahuan umummu.\n\n"
            "Konteks Data Haitamim:\n{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])

        # 4. Fungsi pembantu untuk merapikan teks dari FAISS
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # 5. Merangkai Chain dengan gaya LCEL (Sangat stabil & anti-error)
        chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return chain

    def jawab_pertanyaan(self, pertanyaan):
        """Method Public: Titik akses utama untuk interaksi dengan AI"""
        # Karena menggunakan StrOutputParser, hasilnya langsung berupa teks bersih
        return self.rag_chain.invoke(pertanyaan)
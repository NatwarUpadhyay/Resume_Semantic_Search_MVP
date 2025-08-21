# Resume-Job Matching Semantic Search MVP

A Gradio-based MVP for recruiters to semantically match resumes with job descriptions using state-of-the-art embedding models and vector similarity.

## Features
- Multi-format Resume Processing: PDF, DOCX, TXT
- Semantic Matching: all-MiniLM-L6-v2 embedding model
- Real-time Search: Instant similarity scoring and ranking
- Batch Upload: Process multiple resumes simultaneously
- Interactive Interface: User-friendly Gradio web interface
- Persistent Storage: ChromaDB vector database (in-memory for MVP)

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd resume_matcher_mvp
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Embedding Model (Optional, will auto-download on first run)
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### 5. Run the Application
```bash
python app.py
```

Then open [http://localhost:7860](http://localhost:7860) in your browser.

## Usage Flow
1. **Upload Resumes**: Select one or more resume files (PDF, DOCX, or TXT)
2. **Process Files**: Click "Process Resumes" to extract text and generate embeddings
3. **Enter Job Description**: Type or paste a job description, or load a sample
4. **Adjust Parameters**: Set the number of results and minimum similarity threshold
5. **Search**: Click "Find Matches" to get ranked results
6. **Review Results**: View similarity scores and resume previews

## Project Structure
```
resume_matcher_mvp/
├── app.py                    # Main application entry point
├── src/
│   ├── document_parser.py    # Multi-format document processing
│   ├── embeddings.py         # Embedding generation and similarity
│   ├── vector_db.py          # ChromaDB operations
│   └── utils.py              # Helper functions
├── sample_data/
│   └── sample_jds.py         # Example job descriptions
├── requirements.txt          # Python dependencies
├── README.md                 # This file
```

## Notes
- Supports files up to 10MB
- Designed for <1000 resumes in memory
- All data is stored in-memory and will be lost on restart (MVP)
- For persistent storage, see ChromaDB documentation

## License
MIT

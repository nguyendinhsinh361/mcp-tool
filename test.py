def estimate_tokens(text):
    from langchain.text_splitter import TokenTextSplitter
    
    # Tạo text splitter với chunk size là 1 token
    text_splitter = TokenTextSplitter(chunk_size=1, chunk_overlap=0)
    
    # Split text thành các chunks
    chunks = text_splitter.split_text(text)
    
    # Số chunks chính là số token ước lượng
    return len(chunks)

print(1111, estimate_tokens("Hello World"))
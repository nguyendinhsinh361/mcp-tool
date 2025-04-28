from langchain.text_splitter import TokenTextSplitter
from typing import Dict, List, Optional, Union


class TokenEstimator:
    """
    Class để ước lượng số token trong văn bản sử dụng LangChain TokenTextSplitter.
    Hỗ trợ nhiều loại tokenizer khác nhau và caching kết quả.
    """

    def __init__(self, encoding_name: str = "cl100k_base", chunk_overlap: int = 0, cache_results: bool = True):
        """
        Khởi tạo TokenEstimator.

        Args:
            encoding_name (str): Tên của encoding sẽ sử dụng (mặc định là cl100k_base cho các mô hình như GPT-4)
            chunk_overlap (int): Số token chồng lấp giữa các chunks (mặc định là 0 cho việc đếm token chính xác)
            cache_results (bool): Có lưu cache kết quả hay không để tránh tính toán lặp lại
        """
        self.encoding_name = encoding_name
        self.chunk_overlap = chunk_overlap
        self.cache_results = cache_results
        self._token_cache = {}
        
        # Khởi tạo text splitter với chunk size là 1 token
        self.text_splitter = TokenTextSplitter(
            encoding_name=encoding_name,
            chunk_size=1,
            chunk_overlap=chunk_overlap
        )

    def estimate_tokens(self, text: str) -> int:
        """
        Ước lượng số token trong văn bản.

        Args:
            text (str): Văn bản cần ước lượng số token

        Returns:
            int: Số token ước tính
        """
        # Kiểm tra cache nếu đã bật tính năng cache
        if self.cache_results and text in self._token_cache:
            return self._token_cache[text]
        
        # Split text thành các chunks
        chunks = self.text_splitter.split_text(text)
        
        # Số chunks chính là số token ước lượng
        token_count = len(chunks)
        
        # Lưu vào cache nếu cần
        if self.cache_results:
            self._token_cache[text] = token_count
            
        return token_count
    
    def estimate_tokens_batch(self, texts: List[str]) -> List[int]:
        """
        Ước lượng số token cho một danh sách các văn bản.
        
        Args:
            texts (List[str]): Danh sách các văn bản cần ước lượng
            
        Returns:
            List[int]: Danh sách số token tương ứng
        """
        return [self.estimate_tokens(text) for text in texts]
    
    def estimate_cost(self, text: str, input_price: float, output_price: Optional[float] = None) -> Dict[str, Union[int, float]]:
        """
        Ước lượng chi phí dựa trên số token và giá theo USD/1M token.
        
        Args:
            text (str): Văn bản cần tính chi phí
            input_price (float): Giá cho input token (USD/1M token)
            output_price (Optional[float]): Giá cho output token nếu cần tính cả output
            
        Returns:
            Dict[str, Union[int, float]]: Dictionary chứa số token và chi phí
        """
        token_count = self.estimate_tokens(text)
        input_cost = (token_count / 1_000_000) * input_price
        
        result = {
            "token_count": token_count,
            "input_cost_usd": input_cost
        }
        
        if output_price is not None:
            # Giả định rằng kích thước output là một nửa kích thước input (có thể thay đổi theo nhu cầu)
            estimated_output_tokens = token_count // 2
            output_cost = (estimated_output_tokens / 1_000_000) * output_price
            result["estimated_output_tokens"] = estimated_output_tokens
            result["output_cost_usd"] = output_cost
            result["total_cost_usd"] = input_cost + output_cost
            
        return result
    
    def clear_cache(self) -> None:
        """Xóa cache token."""
        self._token_cache.clear()
        
    def __str__(self) -> str:
        return f"TokenEstimator(encoding={self.encoding_name}, cache_enabled={self.cache_results})"


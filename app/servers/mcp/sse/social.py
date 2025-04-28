"""
Social MCP Server implementation.
Provides basic social operations, weather information, and Kpop idol details.
Returns all data as formatted strings.
"""
from typing import Optional
from app.core.config import settings
from app.core.exceptions import ToolError
from app.servers.mcp.sse.base import BaseMCPServer

class SocialServer(BaseMCPServer):
    """MCP server for social operations"""
    
    def __init__(self):
        """Initialize the social server with default port"""
        port = settings.SOCIAL_PORT
        super().__init__("Social", port=port)
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register all social tools with the MCP server"""
        
        @self.mcp.tool()
        def get_weather(city: str, country: Optional[str] = None) -> str:
            """
            날씨 정보를 가져옵니다.
            특정 도시의 현재 날씨 상태, 온도, 습도 및 기타 관련 정보를 제공합니다.
            
            사용 예시: get_weather("서울", "한국")은 서울의 날씨 정보를 문자열로 반환합니다.
            
            Parameters:
                city (str): 날씨 정보를 가져올 도시 이름
                country (str, optional): 국가 이름 (선택 사항)
                
            Returns:
                str: 날씨 정보를 포함하는 형식화된 문자열
            """
            try:
                self.logger.info(f"Getting weather for {city}, {country if country else 'N/A'}")
                
                # 여기에 실제 날씨 API 호출 코드가 들어갑니다
                # 지금은 예시 데이터를 반환합니다
                
                weather_data = {
                    "city": city,
                    "country": country if country else "정보 없음",
                    "temperature": 22,  # 섭씨
                    "condition": "맑음",
                    "humidity": 65,  # 퍼센트
                    "wind_speed": 10,  # km/h
                    "timestamp": "2025-04-26T14:30:00"
                }
                
                # 데이터를 문자열로 형식화
                weather_str = (
                    f"도시: {weather_data['city']}\n"
                    f"국가: {weather_data['country']}\n"
                    f"온도: {weather_data['temperature']}°C\n"
                    f"상태: {weather_data['condition']}\n"
                    f"습도: {weather_data['humidity']}%\n"
                    f"풍속: {weather_data['wind_speed']} km/h\n"
                    f"측정 시간: {weather_data['timestamp']}"
                )
                
                return weather_str
                
            except Exception as e:
                self.logger.error(f"Error fetching weather data: {str(e)}")
                raise ToolError(f"날씨 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
        
        @self.mcp.tool()
        def get_kpop_idol_info(idol_name: str) -> str:
            """
            K-Pop 아이돌에 대한 정보를 제공합니다.
            아이돌의 이름, 그룹, 데뷔일, 소속사 및 기타 관련 정보를 포함합니다.
            
            사용 예시: get_kpop_idol_info("지민")은 BTS의 지민에 대한 정보를 문자열로 반환합니다.
            
            Parameters:
                idol_name (str): 정보를 검색할 아이돌의 이름
                
            Returns:
                str: 아이돌 정보를 포함하는 형식화된 문자열
            """
            try:
                self.logger.info(f"Getting information for Kpop idol: {idol_name}")
                
                # 여기에 실제 아이돌 정보 데이터베이스 또는 API 호출 코드가 들어갑니다
                # 지금은 몇 가지 인기 아이돌에 대한 예시 데이터를 반환합니다
                
                idol_database = {
                    "지민": {
                        "full_name": "박지민 (Park Jimin)",
                        "group": "BTS",
                        "position": ["주보컬", "리드댄서"],
                        "birth_date": "1995-10-13",
                        "agency": "HYBE (Big Hit Music)",
                        "debut_date": "2013-06-13",
                        "blood_type": "A",
                        "instagram": "@j.m"
                    },
                    "아이유": {
                        "full_name": "이지은 (Lee Ji-eun)",
                        "group": "솔로",
                        "position": ["보컬"],
                        "birth_date": "1993-05-16",
                        "agency": "EDAM 엔터테인먼트",
                        "debut_date": "2008-09-18",
                        "blood_type": "A",
                        "instagram": "@dlwlrma"
                    },
                    "윈터": {
                        "full_name": "김민정 (Kim Minjeong)",
                        "group": "aespa",
                        "position": ["리드보컬", "리드댄서"],
                        "birth_date": "2001-01-01",
                        "agency": "SM 엔터테인먼트",
                        "debut_date": "2020-11-17",
                        "blood_type": "O",
                        "instagram": "@aespa_official"
                    }
                }
                
                if idol_name in idol_database:
                    idol_info = idol_database[idol_name]
                    
                    # 포지션 리스트를 문자열로 변환
                    positions = ", ".join(idol_info["position"])
                    
                    # 데이터를 문자열로 형식화
                    idol_str = (
                        f"이름: {idol_info['full_name']}\n"
                        f"그룹: {idol_info['group']}\n"
                        f"포지션: {positions}\n"
                        f"생년월일: {idol_info['birth_date']}\n"
                        f"소속사: {idol_info['agency']}\n"
                        f"데뷔일: {idol_info['debut_date']}\n"
                        f"혈액형: {idol_info['blood_type']}\n"
                        f"인스타그램: {idol_info['instagram']}"
                    )
                    
                    return idol_str
                else:
                    similar_idols = [name for name in idol_database.keys() 
                                    if idol_name.lower() in name.lower()]
                    
                    if similar_idols:
                        suggestion_msg = f"'{idol_name}'을(를) 찾을 수 없습니다. 혹시 다음 중 하나를 찾으시나요? {', '.join(similar_idols)}"
                        raise ToolError(suggestion_msg)
                    else:
                        raise ToolError(f"'{idol_name}'에 대한 정보를 찾을 수 없습니다.")
                
            except Exception as e:
                if isinstance(e, ToolError):
                    raise e
                self.logger.error(f"Error fetching idol information: {str(e)}")
                raise ToolError(f"아이돌 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
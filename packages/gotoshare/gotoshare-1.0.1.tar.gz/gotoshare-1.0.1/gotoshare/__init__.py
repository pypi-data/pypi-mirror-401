import httpx
import pandas as pd
from typing import Optional, List  # GotoShare SDK - 与tushare接口兼容
__version__ = '1.0.1'
__all__ = ['pro_api', 'GotoShareAPI']

class GotoShareAPI:
    def __init__(self, server_url: str, token: str = None, timeout: int = 30):
        self.url = server_url.rstrip('/')
        self.token = token
        self.timeout = timeout
        self.headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    def _request(self, api_name: str, **kwargs) -> pd.DataFrame:  # 发送请求并返回DataFrame
        params = {k: v for k, v in kwargs.items() if v is not None}
        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers) as c:
                r = c.post(f"{self.url}/api/query", json={"api_name": api_name, "params": params})
                if r.status_code == 401: raise Exception("认证失败: 缺少token")
                if r.status_code == 403: raise Exception("认证失败: token无效或已禁用")
                r.raise_for_status()
                data = r.json().get('data', [])
                return pd.DataFrame(data) if data else pd.DataFrame()
        except httpx.HTTPStatusError as e: raise Exception(f"请求失败({e.response.status_code}): {e.response.text}")
        except Exception as e: raise Exception(f"请求失败: {e}")
    
    def stock_basic(self, ts_code: Optional[str] = None, exchange: Optional[str] = None, list_status: Optional[str] = None, fields: Optional[List[str]] = None) -> pd.DataFrame:
        return self._request('stock_basic', ts_code=ts_code, exchange=exchange, list_status=list_status, fields=fields)
    
    def daily(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        return self._request('daily', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)
    
    def weekly(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        return self._request('weekly', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)
    
    def monthly(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        return self._request('monthly', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)
    
    def daily_basic(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        return self._request('daily_basic', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)

def pro_api(server_url: str, token: str = None, timeout: int = 30) -> GotoShareAPI:  # 创建API实例
    return GotoShareAPI(server_url, token, timeout)

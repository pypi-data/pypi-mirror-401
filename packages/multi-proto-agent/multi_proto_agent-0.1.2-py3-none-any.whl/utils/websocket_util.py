import threading
import time
import queue
import struct
from websocket import WebSocketApp, ABNF
from utils.logger_config import get_logger

logger = get_logger(__name__)

class WebSocketClient:
    """WebSocket客户端类，封装WebSocket连接的所有操作"""
    
    def __init__(self, length_prefix_bytes=2, account_id=None):
        self.ws = None
        self.is_connected = False
        self.message_queue = queue.Queue()  # 消息队列，用于存储收到的消息
        # 线程安全的退出标志（跨线程可见），用于抑制关闭过程中的回调日志等
        self.exit_flag = threading.Event()
        self.url = None
        self.headers = None
        self.length_prefix_bytes = length_prefix_bytes  # 长度前缀字节数，默认为0，0表示不处理长度前缀
        self.account_id = account_id  # 账号ID
        self.connection_error = None  # 存储连接错误，用于跨线程传递异常
    
    def connect(self, ws_url, secret_key=None):
        """建立WebSocket连接
        
        Args:
            ws_url (str): WebSocket服务器地址
            secret_key (str): 连接密钥
            headers (dict): 连接头信息
            auto_start_receiver (bool): 是否自动启动接收线程
            
        Returns:
            bool: 连接是否成功
            
        Raises:
            ConnectionError: 连接失败时抛出
        """
        logger.info(f"----{self.account_id}WebSocket开始建立连接")
        self.url = ws_url
        self.headers = ["Connection: Upgrade",
                        "Upgrade: websocket",
                        "Sec-WebSocket-Version: 13",
                        f"Sec-WebSocket-Key: {secret_key}"]
        try:
            # 重置状态
            self.exit_flag.clear()
            self.connection_error = None  # 重置错误标志
            
            # 创建WebSocket连接
            self.ws = WebSocketApp(
                self.url,
                # header=self.headers,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # 创建独立线程用于建立WebSocket连接
            self.thread = threading.Thread(target=self._connect_and_listen)
            self.thread.daemon = True
            self.thread.start()
            
            # 等待连接建立，设置超时时间
            timeout = 3  # 3秒超时
            start_time = time.time()
            while not self.is_connected and time.time() - start_time < timeout:
                # 检查是否有连接错误
                if self.connection_error:
                    self.close()
                    raise self.connection_error
                time.sleep(0.1)
            
            # 检查连接状态
            if not self.is_connected:
                self.close()
                error_msg = (
                    self.connection_error.args[0] if self.connection_error 
                    else f"{self.account_id} WebSocket连接失败：等待{timeout}秒后仍未建立连接"
                )
                raise ConnectionError(error_msg)
            
            return True
        except ConnectionError:
            # 重新抛出连接错误
            raise
        except Exception as e:
            logger.error(f"----{self.account_id}WebSocket连接异常: {str(e)}")
            self.close()
            raise ConnectionError(f"{self.account_id} WebSocket连接异常: {str(e)}") from e
    
    def _connect_and_listen(self):
        """在独立线程中建立连接并监听消息"""
        try:
            logger.info(f"----{self.account_id}WebSocket开始监听")
            self.ws.run_forever(ping_interval=10, ping_timeout=9, ping_payload="ping")
        except Exception as e:
            # 异常会通过 on_error 回调传递，这里只记录日志
            if not self.exit_flag.is_set():
                logger.error(f"----{self.account_id}WebSocket监听异常: {str(e)}")
        finally:
            logger.info(f"----{self.account_id}WebSocket结束监听")
            # 线程内部不处理清理，只更新状态
            # 清理工作由外部通过 close() 统一处理
            self.is_connected = False
            # 不设置 exit_flag，由外部调用 close() 时设置
            # 不关闭 ws，由外部统一关闭

    def _on_open(self, ws): 
        """WebSocket连接打开回调"""
        try:
            # 双重验证：检查 sock 属性确保连接真正建立
            if ws.sock is not None:
                self.is_connected = True
                logger.info(f"----{self.account_id}的WebSocket连接已打开（握手完成）")
            else:
                logger.warning(f"----{self.account_id}的WebSocket on_open 回调触发，但 sock 为 None，连接可能未完全建立")
                self.is_connected = False
                self.connection_error = ConnectionError(
                    f"{self.account_id}的WebSocket连接失败：on_open 回调触发但 sock 为 None"
                )
        except Exception as e:
            self.connection_error = e
            self.is_connected = False
    
    def _on_message(self, ws, message):
        """WebSocket接收消息回调"""
        if self.length_prefix_bytes > 0 and isinstance(message, bytes):
            # 如果设置了长度前缀且消息是二进制数据，则去掉长度前缀
            if len(message) >= self.length_prefix_bytes:
                # 从消息中去掉长度前缀
                actual_message = message[self.length_prefix_bytes:]
                self.message_queue.put(actual_message)  # 将去掉前缀后的消息放入队列
                # logger.debug(f"----WebSocket收到消息，去掉{self.length_prefix_bytes}字节长度前缀后: {actual_message}")
            else:
                # 消息长度不足，直接放入队列
                self.message_queue.put(message)
                # logger.debug(f"----WebSocket收到消息(长度不足，未去前缀): {message}")
        else:
            # 不需要处理长度前缀，直接放入队列
            self.message_queue.put(message)
            # logger.debug(f"----WebSocket收到消息: {message}")
    
    def _on_error(self, ws, error):
        """WebSocket错误回调"""
        if not self.exit_flag.is_set():
            logger.error(f"----{self.account_id}WebSocket错误: {str(error)}")
    
    def _is_websocket_ready(self):
        """检查 WebSocket 是否真正就绪（双重验证）
        
        Returns:
            bool: True 表示连接已建立且握手完成，可以发送消息
        """
        return (self.is_connected and 
                self.ws is not None and 
                hasattr(self.ws, 'sock') and 
                self.ws.sock is not None)
    
    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket连接关闭回调"""
        if not self.exit_flag.is_set():
            logger.info(f"----{self.account_id}WebSocket连接关闭: code={close_status_code}, reason={close_msg}")
        self.is_connected = False
        # 验证 sock 状态（关闭后应该为 None）
        if hasattr(ws, 'sock') and ws.sock is not None:
            logger.warning(f"----{self.account_id}警告：连接关闭但 sock 仍不为 None")
    
    def send(self, message_bytes:bytes):
        """发送消息到WebSocket服务器"""
        if not self._is_websocket_ready():
            logger.warning(f"----{self.account_id}WebSocket未连接，无法发送消息")
            return False
        try:
            # 处理字符串消息添加长度前缀
            if self.length_prefix_bytes > 0:
                # 添加长度前缀
                if self.length_prefix_bytes == 2:
                    length_prefix = struct.pack(">H", len(message_bytes))
                elif self.length_prefix_bytes == 4:
                    length_prefix = struct.pack(">I", len(message_bytes))
                else:
                    raise ValueError(f"不支持的长度前缀字节数: {self.length_prefix_bytes}")
                # 组合长度前缀和消息体
                full_message = length_prefix + message_bytes
                # logger.debug(f"----WebSocket发送消息的长度前缀: {length_prefix.hex()}")
                # logger.debug(f"----WebSocket发送消息(带长度前缀)，原始长度: {len(message_bytes)}，总长度: {len(length_prefix + message_bytes)}")
                # 以二进制形式发送
                self.ws.send(full_message, opcode=ABNF.OPCODE_BINARY)
                # logger.debug(f"----WebSocket发送消息(带长度前缀): {message_bytes.hex()}")
            else:
                # 不需要添加长度前缀，直接发送
                self.ws.send(message_bytes)
                # logger.debug(f"----WebSocket发送消息(不带前缀): {message_bytes.hex()}")
            return True
        except Exception as e:
            logger.error(f"----{self.account_id}WebSocket发送消息异常: {str(e)}")
            return False
    
    def send_binary(self, binary_data:bytes):
        """发送二进制数据到WebSocket服务器"""
        if not self._is_websocket_ready():
            logger.warning(f"----{self.account_id}WebSocket未连接，无法发送二进制数据")
            return False
        try:
            # 处理二进制数据添加长度前缀
            if self.length_prefix_bytes > 0:
                # 添加长度前缀
                if self.length_prefix_bytes == 2:
                    length_prefix = struct.pack(">H", len(binary_data))
                elif self.length_prefix_bytes == 4:
                    length_prefix = struct.pack(">I", len(binary_data))
                else:
                    raise ValueError(f"不支持的长度前缀字节数: {self.length_prefix_bytes}")
                # 组合长度前缀和二进制数据
                full_data = length_prefix + binary_data
                # 发送带长度前缀的二进制数据
                self.ws.send(full_data, opcode=ABNF.OPCODE_BINARY)
                logger.info(f"----{self.account_id}WebSocket发送二进制数据(带长度前缀)，原始长度: {len(binary_data)}，总长度: {len(full_data)}")
            else:
                # 不需要添加长度前缀，直接发送
                self.ws.send(binary_data, opcode=ABNF.OPCODE_BINARY)
                logger.info(f"----{self.account_id}WebSocket发送二进制数据，长度: {len(binary_data)}")
            return True
        except Exception as e:
            logger.error(f"----{self.account_id}WebSocket发送二进制数据异常: {str(e)}")
            return False
    
    def close(self):
        """关闭WebSocket连接（统一清理入口）"""
        if not self.exit_flag.is_set():
            self.exit_flag.set()
            try:
                # 检查当前线程是否是连接线程，避免 join 自己
                import threading
                current_thread = threading.current_thread()
                is_in_thread = (hasattr(self, 'thread') and 
                               self.thread is not None and 
                               current_thread == self.thread)
                
                # 如果不是在连接线程内部，等待线程结束
                if not is_in_thread and hasattr(self, 'thread') and self.thread and self.thread.is_alive():
                    self.thread.join(timeout=2)
                
                # 关闭WebSocket连接
                if self.ws:
                    try:
                        self.ws.close()
                    except Exception as e:
                        logger.error(f"----{self.account_id}WebSocket关闭连接异常: {str(e)}")
                
                logger.info(f"----{self.account_id}WebSocket连接已关闭")
            except Exception as e:
                logger.error(f"----{self.account_id}WebSocket关闭异常: {str(e)}")
            finally:
                # 统一清理资源
                self.ws = None
                self.is_connected = False
                if hasattr(self, 'thread'):
                    self.thread = None


# def get_websocket_connection(ws_url, headers=None):
#     """创建并返回一个WebSocket连接"""
#     ws_client = WebSocketClient()
#     if ws_client.connect(ws_url, headers):
#         return ws_client
#     else:
#         ws_client.close()
#         raise Exception(f"Failed to establish WebSocket connection to {ws_url}")

if __name__ == "__main__":
    # 示例用法
    # 创建WebSocket客户端
    ws_client = WebSocketClient()
    
    # 这里需要替换为实际的WebSocket服务器地址
    # ws_url = "ws://echo.websocket.org"
    # ws_client.connect(ws_url)
    
    # 保持程序运行一段时间以接收消息
    # time.sleep(10)
    
    # 关闭连接
    # ws_client.close()
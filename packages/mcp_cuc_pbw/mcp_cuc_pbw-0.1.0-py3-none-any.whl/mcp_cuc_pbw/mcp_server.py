#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Implementation

This server provides a tool to get the current time with optional timezone support.
"""

import datetime
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional
import pytz  # 回退到 pytz 以确保兼容性


class MCPRequestHandler(BaseHTTPRequestHandler):
    """MCP Request Handler to process incoming requests"""
    
    def do_POST(self) -> None:
        """Handle POST requests from MCP clients"""
        # 获取请求体长度
        content_length = int(self.headers['Content-Length'])
        # 读取请求体
        post_data = self.rfile.read(content_length)
        # 解析JSON请求
        request = json.loads(post_data.decode('utf-8'))
        
        # 处理请求
        response = self._process_request(request)
        
        # 发送响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process the MCP request and return the response"""
        # 获取工具名称
        tool_name = request.get('tool', '')
        
        if tool_name == 'get_current_time':
            return self._handle_get_current_time(request)
        else:
            return {
                'error': f"Unknown tool: {tool_name}",
                'tool': tool_name
            }
    
    def _handle_get_current_time(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the get_current_time tool request"""
        try:
            # 获取时区参数
            params = request.get('params', {})
            timezone = params.get('timezone')
            
            # 记录调试信息
            print(f"Received request with timezone: {timezone}")
            
            if timezone:
                try:
                    # 使用指定时区
                    tz = pytz.timezone(timezone)
                    current_time = datetime.datetime.now(tz)
                except pytz.UnknownTimeZoneError:
                    return {
                        'tool': 'get_current_time',
                        'error': f"Unknown timezone: {timezone}"
                    }
            else:
                # 使用本地时区
                current_time = datetime.datetime.now()
            
            # 格式化时间
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                'tool': 'get_current_time',
                'result': {
                    'current_time': time_str,
                    'timezone': timezone or 'local'
                }
            }
        except Exception as e:
            # 记录详细错误信息
            print(f"Error handling request: {e}")
            import traceback
            traceback.print_exc()
            return {
                'tool': 'get_current_time',
                'error': f"Internal server error: {str(e)}"
            }


def run_server(host: str = 'localhost', port: int = 8000) -> None:
    """Run the MCP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    print(f"MCP Server running on http://{host}:{port}")
    print("Available tools:")
    print("- get_current_time: Get the current time")
    print("  Parameters:")
    print("    timezone (optional): Timezone string (e.g., 'Asia/Shanghai', 'UTC')")
    print("\nExample request:")
    print('''
{
  "tool": "get_current_time",
  "params": {
    "timezone": "Asia/Shanghai"
  }
}
''')
    httpd.serve_forever()


def main() -> None:
    """Main function for running the MCP server from command line"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    args = parser.parse_args()
    
    # 运行服务器
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
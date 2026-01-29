#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Implementation

This server provides a tool to get the current time with optional timezone support.
"""

import datetime
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import pytz  # For timezone support


class MCPRequestHandler(BaseHTTPRequestHandler):
    """MCP Request Handler to process incoming requests"""
    
    def do_POST(self):
        """Handle POST requests from MCP clients"""
        try:
            # Read request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request = json.loads(post_data.decode('utf-8'))
            
            print(f"Received request: {request}")
            
            # Get tool name
            tool_name = request.get('tool', '').lower()
            
            # Handle different tools
            if tool_name == 'list-tools':
                # Return list of available tools
                response = {
                    'tool': 'list-tools',
                    'result': {
                        'tools': [
                            {
                                'name': 'get_current_time',
                                'description': 'Get the current time with optional timezone support',
                                'parameters': {
                                    'timezone': {
                                        'type': 'string',
                                        'description': 'Timezone string (e.g., Asia/Shanghai, UTC)',
                                        'required': False
                                    }
                                }
                            }
                        ]
                    }
                }
            elif tool_name == 'get_current_time':
                # Get current time with optional timezone
                params = request.get('params', {})
                timezone = params.get('timezone')
                
                try:
                    if timezone:
                        tz = pytz.timezone(timezone)
                        current_time = datetime.datetime.now(tz)
                    else:
                        current_time = datetime.datetime.now()
                    
                    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    response = {
                        'tool': 'get_current_time',
                        'result': {
                            'current_time': time_str,
                            'timezone': timezone or 'local'
                        }
                    }
                except pytz.UnknownTimeZoneError:
                    response = {
                        'tool': 'get_current_time',
                        'error': f"Unknown timezone: {timezone}"
                    }
            else:
                # Unknown tool
                response = {
                    'error': f"Unknown tool: {request.get('tool')}",
                    'tool': request.get('tool', '')
                }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"Error in do_POST: {e}")
            import traceback
            traceback.print_exc()
            
            # Send error response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                'error': f"Internal server error: {str(e)}",
                'tool': request.get('tool', '') if 'request' in locals() else ''
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))


def run_server(host: str = 'localhost', port: int = 8000) -> None:
    """Run the MCP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    print(f"MCP Server running on http://{host}:{port}")
    print("Available tools:")
    print("- list-tools: List all available tools")
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    args = parser.parse_args()
    
    # Run the server
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
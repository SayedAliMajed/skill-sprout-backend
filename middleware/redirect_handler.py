from fastapi import Request
from fastapi.responses import JSONResponse
from urllib.parse import urlparse


class RedirectMiddleware:
    """Middleware to handle trailing slash requests by serving content directly"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Only handle GET requests to avoid interfering with POST/PUT/DELETE
            if request.method == "GET":
                path = request.url.path
                
                # Check if this is an API route without trailing slash that should have one
                if self._should_redirect(path):
                    # Create a new scope with the trailing slash path
                    new_scope = dict(scope)
                    new_scope["path"] = path + "/"
                    
                    # Process the request with the new path
                    await self.app(new_scope, receive, send)
                    return
            
            # For all other cases, proceed normally
            await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
    
    def _should_redirect(self, path):
        """Check if the path should be served with trailing slash"""
        # Only handle API routes that don't end with slash and aren't parameterized
        if (path.startswith("/api/") and 
            not path.endswith("/") and 
            "{" not in path and  # Don't redirect parameterized routes like /api/courses/{id}
            not path.endswith("login") and  # Don't redirect login endpoint
            not path.endswith("register")):  # Don't redirect register endpoint
            return True
        return False

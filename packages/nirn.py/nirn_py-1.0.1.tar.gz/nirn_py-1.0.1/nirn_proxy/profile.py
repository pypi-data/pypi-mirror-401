"""Profile server for runtime performance profiling."""
import asyncio
import logging
from aiohttp import web
import cProfile
import pstats
import io
from typing import Optional

logger = logging.getLogger(__name__)


class ProfileServer:
    """
    HTTP server for runtime profiling (pprof-compatible endpoints).
    
    Provides CPU, memory, and async task profiling.
    """
    
    def __init__(self, bind_ip: str = "0.0.0.0", port: int = 7654):
        self.bind_ip = bind_ip
        self.port = port
        self.app: Optional[web.Application] = None
        self.runner: Optional[web.AppRunner] = None
        self.site: Optional[web.TCPSite] = None
        self.profiler: Optional[cProfile.Profile] = None
        
    async def start(self):
        """Start the profile server."""
        self.app = web.Application()
        self.app.router.add_get("/debug/pprof/", self.handle_index)
        self.app.router.add_get("/debug/pprof/profile", self.handle_profile)
        self.app.router.add_get("/debug/pprof/heap", self.handle_heap)
        self.app.router.add_get("/debug/pprof/tasks", self.handle_tasks)
        self.app.router.add_get("/debug/pprof/cmdline", self.handle_cmdline)
        
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        self.site = web.TCPSite(self.runner, self.bind_ip, self.port)
        await self.site.start()
        
        logger.info(f"Profiling endpoints loaded on :{self.port}")
        
    async def stop(self):
        """Stop the profile server."""
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()
            
    async def handle_index(self, request: web.Request) -> web.Response:
        """Handle index page showing available profiles."""
        html = """
        <html>
        <head><title>pprof</title></head>
        <body>
        <h1>pprof</h1>
        <p>Available profiles:</p>
        <ul>
        <li><a href="/debug/pprof/profile">CPU Profile</a></li>
        <li><a href="/debug/pprof/heap">Heap Profile</a></li>
        <li><a href="/debug/pprof/tasks">Async Tasks Profile</a></li>
        <li><a href="/debug/pprof/cmdline">Command Line</a></li>
        </ul>
        </body>
        </html>
        """
        return web.Response(text=html, content_type="text/html")
        
    async def handle_profile(self, request: web.Request) -> web.Response:
        """Handle CPU profiling."""
        seconds = int(request.query.get("seconds", "30"))
        
        # Start profiling
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Profile for specified duration
        await asyncio.sleep(seconds)
        
        # Stop profiling
        profiler.disable()
        
        # Generate stats
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats()
        
        return web.Response(text=s.getvalue(), content_type="text/plain")
        
    async def handle_heap(self, request: web.Request) -> web.Response:
        """Handle heap profiling (memory usage)."""
        try:
            import tracemalloc
            import gc
            
            # Force garbage collection
            gc.collect()
            
            # Get memory statistics
            if tracemalloc.is_tracing():
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.statistics('lineno')
                
                output = io.StringIO()
                output.write("Top 50 memory allocations:\n\n")
                for stat in top_stats[:50]:
                    output.write(f"{stat}\n")
                
                return web.Response(text=output.getvalue(), content_type="text/plain")
            else:
                return web.Response(
                    text="Memory tracing not enabled. Start with tracemalloc.start()",
                    content_type="text/plain"
                )
        except Exception as e:
            return web.Response(text=f"Error: {e}", content_type="text/plain")
    
    async def handle_tasks(self, request: web.Request) -> web.Response:
        """Handle asyncio tasks profiling."""
        try:
            tasks = asyncio.all_tasks()
            output = io.StringIO()
            output.write(f"Active asyncio tasks: {len(tasks)}\n\n")
            
            for task in tasks:
                output.write(f"Task: {task.get_name()}\n")
                output.write(f"  State: {'running' if not task.done() else 'done'}\n")
                if task.get_coro():
                    output.write(f"  Coro: {task.get_coro()}\n")
                output.write("\n")
            
            return web.Response(text=output.getvalue(), content_type="text/plain")
        except Exception as e:
            return web.Response(text=f"Error: {e}", content_type="text/plain")
    
    async def handle_cmdline(self, request: web.Request) -> web.Response:
        """Handle command line info."""
        import sys
        return web.Response(text=" ".join(sys.argv), content_type="text/plain")


async def start_profile_server(bind_ip: str = "0.0.0.0", port: int = 7654) -> ProfileServer:
    """Start the profile server."""
    server = ProfileServer(bind_ip, port)
    await server.start()
    return server
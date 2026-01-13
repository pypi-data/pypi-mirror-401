"""Main entry point for the nirn.py server."""
import asyncio
import logging
import signal
import sys
from aiohttp import web
from .config import Config
from .queue_manager import QueueManager
from .metrics import start_metrics_server
from .profile import start_profile_server


# Global logger
logger = logging.getLogger("nirn.py")

# Default buffer size
buffer_size = 50


def setup_logger(log_level: str):
    """Setup logging with the specified level."""
    level_map = {
        "trace": logging.DEBUG,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARNING,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "fatal": logging.CRITICAL,
        "panic": logging.CRITICAL,
    }
    
    level = level_map.get(log_level.lower(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Reduce noise from aiohttp
    logging.getLogger('aiohttp.access').setLevel(logging.WARNING)


async def create_app(config: Config) -> web.Application:
    """Create and configure the application."""
    queue_manager = QueueManager(config)
    await queue_manager.initialize()
    
    app = queue_manager.create_app()
    app['queue_manager'] = queue_manager
    
    return app


async def cleanup_app(app: web.Application):
    """Cleanup application resources."""
    queue_manager = app.get('queue_manager')
    if queue_manager:
        await queue_manager.shutdown()


async def main_async():
    """
    Main async function.
    
    Initialization order:
    1. Configure Discord HTTP client
    2. Setup logger
    3. Create queue manager
    4. Start optional servers (pprof, metrics)
    5. Start HTTP server
    6. Wait for server ready, then init cluster
    7. Wait for shutdown signal
    8. Graceful shutdown
    """
    # Load configuration
    config = Config()
    
    # Setup logging
    setup_logger(config.log_level)
    
    # Update buffer size from config
    global buffer_size
    buffer_size = config.buffer_size
    
    # Start profile server if enabled
    profile_server = None
    if config.enable_pprof:
        try:
            profile_server = await start_profile_server(config.bind_ip, 7654)
        except Exception as e:
            logger.error(f"Failed to start profile server: {e}")
    
    # Start metrics server if enabled
    if config.enable_metrics:
        try:
            start_metrics_server(config.bind_ip, config.metrics_port)
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")
            return 1
    
    # Create application
    try:
        app = await create_app(config)
    except Exception as e:
        logger.error(f"Failed to create application: {e}")
        return 1
    
    # Setup graceful shutdown
    shutdown_event = asyncio.Event()
    
    def signal_handler():
        logger.info("Server received shutdown signal")
        shutdown_event.set()
    
    if sys.platform != 'win32':
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, signal_handler)
    
    # Create and start web server
    runner = web.AppRunner(
        app,
        access_log=None if config.log_level.upper() != "DEBUG" else logging.getLogger('aiohttp.access')
    )
    await runner.setup()
    
    # Server configuration with appropriate timeouts
    site = web.TCPSite(
        runner,
        config.bind_ip,
        config.port,
        reuse_address=True,
        reuse_port=True if sys.platform != 'win32' else False
    )
    
    try:
        await site.start()
        logger.info(f"Started proxy on {config.bind_ip}:{config.port}")
        
        # Wait a second for HTTP server to be ready before joining cluster
        await asyncio.sleep(1.0)
        
        # Note: Cluster init happens in QueueManager.initialize() already
        
        # Wait for shutdown signal
        if sys.platform == 'win32':
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
        else:
            await shutdown_event.wait()
            
    except Exception as e:
        logger.error(f"Server error: {e}")
        return 1
    
    finally:
        logger.info("Broadcasting leave message to cluster, if in cluster mode")
        
        # Cleanup resources
        await cleanup_app(app)
        
        logger.info("Gracefully shutting down HTTP server")
        await runner.cleanup()
        
        if profile_server:
            await profile_server.stop()
        
        logger.info("Bye bye")
    
    return 0


def main():
    """Main entry point."""
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        exit_code = asyncio.run(main_async())
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
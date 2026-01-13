"""Memberlist implementation for cluster membership and discovery."""
import asyncio
import json
import socket
import time
import random
import os
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from .util import get_local_ip, generate_node_name


logger = logging.getLogger(__name__)


@dataclass
class Node:
    """Node in the cluster."""
    name: str
    addr: str
    port: int
    meta: bytes
    state: str = "alive"
    
    def address(self) -> str:
        return f"{self.addr}:{self.port}"


class MemberlistDelegate:
    """
    Delegate for memberlist events.
    
    Contains callbacks for join/leave events.
    """
    
    def __init__(self):
        self.on_join: Optional[Callable[[Node], None]] = None
        self.on_leave: Optional[Callable[[Node], None]] = None
        self.on_update: Optional[Callable[[Node], None]] = None
        
    async def notify_join(self, node: Node):
        if self.on_join:
            self.on_join(node)
            
    async def notify_leave(self, node: Node):
        if self.on_leave:
            self.on_leave(node)
            
    async def notify_update(self, node: Node):
        if self.on_update:
            self.on_update(node)


class Memberlist:
    """
    Memberlist for cluster membership and discovery.
    
    Uses UDP for gossip-based membership with failure detection.
    """
    
    def __init__(self, bind_port: int, proxy_port: str, delegate: MemberlistDelegate):
        self.bind_port = bind_port
        self.proxy_port = proxy_port
        self.delegate = delegate
        
        # Support NODE_NAME override like Go
        node_name = os.getenv("NODE_NAME", "")
        if node_name:
            name = node_name
        else:
            name = generate_node_name()
        
        # Local node
        self.local_node = Node(
            name=name,
            addr=get_local_ip(),
            port=bind_port,
            meta=proxy_port.encode()
        )
        
        # Member tracking
        self.members: Dict[str, Node] = {self.local_node.name: self.local_node}
        self.failed_members: Dict[str, float] = {}
        
        # Network
        self.socket: Optional[socket.socket] = None
        self.running = False
        
    async def start(self, existing_members: List[str]) -> None:
        """Start the memberlist and join existing members."""
        # Create UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", self.bind_port))
        self.socket.setblocking(False)
        
        self.running = True
        
        # Start background tasks
        asyncio.create_task(self._listen_loop())
        asyncio.create_task(self._gossip_loop())
        asyncio.create_task(self._failure_detector_loop())
        
        # Join existing members
        if existing_members:
            for member_addr in existing_members:
                await self._join_member(member_addr)
            
            # Log connected nodes like Go
            member_names = " ".join(m.name for m in self.members.values())
            logger.info(f"Connected to cluster nodes: [ {member_names}]")
        else:
            logger.info("Running in stand-alone mode")
                
    async def stop(self, timeout: float = 30.0) -> None:
        """Stop the memberlist and leave the cluster."""
        self.running = False
        
        # Send leave messages to all members
        leave_msg = {
            "type": "leave",
            "node": {
                "name": self.local_node.name,
                "addr": self.local_node.addr,
                "port": self.local_node.port
            }
        }
        
        for member in list(self.members.values()):
            if member.name != self.local_node.name:
                await self._send_message(member.addr, member.port, leave_msg)
                
        if self.socket:
            self.socket.close()
            
    def get_members(self) -> List[Node]:
        """Get all alive members."""
        return [m for m in self.members.values() if m.state == "alive"]
        
    async def _join_member(self, member_addr: str) -> None:
        """Join an existing member."""
        try:
            parts = member_addr.split(":")
            if len(parts) != 2:
                return
                
            host = parts[0]
            port = int(parts[1])
            
            join_msg = {
                "type": "join",
                "node": {
                    "name": self.local_node.name,
                    "addr": self.local_node.addr,
                    "port": self.local_node.port,
                    "meta": self.local_node.meta.decode()
                }
            }
            
            await self._send_message(host, port, join_msg)
            
        except Exception as e:
            logger.info(f"Failed to join existing cluster, ok if this is the first node")
            logger.error(f"{e}")
            
    async def _send_message(self, addr: str, port: int, message: dict) -> None:
        """Send a message to a member."""
        try:
            data = json.dumps(message).encode()
            if self.socket:
                self.socket.sendto(data, (addr, port))
        except Exception as e:
            logger.debug(f"Failed to send message to {addr}:{port}: {e}")
            
    async def _listen_loop(self) -> None:
        """Listen for incoming messages."""
        while self.running:
            try:
                if self.socket:
                    try:
                        data, addr = self.socket.recvfrom(4096)
                        message = json.loads(data.decode())
                        await self._handle_message(message, addr[0])
                    except BlockingIOError:
                        pass
                await asyncio.sleep(0.01)
            except Exception as e:
                if self.running:
                    logger.debug(f"Error in listen loop: {e}")
                
    async def _handle_message(self, message: dict, sender_addr: str) -> None:
        """Handle incoming message."""
        msg_type = message.get("type")
        node_data = message.get("node", {})
        
        if msg_type == "join":
            node = Node(
                name=node_data["name"],
                addr=node_data["addr"],
                port=node_data["port"],
                meta=node_data.get("meta", "").encode()
            )
            
            if node.name not in self.members:
                self.members[node.name] = node
                await self.delegate.notify_join(node)
                
                # Send ack with our info
                ack_msg = {
                    "type": "ack",
                    "node": {
                        "name": self.local_node.name,
                        "addr": self.local_node.addr,
                        "port": self.local_node.port,
                        "meta": self.local_node.meta.decode()
                    }
                }
                await self._send_message(node.addr, node.port, ack_msg)
                
        elif msg_type == "ack":
            node = Node(
                name=node_data["name"],
                addr=node_data["addr"],
                port=node_data["port"],
                meta=node_data.get("meta", "").encode()
            )
            
            if node.name not in self.members:
                self.members[node.name] = node
                await self.delegate.notify_join(node)
                
        elif msg_type == "leave":
            node_name = node_data["name"]
            if node_name in self.members:
                node = self.members[node_name]
                node.state = "left"
                await self.delegate.notify_leave(node)
                del self.members[node_name]
                
        elif msg_type == "ping":
            # Send pong
            pong_msg = {"type": "pong", "node": {"name": self.local_node.name}}
            await self._send_message(sender_addr, message.get("port", self.bind_port), pong_msg)
            
        elif msg_type == "pong":
            # Mark member as alive
            node_name = node_data.get("name", "")
            if node_name in self.failed_members:
                del self.failed_members[node_name]
                
        elif msg_type == "gossip":
            # Handle gossip about other members
            for member_data in message.get("members", []):
                member_name = member_data.get("name")
                if member_name and member_name not in self.members and member_name != self.local_node.name:
                    node = Node(
                        name=member_name,
                        addr=member_data["addr"],
                        port=member_data["port"],
                        meta=member_data.get("meta", "").encode(),
                        state=member_data.get("state", "alive")
                    )
                    if node.state == "alive":
                        self.members[node.name] = node
                        await self.delegate.notify_join(node)
                
    async def _gossip_loop(self) -> None:
        """Gossip member information periodically."""
        while self.running:
            await asyncio.sleep(1.0)
            
            # Select random member to gossip with
            alive_members = [m for m in self.members.values() 
                           if m.state == "alive" and m.name != self.local_node.name]
            
            if alive_members:
                target = random.choice(alive_members)
                gossip_msg = {
                    "type": "gossip",
                    "members": [
                        {
                            "name": m.name,
                            "addr": m.addr,
                            "port": m.port,
                            "meta": m.meta.decode() if m.meta else "",
                            "state": m.state
                        } for m in self.members.values()
                    ]
                }
                await self._send_message(target.addr, target.port, gossip_msg)
                
    async def _failure_detector_loop(self) -> None:
        """Detect failed members periodically."""
        while self.running:
            await asyncio.sleep(5.0)
            
            current_time = time.time()
            
            for member in list(self.members.values()):
                if member.name == self.local_node.name:
                    continue
                    
                # Ping member
                ping_msg = {
                    "type": "ping",
                    "port": self.bind_port,
                    "timestamp": current_time
                }
                
                await self._send_message(member.addr, member.port, ping_msg)
                
                # Check if member has been failing
                if member.name in self.failed_members:
                    if current_time - self.failed_members[member.name] > 30.0:
                        # Member is considered dead
                        member.state = "failed"
                        await self.delegate.notify_leave(member)
                        del self.members[member.name]
                        del self.failed_members[member.name]
                else:
                    # Start tracking for failure
                    self.failed_members[member.name] = current_time
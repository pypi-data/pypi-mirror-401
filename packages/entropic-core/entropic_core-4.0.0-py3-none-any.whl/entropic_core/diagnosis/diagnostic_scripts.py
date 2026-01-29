"""
CLI diagnostic scripts that can be curl'd for instant diagnosis
"""


class DiagnosticScripts:
    """Generates executable diagnostic scripts"""

    @staticmethod
    def generate_curl_script() -> str:
        """Generate the curl-able diagnostic script"""
        return '''#!/usr/bin/env python3
"""
Entropic Core - Instant Diagnostic Tool
Detects real problems in multi-agent systems

Usage: curl -s https://entropic-core.com/diagnose | python3 -
"""

import sys
import json
from datetime import datetime

def check_system():
    """Quick system check"""
    print("\\n" + "="*60)
    print("ENTROPIC CORE - System Diagnostic")
    print("="*60)
    print(f"\\nScanning your multi-agent system...\\n")
    
    # Try to import and diagnose
    try:
        from entropic_core import EntropyBrain
        from entropic_core.diagnosis import ProblemDetector
        
        print("✓ Entropic Core installed")
        
        # Check if system is running
        import os
        if os.path.exists('entropy_memory.db'):
            print("✓ Found active Entropic Core system")
            
            # Create brain and detector
            brain = EntropyBrain()
            detector = ProblemDetector(brain)
            
            # Run diagnostics
            report = detector.generate_diagnostic_report()
            print(report)
            
        else:
            print("\\n⚠️  No active Entropic Core system found")
            print("\\nStart monitoring your agents:")
            print("  pip install entropic-core")
            print("  entropic-quickstart")
            
    except ImportError:
        print("\\n❌ Entropic Core not installed")
        print("\\nInstall now (takes 30 seconds):")
        print("  pip install entropic-core")
        print("\\nThen run:")
        print("  entropic-quickstart")
        print("\\nThis will:")
        print("  ✓ Detect available LLMs (Ollama, OpenAI, etc.)")
        print("  ✓ Create demo multi-agent system")
        print("  ✓ Show you how chaos regulation works")
        print("  ✓ All features included, 100% free")
        
    print("\\n" + "="*60)
    print("Need help? https://github.com/entropic-core/entropic-core")
    print("="*60 + "\\n")

if __name__ == "__main__":
    check_system()
'''

    @staticmethod
    def generate_fix_script(problem_id: str) -> str:
        """Generate problem-specific fix script"""

        fixes = {
            "infinite_loop": """
# Fix: Infinite Loop
# Add this to your agent configuration:

from langchain.agents import AgentExecutor

agent = AgentExecutor(
    agent=your_agent,
    tools=your_tools,
    max_iterations=10,          # Prevent infinite loops
    max_execution_time=60,      # 60 second timeout
    early_stopping_method="force"  # Force stop when limit reached
)
""",
            "memory_leak": """
# Fix: Memory Leak
# Implement cleanup in your agent loop:

for task in tasks:
    # Create fresh runtime for each task
    runtime = create_runtime()
    result = runtime.execute(task)
    
    # Clean up after each task
    runtime.cleanup()
    del runtime
    
    # Explicit garbage collection every N tasks
    if task_count % 100 == 0:
        import gc
        gc.collect()
""",
            "api_runaway": """
# Fix: API Cost Runaway
# Add rate limiting and timeout handling:

import time
from functools import wraps

def rate_limit(max_calls_per_minute=60):
    def decorator(func):
        last_called = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls older than 1 minute
            last_called[:] = [t for t in last_called if now - t < 60]
            
            if len(last_called) >= max_calls_per_minute:
                sleep_time = 60 - (now - last_called[0])
                print(f"Rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
            
            last_called.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls_per_minute=50)
def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            timeout=30  # 30 second timeout
        )
        return response
    except TimeoutError:
        print("API timeout, retrying with exponential backoff...")
        time.sleep(2 ** retry_count)
        return call_llm_with_retry(prompt, retry_count + 1)
""",
            "race_condition": """
# Fix: Race Condition
# Add thread-safe locking:

import threading

class SafeAgentCoordinator:
    def __init__(self):
        self.lock = threading.Lock()
        self.shared_state = {}
    
    def update_state(self, key, value):
        with self.lock:  # Only one thread can update at a time
            self.shared_state[key] = value
    
    def read_state(self, key):
        with self.lock:  # Consistent reads
            return self.shared_state.get(key)

# Use in your multi-agent system:
coordinator = SafeAgentCoordinator()

def agent_task(agent_id):
    # Safe access to shared resources
    current_value = coordinator.read_state('counter')
    new_value = current_value + 1
    coordinator.update_state('counter', new_value)
""",
            "frozen_agent": """
# Fix: Frozen Agent
# Add timeout monitoring for stuck agents:

import signal
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Agent timeout")

@contextmanager
def agent_timeout(seconds=30):
    # Set timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)  # Disable alarm

# Use in your agent:
try:
    with agent_timeout(30):
        result = agent.execute(task)
except TimeoutError:
    print("Agent frozen or stuck, restarting...")
    agent.reset()
    result = agent.execute(task)  # Try again with fresh state
""",
            "thinking_freeze": """
# Fix: Thinking State Freeze
# Add timeout monitoring:

import signal
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Agent thinking timeout")

@contextmanager
def thinking_timeout(seconds=30):
    # Set timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)  # Disable alarm

# Use in your agent:
try:
    with thinking_timeout(30):
        result = agent.think_and_act(task)
except TimeoutError:
    print("Agent frozen in thinking, restarting...")
    agent.reset()
    result = agent.think_and_act(task)  # Try again
""",
        }

        return fixes.get(problem_id, "# Unknown problem ID")


DiagnosticScriptGenerator = DiagnosticScripts

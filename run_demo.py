#!/usr/bin/env python3
"""
Main demo runner for Celery examples.
Allows running different demos showcasing Celery's capabilities:
- basic: Basic task execution with stamps used for debugging
- group: Parallel task execution (group primitive)
- chain: Sequential task execution (chain primitive)
- chord: Parallel tasks with callback (chord primitive)
- map: Apply task to list of arguments (map primitive)
- starmap: Apply task with *args (starmap primitive)
- chunks: Split large lists into chunks (chunks primitive)
"""

import sys
import os
import time
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, '/app' if os.path.exists('/app') else '.')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


# ==================== Basic Demo ====================

def run_basic_demo():
    """Run basic tasks demo with stamps used for debugging"""
    from demos.basic_demo import demo_basic_tasks
    
    # Run basic tasks
    demo_basic_tasks()


# ==================== Workflow Demos ====================

def run_group_demo():
    """Run group demo (parallel tasks)"""
    from demos.workflows import demo_group
    demo_group()


def run_chain_demo():
    """Run chain demo (sequential tasks)"""
    from demos.workflows import demo_chain
    demo_chain()


def run_chord_demo():
    """Run chord demo (parallel + callback)"""
    from demos.workflows import demo_chord
    demo_chord()


def run_map_demo():
    """Run map demo (apply task to list)"""
    from demos.workflows import demo_map
    demo_map()


def run_starmap_demo():
    """Run starmap demo (apply task with *args)"""
    from demos.workflows import demo_starmap
    demo_starmap()


def run_chunks_demo():
    """Run chunks demo (split into chunks)"""
    from demos.workflows import demo_chunks 
    demo_chunks()




# ==================== Main Entry Point ====================

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\nUsage: python run_demo.py [demo_type]")
        print("\nAvailable demos:")
        print("  basic     - Basic tasks with stamps used for debugging")
        print("  group      - Group primitive (parallel execution)")
        print("  chain      - Chain primitive (sequential execution)")
        print("  chord      - Chord primitive (parallel + callback)")
        print("  map        - Map primitive (apply task to list)")
        print("  starmap    - Starmap primitive (apply task with *args)")
        print("  chunks     - Chunks primitive (split into chunks)")
        print("Examples:")
        print("  python run_demo.py basic")
        print("  python run_demo.py group")
        sys.exit(1)
    
    demo_type = sys.argv[1].lower()
    
    if demo_type == 'basic':
        run_basic_demo()
    elif demo_type == 'group':
        run_group_demo()
    elif demo_type == 'chain':
        run_chain_demo()
    elif demo_type == 'chord':
        run_chord_demo()
    elif demo_type == 'map':
        run_map_demo()
    elif demo_type == 'starmap':
        run_starmap_demo()
    elif demo_type == 'chunks':
        run_chunks_demo()
    else:
        print(f"Unknown demo type: {demo_type}")
        print("Valid options: basic, group, chain, chord, map, starmap, chunks")
        sys.exit(1)

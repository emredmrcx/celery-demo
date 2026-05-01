"""
Celery Workflow Primitives Demo.

This module demonstrates:
1. group - Parallel task execution 
2. chain - Sequential task execution 
3. chord - Parallel tasks with callback
4. map - Apply task to list of arguments
5. starmap - Apply task with *args
6. chunks - Split large lists into smaller chunks
"""

from src.celery_app import app
from celery import chain, group, chord, chunks
import time
import random
import socket
from datetime import datetime

# ==================== Helper Tasks ====================

@app.task(bind=True)
def add(self, x, y):
    """Simple addition task for map/starmap demos"""
    start_time = datetime.now().strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[add] {x} + {y} | Worker: {worker} | Start: {start_time} | Task ID: {self.request.id}")
    time.sleep(random.uniform(0.5, 1.5))
    result = x + y
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[add] Result: {result} | Worker: {worker} | End: {end_time}")
    return result


@app.task(bind=True)
def multiply(self, x, y):
    """Simple multiplication task for map/starmap demos"""
    start_time = datetime.now().strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[multiply] {x} * {y} | Worker: {worker} | Start: {start_time} | Task ID: {self.request.id}")
    time.sleep(random.uniform(0.5, 1.5))
    result = x * y
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[multiply] Result: {result} | Worker: {worker} | End: {end_time}")
    return result


@app.task(bind=True)
def process_item(self, item):
    """Process a single item for map/chunks demos"""
    start_time = datetime.now().strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[process_item] Processing {item} | Worker: {worker} | Start: {start_time} | Task ID: {self.request.id}")
    time.sleep(random.uniform(0.5, 1.0))
    result = item * 2
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[process_item] Result: {result} | Worker: {worker} | End: {end_time}")
    return result


@app.task(bind=True)
def aggregate_results(self, results):
    """Aggregate results from parallel tasks"""
    start_time = datetime.now().strftime('%H:%M:%S')
    stamps = self.request.stamps if hasattr(self.request, 'stamps') else {}
    worker = socket.gethostname()
    print(f"[aggregate_results] Aggregating {len(results)} results | Worker: {worker} | Start: {start_time}")
    print(f"[aggregate_results] Stamps: {stamps}")
    time.sleep(1)
    total = sum(results) if all(isinstance(r, (int, float)) for r in results) else results
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[aggregate_results] Total: {total} | Worker: {worker} | End: {end_time}")
    return {'count': len(results), 'total': total, 'stamps': stamps}


@app.task(bind=True)
def extract_task(self, source_id):
    """Simulate data extraction for group/chain demos"""
    start_time = datetime.now().strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[extract_task] Extracting from {source_id} | Worker: {worker} | Start: {start_time} | Task ID: {self.request.id}")
    time.sleep(2)
    result = {'source_id': source_id, 'data': f'data_from_{source_id}', 'records': random.randint(50, 150)}
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[extract_task] Complete: {result} | Worker: {worker} | End: {end_time}")
    return result


@app.task(bind=True)
def transform_task(self, extract_result):
    """Transform data from extraction"""
    start_time = datetime.now().strftime('%H:%M:%S')
    source_id = extract_result.get('source_id')
    worker = socket.gethostname()
    print(f"[transform_task] Transforming data from {source_id} | Worker: {worker} | Start: {start_time} | Task ID: {self.request.id}")
    time.sleep(1.5)
    result = {**extract_result, 'transformed': True, 'quality_score': round(random.uniform(0.85, 0.99), 2)}
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[transform_task] Complete: {result} | Worker: {worker} | End: {end_time}")
    return result


@app.task(bind=True)
def load_task(self, transform_result):
    """Load transformed data"""
    start_time = datetime.now().strftime('%H:%M:%S')
    source_id = transform_result.get('source_id')
    worker = socket.gethostname()
    print(f"[load_task] Loading data from {source_id} | Worker: {worker} | Start: {start_time} | Task ID: {self.request.id}")
    time.sleep(1)
    result = {**transform_result, 'loaded': True, 'table': 'final_data'}
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[load_task] Complete: {result} | Worker: {worker} | End: {end_time}")
    return result


# ==================== GROUP Demo ====================

def demo_group():
    """
    GROUP Demo: Parallel Task Execution
    
    The group primitive runs tasks in parallel.
    All tasks execute simultaneously, and results are collected when all complete.
    """
    print("\n" + "="*60)
    print("GROUP DEMO - Parallel Task Execution")
    print("="*60 + "\n")
    
    print("The group primitive runs tasks in parallel.")
    print("All tasks execute simultaneously, and results are collected.\n")
    
    # Create group 
    workflow = group(
        extract_task.s('source_1'),
        extract_task.s('source_2'),
        extract_task.s('source_3')
    )
    
    # Apply Canvas Stamping - attaches to all tasks in the group
    workflow.stamp(
        demo_type='group',
        priority='high',
        timestamp=datetime.now().isoformat()
    )
    
    result = workflow.apply_async()
    print(f"Group ID: {result.id}")
    print(f"Stamps applied: demo_type='group', priority='high'\n")
    
    try:
        results = result.get(timeout=15)
        print(f"Group completed: {len(results)} tasks finished")
        for i, r in enumerate(results, 1):
            print(f"  Task {i}: {r}")
    except Exception as e:
        print(f"Group error: {e}")
    
    print("\n" + "="*60)
    print("GROUP DEMO COMPLETED")
    print("="*60 + "\n")


# ==================== CHAIN Demo ====================

def demo_chain():
    """
    CHAIN Demo: Sequential Task Execution
    
    The chain primitive links signatures so that one is called after another,
    forming a chain of callbacks. Each task receives the result of the previous task.
    """
    print("\n" + "="*60)
    print("CHAIN DEMO - Sequential Task Execution")
    print("="*60 + "\n")
    
    print("The chain primitive links tasks sequentially.")
    print("Each task receives the result of the previous task.\n")
    
    # Create chain for ETL pipeline
    workflow = chain(
        extract_task.s('main_source'),
        transform_task.s(),
        load_task.s()
    )
    
    # Apply Canvas Stamping - attaches to all tasks in the chain
    workflow.stamp(
        workflow_type='etl_pipeline',
        version='1.0',
        environment='production'
    )
    
    result = workflow.apply_async()
    print(f"Chain ID: {result.id}")
    print(f"Stamps applied: workflow_type='etl_pipeline'\n")
    
    try:
        res = result.get(timeout=20)
        print(f"Chain completed: {res}")
    except Exception as e:
        print(f"Chain error: {e}")
    
    print("\n" + "="*60)
    print("CHAIN DEMO COMPLETED")
    print("="*60 + "\n")


# ==================== CHORD Demo ====================

def demo_chord():
    """
    CHORD Demo: Parallel Tasks + Callback
    
    A chord consists of a header group and a body (callback).
    The body executes after all tasks in the header are complete,
    receiving the list of results from the header tasks.
    """
    print("\n" + "="*60)
    print("CHORD DEMO - Parallel Tasks + Callback")
    print("="*60 + "\n")
    
    print("A chord is like a group but with a callback.")
    print("The callback executes after all parallel tasks complete.\n")
    
    # Create header group
    header = group(
        extract_task.s('source_A'),
        extract_task.s('source_B'),
        extract_task.s('source_C')
    )
    
    # Create callback with stamp
    callback = aggregate_results.s().stamp(
        callback_type='aggregation',
        notify='admin@example.com',
        timestamp=datetime.now().isoformat()
    )
    
    # Create chord
    workflow = chord(header, callback)
    
    result = workflow.apply_async()
    print(f"Chord ID: {result.id}")
    
    try:
        res = result.get(timeout=20)
        print(f"Chord completed: {res}")
    except Exception as e:
        print(f"Chord error: {e}")
    
    print("\n" + "="*60)
    print("CHORD DEMO COMPLETED")
    print("="*60 + "\n")


# ==================== MAP Demo ====================

def demo_map():
    """
    MAP Demo: Apply Task to List of Arguments
    
    The map primitive works like Python's built-in map function.
    It creates a temporary task where a list of arguments is applied to the task.
    """
    print("\n" + "="*60)
    print("MAP DEMO - Apply Task to List of Arguments")
    print("="*60 + "\n")
    
    print("The map primitive applies a task to each item in a list.")
    print("It works like Python's built-in map function.")
    
    # Create a list of arguments
    numbers = [1, 2, 3, 4, 5]
    print(f"Input list: {numbers}")
    print(f"Task: process_item (multiplies each number by 2)")
    
    # Use map to apply process_item to each number
    workflow = process_item.map(numbers)
    
    # Apply Canvas Stamping
    workflow.stamp(
        operation='map_demo',
        batch_id='batch_123',
        user='emre'
    )
    
    result = workflow.apply_async()
    print(f"Map ID: {result.id}")
    print(f"Stamps applied: operation='map_demo', batch_id='batch_123'\n")
    
    try:
        results = result.get(timeout=15)
        print(f"Map completed: {len(results)} items processed")
        print(f"Results: {results}")
    except Exception as e:
        print(f"Map error: {e}")
    
    print("\n" + "="*60)
    print("MAP DEMO COMPLETED")
    print("="*60 + "\n")


# ==================== STARMAP Demo ====================

def demo_starmap():
    """
    STARMAP Demo: Apply Task with *args 
    
    The starmap primitive works like map but applies arguments as *args.
    Each tuple in the list is unpacked as arguments to the task.
    """
    print("\n" + "="*60)
    print("STARMAP DEMO - Apply Task with *args")
    print("="*60 + "\n")
    
    print("The starmap primitive works like map but applies arguments as *args.")
    print("Each tuple in the list is unpacked as arguments to the task.\n")
    
    
    # List of argument tuples
    arg_pairs = [(1, 2), (3, 4), (5, 6), (7, 8)]
    print(f"Input pairs: {arg_pairs}")
    print(f"Task: add (adds two numbers)\n")
    
    # Use starmap to apply add to each pair
    workflow = add.starmap(arg_pairs)
    
    # Apply Custom Stamping
    workflow.stamp(
        demo_type='starmap',
        priority='low',
        experiment='celery_demo'
    )
    
    result = workflow.apply_async()
    print(f"Starmap ID: {result.id}")
    print(f"Stamps applied: demo_type='starmap', priority='low'\n")
    
    try:
        results = result.get(timeout=15)
        print(f"Starmap completed: {len(results)} operations")
        print(f"Results: {results}")
    except Exception as e:
        print(f"Starmap error: {e}")
    
    print("\n" + "="*60)
    print("STARMAP DEMO COMPLETED")
    print("="*60 + "\n")


# ==================== CHUNKS Demo ====================

def demo_chunks():
    """
    CHUNKS Demo: Split Large Lists into Smaller Chunks 
    
    Chunking splits a long list of arguments into parts.
    """
    print("\n" + "="*60)
    print("CHUNKS DEMO - Split Large Lists into Chunks")
    print("="*60 + "\n")
    
    print("The chunks primitive splits a long list of arguments into parts.")
    print("Each chunk is processed as a separate task.\n")
    
    
    # Create 500 items for processing
    items = list(zip(range(500), range(500)))
    print(f"Total items: {len(items)}")
    print(f"Chunk size: 5")
    
    # Use chunks to split into groups of 5
    workflow = add.chunks(items, 5)
    
    # Apply Canvas Stamping
    workflow.stamp(
        chunk_size=5,
        total_items=len(items),
        processing_type='batch'
    )
    
    result = workflow.apply_async()
    print(f"Chunks ID: {result.id}")
    print(f"Stamps applied: chunk_size=5, total_items=500, processing_type='batch'\n")
    
    try:
        results = result.get(timeout=30)
        print(f"Chunks completed: {len(results)} chunks processed")
    except Exception as e:
        print(f"Chunks error: {e}")
    
    print("\n" + "="*60)
    print("CHUNKS DEMO COMPLETED")
    print("="*60 + "\n")



if __name__ == '__main__':
    pass

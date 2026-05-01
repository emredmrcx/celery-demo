"""
Basic Celery Tasks Demo.
"""

from src.celery_app import app
from celery import group, chord, chain
import time
import random
from datetime import datetime
from celery import current_task

# ==================== Basic Tasks ====================

@app.task(bind=True)
def extract_data(self, source='api'):
    """
    Simulate extracting data from an external API.
    """
    start_time = datetime.now().strftime('%H:%M:%S')
    self.update_state(state='PROGRESS', meta={'status': 'Extracting data...'})
    print(f"[extract_data] Start time: {start_time} | Task ID: {self.request.id}")
    
    # Simulate API call delay
    sleep_time = random.uniform(2, 4)
    time.sleep(sleep_time)
    
    # Simulate extracted data
    data = {
        'source': source,
        'records': random.randint(100, 1000),
        'timestamp': time.time(),
        'status': 'extracted'
    }
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[extract_data] Completed in {sleep_time:.2f}s. Records: {data['records']} (End: {end_time})")
    return data


@app.task(bind=True)
def transform_data(self, data):
    """
    Simulate transforming/cleaning data.
    """
    start_time = datetime.now().strftime('%H:%M:%S')
    self.update_state(state='PROGRESS', meta={'status': 'Transforming data...'})
    print(f"[transform_data] Start time: {start_time} | Task ID: {self.request.id}")
    
    # Simulate transformation time
    sleep_time = random.uniform(3, 5)
    time.sleep(sleep_time)
    
    # Simulate transformed data
    transformed = {
        'original_records': data.get('records', 0),
        'transformed_records': int(data.get('records', 0) * 0.95),
        'transformations': ['cleaned', 'normalized', 'validated'],
        'status': 'transformed'
    }
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[transform_data] Completed in {sleep_time:.2f}s. Transformed: {transformed['transformed_records']} (End: {end_time})")
    return transformed


@app.task(bind=True)
def load_to_database(self, data):
    """
    Simulate loading data to a database.
    """
    start_time = datetime.now().strftime('%H:%M:%S')
    self.update_state(state='PROGRESS', meta={'status': 'Loading to database...'})
    print(f"[load_to_database] Start time: {start_time} | Task ID: {self.request.id}")
    
    # Simulate database load time
    sleep_time = random.uniform(2, 3)
    time.sleep(sleep_time)
    
    result = {
        'records_loaded': data.get('transformed_records', 0),
        'table': 'processed_data',
        'load_time': sleep_time,
        'status': 'loaded'
    }
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[load_to_database] Completed in {sleep_time:.2f}s. Loaded: {result['records_loaded']} (End: {end_time})")
    return result


@app.task(bind=True)
def generate_report(self, data):
    """
    Simulate generating a report from processed data.
    """
    start_time = datetime.now().strftime('%H:%M:%S')
    self.update_state(state='PROGRESS', meta={'status': 'Generating report...'})
    print(f"[generate_report] Start time: {start_time} | Task ID: {self.request.id}")
    
    # Simulate report generation
    sleep_time = random.uniform(3, 5)
    time.sleep(sleep_time)
    
    report = {
        'report_id': f"RPT-{random.randint(1000, 9999)}",
        'records_in_report': data.get('records_loaded', 0),
        'generation_time': sleep_time,
        'format': 'PDF',
        'status': 'completed'
    }
    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"[generate_report] Completed in {sleep_time:.2f}s. Report ID: {report['report_id']} (End: {end_time})")
    return report


# ==================== Callback Task ====================

@app.task(bind=True)
def callback_task(self, results):
    """Callback that processes results from parallel tasks"""
    stamps = self.request.stamps if hasattr(self.request, 'stamps') else {}
    print(f"[callback_task] Received {len(results)} results")
    print(f"[callback_task] Stamps: {stamps}")
    return {
        'results_count': len(results),
        'callback_stamps': stamps,
        'status': 'callback_completed'
    }


# ==================== Demo Function ====================

def demo_basic_tasks():
    """
    Run basic tasks demo with stamps integrated for debugging.
    """
    print("\n" + "="*60)
    print("BASIC TASKS DEMO - Individual Task Execution")
    print("="*60 + "\n")
    
    # Run individual tasks with stamps for debugging/tracking
    print("[1/4] Running extract_data...")
    result1 = extract_data.apply_async(
        args=('api',),
        stamp={'task_type': 'extraction', 'source': 'api', 'debug': True}
    )
    print(f"     Task ID: {result1.id}")
    print(f"     Stamp: task_type='extraction', debug=True")
    
    print("\n[2/4] Running transform_data with stamping...")
    result2 = transform_data.apply_async(
        args=({'records': 500, 'source': 'api'},),
        stamp={'task_type': 'transformation', 'input_records': 500}
    )
    print(f"     Task ID: {result2.id}")
    print(f"     Stamp: task_type='transformation', input_records=500")
    
    print("\n[3/4] Running load_to_database with stamping...")
    result3 = load_to_database.apply_async(
        args=({'transformed_records': 475},),
        stamp={'task_type': 'loading', 'destination': 'processed_data'}
    )
    print(f"     Task ID: {result3.id}")
    print(f"     Stamp: task_type='loading', destination='processed_data'")
    
    print("\n[4/4] Running generate_report with stamping...")
    result4 = generate_report.apply_async(
        args=({'records_loaded': 475},),
        stamp={'task_type': 'reporting', 'format': 'PDF', 'priority': 'normal'}
    )
    print(f"     Task ID: {result4.id}")
    print(f"     Stamp: task_type='reporting', format='PDF'\n")
    
    results = [result1, result2, result3, result4]
    for i, r in enumerate(results, 1):
        try:
            res = r.get(timeout=10)
            print(f"Task {i} result: {res.get('status', 'completed')}")
        except Exception as e:
            print(f"Task {i} error: {e}")
    
    print("\n" + "="*60)
    print("BASIC TASKS DEMO COMPLETED")
    print("="*60 + "\n")


# ==================== Main Entry Point ====================

if __name__ == '__main__':
    # Run basic tasks demo only
    demo_basic_tasks()

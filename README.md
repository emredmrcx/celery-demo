# Celery Demo - Advanced Data Engineering Examples

## Table of Contents

1. [What is this tool?](#what-is-this-tool)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Running the Examples](#running-the-examples)
   - [Flower Monitoring (Start Here!)](#flower-monitoring-start-here)
   - [Basic Tasks Demo with Stamping](#1-basic-tasks-demo-with-stamping)
   - [Group Demo (Parallel Execution)](#2-group-demo-parallel-execution)
   - [Chain Demo (Sequential Execution)](#3-chain-demo-sequential-execution)
   - [Chord Demo (Parallel + Callback)](#4-chord-demo-parallel--callback)
   - [Map Demo (Apply Task to List)](#5-map-demo-apply-task-to-list)
   - [Starmap Demo (Apply Task with *args)](#6-starmap-demo-apply-task-with-args)
   - [Chunks Demo (Split into Chunks)](#7-chunks-demo-split-into-chunks)
   - [Periodic Tasks (Celery Beat)](#8-periodic-tasks-celery-beat)
6. [Celery Workflow Primitives Summary](#celery-workflow-primitives-summary)
7. [Stamping Features Summary](#stamping-features-summary)
8. [Use Cases](#use-cases)
9. [Limitations](#limitations)
10. [References](#references)

---

## What is this tool?

Celery is a distributed task queue system for Python that enables asynchronous task execution, background processing, and distributed computing. Released in 2010 by Ask Solem, Celery is open-source software licensed under the BSD License. It is widely used in data engineering pipelines for ETL workflows, periodic tasks, and distributed processing across multiple workers.

---

## Prerequisites

- **Operating System**: Windows 10/11, macOS, or Linux
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 1.29 or higher (or Docker Compose V2)
- **Git**: For cloning the repository

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/emredmrcx/celery-demo.git
cd celery-demo
```

### Step 2: Copy Environment File

```bash
cp .env.example .env
```

### Step 3: Start Docker Services

```bash
docker-compose up -d
```

### Step 4: Verify Services are Running

```bash
docker-compose ps
```

---

## Project Structure

```
celery-demo/
├── src/
│   ├── __init__.py
│   └── celery_app.py          # Main Celery application config
├── demos/
│   ├── __init__.py
│   ├── basic_demo.py          # Basic tasks with stamping examples
│   ├── workflows.py           # Group, chain, chord, map, starmap, 
│   └── periodic.py            # Periodic/scheduled tasks (Celery Beat)
├── run_demo.py                # Main demo runner script
├── requirements.txt           # Python dependencies (includes Flower)
├── docker-compose.yml        # Docker services (redis, worker, beat, flower)
├── Dockerfile                 # Container image definition
├── .env.example              # Environment variables template
├── README.md                 # This file
├── AI_USAGE.md               # AI usage disclosure
```

---

## Running the Examples

### Flower Monitoring (Start Here!)

Flower is a  web-based monitoring tool for Celery. After starting all services with `docker-compose up -d`, Flower will be available to monitor all your Celery tasks and workers.

```bash
# Access the Flower web interface (already started with docker-compose up -d)
# Open your browser and navigate to:
http://localhost:5555
```

**Flower Features:**
| Feature | Description |
|---------|-------------|
| **Dashboard** | Overview of all workers and task details (arguments, results, execution time) |
| **Tasks** | List of all tasks with status (pending, active, finished, failed) |
| **Workers** | Monitor worker status and pool processes |
| **Broker** | View queue lengths and message rates |


---

### 1. Basic Tasks Demo with Stamping

```bash
docker-compose exec celery-app python run_demo.py basic
```

**Expected Output:**
```
============================================================
  BASIC TASKS DEMO - Individual Task Execution with Stamping
============================================================

[1/4] Running extract_data with stamping...
     Task ID: [uuid]
     Stamp: task_type='extraction', debug=True

[2/4] Running transform_data with stamping...
     Task ID: [uuid]
     Stamp: task_type='transformation', input_records=500

... (similar for other tasks)

Task 1 result: extracted
Task 2 result: transformed
Task 3 result: loaded
Task 4 result: completed

============================================================
BASIC TASKS DEMO COMPLETED
============================================================
```

---

### 2. Group Demo (Parallel Execution)

```bash
docker-compose exec celery-app python run_demo.py group
```

**What it shows:** The `group` primitive runs tasks in parallel. All tasks execute simultaneously, and results are collected when all complete. Includes canvas stamping example.

**Expected Output:**
```
============================================================
  GROUP DEMO - Parallel Task Execution
============================================================

The group primitive runs tasks in parallel.
All tasks execute simultaneously, and results are collected.

Group with Canvas Stamping...
Canvas stamping attaches metadata to all tasks in the group.

Group ID: [uuid]
Stamps applied: demo_type='group', priority='high'

Stamped group completed: 3 tasks finished
  Task 1: {'source_id': 'source_1', 'data': 'data_from_source_1', 'records': 148}
  Task 2: {'source_id': 'source_2', 'data': 'data_from_source_2', 'records': 131}
  Task 3: {'source_id': 'source_3', 'data': 'data_from_source_3', 'records': 70}

============================================================
GROUP DEMO COMPLETED
============================================================
```

---

### 3. Chain Demo (Sequential Execution)

```bash
docker-compose exec celery-app python run_demo.py chain
```

**What it shows:** The `chain` primitive links tasks sequentially. Each task receives the result of the previous task (e.g., extract → transform → load). Includes canvas stamping example.

**Expected Output:**
```
============================================================
  CHAIN DEMO - Sequential Task Execution
============================================================

The chain primitive links tasks sequentially.
Each task receives the result of the previous task.

Chain with Canvas Stamping...
Canvas stamping attaches metadata to all tasks in the chain.

Chain ID: [uuid]
Stamps applied: workflow_type='etl_pipeline', version='1.0'

Stamped chain completed: {'source_id': 'main_source', 'data': 'data_from_main_source', 'records': 118, 'transformed': True, 'quality_score': 0.95, 'loaded': True, 'table': 'final_data'}

============================================================
CHAIN DEMO COMPLETED
============================================================
```

---

### 4. Chord Demo (Parallel + Callback)

```bash
docker-compose exec celery-app python run_demo.py chord
```

**What it shows:** A `chord` is like a group but with a callback. The callback executes after all parallel tasks complete, receiving the list of results. Includes callback stamping example.

**Expected Output:**
```
============================================================
  CHORD DEMO - Parallel Tasks + Callback
============================================================

A chord is like a group but with a callback.
The callback executes after all parallel tasks complete.

Chord with Callback Stamping...
Callback stamping attaches metadata to the callback task.

Chord ID: [uuid]
Callback stamped with: callback_type='aggregation', notify='admin@example.com'

Stamped chord completed: {'count': 3, 'total': [{'source_id': 'source_A', ...}], 'stamps': {'callback_type': 'aggregation', ...}}

============================================================
CHORD DEMO COMPLETED
============================================================
```

---

### 5. Map Demo (Apply Task to List)

```bash
docker-compose exec celery-app python run_demo.py map
```

**What it shows:** The `map` primitive works like Python's built-in `map` function. It creates a temporary task where a list of arguments is applied to the task. Tasks are distributed across ALL available workers (3 workers in this setup).

**Expected Output:**
```
============================================================
  MAP DEMO - Apply Task to List of Arguments
============================================================

The map primitive applies a task to each item in a list.
It works like Python's built-in map function.
Tasks are distributed across ALL available workers (3 workers in this setup).

Map with Canvas Stamping...

Input list: [1, 2, 3, 4, 5]
Task: process_item (multiplies each number by 2)
Watch the worker names in the output to see distribution across workers!

Map ID: [uuid]
Stamps applied: operation='map_demo', batch_id='batch_123'

Stamped map completed: 5 items processed
Results: [2, 4, 6, 8, 10]

============================================================
MAP DEMO COMPLETED
============================================================
```

---

### 6. Starmap Demo (Apply Task with *args)

```bash
docker-compose exec celery-app python run_demo.py starmap
```

**What it shows:** The `starmap` primitive works like `map` but applies arguments as `*args`.

**Expected Output:**
```
============================================================
  STARMAP DEMO - Apply Task with *args
============================================================

The starmap primitive works like map but applies arguments as *args.
Each tuple in the list is unpacked as arguments to the task.

Starmap with Custom Stamping...

Input pairs: [(1, 2), (3, 4), (5, 6), (7, 8)]
Task: add (adds two numbers)

Starmap ID: [uuid]
Stamps applied: demo_type='starmap', priority='low'

Stamped starmap completed: 4 operations
Results: [3, 7, 11, 15]

============================================================
STARMAP DEMO COMPLETED
============================================================
```

---

### 7. Chunks Demo (Split into Chunks)

```bash
docker-compose exec celery-app python run_demo.py chunks
```

**What it shows:** The `chunks` primitive splits a long list of arguments into parts.

**Expected Output:**
```
============================================================
  CHUNKS DEMO - Split Large Lists into Chunks
============================================================

The chunks primitive splits a long list of arguments into parts.
Each chunk is processed as a separate task.

Chunks with Canvas Stamping...

Total items: 20
Chunk size: 5
Chunks ID: [uuid]
Stamps applied: chunk_size=5, total_items=20, processing_type='batch'

Stamped chunks completed: 4 chunks processed

============================================================
CHUNKS DEMO COMPLETED
============================================================
```

---


### 8. Periodic Tasks (Celery Beat)

Periodic tasks are configured in `demos/periodic.py` and run automatically when Celery Beat is started:

**What it shows:**
- **Hourly Health Check**: Runs every hour
- **Daily Report Generation**: Runs daily at midnight
- **Weekly Cleanup**: Runs weekly on Sunday at 2AM

**Expected Output (in worker logs):**
```
[periodic] Running health check... | Worker: [hostname] | Time: [time]
[periodic] Health check completed | Worker: [hostname]
```

To show in demo, first stop the setup
```
docker-compose down
```

Then, in `periodic.py` change :
```
'schedule': timedelta(hours=1),  # Run every hour
```

with

```
'schedule': timedelta(seconds=5),  # Run every 5 seconds
```

Start compose again:
```
docker-compose up -d
```

---

## Celery Workflow Primitives Summary

| Primitive | Description | Use Case |
|-----------|-------------|----------|
| **group** | Parallel task execution | Run multiple independent tasks simultaneously |
| **chain** | Sequential task execution | ETL pipelines, dependent tasks |
| **chord** | Parallel + callback | Map-reduce patterns, aggregation after parallel work |
| **map** | Apply task to list | Process each item in a list with the same task |
| **starmap** | Apply task with *args | Process tuples of arguments with the same task |
| **chunks** | Split into chunks | Process large datasets in manageable pieces |

---


## Use Cases

Celery is used in various scenarios across data engineering and software development:

### 1. Asynchronous Task Execution
- **Purpose**: Don't block main application/web requests while long-running tasks execute
- **Example**: Processing uploaded files, generating reports, sending emails
- **Benefit**: Improved user experience, faster response times

### 2. Background Processing
- **Purpose**: Handle tasks that don't need immediate results
- **Examples**: Email notifications, report generation, data cleanup jobs
- **Benefit**: Decouple time-consuming work from user-facing operations

### 3. Distributed Computing
- **Purpose**: Scale task execution across multiple workers/machines
- **Examples**: Parallel data processing, distributed machine learning training
- **Benefit**: Horizontal scaling, improved throughput

### 4. ETL Pipelines
- **Purpose**: Extract, Transform, Load workflows for data processing
- **Examples**: Data warehouse population, API data ingestion, database migrations
- **Benefit**: Reliable pipeline execution with error handling and retries

### 5. Periodic/Scheduled Tasks
- **Purpose**: Run tasks on schedules (like cron jobs)
- **Examples**: Daily reports, hourly data syncs, weekly cleanups
- **Benefit**: Automated recurring operations with Celery Beat

### 6. Data Engineering Workflows
- **Purpose**: Complement to tools like Apache Airflow
- **Examples**: Celery as Airflow executor (CeleryExecutor), standalone pipelines
- **Benefit**: Flexible task execution within larger orchestration frameworks

### 7. Microservices Communication
- **Purpose**: Async events between services
- **Examples**: Order processing, inventory updates, notification cascades
- **Benefit**: Loose coupling between services

---

## Limitations

Understanding Celery's limitations is crucial for proper adoption:

### 1. Infrastructure Requirements
- **Issue**: Requires message broker (Redis/RabbitMQ) and optionally result backend
- **Impact**: Adds infrastructure complexity and maintenance overhead
- **Mitigation**: Use Docker for easy setup, or managed services (AWS ElastiCache, etc.)

### 2. No Built-in Monitoring
- **Issue**: Celery doesn't include a UI for monitoring tasks
- **Impact**: Need third-party tools like Flower for task monitoring
- **Mitigation**: Install and configure Flower for web-based monitoring (still not as useful as Apache AirFlow UI)


### 3. Result Backend Dependency
- **Issue**: Return values require a result backend (Redis, database, etc.)
- **Impact**: Additional infrastructure for getting task results
- **Mitigation**: Use Redis or configure appropriate backend

### 4. Not Suitable for CPU-Bound Tasks
- **Issue**: Celery uses processes/threads, not ideal for CPU-intensive work
- **Impact**: Poor performance for heavy computations
- **Mitigation**: Use multiprocessing, or delegate to specialized workers


### 5. Broker Dependency
- **Issue**: If broker (Redis/RabbitMQ) is down, Celery can't work
- **Impact**: Single point of failure
- **Mitigation**: Use broker clustering, high-availability setups

### 6. No Built-in Workflow Engine
- **Issue**: While Celery supports chains/groups/chords, it's not a full workflow engine
- **Impact**: Complex workflows may need external orchestration (Airflow)
- **Mitigation**: Use Celery for task execution, Airflow for orchestration

---

## References

- [Celery Official Documentation](https://docs.celeryq.dev/)
- [Celery GitHub Repository](https://github.com/celery/celery)
- [Docker Official Documentation](https://docs.docker.com/)
- [Redis Documentation](https://redis.io/docs/)
- [Flower Documentation](https://flower.readthedocs.io/)
- [Celery Workflow Primitives (Canvas)](https://docs.celeryq.dev/en/stable/userguide/canvas.html)
- [Celery Stamping](https://docs.celeryq.dev/en/stable/userguide/canvas.html#stamping)
- [Celery Error Handling](https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying)
- [Apache Airflow](https://airflow.apache.org/) (Course Week 7 - Related tool)
- Course materials: YZV322E - Data Engineering Pipeline Tools

# KWS Library (kwslib)

Python client library for interacting with the KWS Platform backend API.

## Features

- **Complete API Coverage**: Wraps all backend API endpoints
- **MinIO Integration**: Download .wav and .npz files for training
- **Telegram Notifications**: Optional notifications for training jobs
- **Easy to Use**: Simple, intuitive API design
- **Type Hints**: Full type annotations for better IDE support

## Installation

```bash
pip install kwslib
```

Or from source:

```bash
git clone <repository>
cd KWS_Lib
pip install -e .
```

## Quick Start

### Basic Usage

```python
from kwslib import KWSClient

# Initialize client
client = KWSClient(base_url="http://localhost:8000")

# Login
client.login(username="admin", password="password")

# List datasets
datasets = client.datasets.list()
print(f"Found {datasets['total']} datasets")

# Get dataset details
dataset = client.datasets.get(dataset_id=1)
print(f"Dataset: {dataset['name']}")
```

### Download Dataset Split Files for Training

```python
from kwslib import KWSClient, DatasetSplitFilesClient

# Initialize API client
api = KWSClient(base_url="http://localhost:8000")
api.login(username="admin", password="password")

# Initialize files client (uses API, no direct MinIO connection)
files_client = DatasetSplitFilesClient(api)

# List all files in split
files_info = files_client.list_files(split_id=1, file_type="npz")
print(f"Found {files_info['total_files']} files")

# Download all .npz files
files_client.download_all_npz(
    split_id=1,
    output_dir="features"
)

# Download all .wav files
files_client.download_all_wav(
    split_id=1,
    output_dir="audio"
)

# Or download as ZIP
files_client.download_all_files_zip(
    split_id=1,
    file_type="npz",
    output_path="features.zip"
)

# Get presigned URLs (for Google Colab)
urls = files_client.get_file_urls(split_id=1, file_type="npz")
for file_info in urls["files"]:
    print(f"{file_info['file_name']}: {file_info['url']}")
```

### With Telegram Notifications

```python
from kwslib import KWSClient, TelegramNotifier

# Initialize
client = KWSClient(base_url="http://localhost:8000")
client.login(username="admin", password="password")

notifier = TelegramNotifier(
    bot_token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID"
)

# Create experiment run
run = client.experiments.create_run(
    experiment_id=1,
    name="Training Run 1",
    model_id=1,
    dataset_split_id=1
)

# Wait for completion
job_id = run.get("job_id")
status = client.jobs.wait_for_completion(job_id)

# Send notification
if status["status"] == "completed":
    notifier.send(f"Training completed! Results: {status['result']}")
else:
    notifier.send(f"Training failed: {status.get('error')}")
```

## API Modules

### Authentication
- `client.auth.login()` - Login
- `client.auth.logout()` - Logout
- `client.auth.get_me()` - Get current user info

### Datasets
- `client.datasets.list()` - List datasets
- `client.datasets.get()` - Get dataset
- `client.datasets.create()` - Create dataset
- `client.datasets.update()` - Update dataset
- `client.datasets.delete()` - Delete dataset
- `client.datasets.list_versions()` - List versions
- `client.datasets.create_version()` - Create version

### Models
- `client.models.list()` - List models
- `client.models.get()` - Get model
- `client.models.create()` - Create model
- `client.models.list_model_inits()` - List model architectures

### Experiments
- `client.experiments.list()` - List experiments
- `client.experiments.create()` - Create experiment
- `client.experiments.create_run()` - Create experiment run
- `client.experiments.list_runs()` - List experiment runs

### Dataset Splits
- `client.dataset_splits.list()` - List splits
- `client.dataset_splits.create()` - Create split
- `client.dataset_splits.download()` - Download split as ZIP
- `client.dataset_splits.generate()` - Generate split

### Audio
- `client.audio.list_keyword_samples()` - List keyword audio
- `client.audio.upload_keyword_sample()` - Upload audio
- `client.audio.get_keyword_sample_url()` - Get presigned URL

### Features
- `client.features.get_keyword_features()` - Get features
- `client.features.extract_keyword_features()` - Extract features

### Jobs
- `client.jobs.get()` - Get job status
- `client.jobs.list()` - List jobs
- `client.jobs.wait_for_completion()` - Wait for job completion

### Dataset Split Files Client
- `files_client.list_files()` - List all files in split
- `files_client.download_wav()` - Download a .wav file
- `files_client.download_npz()` - Download and load a .npz file
- `files_client.download_all_wav()` - Download all .wav files
- `files_client.download_all_npz()` - Download all .npz files
- `files_client.download_all_files_zip()` - Download all files as ZIP
- `files_client.get_file_urls()` - Get presigned URLs for all files

### Telegram Notifier
- `notifier.send()` - Send message
- `notifier.send_file()` - Send file
- `notifier.send_photo()` - Send photo

## Examples

### Complete Training Workflow

```python
from kwslib import KWSClient, DatasetSplitFilesClient, TelegramNotifier

# Setup
api = KWSClient(base_url="http://localhost:8000")
api.login(username="admin", password="password")

files_client = DatasetSplitFilesClient(api)

notifier = TelegramNotifier(
    bot_token="YOUR_TOKEN",
    chat_id="YOUR_CHAT_ID"
)

# 1. Create dataset split
split = api.dataset_splits.create(
    dataset_version_id=1,
    name="train_split",
    config_name="train",
    seed=42,
    split_option="fixed",
    fixed_count=1000,
    keyword_ids=[1, 2, 3]
)

split_id = split["dataset_splits_id"]

# 2. Generate split
job = api.dataset_splits.generate(split_id)
job_id = job["job_id"]

# 3. Wait for completion
status = api.jobs.wait_for_completion(job_id)
notifier.send(f"Split generation: {status['status']}")

# 4. Download features (via API, no direct MinIO access)
features_dir = f"features/split_{split_id}"
files_client.download_all_npz(
    split_id=split_id,
    output_dir=features_dir
)

# 5. Create experiment run
run = api.experiments.create_run(
    experiment_id=1,
    name="Training Run",
    model_id=1,
    dataset_split_id=split_id
)

notifier.send(f"Training started: {run['name']}")
```

### Google Colab Usage

```python
# In Google Colab, use presigned URLs for direct download
from kwslib import KWSClient, DatasetSplitFilesClient

api = KWSClient(base_url="https://your-api.com")
api.login(username="admin", password="password")

files_client = DatasetSplitFilesClient(api)

# Get presigned URLs
urls = files_client.get_file_urls(split_id=1, file_type="npz")

# Download in Colab
import urllib.request
for file_info in urls["files"]:
    urllib.request.urlretrieve(
        file_info["url"],
        f"/content/{file_info['file_name']}"
    )
```

### Google Colab Usage

```python
# In Google Colab, use presigned URLs for direct download
from kwslib import KWSClient, DatasetSplitFilesClient

api = KWSClient(base_url="https://your-api.com")
api.login(username="admin", password="password")

files_client = DatasetSplitFilesClient(api)

# Get presigned URLs
urls = files_client.get_file_urls(split_id=1, file_type="npz")

# Download in Colab
import urllib.request
for file_info in urls["files"]:
    urllib.request.urlretrieve(
        file_info["url"],
        f"/content/{file_info['file_name']}"
    )
```

## Configuration

### Environment Variables

You can set default values using environment variables:

```bash
export KWS_BASE_URL="http://localhost:8000"
export KWS_USERNAME="admin"
export KWS_PASSWORD="password"
export MINIO_ENDPOINT="localhost:9000"
export MINIO_ACCESS_KEY="minioadmin"
export MINIO_SECRET_KEY="minioadmin"
```

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

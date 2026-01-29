### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Set your HuggingFace API key in the environment or update `config.py`:

```python
# In geomind/config.py
HF_API_KEY = "your_huggingface_api_key"
```

Get a free API key from [HuggingFace](https://huggingface.co/settings/tokens).

### 3. Run the Agent

```bash
python main.py
```

## Example Queries

```

💬 "Create an RGB composite for the most recent image of London"

💬 "Calculate NDVI for Central Park, New York"

💬 "What images are available for Tokyo with less than 10% cloud cover?"
```

## Approach

### Traditional Approach
```
Full Scene Download → Local Storage → Process → Result
     ~720 MB            Disk I/O      Slow      
```

### GeoMind Approach (Zarr + fsspec)
```
HTTP Range Request → Stream Chunks → Process in Memory → Result
     ~1-5 MB           No disk          Fast           
```

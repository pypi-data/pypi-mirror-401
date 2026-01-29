###  Install Dependencies

```bash
pip install -r requirements.txt
```

###  Run the Agent

```bash
# Interactive mode
geomind

# Single query
geomind --query "Find recent imagery of Paris"
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

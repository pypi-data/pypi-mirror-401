# CFT Zarr Custom Codecs

Custom codecs for Zarr v3 optimized for CFT (Cryo-Fluorescence Tomography) data storage.

## Codecs

### Chunked JPEG Codec (`cft_zarr.chunked_jpeg`)

Efficient lossy compression for RGB images using chunked JPEG encoding.

- **Purpose**: Compress RGB images in chunks of N slices (default: 4) with JPEG compression
- **Chunk Shape**: Configurable, default (4, 512, 512, 3) for RGB
- **Quality**: Configurable JPEG quality (0-100, default: 85)

## Usage

```python
from cft_zarr.chunked_jpeg import ChunkedJPEGCodec
import zarr

# Create codec
codec = ChunkedJPEGCodec(quality=85, chunk_shape=(4, 512, 512, 3))

# Use with Zarr array
arr = zarr.open_array(
    'rgb.zarr',
    mode='w',
    shape=(100, 512, 512, 3),
    chunks=(4, 512, 512, 3),
    dtype='uint8',
    codec=codec
)
```

## Installation

```bash
cd src/python/public/cft_zarr
poetry install
```


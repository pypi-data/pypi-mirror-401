# `hwc-bgrx-8888-ndarray-to-pil-image`

Convert an HWC BGR 888 or BGRX 8888 NumPy ndarray to an HWC RGB 888 PIL.Image, with the alpha/unused channel discarded.

This function helps bridge interoperability between Qt, OpenCV (which often use HWC BGRX 8888 images), and PIL.

## Installation

```commandline
pip install hwc-bgrx-8888-ndarray-to-pil-image
```

## Usage

```python
import numpy as np
from hwc_bgrx_8888_ndarray_to_pil_image import hwc_bgrx_8888_ndarray_to_pil_image

# Example: create a dummy BGRX image
hwc_bgrx = np.random.randint(0, 256, (224, 224, 4), dtype=np.uint8)

pil_image = hwc_bgrx_8888_ndarray_to_pil_image(hwc_bgrx)  # <PIL.Image.Image image mode=RGB size=224x224>
pil_image.show()
```

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
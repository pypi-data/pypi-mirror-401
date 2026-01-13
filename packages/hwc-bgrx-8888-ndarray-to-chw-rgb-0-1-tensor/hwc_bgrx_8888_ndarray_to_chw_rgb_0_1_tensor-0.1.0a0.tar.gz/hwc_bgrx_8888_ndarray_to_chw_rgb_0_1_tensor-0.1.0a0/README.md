# `hwc-bgrx-8888-ndarray-to-chw-rgb-0-1-tensor`

Convert an HWC BGR 888 or BGRX 8888 NumPy ndarray to a CHW RGB PyTorch tensor, with pixel values normalized to `[0, 1]`
and the alpha/unused channel discarded.

This function helps bridge interoperability between Qt, OpenCV (which often use HWC BGRX 8888 images), and PyTorch (
which often uses CHW RGB tensors with pixel values normalized to `[0, 1]`).

## Installation

```commandline
pip install hwc-bgrx-8888-ndarray-to-chw-rgb-0-1-tensor
```

## Usage

```python
import numpy as np
from hwc_bgrx_8888_ndarray_to_chw_rgb_0_1_tensor import hwc_bgrx_8888_ndarray_to_chw_rgb_0_1_tensor

# Example: create a dummy BGRX image
hwc_bgrx = np.random.randint(0, 256, (224, 224, 4), dtype=np.uint8)

tensor = hwc_bgrx_8888_ndarray_to_chw_rgb_0_1_tensor(hwc_bgrx)
print(tensor.shape)  # (3, 224, 224)
print(tensor.min(), tensor.max())  # [0.0, 1.0]
```

## Notes

- This function makes the array contiguous for compatibility with PyTorch tensors.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
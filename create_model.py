"""
Masthik Anveshan - ResNet-50 Deep Learning Classifier Generator
Builds, initializes, validates, and serializes the 4-class ResNet-50 architecture
using PyTorch (torch, torch.nn) and Torchvision (torchvision.models).
"""

import os
from typing import Optional
# pyrefly: ignore[missing-import]
import torch
# pyrefly: ignore[missing-import]
import torch.nn as nn
# pyrefly: ignore[missing-import]
from torchvision import models


def build_resnet50_classifier(num_classes: int = 4) -> nn.Module:
    """
    Constructs the ResNet-50 architecture with custom fully connected classification head.

    Args:
        num_classes: Number of target categories (Default: 4 - Glioma, Meningioma, Pituitary, No Tumor).

    Returns:
        Configured PyTorch nn.Module ready for inference or fine-tuning.
    """
    # Instantiate base ResNet-50 backbone
    resnet = models.resnet50(weights=None)

    # Ensure all parameters require gradient during training
    for param in resnet.parameters():
        param.requires_grad = True

    # Replace final fully connected layer with custom deep classifier head
    in_features = resnet.fc.in_features
    classifier_head = nn.Sequential(
        nn.Linear(in_features, 2048),
        nn.SELU(),
        nn.Dropout(p=0.4),
        nn.Linear(2048, 2048),
        nn.SELU(),
        nn.Dropout(p=0.4),
        nn.Linear(2048, num_classes),
        nn.LogSigmoid()
    )

    # Initialize weights of the custom head
    for layer in classifier_head:
        if isinstance(layer, nn.Linear):
            nn.init.kaiming_normal_(layer.weight, nonlinearity='linear')
            nn.init.constant_(layer.bias, 0.0)

    resnet.fc = classifier_head
    return resnet


def validate_model_forward(model: nn.Module) -> bool:
    """
    Executes a test forward pass with a synthetic dummy input tensor to verify output tensor dimensionality.
    """
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    dummy_input = torch.randn(1, 3, 224, 224, device=device)
    with torch.no_grad():
        output = model(dummy_input)

    expected_shape = (1, 4)
    if output.shape != expected_shape:
        raise ValueError(f"Model output shape mismatch: expected {expected_shape}, got {output.shape}")
    return True


def save_resnet50_weights(output_path: Optional[str] = None) -> str:
    """
    Builds the model, validates its forward pass, and writes state_dict to disk.
    """
    if output_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(current_dir, 'models')
        os.makedirs(models_dir, exist_ok=True)
        output_path = os.path.join(models_dir, 'bt_resnet50_model.pt')

    model = build_resnet50_classifier(num_classes=4)
    validate_model_forward(model)

    torch.save(model.state_dict(), output_path)
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print("[create_model] ResNet-50 successfully created and validated.")
    print(f"[create_model] State dictionary saved to: {output_path}")
    print(f"[create_model] Model weight file size: {file_size_mb:.1f} MB")
    return output_path


if __name__ == '__main__':
    save_resnet50_weights()

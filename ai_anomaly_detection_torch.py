AI Anomaly Detection (PyTorch)
import torch
import torch.nn as nn

class AnomalyDetector(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

model = AnomalyDetector()

def detect_anomaly(qber, noise, mismatch):
    x = torch.tensor([[qber, noise, mismatch]], dtype=torch.float32)
    score = model(x)
    return score.item() > 0.6

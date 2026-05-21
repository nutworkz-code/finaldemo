import logging
import random

from fastapi import APIRouter, Depends

from app.models.user import User
from app.services.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/kubernetes", tags=["Kubernetes"])


def _mock_cluster_status() -> dict:
    """Generate mock Kubernetes cluster status data."""
    nodes = []
    for i in range(1, 4):
        nodes.append(
            {
                "name": f"node-{i}",
                "status": "Ready",
                "roles": "worker" if i > 1 else "control-plane",
                "cpu_usage_percent": round(random.uniform(10, 80), 1),
                "memory_usage_percent": round(random.uniform(20, 75), 1),
                "pods_running": random.randint(5, 30),
            }
        )

    pods = []
    namespaces = ["default", "kube-system", "monitoring", "opsinsight"]
    statuses = ["Running", "Running", "Running", "Pending", "Running"]
    for i in range(1, 9):
        pods.append(
            {
                "name": f"pod-{i}",
                "namespace": random.choice(namespaces),
                "status": random.choice(statuses),
                "restarts": random.randint(0, 3),
                "age_hours": random.randint(1, 720),
            }
        )

    return {
        "cluster_name": "opsinsight-cluster",
        "version": "v1.29.4",
        "nodes": nodes,
        "total_pods": len(pods),
        "pods": pods,
        "namespaces": len(namespaces),
    }


@router.get("/status")
def cluster_status(_current_user: User = Depends(get_current_user)) -> dict:
    """Get Kubernetes cluster status (mock data)."""
    return _mock_cluster_status()

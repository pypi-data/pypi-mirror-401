"""
Pattern Marketplace
Share and monetize successful entropy patterns
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class PatternMarketplace:
    """
    Marketplace for entropy homeostasis patterns
    Users can upload, download, and rate patterns
    """

    def __init__(self, storage_dir: str = "patterns"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.patterns_index = self._load_index()

    def _load_index(self) -> Dict:
        """Load patterns index"""
        index_file = self.storage_dir / "index.json"
        if index_file.exists():
            return json.loads(index_file.read_text())
        return {}

    def _save_index(self):
        """Save patterns index"""
        index_file = self.storage_dir / "index.json"
        index_file.write_text(json.dumps(self.patterns_index, indent=2))

    def upload_pattern(
        self, name: str, pattern: Dict, description: str, tags: List[str]
    ) -> Dict[str, Any]:
        """Upload a new pattern to marketplace"""
        pattern_id = hashlib.sha256(
            f"{name}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        pattern_data = {
            "id": pattern_id,
            "name": name,
            "description": description,
            "tags": tags,
            "pattern": pattern,
            "uploaded_at": datetime.now().isoformat(),
            "uploaded_by": "user",  # Would be actual user in production
            "download_count": 0,
            "ratings": [],
            "average_rating": 0.0,
            "success_metrics": self._analyze_pattern_success(pattern),
        }

        # Save pattern file
        pattern_file = self.storage_dir / f"{pattern_id}.json"
        pattern_file.write_text(json.dumps(pattern_data, indent=2))

        # Update index
        self.patterns_index[pattern_id] = {
            "id": pattern_id,
            "name": name,
            "description": description,
            "tags": tags,
            "download_count": 0,
            "average_rating": 0.0,
        }
        self._save_index()

        return {
            "pattern_id": pattern_id,
            "status": "uploaded",
            "marketplace_url": f"marketplace://patterns/{pattern_id}",
        }

    def download_pattern(self, pattern_id: str) -> Dict[str, Any]:
        """Download a pattern from marketplace"""
        pattern_file = self.storage_dir / f"{pattern_id}.json"

        if not pattern_file.exists():
            return {"error": "Pattern not found"}

        pattern_data = json.loads(pattern_file.read_text())

        # Increment download count
        pattern_data["download_count"] += 1
        pattern_file.write_text(json.dumps(pattern_data, indent=2))

        # Update index
        if pattern_id in self.patterns_index:
            self.patterns_index[pattern_id]["download_count"] += 1
            self._save_index()

        return {
            "pattern": pattern_data["pattern"],
            "success_metrics": pattern_data["success_metrics"],
            "implementation_guide": self._generate_implementation_guide(pattern_data),
            "compatible_with": self._check_compatibility(pattern_data),
        }

    def rate_pattern(self, pattern_id: str, rating: float, review: str = ""):
        """Rate a pattern"""
        pattern_file = self.storage_dir / f"{pattern_id}.json"

        if not pattern_file.exists():
            return {"error": "Pattern not found"}

        pattern_data = json.loads(pattern_file.read_text())

        # Add rating
        pattern_data["ratings"].append(
            {
                "rating": rating,
                "review": review,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Recalculate average
        ratings = [r["rating"] for r in pattern_data["ratings"]]
        pattern_data["average_rating"] = sum(ratings) / len(ratings)

        pattern_file.write_text(json.dumps(pattern_data, indent=2))

        # Update index
        if pattern_id in self.patterns_index:
            self.patterns_index[pattern_id]["average_rating"] = pattern_data[
                "average_rating"
            ]
            self._save_index()

        return {"status": "rated", "new_average": pattern_data["average_rating"]}

    def search_patterns(
        self, query: str = "", tags: List[str] = None, min_rating: float = 0.0
    ) -> List[Dict]:
        """Search patterns in marketplace"""
        results = []

        for pattern_id, pattern_meta in self.patterns_index.items():
            # Filter by query
            if (
                query
                and query.lower() not in pattern_meta["name"].lower()
                and query.lower() not in pattern_meta["description"].lower()
            ):
                continue

            # Filter by tags
            if tags and not any(tag in pattern_meta["tags"] for tag in tags):
                continue

            # Filter by rating
            if pattern_meta["average_rating"] < min_rating:
                continue

            results.append(pattern_meta)

        # Sort by popularity
        results.sort(
            key=lambda x: (x["average_rating"], x["download_count"]), reverse=True
        )

        return results

    def get_trending_patterns(self, limit: int = 10) -> List[Dict]:
        """Get trending patterns"""
        all_patterns = list(self.patterns_index.values())
        all_patterns.sort(key=lambda x: x["download_count"], reverse=True)
        return all_patterns[:limit]

    def _analyze_pattern_success(self, pattern: Dict) -> Dict:
        """Analyze pattern success metrics"""
        # Placeholder - would analyze actual pattern effectiveness
        return {
            "stability_improvement": 0.25,
            "chaos_reduction": 0.30,
            "homeostasis_time": "85%",
            "recommended_for": ["trading", "logistics", "multi-agent-coordination"],
        }

    def _generate_implementation_guide(self, pattern_data: Dict) -> List[str]:
        """Generate implementation guide for pattern"""
        return [
            "1. Initialize your EntropyBrain instance",
            "2. Apply pattern configuration to regulator",
            "3. Set recommended thresholds",
            "4. Monitor for 24 hours",
            "5. Fine-tune based on your specific use case",
        ]

    def _check_compatibility(self, pattern_data: Dict) -> List[str]:
        """Check pattern compatibility"""
        return [
            "entropic-core >= 1.0.0",
            "AutoGen",
            "LangChain",
            "Custom multi-agent systems",
        ]

    def calculate_revenue_share(self, pattern_id: str) -> Dict[str, Any]:
        """Calculate revenue for pattern creator"""
        pattern_file = self.storage_dir / f"{pattern_id}.json"

        if not pattern_file.exists():
            return {"error": "Pattern not found"}

        pattern_data = json.loads(pattern_file.read_text())

        # Revenue calculation (placeholder)
        downloads = pattern_data["download_count"]
        price_per_download = 5.0  # $5 per download
        platform_fee = 0.30  # 30% platform fee

        gross_revenue = downloads * price_per_download
        net_revenue = gross_revenue * (1 - platform_fee)

        return {
            "pattern_id": pattern_id,
            "downloads": downloads,
            "gross_revenue": gross_revenue,
            "platform_fee": gross_revenue * platform_fee,
            "net_revenue": net_revenue,
            "average_rating": pattern_data["average_rating"],
            "estimated_monthly": net_revenue
            / max(1, self._months_since_upload(pattern_data)),
        }

    def _months_since_upload(self, pattern_data: Dict) -> int:
        """Calculate months since pattern upload"""
        uploaded = datetime.fromisoformat(pattern_data["uploaded_at"])
        months = (datetime.now() - uploaded).days / 30
        return max(1, int(months))

    def submit_pattern(
        self,
        name: str,
        description: str,
        pattern: Dict,
        author: str,
        tags: List[str] = None,
    ) -> Dict[str, Any]:
        """Submit a pattern (alias for upload_pattern)"""
        return self.upload_pattern(
            name=name, pattern=pattern, description=description, tags=tags or []
        )

    def get_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Get a pattern (alias for download_pattern)"""
        result = self.download_pattern(pattern_id)
        if "error" in result:
            return None
        return result

"""
Business Metrics Module - ROI and Business Intelligence for Entropic Core

Tracks business-relevant metrics like cost savings, efficiency,
and return on investment from using Entropic Core.
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# Configuración de costes centralizada
TOKEN_COSTS = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
    "default": {"input": 0.002, "output": 0.006},
}


class MetricType(str, Enum):
    COST_SAVED = "cost_saved"
    TOKENS_SAVED = "tokens_saved"
    HALLUCINATIONS_PREVENTED = "hallucinations_prevented"
    INTERVENTIONS_PERFORMED = "interventions_performed"


@dataclass
class CostEvent:
    """Representa un evento individual de coste"""

    timestamp: float
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    saved_tokens: int = 0
    saved_cost: float = 0.0
    intervention_type: Optional[str] = None


@dataclass
class ROISummary:
    """Resumen de retorno de inversión"""

    period_start: datetime
    period_end: datetime
    total_llm_calls: int
    total_tokens: int
    total_cost: float
    tokens_saved: int
    cost_saved: float
    hallucinations_prevented: int
    interventions: int
    roi_percentage: float

    @property
    def total_roi_percentage(self) -> float:
        return self.roi_percentage

    @property
    def interventions_performed(self) -> int:
        return self.interventions


@dataclass
class BusinessMetricsConfig:
    default_model: str = "gpt-4o"
    retention_days: int = 90
    cost_multiplier: float = 1.0


class BusinessMetrics:
    """
    Tracking de métricas de negocio.
    Refactorizado para cumplir con los tests de integración y ROI.
    """

    def __init__(self, config: BusinessMetricsConfig = None):
        self.config = config or BusinessMetricsConfig()
        self.events: List[CostEvent] = []
        self.hallucinations_prevented: int = 0

        # Atributos requeridos por tests
        self.total_interventions: int = 0
        self.interventions_count: int = 0
        self.total_tokens: int = 0  # FIX: Soluciona AttributeError en test_track_tokens

        # Acumuladores rápidos
        self.total_cost: float = 0.0
        self.total_saved: float = 0.0

    def record_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        saved_tokens: int = 0,
        intervention_type: Optional[str] = None,
    ) -> CostEvent:
        """Registra una llamada a LLM y actualiza acumuladores"""
        costs = TOKEN_COSTS.get(model, TOKEN_COSTS["default"])

        call_cost = (input_tokens / 1000 * costs["input"]) + (
            output_tokens / 1000 * costs["output"]
        )
        saved_call_cost = saved_tokens / 1000 * costs["input"]

        # Actualizar contadores globales (Requerido por tests)
        self.total_cost += call_cost
        self.total_saved += saved_call_cost
        self.total_tokens += input_tokens + output_tokens

        event = CostEvent(
            timestamp=time.time(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=call_cost,
            saved_tokens=saved_tokens,
            saved_cost=saved_call_cost,
            intervention_type=intervention_type,
        )

        self.events.append(event)

        if intervention_type:
            self.interventions_count += 1
            self.total_interventions += 1

        return event

    def track_tokens(
        self,
        count_or_model: Union[int, str],
        model_or_in: Union[str, int] = "gpt-4",
        saved_or_out: Union[bool, int] = False,
    ) -> None:
        """
        Método de compatibilidad para tracking de tokens.
        Maneja tanto (count, model, saved) como (model, input, output).
        """
        # Caso: track_tokens(model, input, output)
        if isinstance(count_or_model, str):
            self.record_call(
                model=count_or_model,
                input_tokens=int(model_or_in),
                output_tokens=int(saved_or_out),
            )
            return

        # Caso: track_tokens(count, model, saved=True)
        count = int(count_or_model)
        model = str(model_or_in)
        if bool(saved_or_out):
            self.record_call(model, 0, 0, saved_tokens=count)
        else:
            self.record_call(model, count, 0)

    def track_intervention(self, type: str = "standard") -> None:
        """Registra una intervención"""
        self.record_call("system", 0, 0, intervention_type=type)

    def record_hallucination_prevented(self) -> None:
        self.hallucinations_prevented += 1

    def generate_roi_report(self) -> Dict[str, Any]:
        """Genera reporte compatible con tests que esperan diccionarios"""
        roi = (self.total_saved / self.total_cost * 100) if self.total_cost > 0 else 0.0
        return {
            "total_cost": self.total_cost,
            "total_saved": self.total_saved,
            "roi": roi,
            "total_tokens": self.total_tokens,
            "interventions": self.total_interventions,
        }

    def get_summary(self, days: int = None) -> ROISummary:
        """Resumen detallado de ROI"""
        limit = datetime.now() - timedelta(days=days or self.config.retention_days)
        recent = [e for e in self.events if e.timestamp >= limit.timestamp()]

        t_tokens = sum(e.input_tokens + e.output_tokens for e in recent)
        t_cost = sum(e.cost for e in recent)
        s_tokens = sum(e.saved_tokens for e in recent)
        s_cost = sum(e.saved_cost for e in recent)

        return ROISummary(
            period_start=limit,
            period_end=datetime.now(),
            total_llm_calls=len(recent),
            total_tokens=t_tokens,
            total_cost=t_cost,
            tokens_saved=s_tokens,
            cost_saved=s_cost,
            hallucinations_prevented=self.hallucinations_prevented,
            interventions=self.interventions_count,
            roi_percentage=(s_cost / t_cost * 100) if t_cost > 0 else 0.0,
        )

    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas actuales"""
        return {
            "total_events": len(self.events),
            "hallucinations_prevented": self.hallucinations_prevented,
            "interventions": self.interventions_count,
            "total_cost": self.total_cost,
            "total_saved": self.total_saved,
            "total_tokens": self.total_tokens,
        }


# Alias para compatibilidad
ROIReport = ROISummary


def create_metrics(config: BusinessMetricsConfig = None) -> BusinessMetrics:
    return BusinessMetrics(config)

"""Analytics Service for tracking usage and audit logs via PostgreSQL."""

import asyncio
from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from ..core.config import ENABLE_ANALYTICS, POSTGRES_DB

class AnalyticsService:
    """
    Handles optional analytics tracking to a PostgreSQL database.
    Does nothing if ENABLE_ANALYTICS is False or POSTGRES_DB is missing.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalyticsService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
            
        self.enabled = ENABLE_ANALYTICS and POSTGRES_DB
        self.engine = None
        self.session_maker = None
        
        if self.enabled:
            # Create async engine
            # POSTGRES_DB examples: postgresql+asyncpg://user:pass@localhost:5432/dbname
            # Ensure the driver is asyncpg if not specified, usually user provides full DSN
            self.engine = create_async_engine(POSTGRES_DB, echo=False)
            self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)
            
        self.initialized = True

    async def ensure_tables(self):
        """Create necessary tables if they don't exist."""
        if not self.enabled:
            return
            
        async with self.engine.begin() as conn:
            # Table: token_usage
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS analytics_token_usage (
                    id SERIAL PRIMARY KEY,
                    project_id TEXT,
                    model TEXT,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    total_tokens INTEGER,
                    cost_usd DOUBLE PRECISION,
                    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
                );
            """))
            
            # Table: audit_log
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS analytics_audit_log (
                    id SERIAL PRIMARY KEY,
                    project_id TEXT,
                    action TEXT,
                    details JSONB,
                    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
                );
            """))

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate USD cost based on model pricing (per 1M tokens)."""
        # Pricing Map (Model -> [Input Cost, Output Cost] per 1M tokens)
        PRICING = {
            # OpenAI
            "gpt-4o": [5.00, 15.00],
            "gpt-4o-mini": [0.15, 0.60],
            "o1-preview": [15.00, 60.00],
            "o1-mini": [3.00, 12.00],
            "gpt-4-turbo": [10.00, 30.00],
            "gpt-3.5-turbo": [0.50, 1.50],
            
            # Anthropic
            "claude-3-5-sonnet": [3.00, 15.00],
            "claude-3-opus": [15.00, 75.00],
            "claude-3-haiku": [0.25, 1.25],
            
            # Generic/Default
            "default": [0.0, 0.0]
        }
        
        # Normalize model name for matching (e.g., 'gpt-4o-2024-05-13' -> 'gpt-4o')
        model_low = model.lower()
        pricing = PRICING.get("default")
        
        for key in PRICING:
            if key in model_low and key != "default":
                pricing = PRICING[key]
                break
                
        input_cost = (input_tokens / 1_000_000) * pricing[0]
        output_cost = (output_tokens / 1_000_000) * pricing[1]
        
        return round(input_cost + output_cost, 6)

    async def track_token_usage(
        self, 
        project_id: str, 
        model: str, 
        input_tokens: int, 
        output_tokens: int,
        total_tokens: int,
        cost_usd: float = 0.0
    ):
        """Record token usage."""
        if not self.enabled:
            return

        # Auto-calculate cost if not provided
        if cost_usd == 0.0:
            cost_usd = self.calculate_cost(model, input_tokens, output_tokens)

        try:
            async with self.session_maker() as session:
                await session.execute(
                    text("""
                        INSERT INTO analytics_token_usage 
                        (project_id, model, input_tokens, output_tokens, total_tokens, cost_usd) 
                        VALUES (:pid, :model, :in_tok, :out_tok, :tot_tok, :cost)
                    """),
                    {
                        "pid": project_id,
                        "model": model, 
                        "in_tok": input_tokens,
                        "out_tok": output_tokens,
                        "tot_tok": total_tokens,
                        "cost": cost_usd
                    }
                )
                await session.commit()
        except Exception as e:
            # Fallback: Don't crash the app if analytics fails
            print(f"Analytics Error (Token): {e}")

    async def log_action(self, project_id: str, action: str, details: Dict[str, Any]):
        """Record an audit log application event."""
        if not self.enabled:
            return
            
        try:
            import json
            details_json = json.dumps(details)
            async with self.session_maker() as session:
                await session.execute(
                    text("""
                        INSERT INTO analytics_audit_log (project_id, action, details) 
                        VALUES (:pid, :action, :details)
                    """),
                    {
                        "pid": project_id,
                        "action": action,
                        "details": details_json
                    }
                )
                await session.commit()
        except Exception as e:
             print(f"Analytics Error (Audit): {e}")

# Global instance
analytics = AnalyticsService()

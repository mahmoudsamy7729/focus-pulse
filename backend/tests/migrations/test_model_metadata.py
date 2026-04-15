from app.core.database import Base

from app.modules.ai_insights.models import AIInsightRun, AIInsightRunSource
from app.modules.daily_logs.models import DailyLog
from app.modules.imports.models import ImportRowOutcome, ImportRun
from app.modules.notes.models import Note
from app.modules.tasks.models import Category, Task


def test_phase_1_models_are_registered_in_metadata() -> None:
    assert DailyLog.__tablename__ in Base.metadata.tables
    assert Task.__tablename__ in Base.metadata.tables
    assert Category.__tablename__ in Base.metadata.tables
    assert Note.__tablename__ in Base.metadata.tables
    assert ImportRun.__tablename__ in Base.metadata.tables
    assert ImportRowOutcome.__tablename__ in Base.metadata.tables
    assert AIInsightRun.__tablename__ in Base.metadata.tables
    assert AIInsightRunSource.__tablename__ in Base.metadata.tables

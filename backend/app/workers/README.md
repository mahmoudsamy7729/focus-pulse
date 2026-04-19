# Workers

Phase 4 registers `ai_insights.process_analysis_run`.

The task accepts an AI insight run ID and owner ID, opens a backend database
session, constructs the AI analysis services, delegates all business rules to
`AIAnalysisService`, commits the result, and returns a small status payload.
Retry classification, output validation, failure detail persistence, and run
status transitions stay in the service layer.

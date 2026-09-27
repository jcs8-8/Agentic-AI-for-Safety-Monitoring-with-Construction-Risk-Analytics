# Copilot Demo Script

Open any dashboard page and select **Copilot** in the lower-right corner. The default frontend mode is mock mode, so these queries work without an LLM key.

1. `Show all PPE violations in Zone B this week` - alert cards and Alert Management deep link.
2. `How many critical alerts are open right now?` - open alert summary.
3. `What's the current project risk score?` - project gauge and zone ranking.
4. `Which zone is riskiest today?` - zone ranking with open hazard counts.
5. `Compare safety compliance this month vs last month` - inline trend chart.
6. `Show me hazard trends by time of day` - inline analytics chart.
7. `What's the risk forecast for tomorrow's night shift?` - forecast confidence and recommended actions.
8. `If we have 3 open scaffolding hazards, what's our exposure?` - what-if forecast card.
9. `Generate yesterday's site report` - report preview and PDF action.
10. `Assign the Zone C scaffolding alert to Rajesh` - confirmation card before workflow execution.

Set `VITE_COPILOT_MODE=live` to call `/api/v1/copilot/chat`. The backend also exposes the requested `/api/copilot/chat` alias. In live mode, replace `answer()` in `backend/app/services/copilot_service.py` with the project’s LLM/function-calling adapter while retaining the typed response contract.
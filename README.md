# Cardiac Baroreflex Sensitivity (BRS) & Vagal Tone Sentinel Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Sequence method Baroreflex Sensitivity (BRS ms/mmHg), blood pressure-to-RR interval cross-correlation, and autonomic vagal failure screener. Built for GenPark (https://www.genpark.ai).

## Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## MCP Tools Exposed
- `compute_baroreflex_sensitivity_index`: Calculate BRS slope (ms/mmHg) from continuous beat-to-beat systolic pressure and ECG RR-intervals.
- `synthesize_vagal_nerve_stimulation_protocol`: Formulate resonant frequency slow-paced breathing (0.1 Hz / 6 breaths/min) to restore baroreflex buffering.

## Installation & Usage
```bash
python -m genpark_personal_agent_cardiac_baroreflex_sensitivity_autonomic_skill.server --test
```

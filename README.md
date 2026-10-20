# Critical Power & W-Prime Anaerobic Work Capacity Battery Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Cycling & running 2-parameter Critical Power (CP) and anaerobic work capacity (W') depleting/reconstituting battery model for real-time race surge pacing. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `compute_critical_power_and_wprime`: Calculate Critical Power (watts) and anaerobic work capacity W' (kilojoules) from 3-minute and 12-minute maximal mean power efforts.
- `simulate_wprime_depletion_and_recovery`: Simulate real-time anaerobic battery W' depletion during above-CP surges and exponential reconstitution during sub-CP recovery intervals.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_personal_agent_critical_power_wprime_anaerobic_battery_skill.server --test
```

"""اختبارات أولية."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from bikagent.agent import BikAgent

def test_agent_returns_string():
    agent = BikAgent(config={"max_cycles": 1})
    result = agent.run("اختبار")
    assert isinstance(result, str)
    assert "اختبار" in result

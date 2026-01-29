import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

advisor_port = 9989

llm_model = "mistral/mistral-small-latest"
# llm_model = "gpt-4o-mini"

max_token = 100

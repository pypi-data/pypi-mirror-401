A client that just sends two ACL messages to a refactoring advisor agent at port 9999:
one tell-message with a specification and one propose-message with a source code.

You can use this client with any A2A/ACL agent listening on port 9999.

First run your advisor agent, then run this client :

```bash
  python3 run_test_client.py
```

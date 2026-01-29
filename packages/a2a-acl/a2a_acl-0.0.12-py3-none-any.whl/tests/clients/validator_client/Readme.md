A client that just sends two ACL messages to a validator agent at port 9999:
one tell-message with a specification and one propose-message with a requirement.

You can use this client with any A2A/ACL agent listening on port 9999.

First run your other agents, then run the client :

```bash
  python3 run_test_client.py
```

from chat import ChatSession
import json
import sys

# allow use to provide the query as a command line argument
if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    raise Exception("Please provide a query as a command line argument")

sys_msg = "You are a chatbot designed to help people answer questions about the news"

session = ChatSession(sys_msg)

ans = session.answer_query(query)
print("Response:", "\n", ans)
print("\n\n")
print("Citations:", "\n", json.dumps(session.citations[ans], indent=4))
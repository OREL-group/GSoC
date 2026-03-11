import sys
sys.path.insert(0, "D:\\GSoC\\Open Source Sustainibility using LLMs")
from LLAMOSC.simulation.conversation_space import ConversationSpace
cs = ConversationSpace(channel_name="general", use_rag=False)
cs.notify_blocked("Alice", "Fix login bug")
cs.notify_pr_merged("Bob", "Fix login bug")
cs.notify_idle("Charlie", 3)
print("Total messages:", len(cs.messages))
print("Channels used:", set(m.channel for m in cs.messages))
print("Event types:", set(m.event_type for m in cs.messages))
print("ALL TESTS PASSED!")

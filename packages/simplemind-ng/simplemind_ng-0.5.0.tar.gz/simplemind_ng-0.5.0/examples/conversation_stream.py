from _context import sm

# Create a conversation
conv = sm.create_conversation()

# Add a message to the conversation (role defaults to "user")
conv.add_message(text="Write a short poem about the stars")

# Stream the response
print("Assistant: ", end="")
for chunk in conv.send_stream():
    print(chunk, end="", flush=True)
print()  # newline after streaming completes

# Continue the conversation with another streamed response
conv.add_message(text="Now make it shorter, just 4 lines")

print("\nAssistant: ", end="")
for chunk in conv.send_stream():
    print(chunk, end="", flush=True)
print()

from context_compressor import ContextCompressor, TokenCounter

# Define your summarizer function
def simple_summarizer(messages_list, previous_summary=None):
    """
    Args:
        messages_list: List of dicts like [{"role": "user", "content": "..."}]
        previous_summary: Optional previous summary to build upon
    Returns:
        A summary string
    """
    summary_parts = []
    
    if previous_summary:
        summary_parts.append(f"[Previous: {previous_summary}]")
    for msg in messages_list:
        role = msg["role"]
        content = msg["content"]
        # Take first 50 chars of each message
        snippet = content[:50].replace("\n", " ")
        summary_parts.append(f"{role.upper()}: {snippet}...")
    return "\n".join(summary_parts)

# Initialize compressor
compressor = ContextCompressor(
    summarizer=simple_summarizer,
    t_max=2000,      # Max tokens before compression
    t_retained=300, # Tokens to keep after compression
    t_summary=200,   # Reserved tokens for summary
    tokenizer=TokenCounter(
        model_name="gpt-4o",
        use_transformers=False   # Will use default tiktoken encoding
    )
)

# Add messages to your conversation
for _ in range(100):
    compressor.add_message("Hello, can you give me a short introduction about yourself?", role="user")
    compressor.add_message("Sure! I am a helpful assistant developed by OpenAI. I can help you with your questions.", role="assistant")

# Get compressed context (auto-compresses if needed)
context = compressor.get_current_context()

# View statistics
stats = compressor.get_stats()
print(f"Compressions: {stats['compression_count']}")
print(f"Tokens saved: {stats['total_tokens_saved']}")
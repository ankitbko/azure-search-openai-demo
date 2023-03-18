from langchain.memory import ConversationBufferWindowMemory
import pickle

class MemoryCache:
    memory_cache = {}

    @classmethod
    def create_memory(cls):
        return ConversationBufferWindowMemory(memory_key="chat_history", output_key='answer', return_messages=True, k=10)

    @classmethod
    def get_memory(cls, id):
        if id in cls.memory_cache:
            return cls.memory_cache[id]
        
        memory = cls.create_memory()
        cls.memory_cache[id] = memory
        return memory
    
    @classmethod
    def save(cls):
        with open('memory_cache.pickle', 'wb') as f:
            pickle.dump(cls.memory_cache, f)
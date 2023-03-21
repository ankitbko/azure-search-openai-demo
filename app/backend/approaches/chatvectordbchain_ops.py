from pathlib import Path
from approaches.approach import Approach
from langchainadapters import HtmlCallbackHandler
"""Chain for chatting with a vector database."""
from langchain import PromptTemplate
from langchain.schema import BaseLanguageModel
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.chat_vector_db.base import ChatVectorDBChain
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel

from langchain.chains.base import Chain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms.base import BaseLLM
from langchain.prompts.base import BasePromptTemplate
from langchain.vectorstores.base import VectorStore
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def get_chat_history(inputs) -> str:
    res = []
    for i in range(0, len(inputs), 2):
        res.append(f"Human:{inputs[i].content}\nAI:{inputs[i+1].content}")
    
    return "\n".join(res)

system_template="""Use the following pieces of context to answer the users question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
ALWAYS include the "SOURCE" for each fact that you use in response. The "SOURCE" part should be a reference to the source of the document from which you got your answer. Use square brackets to reference the "SOURCES", e.g. [info1.txt]. Don't combine sources, list each source separately, in square bracket, separated by space e.g. [C:/Users/JohnDoe/Documents/info1.txt] [C:/Users/JohnDoe/Documents/info2.txt]. In these examples, info1.txt and info2.pdf are source of the document you are referencing. Always list the complete path to the source of the document, e.g. [C:/Users/JohnDoe/Documents/info1.txt]. 

Example of your response should be as below where square brackets contains the Source for the facts used to generate response:

```
The answer is foo [https://xyz.com/a]. This is more information about it [https://abc.com/a].
```

Begin!
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
qa_prompt = ChatPromptTemplate.from_messages(messages)

class ChatVectorDBChainApproach(Approach):
    def __init__(self, llm, vectorstore):
        self.llm = llm
        self.vectorstore = vectorstore

    def run(self, q: str, overrides: dict, memory) -> any:
        cb_handler = HtmlCallbackHandler()
        cb_manager = CallbackManager(handlers=[cb_handler])

        question_generator = LLMChain(llm=self.llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=True)
        doc_chain = load_qa_with_sources_chain(self.llm, chain_type="stuff",prompt=qa_prompt)

        qa = ChatVectorDBChain(
            memory=memory,
            vectorstore=self.vectorstore,
            question_generator=question_generator,
            combine_docs_chain=doc_chain,
            get_chat_history=get_chat_history, 
            verbose=True,
            return_source_documents=True,
            callback_manager=cb_manager
        )

        result = qa(q[-1]['user'])

        data_points = [{'source': doc.metadata['source'], 'content': doc.page_content} for doc in result['source_documents']]
        return {"data_points": data_points or [], "answer": result['answer'], "thoughts": cb_handler.get_and_reset_log()}
        
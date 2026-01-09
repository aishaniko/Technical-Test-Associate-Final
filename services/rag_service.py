from langgraph.graph import StateGraph, END


class RAGService:
    def __init__(self, embedding_service, document_store):
        self.embedding_service = embedding_service
        self.document_store = document_store
        self.chain = self._build_workflow()

    def _retrieve_node(self, state):
        query = state["question"]
        emb = self.embedding_service.generate(query)

        results = self.document_store.search(emb, query)
        state["context"] = results
        return state

    def _answer_node(self, state):
        ctx = state["context"]
        question = state["question"]

        if not ctx:
            answer = "I Dont Know"
        else:
            question_lower = question.lower()
            context_text = ctx[0].lower()

            question_words = question_lower.split()
            relevant_words = [
                word
                for word in question_words
                if len(word) > 3 and word in context_text
            ]

            if relevant_words:
                answer = f"I Found This: '{ctx[0][:100]}...'"
            else:
                answer = "I Dont Know"

        state["answer"] = answer
        return state

    def _build_workflow(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("answer", self._answer_node)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def ask(self, question: str) -> dict:
        return self.chain.invoke({"question": question})

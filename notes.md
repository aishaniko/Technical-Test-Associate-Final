# Refactoring Notes - RAG Service Code Quality Test

## Main Design Decisions

### 1. Modular Architecture & Concern Separation
I reorganized the monolithic `main.py` into a modular framework with distinct roles:
- **API Layer**(`api/routes.py`): Manages error handling, HTTP requests, and response formatting - **Business Logic Layer**(`services/`): Contains essential application logic
  - `EmbeddingService`: Produces text vector embeddings - `DocumentStore`: Oversees document storage using Qdrant/in-memory fallback
  - `RAGService`: Uses LangGraph to orchestrate the RAG workflow
- **Configuration Layer** (`main.py`): Initializes and connects all dependencies. - **Data Models Layer** (`models/schemas.py`): Defines Pydantic models for request/response validation

### 2. Application of Object-Oriented Principles:
- **Encapsulation**: Every service class encapsulates its own state and behavior
- **Dependency Injection**: Services receive dependencies through constructors, making them interchangeable and testable
- **Single Responsibility**: Every class has a single, distinct function (e.g., `DocumentStore` only handles storage)

### 3. Elimination of Anti-Patterns
- **Removed Global State**: Eliminated global variables like `docs_memory` and `USING_QDRANT`
- **Reduced Coupling**: Services are loosely coupled through well-defined interfaces
- **Explicit Dependencies**: All dependencies are explicitly passed and visible


## Trade-Off Considered

### Functional vs. Class-Based Approach
I decided against a strictly functional design in favor of a class-based one after taking into account:

**Class-Based Approach Benefits**
   - Improved state encapsulation for services such as `DocumentStore`; simpler isolation testing and mocking; and more scalability for upcoming feature additions
   - Complies with standard Python production procedures

**Accepted Trade-Off**
   - There is a little bit more boilerplate code than pure functions.
   - New developers must comprehend OOP ideas.

The demand for production-suitable code, where testability and maintainability take precedence above minimalism, was the basis for the decision.



## How Maintainability Is Improved by This Version

### 1. Improved Testability
Unit testing is made simple by the redesigned structure:
- It is possible to test each service separately using fictitious dependencies.
- It is possible to test API endpoints without executing the complete application. For instance, it is possible to test `EmbeddingService` without Qdrant or FastAPI.

### 2. Improved New Developer Onboarding:
- A well-organized directory structure makes it clear where various components are located.
- The goal of well-named classes and methods is evident.
- Developers can work on one layer without comprehending others when concerns are kept apart.

### 3. Simpler Evolution and Maintenance 
- **Adding new storage backends**: Extend `DocumentStore` or develop a new implementation 
- **Changing RAG workflow**: Modify `RAGService` without affecting the API layer
- **Scaling the application** If necessary, each layer can be resized separately.

### 4. Production Readiness: Appropriate error handling at every layer; dependency injection for configuration management; and clear separation for monitoring and logging at the right levels
Environment-specific setting is centralized (e.g., Qdrant vs. in-memory).

## Maintained Conduct
It retains all of its original functionality:
The same request/response formats; the same fallback behavior (Qdrant → in-memory); the same RAG process logic; and the same API endpoints (/`add`, `/ask`, `/status`).

The refactoring preserved 100% backward compatibility with the previous API contract while concentrating solely on internal structure.
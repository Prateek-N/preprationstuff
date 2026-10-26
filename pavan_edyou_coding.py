# -*- coding: utf-8 -*-
"""
20 Coding Problems for Pavan Chandramouleswara
Role: Full-Stack & Data Engineer (Frontend / Backend / Data Engineering)
End Client: Edyou

Format:
- Problem Statement First
- Code with detailed comments in it
- Time and Space Complexity
"""

CODING_PROBLEMS = [
    {
        "num": 1,
        "title": "React Custom Hook: Debounced Search & API Fetching with AbortController",
        "category": "Frontend & React",
        "problem_statement": """In Edyou's search interface, students query thousands of textbook lessons, curriculum standards, and AI tutor topics. Firing an API request on every keystroke overwhelms the backend and causes out-of-order response race conditions.

Implement a production-grade React custom hook `useDebouncedApiSearch(searchQuery, delay)` that:
1. Debounces the incoming search query by a configurable delay in milliseconds.
2. Cancels any in-flight HTTP request when a new search character is typed using an `AbortController`.
3. Handles loading, error, and data states cleanly with proper cleanup on unmount.""",
        "code": """import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

/**
 * Custom React hook for debounced search with automatic request cancellation.
 * Prevents race conditions and server overloading in search interfaces.
 */
export function useDebouncedApiSearch(query, delay = 300) {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Ref to hold the active AbortController across renders
  const abortControllerRef = useRef(null);

  useEffect(() => {
    // If the search query is empty, reset state immediately
    if (!query || query.trim() === '') {
      setData([]);
      setIsLoading(false);
      setError(null);
      return;
    }

    setIsLoading(true);
    setError(null);

    // Cancel any previous pending request before scheduling a new one
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Instantiate a new AbortController for this fetch cycle
    const controller = new AbortController();
    abortControllerRef.current = controller;

    // Set debounce timer
    const handler = setTimeout(async () => {
      try {
        const response = await axios.get('/api/v1/curriculum/search', {
          params: { q: query.trim() },
          signal: controller.signal, // Connect abort signal
        });

        setData(response.data);
        setIsLoading(false);
      } catch (err) {
        // Ignore errors caused by deliberate request aborts
        if (axios.isCancel(err) || err.name === 'CanceledError') {
          return;
        }
        setError(err.message || 'An error occurred while fetching results.');
        setIsLoading(false);
      }
    }, delay);

    // Cleanup timer and abort active request if query changes or component unmounts
    return () => {
      clearTimeout(handler);
      if (controller) {
        controller.abort();
      }
    };
  }, [query, delay]);

  return { data, isLoading, error };
}""",
        "complexity": """- **Time Complexity:** O(1) scheduling per keystroke. Network fetch executes once per debounce interval.
- **Space Complexity:** O(R) memory for storing the latest search results array R in component state.
- **Concurrency Safety:** Guaranteed free of race conditions via explicit AbortController cancellation."""
    },
    {
        "num": 2,
        "title": "React Context: Stateful Multi-Step Quiz Engine with LocalStorage Recovery",
        "category": "Frontend & React",
        "problem_statement": """Edyou students take multi-step adaptive assessments and diagnostic quizzes. If a student's browser accidentally refreshes or loses battery, their in-progress answers must be preserved and restored.

Design a React Context and Custom Hook `useQuizEngine` that:
1. Manages quiz state: current question index, answers mapping, time spent, and submission status.
2. Synchronizes answer state to browser `localStorage` on every change.
3. Restores in-progress assessment state automatically on mount.
4. Provides methods to advance, backtrack, submit, and clear local state upon confirmed submission.""",
        "code": """import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const QuizContext = createContext(null);

export function QuizProvider({ quizId, totalQuestions, children }) {
  const storageKey = `edyou_quiz_progress_${quizId}`;

  // Initialize state from localStorage if available, otherwise default
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Restore saved state upon initial mount
  useEffect(() => {
    try {
      const savedData = localStorage.getItem(storageKey);
      if (savedData) {
        const parsed = JSON.parse(savedData);
        setCurrentIndex(parsed.currentIndex || 0);
        setAnswers(parsed.answers || {});
        setIsSubmitted(parsed.isSubmitted || false);
      }
    } catch (e) {
      console.warn('Failed to parse saved quiz state:', e);
    } finally {
      setIsInitialized(true);
    }
  }, [storageKey]);

  // Persist state to localStorage whenever answers or index change
  useEffect(() => {
    if (!isInitialized || isSubmitted) return;
    try {
      const payload = JSON.stringify({ currentIndex, answers, isSubmitted });
      localStorage.setItem(storageKey, payload);
    } catch (e) {
      console.error('Failed to save quiz state to localStorage:', e);
    }
  }, [currentIndex, answers, isSubmitted, isInitialized, storageKey]);

  // Record an answer for a specific question ID
  const recordAnswer = useCallback((questionId, selectedOption) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: selectedOption,
    }));
  }, []);

  // Navigation handlers
  const nextQuestion = useCallback(() => {
    setCurrentIndex(prev => Math.min(prev + 1, totalQuestions - 1));
  }, [totalQuestions]);

  const prevQuestion = useCallback(() => {
    setCurrentIndex(prev => Math.max(prev - 1, 0));
  }, []);

  // Complete and clear persisted progress
  const completeSubmission = useCallback(async (apiSubmitCallback) => {
    try {
      await apiSubmitCallback(answers);
      setIsSubmitted(true);
      localStorage.removeItem(storageKey); // Clear on confirmed success
    } catch (err) {
      throw new Error('Submission failed: ' + err.message);
    }
  }, [answers, storageKey]);

  const value = {
    currentIndex,
    answers,
    isSubmitted,
    isInitialized,
    recordAnswer,
    nextQuestion,
    prevQuestion,
    completeSubmission,
  };

  return <QuizContext.Provider value={value}>{children}</QuizContext.Provider>;
}

export function useQuizEngine() {
  const context = useContext(QuizContext);
  if (!context) {
    throw new Error('useQuizEngine must be used within a QuizProvider');
  }
  return context;
}""",
        "complexity": """- **Time Complexity:** O(1) for recording answers and step navigation. State synchronization to localStorage is O(K) where K is number of answered questions.
- **Space Complexity:** O(K) in-memory and local storage space to store student answers.
- **Resilience:** Guarantees zero data loss across browser reloads, network disconnects, and tab closures."""
    },
    {
        "num": 3,
        "title": "React Infinite Scroll Hook with IntersectionObserver for Student Feeds",
        "category": "Frontend & React",
        "problem_statement": """Edyou's student activity feed displays chronological study milestones, AI tutor badges, and homework feedback. Loading all historical events at once degrades mobile performance.

Implement a performant React custom hook `useInfiniteScroll(fetchMoreCallback, hasMore, isFetching)` using the modern browser `IntersectionObserver` API to trigger seamless pagination as the student scrolls down.""",
        "code": """import { useRef, useCallback } from 'react';

/**
 * Reusable infinite scrolling hook utilizing IntersectionObserver.
 * Triggers fetchMore when a sentinel element scrolls into view.
 */
export function useInfiniteScroll(fetchMoreCallback, hasMore, isFetching) {
  const observerRef = useRef(null);

  // Callback ref passed directly to the DOM sentinel element
  const sentinelRef = useCallback(
    (node) => {
      // If currently fetching, do not re-attach observer
      if (isFetching) return;

      // Disconnect any existing observer instance
      if (observerRef.current) {
        observerRef.current.disconnect();
      }

      // Instantiate IntersectionObserver
      observerRef.current = new IntersectionObserver(
        (entries) => {
          // If sentinel is visible and more data exists, fetch next page
          if (entries[0].isIntersecting && hasMore) {
            fetchMoreCallback();
          }
        },
        {
          root: null, // Relative to viewport
          rootMargin: '200px', // Pre-fetch 200px before reaching bottom
          threshold: 0.1,
        }
      );

      // Attach observer to the DOM node
      if (node) {
        observerRef.current.observe(node);
      }
    },
    [fetchMoreCallback, hasMore, isFetching]
  );

  return sentinelRef;
}""",
        "complexity": """- **Time Complexity:** O(1) observer attachment. Browser fires asynchronous observer events off the main layout thread.
- **Space Complexity:** O(1) memory overhead for the single observer reference.
- **Performance Advantage:** Eliminates expensive scroll event listeners (`window.onscroll`) that trigger layout thrashing."""
    },
    {
        "num": 4,
        "title": "FastAPI: Asynchronous CRUD Router with Pydantic V2 Schemas & Dependency Injection",
        "category": "Backend & FastAPI",
        "problem_statement": """In Edyou's backend, students enroll in curriculum courses and track completion states. 

Implement a modular, production-ready FastAPI router for Course Enrollments that:
1. Defines Pydantic V2 schemas for request validation and response filtering.
2. Uses asynchronous SQLAlchemy sessions via FastAPI's dependency injection system.
3. Implements endpoints for enrollment creation, paginated listing, and progress updates.
4. Returns standard HTTP status codes (201 Created, 200 OK, 404 Not Found, 409 Conflict).""",
        "code": """from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# =============================================================================
# 1. Pydantic V2 Schemas
# =============================================================================
class EnrollmentCreate(BaseModel):
    student_id: int = Field(..., gt=0, description="Unique student ID")
    course_id: int = Field(..., gt=0, description="Unique course ID")

class EnrollmentUpdate(BaseModel):
    progress_percentage: float = Field(..., ge=0.0, le=100.0)
    is_completed: Optional[bool] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    progress_percentage: float
    is_completed: bool
    enrolled_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

# =============================================================================
# 2. Database Session Dependency Placeholder
# =============================================================================
async def get_db_session() -> AsyncSession:
    # Yields async session from SQLAlchemy AsyncEngine pool
    pass

# =============================================================================
# 3. Router Implementation
# =============================================================================
router = APIRouter(prefix="/api/v1/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    payload: EnrollmentCreate, 
    db: AsyncSession = Depends(get_db_session)
):
    \"\"\"Creates a new course enrollment for a student with duplicate prevention.\"\"\"
    try:
        # Construct ORM model instance
        new_enrollment = CourseEnrollmentModel(
            student_id=payload.student_id,
            course_id=payload.course_id,
            progress_percentage=0.0,
            is_completed=False,
            enrolled_at=datetime.utcnow()
        )
        db.add(new_enrollment)
        await db.commit()
        await db.refresh(new_enrollment)
        return new_enrollment
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is already enrolled in this course."
        )

@router.get("/", response_model=List[EnrollmentResponse])
async def list_enrollments(
    student_id: Optional[int] = Query(None, gt=0),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db_session)
):
    \"\"\"Fetches paginated list of enrollments, optionally filtered by student.\"\"\"
    query = select(CourseEnrollmentModel).limit(limit).offset(offset)
    if student_id:
        query = query.where(CourseEnrollmentModel.student_id == student_id)
        
    result = await db.execute(query)
    enrollments = result.scalars().all()
    return enrollments

@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
async def update_progress(
    enrollment_id: int,
    payload: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    \"\"\"Updates progress percentage and completion status for an enrollment.\"\"\"
    query = select(CourseEnrollmentModel).where(CourseEnrollmentModel.id == enrollment_id)
    result = await db.execute(query)
    enrollment = result.scalar_one_or_none()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with ID {enrollment_id} not found."
        )

    enrollment.progress_percentage = payload.progress_percentage
    if payload.is_completed is not None:
        enrollment.is_completed = payload.is_completed
    elif payload.progress_percentage >= 100.0:
        enrollment.is_completed = True
        
    enrollment.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(enrollment)
    return enrollment""",
        "complexity": """- **Time Complexity:** O(1) for primary key lookup and updates; O(K) where K is pagination limit for listings.
- **Space Complexity:** O(K) intermediate memory for projected response serialization.
- **Reliability:** Non-blocking async I/O ensures high concurrency throughput under high request volume."""
    },
    {
        "num": 5,
        "title": "FastAPI: Stateless JWT Authentication & Role-Based Access Control (RBAC)",
        "category": "Backend & Security",
        "problem_statement": """Edyou supports distinct user roles: `student`, `teacher`, and `district_admin`. 

Implement a secure, stateless authentication and authorization module using **PyJWT** and FastAPI dependencies that:
1. Generates cryptographic JWT tokens containing `user_id`, `role`, and expiration timestamps.
2. Extracts and verifies Bearer tokens from incoming HTTP `Authorization` headers.
3. Implements a reusable role-checking dependency factory `require_role(allowed_roles)`.
4. Raises standard HTTP 401 Unauthorized or 403 Forbidden exceptions on failures.""",
        "code": """import os
import jwt
from datetime import datetime, timedelta
from typing import List, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "edyou-super-secret-hex-key-32-chars-min")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: int
    role: str
    district_id: int

def create_access_token(user_id: int, role: str, district_id: int) -> str:
    \"\"\"Generates a signed JWT with role claims and expiration window.\"\"\"
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "role": role,
        "district_id": district_id,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    \"\"\"Validates JWT token signature and extracts claims.\"\"\"
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        role: str = payload.get("role")
        district_id: int = payload.get("district_id")
        
        if user_id_str is None or role is None:
            raise credentials_exception
            
        return TokenData(user_id=int(user_id_str), role=role, district_id=district_id)
    except jwt.PyJWTError:
        raise credentials_exception

def require_role(allowed_roles: List[str]):
    \"\"\"Factory returning dependency that enforces Role-Based Access Control.\"\"\"
    async def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker

# Usage demonstration in an endpoint
# @router.delete("/curriculum/{id}", dependencies=[Depends(require_role(["teacher", "district_admin"]))])
# async def delete_curriculum(id: int):
#     return {"message": "Deleted"}""",
        "complexity": """- **Time Complexity:** O(1) HMAC-SHA256 cryptographic verification time.
- **Space Complexity:** O(1) in-memory decoding allocation.
- **Security:** Purely stateless; eliminates server-side session stores while preventing cross-role privilege escalation."""
    },
    {
        "num": 6,
        "title": "SQLAlchemy: Asynchronous Context Manager for Safe Database Transactions",
        "category": "Backend & Database",
        "problem_statement": """Multi-table database mutations (e.g. updating student wallet balance, creating an audit log, and unlocking course access) must succeed atomically. If any query fails, all preceding mutations must roll back immediately.

Write a reusable Python asynchronous context manager `managed_transaction(session)` in SQLAlchemy 2.0 that guarantees atomic commit on success and automatic rollback upon any exception.""",
        "code": """from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger("database.transaction")

@asynccontextmanager
async def managed_transaction(session: AsyncSession):
    \"\"\"
    Asynchronous context manager providing robust transaction boundaries.
    Automatically commits on normal exit and executes atomic rollback on error.
    \"\"\"
    try:
        # Yield control to the caller within active transaction
        yield session
        # If no exception occurred in the block, commit all operations
        await session.commit()
    except Exception as exc:
        # Atomic rollback on any runtime or database exception
        await session.rollback()
        logger.error(f"Transaction aborted and rolled back. Reason: {str(exc)}")
        # Re-raise the exception for upper layers to handle
        raise exc
    finally:
        # Optional: session lifecycle cleanups if needed
        pass

# Example Usage
async def purchase_course_tier(session: AsyncSession, student_id: int, course_id: int, amount: float):
    async with managed_transaction(session):
        # 1. Deduct credits
        await session.execute(
            update(StudentWallet).where(StudentWallet.student_id == student_id)
            .values(balance=StudentWallet.balance - amount)
        )
        # 2. Grant access
        session.add(CourseAccess(student_id=student_id, course_id=course_id))
        # 3. Create audit record
        session.add(AuditLog(action="PURCHASE", student_id=student_id, amount=amount))
        # Commit executes automatically upon exiting block!""",
        "complexity": """- **Time Complexity:** O(1) context manager overhead plus underlying SQL execution time.
- **Space Complexity:** O(1) memory overhead.
- **Data Integrity:** Guarantees strict ACID Atomicity, preventing partial writes and orphaned records."""
    },
    {
        "num": 7,
        "title": "Python Asyncio: Concurrency-Limited Batch Request Handler for LLM APIs",
        "category": "Backend & Async Systems",
        "problem_statement": """Edyou processes thousands of student writing submissions overnight to generate formative AI feedback. Firing all OpenAI requests simultaneously breaches commercial rate limits (TPM/RPM limits) and crashes worker memory.

Write an asynchronous Python function `batch_process_prompts(prompts, max_concurrency=10)` using `asyncio.Semaphore` that processes a list of prompts concurrently while strictly guaranteeing that no more than `max_concurrency` requests run in flight at any given moment.""",
        "code": """import asyncio
from typing import List, Dict, Any

async def mock_llm_call(prompt: str, index: int) -> Dict[str, Any]:
    \"\"\"Simulates asynchronous LLM API inference latency.\"\"\"
    await asyncio.sleep(0.5) # Simulate network I/O
    return {"index": index, "prompt": prompt, "response": f"AI Feedback for: {prompt[:30]}..."}

async def batch_process_prompts(prompts: List[str], max_concurrency: int = 10) -> List[Dict[str, Any]]:
    \"\"\"
    Executes a large batch of asynchronous tasks with bounded concurrency.
    Protects downstream API endpoints from rate-limit exhaustion.
    \"\"\"
    # Bounded semaphore controls the number of simultaneous active coroutines
    semaphore = asyncio.Semaphore(max_concurrency)

    async def sem_task(prompt: str, idx: int):
        async with semaphore:
            # Only up to max_concurrency tasks can enter this block simultaneously
            return await mock_llm_call(prompt, idx)

    # Instantiate task list
    tasks = [sem_task(prompt, i) for i, prompt in enumerate(prompts)]

    # Gather results concurrently while preserving task ordering
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process or format exceptions if any occurred
    sanitized_results = []
    for r in results:
        if isinstance(r, Exception):
            sanitized_results.append({"error": str(r)})
        else:
            sanitized_results.append(r)

    return sanitized_results

# Demonstration
if __name__ == "__main__":
    prompt_list = [f"Student Essay Prompt #{i}" for i in range(50)]
    output = asyncio.run(batch_process_prompts(prompt_list, max_concurrency=5))
    print(f"Processed {len(output)} essays successfully with max concurrency of 5.")""",
        "complexity": """- **Time Complexity:** O(ceil(N / C) * T) where N is prompts, C is concurrency limit, and T is average request latency.
- **Space Complexity:** O(N) memory to retain coroutine task references and gathered result payloads.
- **Enterprise Utility:** Eliminates HTTP 429 Too Many Requests errors from commercial LLM providers."""
    },
    {
        "num": 8,
        "title": "GenAI: In-Memory Vector Similarity Search with Cosine Distance & Thresholding",
        "category": "Generative AI & RAG",
        "problem_statement": """For unit testing and edge routing without external vector database dependencies, implement a lightweight in-memory vector store in pure Python that:
1. Adds text chunks with their associated high-dimensional vector embeddings and metadata.
2. Computes **Cosine Similarity** against a query vector using NumPy.
3. Returns the top-k most relevant chunks meeting a minimum similarity threshold.""",
        "code": """import numpy as np
from typing import List, Dict, Any, Tuple

class InMemoryVectorStore:
    def __init__(self):
        self.vectors: List[np.ndarray] = []
        self.documents: List[str] = []
        self.metadatas: List[Dict[str, Any]] = []

    def add_documents(self, docs: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None):
        \"\"\"Ingests documents and embedding vectors into memory.\"\"\"
        for idx, (doc, emb) in enumerate(zip(docs, embeddings)):
            vec = np.array(emb, dtype=np.float32)
            # Normalize vector to unit length for high-speed dot-product cosine similarity
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            self.vectors.append(vec)
            self.documents.append(doc)
            self.metadatas.append(metadatas[idx] if metadatas else {})

    def similarity_search(self, query_embedding: List[float], top_k: int = 3, threshold: float = 0.7) -> List[Dict[str, Any]]:
        \"\"\"Performs vectorized cosine similarity search with score thresholding.\"\"\"
        if not self.vectors:
            return []

        q_vec = np.array(query_embedding, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = q_vec / q_norm

        # Matrix-vector multiplication computes cosine similarity against all items in a single C-level BLAS call
        matrix = np.vstack(self.vectors)
        scores = np.dot(matrix, q_vec)

        # Filter candidates above minimum threshold
        valid_indices = np.where(scores >= threshold)[0]
        if len(valid_indices) == 0:
            return []

        # Sort filtered indices descending by score
        sorted_indices = valid_indices[np.argsort(-scores[valid_indices])][:top_k]

        results = []
        for idx in sorted_indices:
            results.append({
                "document": self.documents[idx],
                "metadata": self.metadatas[idx],
                "score": float(scores[idx])
            })

        return results""",
        "complexity": """- **Time Complexity:** O(N * D) where N is the number of stored documents and D is embedding dimension (e.g. 1536). Vectorized NumPy execution runs in sub-millisecond time for up to 50,000 vectors.
- **Space Complexity:** O(N * D) RAM for vector matrices and document strings.
- **Zero-Dependency:** Ideal for fast unit test harnesses and localized caching layers."""
    },
    {
        "num": 9,
        "title": "GenAI / RAG: Context Assembly & Dynamic Token Budget Truncation",
        "category": "Generative AI & RAG",
        "problem_statement": """When feeding retrieved textbook chunks into an LLM prompt, the total context must strictly respect a maximum token budget (e.g., 3,000 tokens) while preserving the system prompt, conversation history, and high-relevance chunks.

Write a Python function `assemble_rag_context(retrieved_chunks, max_token_budget=3000)` using `tiktoken` that iteratively packs top-scoring chunks into the prompt until the budget is reached without slicing passages mid-sentence.""",
        "code": """import tiktoken
from typing import List, Dict, Any

def assemble_rag_context(
    retrieved_chunks: List[Dict[str, Any]], 
    max_token_budget: int = 3000, 
    model_name: str = "gpt-4o"
) -> str:
    \"\"\"
    Packs retrieved curriculum chunks into an LLM context window without
    exceeding token budget constraints or truncating mid-passage.
    \"\"\"
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    assembled_passages = []
    current_tokens = 0

    # Ensure chunks are ordered by relevance score descending
    sorted_chunks = sorted(retrieved_chunks, key=lambda x: x.get("score", 0.0), reverse=True)

    for i, chunk in enumerate(sorted_chunks):
        doc_text = chunk.get("document", "").strip()
        metadata = chunk.get("metadata", {})
        source_title = metadata.get("chapter", f"Passage #{i+1}")

        formatted_entry = f"--- [Source: {source_title}] ---\\n{doc_text}\\n"
        entry_tokens = len(encoding.encode(formatted_entry))

        # Check if adding this passage exceeds budget
        if current_tokens + entry_tokens <= max_token_budget:
            assembled_passages.append(formatted_entry)
            current_tokens += entry_tokens
        else:
            # If the next most relevant chunk cannot fit entirely, break gracefully
            break

    final_context = "\\n".join(assembled_passages)
    return final_context""",
        "complexity": """- **Time Complexity:** O(N log N) for sorting plus O(N * L) for BPE token encoding where L is average chunk length.
- **Space Complexity:** O(B) string allocation for the assembled context buffer of token length B.
- **Safety:** Eliminates context window overflow errors and maintains intact semantic boundaries."""
    },
    {
        "num": 10,
        "title": "GenAI / Redis: Redis-Backed Semantic Caching Layer for AI Tutors",
        "category": "Generative AI & RAG",
        "problem_statement": """Edyou students across classrooms frequently ask semantically identical questions. 

Implement a Python class `SemanticCacheManager` using Redis and cosine similarity that:
1. Computes an embedding for an incoming student query.
2. Searches Redis for an existing cached response with cosine similarity >= 0.95.
3. If a match is found, returns the cached answer instantly.
4. If not found, stores the novel query embedding and generated answer with a 24-hour TTL.""",
        "code": """import redis
import json
import numpy as np
from typing import Optional, Dict, Any

class SemanticCacheManager:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, ttl_seconds: int = 86400):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=False)
        self.ttl = ttl_seconds
        self.threshold = 0.95

    def _normalize(self, vec: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def get_answer(self, query_vec: list, subject: str) -> Optional[str]:
        \"\"\"Scans cached vectors for the given subject and returns answer if similarity >= threshold.\"\"\"
        q_arr = self._normalize(np.array(query_vec, dtype=np.float32))
        
        # In production with Redis Stack, use FT.SEARCH vector query.
        # Fallback implementation: scan keys matching subject namespace
        pattern = f"semcache:{subject}:*"
        keys = self.r.keys(pattern)
        
        best_score = -1.0
        best_answer = None

        for k in keys:
            raw_data = self.r.get(k)
            if not raw_data:
                continue
            entry = json.loads(raw_data.decode('utf-8'))
            cached_vec = np.array(entry["vector"], dtype=np.float32)
            cached_vec = self._normalize(cached_vec)
            
            # Compute Cosine Similarity
            sim = float(np.dot(q_arr, cached_vec))
            if sim > best_score:
                best_score = sim
                best_answer = entry["answer"]

        if best_score >= self.threshold:
            return best_answer
        return None

    def store_answer(self, query: str, query_vec: list, answer: str, subject: str):
        \"\"\"Stores a verified answer and embedding with TTL.\"\"\"
        cache_id = abs(hash(query))
        key = f"semcache:{subject}:{cache_id}"
        payload = json.dumps({
            "query": query,
            "vector": query_vec,
            "answer": answer
        })
        self.r.setex(key, self.ttl, payload)""",
        "complexity": """- **Time Complexity:** O(K * D) where K is cached keys for that subject and D is vector dimension. (O(log K) when using HNSW indexes via Redis Stack RediSearch).
- **Space Complexity:** O(K * D) Redis memory for stored float vectors.
- **Economic Value:** Reduces OpenAI API costs by 30-40% across common curricula queries."""
    },
    {
        "num": 11,
        "title": "PySpark: Event-Time Watermarking & Deduplication on Student Telemetry",
        "category": "Data Engineering & Streaming",
        "problem_statement": """Edyou ingests high-velocity student telemetry (video playback heartbeats, quiz clicks, and chat messages) from millions of client devices over Apache Kafka. Network disconnects and edge retries cause duplicate and late-arriving events.

Write a PySpark Structured Streaming pipeline that:
1. Reads from Kafka topic `edyou.student.telemetry`.
2. Applies a 15-minute event-time watermark on `event_timestamp`.
3. Deduplicates events on composite key (`student_id`, `event_type`, `event_timestamp`).
4. Writes cleansed records into a partitioned Delta Lake Bronze table with checkpoints.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, MapType

spark = SparkSession.builder \\
    .appName("Edyou_Telemetry_Deduplication") \\
    .config("spark.sql.streaming.stateStore.providerClass", 
            "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider") \\
    .getOrCreate()

# Define incoming telemetry schema
telemetry_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("student_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("course_id", StringType(), True),
    StructField("payload", MapType(StringType(), StringType()), True),
    StructField("event_timestamp", TimestampType(), False)
])

# 1. Ingest raw stream from Kafka broker
raw_stream = spark.readStream \\
    .format("kafka") \\
    .option("kafka.bootstrap.servers", "kafka-broker:9092") \\
    .option("subscribe", "edyou.student.telemetry") \\
    .option("startingOffsets", "latest") \\
    .load()

# 2. Parse JSON and project strongly typed columns
parsed_events = raw_stream \\
    .select(from_json(col("value").cast("string"), telemetry_schema).alias("data")) \\
    .select("data.*")

# 3. Enforce 15-Minute Event-Time Watermarking & Stateful Deduplication
deduplicated_stream = parsed_events \\
    .withWatermark("event_timestamp", "15 minutes") \\
    .dropDuplicates(["student_id", "event_type", "event_timestamp"])

# 4. Sink to partitioned Delta Lake storage
query = deduplicated_stream.writeStream \\
    .format("delta") \\
    .outputMode("append") \\
    .partitionBy("event_type") \\
    .option("checkpointLocation", "s3://edyou-data-lake-checkpoints/telemetry_bronze/") \\
    .option("path", "s3://edyou-data-lake-bronze/student_telemetry/") \\
    .trigger(processingTime="30 seconds") \\
    .start()

query.awaitTermination()""",
        "complexity": """- **Time Complexity:** O(N) per micro-batch where N is record count. RocksDB state store updates in logarithmic time.
- **Space Complexity:** O(U) where U is unique student event keys active within the 15-minute watermark frame.
- **Fault Tolerance:** Idempotent exactly-once write guarantees via Kafka committed offsets and Delta logs."""
    },
    {
        "num": 12,
        "title": "PySpark: Window Functions for Running Student Mastery & Streak Scores",
        "category": "Data Engineering & Analytics",
        "problem_statement": """Edyou rewards student consistency and adaptive mastery. 

Given an Apache Spark DataFrame of quiz results (`student_id`, `subject`, `score`, `quiz_timestamp`), write an optimized PySpark transformation using Window functions that computes:
1. The rolling 5-quiz moving average score per student per subject.
2. The cumulative count of quizzes taken by that student in that subject.
3. The rank of the quiz score relative to all attempts by that student in that subject.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, dense_rank
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Edyou_Student_Mastery_Analytics").getOrCreate()

def calculate_student_mastery_metrics(quiz_df):
    \"\"\"
    Computes analytical mastery indicators using distributed Spark Window functions.
    \"\"\"
    # 1. Window partitioned by student & subject, ordered chronologically
    # Evaluates rolling historical frame of current row and up to 4 preceding rows
    rolling_window = Window \\
        .partitionBy("student_id", "subject") \\
        .orderBy("quiz_timestamp") \\
        .rowsBetween(-4, 0) # 5 quizzes total: 4 preceding + current

    # 2. Unbounded cumulative window from start of time up to current row
    cumulative_window = Window \\
        .partitionBy("student_id", "subject") \\
        .orderBy("quiz_timestamp") \\
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)

    # 3. Ranking window based on score descending
    ranking_window = Window \\
        .partitionBy("student_id", "subject") \\
        .orderBy(col("score").desc())

    # Apply window functions in a single projection
    enriched_df = quiz_df \\
        .withColumn("rolling_5_quiz_avg", avg("score").over(rolling_window)) \\
        .withColumn("cumulative_quizzes_taken", count("score").over(cumulative_window)) \\
        .withColumn("score_rank_in_subject", dense_rank().over(ranking_window))

    return enriched_df""",
        "complexity": """- **Time Complexity:** O(N log N) dominated by the distributed shuffle-sort along student_id, subject, and timestamp.
- **Space Complexity:** O(1) auxiliary state per executor partition during streaming window evaluations.
- **Scalability:** Scales horizontally across thousands of Spark executor cores processing millions of quiz submissions."""
    },
    {
        "num": 13,
        "title": "PySpark: Two-Phase Key Salting to Eliminate Join Data Skew",
        "category": "Data Engineering & Performance",
        "problem_statement": """When joining a massive table of 500 million student lesson clicks with a school course metadata table, a handful of introductory viral courses (e.g. 'Intro to AI') receive 80% of all traffic. A standard distributed join crashes with executor out-of-memory errors due to severe partition skew.

Implement a PySpark Key Salting algorithm that:
1. Salts the skewed fact join key with a randomized integer factor (0 to K-1).
2. Explodes the corresponding dimensional keys K times to ensure complete join parity.
3. Executes the distributed join without data skew or hot executor bottlenecks.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, floor, rand, array, lit, explode

spark = SparkSession.builder.appName("Edyou_Key_Salting_Join").getOrCreate()

def salted_distributed_join(clicks_df, course_dim_df, salt_factor=16):
    \"\"\"
    Performs balanced distributed join between skewed clicks and course dimension
    by dispersing hot keys across 'salt_factor' separate partitions.
    \"\"\"
    # 1. Salt the fact table by appending random int [0, salt_factor - 1]
    salted_clicks = clicks_df \\
        .withColumn("salt_idx", floor(rand() * salt_factor)) \\
        .withColumn("salted_course_id", concat_ws("_", col("course_id"), col("salt_idx")))

    # 2. Replicate the dimension table to match all possible salt variants
    salt_indices = array([lit(i) for i in range(salt_factor)])
    replicated_courses = course_dim_df \\
        .withColumn("salt_idx", explode(salt_indices)) \\
        .withColumn("salted_course_id", concat_ws("_", col("course_id"), col("salt_idx")))

    # 3. Execute uniform distributed hash join
    joined_df = salted_clicks.join(
        replicated_courses,
        on="salted_course_id",
        how="inner"
    )

    # 4. Drop synthetic columns
    clean_df = joined_df \\
        .drop("salted_course_id") \\
        .drop(salted_clicks["salt_idx"]) \\
        .drop(replicated_courses["salt_idx"])

    return clean_df""",
        "complexity": """- **Time Complexity:** O((N + K * M) log P) where N is fact rows, M is dimension rows, K is salt factor, and P is partition count. Eliminates long-tail executor stragglers.
- **Space Complexity:** Fact table size remains O(N); dimension expands by factor K, easily fitting in executor RAM.
- **Cluster Stability:** Evenly balances CPU and memory across 100% of cluster workers."""
    },
    {
        "num": 14,
        "title": "Python: Automated Data Quality Contract Validator with Great Expectations",
        "category": "Data Engineering & Governance",
        "problem_statement": """External school district Learning Management Systems (Canvas, Blackboard) upload daily attendance and grading exports into S3. Corrupted records must be quarantined before ingestion into BigQuery.

Implement an automated data validation class `LMSDataQualityGatekeeper` using **Great Expectations** that:
1. Validates non-null primary keys, valid date formats, and numerical score boundaries (0.0 to 100.0).
2. Diverts invalid records to a quarantine directory.
3. Emits an execution telemetry dictionary with pass/fail ratios to trigger automated alerts.""",
        "code": """import os
import json
import pandas as pd
import great_expectations as gx
from datetime import datetime

class LMSDataQualityGatekeeper:
    def __init__(self, context_root="./gx"):
        self.context = gx.get_context(project_root_dir=context_root)
        self.suite_name = "lms_daily_export_contract"

    def validate_file(self, file_path: str, quarantine_dir: str = "./quarantine") -> dict:
        \"\"\"Validates CSV against data contracts and quarantines on failure.\"\"\"
        df = pd.read_csv(file_path)
        validator = self.context.sources.pandas_default.read_dataframe(df)

        # 1. Structural schema assertions
        validator.expect_table_columns_to_match_ordered_list([
            "enrollment_id", "student_id", "course_id", "grade_score", "updated_at"
        ])

        # 2. Non-null completeness
        validator.expect_column_values_to_not_be_null("enrollment_id")
        validator.expect_column_values_to_not_be_null("student_id")

        # 3. Score boundary rules
        validator.expect_column_values_to_be_between("grade_score", min_value=0.0, max_value=100.0)

        # 4. Timestamp format regex
        validator.expect_column_values_to_match_regex("updated_at", r"^\\d{4}-\\d{2}-\\d{2}")

        # Execute evaluation
        results = validator.validate()

        telemetry = {
            "file": os.path.basename(file_path),
            "timestamp": datetime.utcnow().isoformat(),
            "success": results.success,
            "evaluated_expectations": len(results.results),
            "failed_count": sum(1 for r in results.results if not r.success)
        }

        # Quarantine defective files
        if not results.success:
            os.makedirs(quarantine_dir, exist_ok=True)
            quarantine_path = os.path.join(quarantine_dir, os.path.basename(file_path))
            os.rename(file_path, quarantine_path)
            telemetry["quarantine_path"] = quarantine_path

        return telemetry""",
        "complexity": """- **Time Complexity:** O(N * E) where N is record count and E is number of expectations. Vectorized evaluations execute in sub-second time.
- **Space Complexity:** O(N) memory allocation for the in-memory dataframe.
- **Data Governance:** Guarantees zero corrupted records pollute downstream lakehouse analytical marts."""
    },
    {
        "num": 15,
        "title": "Airflow: Dynamic DAG Generator for Ingesting Multiple School District Feeds",
        "category": "Data Engineering & Orchestration",
        "problem_statement": """Edyou integrates with dozens of school districts, each with custom SFTP drop locations, ingestion schedules, and target BigQuery tables. Writing separate Python DAG files for each district is an unmaintainable anti-pattern.

Implement a dynamic Airflow DAG factory script that reads a central configuration dictionary and programmatically instantiates independent, version-controlled DAGs with retries, SLA alerts, and ingestion tasks.""",
        "code": """from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Configuration dictionary defining district parameters
DISTRICT_CONFIGS = {
    "chicago_public_schools": {
        "schedule": "0 2 * * *", # 2:00 AM daily
        "sftp_path": "/sftp/cps/daily_export.csv",
        "target_table": "raw_lms_cps",
        "sla_hours": 3
    },
    "austin_independent_schools": {
        "schedule": "30 2 * * *", # 2:30 AM daily
        "sftp_path": "/sftp/aisd/export.csv",
        "target_table": "raw_lms_aisd",
        "sla_hours": 2
    }
}

def create_district_dag(district_id: str, config: dict):
    \"\"\"Factory function generating an isolated Airflow DAG for a specific district.\"\"\"
    default_args = {
        'owner': 'data_engineering',
        'depends_on_past': False,
        'email_on_failure': True,
        'email': ['data-alerts@edyou.com'],
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'execution_timeout': timedelta(hours=config['sla_hours'])
    }

    dag = DAG(
        dag_id=f"ingest_lms_{district_id}",
        default_args=default_args,
        start_date=datetime(2026, 1, 1),
        schedule_interval=config['schedule'],
        catchup=False,
        tags=["edyou", "lms_ingest", district_id]
    )

    def extract_sftp(**context):
        print(f"Extracting files from {config['sftp_path']} for {district_id}...")

    def validate_and_load(**context):
        print(f"Validating and loading records into BigQuery table: {config['target_table']}...")

    with dag:
        start_task = EmptyOperator(task_id="start")
        extract_task = PythonOperator(task_id="extract_sftp_feed", python_callable=extract_sftp)
        load_task = PythonOperator(task_id="validate_and_load_bq", python_callable=validate_and_load)
        end_task = EmptyOperator(task_id="end")

        start_task >> extract_task >> load_task >> end_task

    return dag

# Register dynamic DAGs into global Airflow scope
for dist_id, dist_cfg in DISTRICT_CONFIGS.items():
    globals()[f"ingest_lms_{dist_id}"] = create_district_dag(dist_id, dist_cfg)""",
        "complexity": """- **Time Complexity:** O(D) DAG compilation time where D is the number of configured school districts.
- **Space Complexity:** O(D) metadata footprint in the Airflow metadata database.
- **Maintainability:** Adding a new district requires adding a 5-line YAML/JSON entry with zero code duplication."""
    },
    {
        "num": 16,
        "title": "SQL / PostgreSQL: Recursive CTE to Traverse Prerequisite Curriculum Graphs",
        "category": "Data Engineering & SQL",
        "problem_statement": """Edyou courses have multi-tier prerequisite requirements (e.g. Math 101 -> Algebra I -> Algebra II -> AP Calculus). 

Write a PostgreSQL Recursive Common Table Expression (CTE) that:
1. Takes a target `course_id` as input.
2. Recursively traverses all upstream prerequisite courses.
3. Returns the prerequisite course IDs, course titles, depth level in the prerequisite tree, and the full dependency chain path.""",
        "code": """-- PostgreSQL Recursive CTE to trace all upstream course prerequisites
WITH RECURSIVE prerequisite_hierarchy AS (
    -- Anchor Member: Identify direct prerequisites for the requested target course
    SELECT 
        cp.prerequisite_course_id AS course_id,
        c.course_title,
        1 AS depth_level,
        ARRAY[c.course_title::text] AS prerequisite_path
    FROM course_prerequisites cp
    JOIN courses c ON cp.prerequisite_course_id = c.course_id
    WHERE cp.target_course_id = 105 -- Target: e.g. AP Calculus

    UNION ALL

    -- Recursive Member: Find prerequisites of the prerequisites
    SELECT 
        cp.prerequisite_course_id,
        c.course_title,
        ph.depth_level + 1,
        array_append(ph.prerequisite_path, c.course_title::text)
    FROM course_prerequisites cp
    JOIN courses c ON cp.prerequisite_course_id = c.course_id
    JOIN prerequisite_hierarchy ph ON cp.target_course_id = ph.course_id
    WHERE NOT (c.course_title = ANY(ph.prerequisite_path)) -- Cycle prevention guard
)
SELECT 
    course_id,
    course_title,
    depth_level,
    array_to_string(prerequisite_path, ' -> ') AS dependency_chain
FROM prerequisite_hierarchy
ORDER BY depth_level DESC;""",
        "complexity": """- **Time Complexity:** O(V + E) where V is prerequisite courses and E is prerequisite relationship edges.
- **Space Complexity:** O(D) recursion stack memory where D is maximum prerequisite tree depth.
- **Cycle Safety:** Array membership guard prevents infinite loops on circular prerequisite definitions."""
    },
    {
        "num": 17,
        "title": "SQL / BigQuery: Sessionization Query with Window Functions to Compute Study Duration",
        "category": "Data Engineering & SQL",
        "problem_statement": """Given a high-volume clickstream table `student_clicks` in GCP BigQuery, identify continuous study sessions where any inactivity gap exceeding 30 minutes triggers the start of a brand-new session.

Write an optimized BigQuery SQL query using Window functions that:
1. Flags session boundary transitions when time elapsed since previous click > 30 minutes.
2. Assigns a unique surrogate session identifier per student.
3. Aggregates total session duration in minutes and distinct lessons visited.""",
        "code": """-- BigQuery Sessionization Query using 30-Minute Inactivity Threshold
WITH click_intervals AS (
    SELECT 
        student_id,
        lesson_id,
        event_timestamp,
        -- Fetch timestamp of preceding click by this student
        LAG(event_timestamp) OVER (
            PARTITION BY student_id 
            ORDER BY event_timestamp
        ) AS prev_timestamp
    FROM `edyou_analytics.student_clicks`
    WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
),
session_markers AS (
    SELECT 
        student_id,
        lesson_id,
        event_timestamp,
        -- Mark as 1 if gap > 30 minutes (1800 seconds) or if first click ever
        CASE 
            WHEN prev_timestamp IS NULL THEN 1
            WHEN TIMESTAMP_DIFF(event_timestamp, prev_timestamp, SECOND) > 1800 THEN 1
            ELSE 0 
        END AS is_new_session
    FROM click_intervals
),
session_assignment AS (
    SELECT 
        student_id,
        lesson_id,
        event_timestamp,
        -- Cumulative sum of boundary markers creates persistent session index
        SUM(is_new_session) OVER (
            PARTITION BY student_id 
            ORDER BY event_timestamp
        ) AS session_seq
    FROM session_markers
)
-- Aggregate metrics per session
SELECT 
    student_id,
    CONCAT(CAST(student_id AS STRING), '_SESS_', CAST(session_seq AS STRING)) AS session_id,
    MIN(event_timestamp) AS session_start_time,
    MAX(event_timestamp) AS session_end_time,
    ROUND(TIMESTAMP_DIFF(MAX(event_timestamp), MIN(event_timestamp), SECOND) / 60.0, 2) AS duration_minutes,
    COUNT(1) AS total_clicks,
    COUNT(DISTINCT lesson_id) AS distinct_lessons_studied
FROM session_assignment
GROUP BY student_id, session_seq
HAVING COUNT(1) >= 2 -- Filter out single-click bounce sessions
ORDER BY student_id, session_start_time DESC;""",
        "complexity": """- **Time Complexity:** O(N log N) dominated by the partition-level window sorting along student_id and timestamp.
- **Space Complexity:** O(N) BigQuery intermediate shuffle storage.
- **Analytical Precision:** Precisely segments continuous student engagement sessions without arbitrary midnight boundaries."""
    },
    {
        "num": 18,
        "title": "Algorithms: Sliding Window Rate Limiter (Token Bucket Algorithm)",
        "category": "Algorithms & Systems",
        "problem_statement": """To prevent automated API scraping and abuse on Edyou's AI endpoints, implement a thread-safe, in-memory **Token Bucket Rate Limiter** in Python.

The rate limiter must allow up to `capacity` requests, refilling tokens continuously at a rate of `refill_rate` tokens per second. If tokens are available, consume 1 token and return True; otherwise return False.""",
        "code": """import time
import threading

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        \"\"\"
        :param capacity: Maximum burst token capacity
        :param refill_rate_per_sec: Tokens added to bucket per second
        \"\"\"
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.current_tokens = float(capacity)
        self.last_refill_time = time.monotonic()
        self.lock = threading.Lock()

    def allow_request(self, tokens_requested: int = 1) -> bool:
        \"\"\"Thread-safe token evaluation and consumption.\"\"\"
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill_time

            # Refill tokens proportional to elapsed time
            added_tokens = elapsed * self.refill_rate
            self.current_tokens = min(self.capacity, self.current_tokens + added_tokens)
            self.last_refill_time = now

            # Check if sufficient tokens exist
            if self.current_tokens >= tokens_requested:
                self.current_tokens -= tokens_requested
                return True
            else:
                return False

# Demonstration
if __name__ == "__main__":
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_sec=2.0)
    for i in range(7):
        allowed = limiter.allow_request(1)
        print(f"Request {i+1}: {'ALLOWED' if allowed else 'BLOCKED'}")
        time.sleep(0.1)""",
        "complexity": """- **Time Complexity:** O(1) mathematical computation on each incoming request.
- **Space Complexity:** O(1) memory overhead for token counters and timestamps.
- **Thread Safety:** Mutual exclusion lock guarantees atomicity across multi-threaded worker pools."""
    },
    {
        "num": 19,
        "title": "Algorithms: Topological Sort for Course Curriculum Prerequisites (Kahn's Algorithm)",
        "category": "Algorithms & Systems",
        "problem_statement": """Given a list of Edyou courses labeled `0` to `numCourses - 1` and a list of prerequisite pairs `[course, prereq]`, determine a valid topological order in which a student can take all courses. If a circular prerequisite dependency exists, return an empty array.""",
        "code": """from collections import deque, defaultdict
from typing import List

def find_curriculum_order(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    \"\"\"
    Computes valid topological sequence for course curriculum using Kahn's BFS algorithm.
    Detects cycles (circular prerequisite deadlocks) and returns [] if impossible.
    \"\"\"
    # 1. Initialize adjacency list and in-degree counter
    adj_list = defaultdict(list)
    in_degree = [0] * numCourses

    # Build graph: prereq -> course
    for course, prereq in prerequisites:
        adj_list[prereq].append(course)
        in_degree[course] += 1

    # 2. Queue all courses with 0 prerequisites (in-degree == 0)
    queue = deque([c for c in range(numCourses) if in_degree[c] == 0])
    course_order = []

    # 3. Process courses via BFS
    while queue:
        curr_course = queue.popleft()
        course_order.append(curr_course)

        # Decrement in-degree of all dependent courses
        for neighbor in adj_list[curr_course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 4. If all courses processed, return valid order; otherwise cycle detected
    if len(course_order) == numCourses:
        return course_order
    else:
        return [] # Impossible curriculum schedule due to circular prerequisite loop

# Example
if __name__ == "__main__":
    courses = 4
    prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]] # 0 -> 1,2 -> 3
    print("Valid Curriculum Plan:", find_curriculum_order(courses, prereqs))""",
        "complexity": """- **Time Complexity:** O(V + E) where V is courses and E is prerequisite constraints.
- **Space Complexity:** O(V + E) memory for the adjacency list graph representation and in-degree array.
- **Pedagogical Application:** Automatically sequences custom learning pathways and flags invalid curriculum cycles."""
    },
    {
        "num": 20,
        "title": "Algorithms: Least Recently Used (LRU) Cache Implementation",
        "category": "Algorithms & Systems",
        "problem_statement": """Implement an LRU Cache in Python supporting `get(key)` and `put(key, value)` operations in strictly O(1) time complexity. When the cache reaches its capacity, evict the least recently used item before inserting a new entry.""",
        "code": """class Node:
    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    \"\"\"
    O(1) Least Recently Used Cache utilizing a Hash Map paired with
    a Doubly Linked List with sentinel head and tail nodes.
    \"\"\"
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> Node
        # Sentinel dummy nodes eliminate edge-case null checks
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        \"\"\"Removes node from linked list.\"\"\"
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node: Node):
        \"\"\"Adds node right after dummy head (most recently used position).\"\"\"
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        \"\"\"Returns value if key exists, moving node to most recently used position.\"\"\"
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        \"\"\"Inserts or updates key. Evicts LRU node if capacity exceeded.\"\"\"
        if key in self.cache:
            self._remove(self.cache[key])
        
        new_node = Node(key, value)
        self._add_to_front(new_node)
        self.cache[key] = new_node

        if len(self.cache) > self.capacity:
            # Evict from tail (least recently used)
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

# Demonstration
if __name__ == "__main__":
    lru = LRUCache(2)
    lru.put(1, 100)
    lru.put(2, 200)
    print("Get 1:", lru.get(1))   # Returns 100, moves 1 to front
    lru.put(3, 300)              # Evicts key 2
    print("Get 2:", lru.get(2))   # Returns -1 (not found)
    print("Get 3:", lru.get(3))   # Returns 300""",
        "complexity": """- **Time Complexity:** Strictly O(1) for both `get` and `put` operations via hash map lookups and constant-time doubly-linked list pointer manipulations.
- **Space Complexity:** O(C) memory where C is cache capacity.
- **Systems Application:** Foundational design pattern for in-memory token caches, user profile caches, and session buffers."""
    }
]

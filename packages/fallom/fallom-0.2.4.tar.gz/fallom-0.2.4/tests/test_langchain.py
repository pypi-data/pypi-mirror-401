"""
Tests for the LangChain callback handler.

Quick manual test:
    cd sdk/python-sdk
    pip install langchain langchain-openai
    FALLOM_API_KEY=your-key OPENAI_API_KEY=your-key python tests/test_langchain.py

Unit tests:
    pytest tests/test_langchain.py -v
"""
import os
import pytest


class TestLangChainCallbackHandler:
    """Unit tests for FallomCallbackHandler (no API calls needed)."""

    def test_import_without_langchain(self):
        """Should be able to import the module even without langchain installed."""
        # This tests that lazy imports work correctly
        from fallom.trace.wrappers.langchain import FallomCallbackHandler
        assert FallomCallbackHandler is not None

    def test_handler_raises_without_langchain(self):
        """Should raise ImportError with helpful message if langchain not installed."""
        # Skip if langchain IS installed
        try:
            import langchain_core
            pytest.skip("langchain is installed, skipping this test")
        except ImportError:
            pass

        from fallom.trace.wrappers.langchain import FallomCallbackHandler
        
        with pytest.raises(ImportError, match="pip install"):
            FallomCallbackHandler(
                config_key="test",
                session_id="test-session",
            )

    @pytest.mark.skipif(
        not os.environ.get("FALLOM_API_KEY"),
        reason="FALLOM_API_KEY not set"
    )
    def test_handler_creation_with_langchain(self):
        """Should create handler successfully when langchain is installed."""
        try:
            import langchain_core
        except ImportError:
            pytest.skip("langchain not installed")

        import fallom
        from fallom.trace.wrappers.langchain import FallomCallbackHandler

        fallom.init()

        handler = FallomCallbackHandler(
            config_key="test-langchain",
            session_id="test-session-123",
            customer_id="test-user",
            metadata={"env": "test"},
            tags=["test", "langchain"],
        )

        assert handler is not None
        # Verify it has the expected callback methods
        assert hasattr(handler, "on_llm_start")
        assert hasattr(handler, "on_llm_end")
        assert hasattr(handler, "on_chat_model_start")
        assert hasattr(handler, "on_chain_start")
        assert hasattr(handler, "on_tool_start")

    @pytest.mark.skipif(
        not os.environ.get("FALLOM_API_KEY"),
        reason="FALLOM_API_KEY not set"
    )
    def test_session_langchain_callback(self):
        """Should create handler from session."""
        try:
            import langchain_core
        except ImportError:
            pytest.skip("langchain not installed")

        import fallom

        fallom.init()

        session = fallom.session(
            config_key="test-langchain",
            session_id="test-session-456",
        )

        handler = session.langchain_callback()
        assert handler is not None
        assert hasattr(handler, "on_llm_start")


# =============================================================================
# Manual Integration Test (run directly)
# =============================================================================

def manual_test():
    """
    Run this manually to test with real LLM calls.
    
    Requires:
        - FALLOM_API_KEY set
        - OPENAI_API_KEY set (or use a different provider)
        - langchain and langchain-openai installed
    """
    import fallom
    
    # Initialize with debug mode to see traces being sent
    fallom.init(debug=True)
    
    print("\n" + "="*60)
    print("Testing FallomCallbackHandler with LangChain")
    print("="*60 + "\n")

    # Create handler
    from fallom.trace.wrappers.langchain import FallomCallbackHandler
    
    handler = FallomCallbackHandler(
        config_key="langchain-test",
        session_id="manual-test-session",
        metadata={"test": True},
        tags=["manual-test"],
    )
    
    print("✅ Handler created successfully\n")

    # Test 1: Simple LLM call
    print("-" * 40)
    print("Test 1: Simple ChatOpenAI call")
    print("-" * 40)
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini", callbacks=[handler])
        response = llm.invoke("Say 'Hello from LangChain!' in exactly 5 words.")
        
        print(f"Response: {response.content}")
        print("✅ LLM call traced\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 2: Chain
    print("-" * 40)
    print("Test 2: Simple Chain")
    print("-" * 40)
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        llm = ChatOpenAI(model="gpt-4o-mini", callbacks=[handler])
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{input}")
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke(
            {"input": "What is 2+2? Reply with just the number."},
            config={"callbacks": [handler]}
        )
        
        print(f"Response: {response}")
        print("✅ Chain traced\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 3: Test with Gemini (if available)
    print("-" * 40)
    print("Test 3: Google Gemini (optional)")
    print("-" * 40)
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", callbacks=[handler])
        response = llm.invoke("Say 'Hello from Gemini!' in exactly 5 words.")
        
        print(f"Response: {response.content}")
        print("✅ Gemini call traced\n")
    except ImportError:
        print("⏭️  Skipped (langchain-google-genai not installed)\n")
    except Exception as e:
        print(f"⏭️  Skipped: {e}\n")

    print("="*60)
    print("Test complete! Check your Fallom dashboard for traces.")
    print("Dashboard: https://app.fallom.com")
    print("="*60)


if __name__ == "__main__":
    # Check for required env vars
    if not os.environ.get("FALLOM_API_KEY"):
        print("❌ Error: FALLOM_API_KEY environment variable not set")
        print("   Set it with: export FALLOM_API_KEY=your-api-key")
        exit(1)
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set, OpenAI tests will fail")
    
    # Check for langchain
    try:
        import langchain_core
        print(f"✅ langchain-core installed: {langchain_core.__version__}")
    except ImportError:
        print("❌ Error: langchain not installed")
        print("   Install with: pip install langchain langchain-openai")
        exit(1)
    
    try:
        import langchain_openai
        print(f"✅ langchain-openai installed")
    except ImportError:
        print("❌ Error: langchain-openai not installed")
        print("   Install with: pip install langchain-openai")
        exit(1)
    
    print()
    manual_test()

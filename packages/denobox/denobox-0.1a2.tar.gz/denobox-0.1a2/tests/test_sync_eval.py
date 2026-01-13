"""Tests for synchronous JavaScript evaluation."""

import pytest
from denobox import Denobox


class TestDenoboxSync:
    """Test synchronous Denobox functionality."""

    def test_simple_eval(self):
        """Test evaluating a simple expression."""
        with Denobox() as box:
            result = box.eval("1 + 1")
            assert result == 2

    def test_string_result(self):
        """Test evaluating code that returns a string."""
        with Denobox() as box:
            result = box.eval("'hello' + ' ' + 'world'")
            assert result == "hello world"

    def test_array_result(self):
        """Test evaluating code that returns an array."""
        with Denobox() as box:
            result = box.eval("[1, 2, 3].map(x => x * 2)")
            assert result == [2, 4, 6]

    def test_object_result(self):
        """Test evaluating code that returns an object."""
        with Denobox() as box:
            result = box.eval("({name: 'test', value: 42})")
            assert result == {"name": "test", "value": 42}

    def test_null_result(self):
        """Test evaluating code that returns null."""
        with Denobox() as box:
            result = box.eval("null")
            assert result is None

    def test_undefined_result(self):
        """Test evaluating code that returns undefined."""
        with Denobox() as box:
            result = box.eval("undefined")
            assert result is None

    def test_boolean_result(self):
        """Test evaluating code that returns boolean."""
        with Denobox() as box:
            assert box.eval("true") is True
            assert box.eval("false") is False

    def test_multiple_evals(self):
        """Test multiple evaluations in same session."""
        with Denobox() as box:
            box.eval("var x = 10")
            box.eval("var y = 20")
            result = box.eval("x + y")
            assert result == 30

    def test_error_handling(self):
        """Test that JavaScript errors are properly raised."""
        with Denobox() as box:
            with pytest.raises(Exception) as exc_info:
                box.eval("throw new Error('test error')")
            assert "test error" in str(exc_info.value)

    def test_syntax_error(self):
        """Test that syntax errors are properly raised."""
        with Denobox() as box:
            with pytest.raises(Exception):
                box.eval("this is not valid javascript {{{")

    def test_context_manager_cleanup(self):
        """Test that context manager properly cleans up."""
        box = Denobox()
        box.start()
        assert box.eval("1 + 1") == 2
        box.stop()
        # Should not be able to eval after stop
        with pytest.raises(Exception):
            box.eval("1 + 1")

    def test_promise_resolution(self):
        """Test that promises are automatically resolved."""
        with Denobox() as box:
            result = box.eval("Promise.resolve(42)")
            assert result == 42

    def test_async_function_result(self):
        """Test evaluating async functions."""
        with Denobox() as box:
            result = box.eval("(async () => { return 'async result'; })()")
            assert result == "async result"

    def test_function_auto_invoke(self):
        """Test that functions are automatically invoked."""
        with Denobox() as box:
            result = box.eval("() => 42")
            assert result == 42

    def test_async_function_auto_invoke(self):
        """Test that async functions are automatically invoked."""
        with Denobox() as box:
            result = box.eval("async () => { return 4 + 5; }")
            assert result == 9

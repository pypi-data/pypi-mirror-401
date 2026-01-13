"""
Tests for qixo - QuickJS sandbox
"""

import pytest
from qixo import Qixo, QixoError


class TestBasicEvaluation:
    """Test basic JavaScript evaluation"""
    
    def test_simple_arithmetic(self):
        with Qixo() as box:
            assert box.eval("1 + 1") == 2
            assert box.eval("10 - 5") == 5
            assert box.eval("3 * 4") == 12
            assert box.eval("15 / 3") == 5
    
    def test_string_operations(self):
        with Qixo() as box:
            assert box.eval("'hello' + ' ' + 'world'") == "hello world"
            assert box.eval("'test'.toUpperCase()") == "TEST"
            assert box.eval("'HELLO'.toLowerCase()") == "hello"
    
    def test_boolean_operations(self):
        with Qixo() as box:
            assert box.eval("true") is True
            assert box.eval("false") is False
            assert box.eval("true && true") is True
            assert box.eval("true && false") is False
            assert box.eval("true || false") is True
            assert box.eval("!true") is False
    
    def test_null_and_undefined(self):
        with Qixo() as box:
            assert box.eval("null") is None
            assert box.eval("undefined") is None


class TestDataTypes:
    """Test JavaScript to Python type conversion"""
    
    def test_arrays(self):
        with Qixo() as box:
            assert box.eval("[1, 2, 3]") == [1, 2, 3]
            assert box.eval("[]") == []
            assert box.eval("[1, 'two', true, null]") == [1, "two", True, None]
    
    def test_objects(self):
        with Qixo() as box:
            result = box.eval("({name: 'test', value: 42})")
            assert result == {"name": "test", "value": 42}
            
            result = box.eval("{}")
            assert result == {}
    
    def test_nested_structures(self):
        with Qixo() as box:
            result = box.eval("({users: [{name: 'alice', age: 30}, {name: 'bob', age: 25}]})")
            expected = {
                "users": [
                    {"name": "alice", "age": 30},
                    {"name": "bob", "age": 25}
                ]
            }
            assert result == expected
    
    def test_array_methods(self):
        with Qixo() as box:
            assert box.eval("[1, 2, 3].map(x => x * 2)") == [2, 4, 6]
            assert box.eval("[1, 2, 3, 4, 5].filter(x => x > 2)") == [3, 4, 5]
            assert box.eval("[1, 2, 3].reduce((a, b) => a + b, 0)") == 6


class TestStatePersistence:
    """Test that state persists between eval calls"""
    
    def test_variable_persistence(self):
        with Qixo() as box:
            box.eval("var x = 10")
            box.eval("var y = 20")
            assert box.eval("x + y") == 30
    
    def test_function_persistence(self):
        with Qixo() as box:
            box.eval("function add(a, b) { return a + b; }")
            assert box.eval("add(5, 3)") == 8
            assert box.eval("add(10, 20)") == 30
    
    def test_object_mutation(self):
        with Qixo() as box:
            box.eval("var obj = {count: 0}")
            box.eval("obj.count++")
            box.eval("obj.count++")
            assert box.eval("obj.count") == 2


class TestFunctions:
    """Test function definitions and calls"""
    
    def test_simple_function(self):
        with Qixo() as box:
            box.eval("""
                function fibonacci(n) {
                    if (n <= 1) return n;
                    return fibonacci(n - 1) + fibonacci(n - 2);
                }
            """)
            assert box.eval("fibonacci(0)") == 0
            assert box.eval("fibonacci(1)") == 1
            assert box.eval("fibonacci(5)") == 5
            assert box.eval("fibonacci(10)") == 55
    
    def test_arrow_functions(self):
        with Qixo() as box:
            box.eval("const square = x => x * x")
            assert box.eval("square(5)") == 25
            
            box.eval("const sum = (a, b) => a + b")
            assert box.eval("sum(3, 4)") == 7
    
    def test_closures(self):
        with Qixo() as box:
            box.eval("""
                function createCounter() {
                    let count = 0;
                    return function() {
                        return ++count;
                    };
                }
                var counter = createCounter();
            """)
            assert box.eval("counter()") == 1
            assert box.eval("counter()") == 2
            assert box.eval("counter()") == 3


class TestErrorHandling:
    """Test error handling and exceptions"""
    
    def test_syntax_error(self):
        with Qixo() as box:
            with pytest.raises(QixoError):
                box.eval("invalid javascript {{{")
    
    def test_runtime_error(self):
        with Qixo() as box:
            with pytest.raises(QixoError) as exc_info:
                box.eval("throw new Error('Something went wrong')")
            assert "Something went wrong" in str(exc_info.value)
    
    def test_reference_error(self):
        with Qixo() as box:
            with pytest.raises(QixoError):
                box.eval("nonexistentVariable")
    
    def test_type_error(self):
        with Qixo() as box:
            with pytest.raises(QixoError):
                box.eval("null.property")


class TestMemoryLimits:
    """Test memory limitation features"""
    
    def test_small_allocation_succeeds(self):
        with Qixo(memory_limit_mb=5) as box:
            # Small string should work fine
            result = box.eval("'a'.repeat(1000)")
            assert len(result) == 1000
    
    def test_large_allocation_fails(self):
        with Qixo(memory_limit_mb=1) as box:
            # Try to allocate a very large string
            with pytest.raises(QixoError):
                box.eval("'a'.repeat(10000000)")  # 10MB string


class TestTimeoutLimits:
    """Test execution timeout features"""
    
    def test_fast_execution_succeeds(self):
        with Qixo(timeout_ms=1000) as box:
            result = box.eval("1 + 1")
            assert result == 2
    
    def test_slow_execution_fails(self):
        with Qixo(timeout_ms=100) as box:
            with pytest.raises(QixoError):
                # Infinite loop
                box.eval("while(true) {}")


class TestContextManager:
    """Test context manager functionality"""
    
    def test_context_manager_usage(self):
        with Qixo() as box:
            result = box.eval("1 + 1")
            assert result == 2
    
    def test_error_without_context_manager(self):
        box = Qixo()
        with pytest.raises(QixoError) as exc_info:
            box.eval("1 + 1")
        assert "not initialized" in str(exc_info.value)
    
    def test_multiple_contexts(self):
        # Each context should be independent
        with Qixo() as box1:
            box1.eval("var x = 10")
            
        with Qixo() as box2:
            # x should not exist in new context
            with pytest.raises(QixoError):
                box2.eval("x")


class TestComplexScenarios:
    """Test more complex real-world scenarios"""
    
    def test_json_parsing(self):
        with Qixo() as box:
            json_str = '{"name": "test", "values": [1, 2, 3]}'
            result = box.eval(f"JSON.parse('{json_str}')")
            assert result == {"name": "test", "values": [1, 2, 3]}
    
    def test_json_stringification(self):
        with Qixo() as box:
            result = box.eval("JSON.stringify({name: 'test', value: 42})")
            assert result == '{"name":"test","value":42}'
    
    def test_array_manipulation(self):
        with Qixo() as box:
            box.eval("""
                var data = [
                    {name: 'Alice', score: 85},
                    {name: 'Bob', score: 92},
                    {name: 'Charlie', score: 78}
                ];
            """)
            
            # Get top scorer
            result = box.eval("""
                data.reduce((max, item) => 
                    item.score > max.score ? item : max
                )
            """)
            assert result == {"name": "Bob", "score": 92}
            
            # Calculate average
            avg = box.eval("""
                data.reduce((sum, item) => sum + item.score, 0) / data.length
            """)
            assert avg == (85 + 92 + 78) / 3
    
    def test_string_template_literals(self):
        with Qixo() as box:
            box.eval("var name = 'World'")
            result = box.eval("`Hello, ${name}!`")
            assert result == "Hello, World!"


class TestES6Features:
    """Test ES6+ JavaScript features"""
    
    def test_destructuring(self):
        with Qixo() as box:
            box.eval("const [a, b, c] = [1, 2, 3]")
            assert box.eval("a") == 1
            assert box.eval("b") == 2
            assert box.eval("c") == 3
    
    def test_spread_operator(self):
        with Qixo() as box:
            result = box.eval("[1, ...[2, 3], 4]")
            assert result == [1, 2, 3, 4]
    
    def test_object_shorthand(self):
        with Qixo() as box:
            box.eval("const x = 1, y = 2")
            result = box.eval("({x, y})")
            assert result == {"x": 1, "y": 2}
    
    def test_default_parameters(self):
        with Qixo() as box:
            box.eval("function greet(name = 'Guest') { return 'Hello, ' + name; }")
            assert box.eval("greet()") == "Hello, Guest"
            assert box.eval("greet('Alice')") == "Hello, Alice"

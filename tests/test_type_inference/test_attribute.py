import nose
from nose import SkipTest
import astroid
from typing import *
from typing import _ForwardRef
from python_ta.typecheck.base import TypeFail
import tests.custom_hypothesis_support as cs


def test_instance_dot_method():
    program = \
        '''
        class A:
            def foo(self, x):
                return x + 1
                
        A().foo(0)
        '''
    module, _ = cs._parse_text(program, reset=True)
    for attribute_node in module.nodes_of_class(astroid.Attribute):
        assert attribute_node.inf_type.getValue() == Callable[[_ForwardRef('A'), int], int]


def test_instance_dot_classmethod():
    program = \
        '''
        class A:
            @classmethod
            def foo(cls, x):
                return x + 1

        A().foo(0)
        '''
    module, _ = cs._parse_text(program, reset=True)
    for attribute_node in module.nodes_of_class(astroid.Attribute):
        assert attribute_node.inf_type.getValue() == Callable[[Type[_ForwardRef('A')], int], int]


def test_instance_dot_staticmethod():
    program = \
        '''
        class A:
            @staticmethod
            def foo(x):
                return x + 1

        A().foo(0)
        '''
    module, _ = cs._parse_text(program, reset=True)
    for attribute_node in module.nodes_of_class(astroid.Attribute):
        assert attribute_node.inf_type.getValue() == Callable[[int], int]


def test_class_dot_method():
    program = \
        '''
        class A:
            def foo(self, x):
                return x + 1

        A.foo(A(), 0)
        '''
    module, _ = cs._parse_text(program, reset=True)
    for attribute_node in module.nodes_of_class(astroid.Attribute):
        assert attribute_node.inf_type.getValue() == Callable[[_ForwardRef('A'), int], int]


def test_class_dot_classmethod():
    program = \
        '''
        class A:
            @classmethod
            def foo(cls, x):
                return x + 1

        A.foo(0)
        '''
    module, _ = cs._parse_text(program, reset=True)
    for attribute_node in module.nodes_of_class(astroid.Attribute):
        assert attribute_node.inf_type.getValue() == Callable[[Type[_ForwardRef('A')], int], int]


def test_class_dot_staticmethod():
    program = \
        '''
        class A:
            @staticmethod
            def foo(x):
                return x + 1

        A.foo(0)
        '''
    module, _ = cs._parse_text(program, reset=True)
    for attribute_node in module.nodes_of_class(astroid.Attribute):
        assert attribute_node.inf_type.getValue() == Callable[[int], int]


def test_attribute_self_bind():
    """Make sure auto-binding of self persists"""
    raise SkipTest('This special case is not supported yet')
    program = \
        '''
        x = []
        f = x.append
        f(4)
        '''
    module, ti = cs._parse_text(program, reset=True)
    from sample_usage.print_ast_from_mod import print_ast
    print_ast(module)
    x = [ti.lookup_typevar(node, node.name) for node
         in module.nodes_of_class(astroid.AssignName)][0]
    assert ti.type_constraints.resolve(x).getValue() == List[int]
#!/usr/bin/env python3
"""Demo of L* active learning for protocol inference.

This example demonstrates how to use the L* algorithm to learn a DFA
from captured protocol traces using the SimulatorTeacher oracle.

Run with: python examples/lstar_demo.py
"""

from tracekit.inference.active_learning import LStarLearner, SimulatorTeacher


def main() -> None:
    """Demonstrate L* learning from protocol traces."""
    print("=" * 70)
    print("L* Active Learning Demo")
    print("=" * 70)
    print()

    # Example 1: Simple protocol with two message types
    print("Example 1: Simple Request-Response Protocol")
    print("-" * 70)

    traces = [
        ["CONNECT", "ACK"],
        ["CONNECT", "ACK", "DATA", "ACK"],
        ["CONNECT", "ACK", "DATA", "ACK", "DATA", "ACK"],
        ["CONNECT", "ACK", "DISCONNECT"],
    ]

    print("Training traces:")
    for i, trace in enumerate(traces, 1):
        print(f"  {i}. {' -> '.join(trace)}")
    print()

    # Create oracle from traces
    teacher = SimulatorTeacher(traces)

    # Learn DFA using L*
    learner = LStarLearner(teacher, verbose=True)
    dfa = learner.learn(max_iterations=100)

    print()
    print(f"Learned DFA with {len(dfa.states)} states")
    print(f"Alphabet: {sorted(dfa.alphabet)}")
    print("Query statistics:")
    print(f"  - Membership queries: {learner.membership_queries}")
    print(f"  - Equivalence queries: {learner.equivalence_queries}")
    print()

    # Test learned DFA
    print("Testing learned DFA:")
    test_sequences = [
        [],
        ["CONNECT"],
        ["CONNECT", "ACK"],
        ["CONNECT", "ACK", "DATA"],
        ["DATA"],  # Should not accept (must start with CONNECT)
    ]

    for seq in test_sequences:
        accepted = dfa.accepts(seq)
        seq_str = " -> ".join(seq) if seq else "(empty)"
        print(f"  {seq_str}: {'✓ accepted' if accepted else '✗ rejected'}")
    print()

    # Export to DOT format
    print("DOT format (for Graphviz):")
    print("-" * 70)
    print(dfa.to_dot())
    print()

    # Example 2: Learning binary protocol with states
    print()
    print("Example 2: Binary Protocol (even/odd parity)")
    print("-" * 70)

    # Traces showing protocol that accepts strings with even number of 1's
    binary_traces = [
        ["0", "0"],  # Even (0 ones)
        ["1", "1"],  # Even (2 ones)
        ["0", "1", "1", "0"],  # Even (2 ones)
        ["1", "0", "1"],  # Even (2 ones)
    ]

    print("Training traces (binary sequences with even parity):")
    for i, trace in enumerate(binary_traces, 1):
        ones = sum(1 for bit in trace if bit == "1")
        print(f"  {i}. {''.join(trace)} (parity: {'even' if ones % 2 == 0 else 'odd'})")
    print()

    # Learn with L*
    binary_teacher = SimulatorTeacher(binary_traces)
    binary_learner = LStarLearner(binary_teacher, verbose=False)
    binary_dfa = binary_learner.learn(max_iterations=100)

    print(f"Learned DFA with {len(binary_dfa.states)} states")
    print(f"Membership queries: {binary_learner.membership_queries}")
    print(f"Equivalence queries: {binary_learner.equivalence_queries}")
    print()

    # Test learned DFA
    print("Testing learned DFA:")
    binary_tests = [
        [],
        ["0"],
        ["1"],
        ["0", "0"],
        ["0", "1"],
        ["1", "0"],
        ["1", "1"],
        ["1", "1", "1", "1"],
    ]

    for seq in binary_tests:
        accepted = binary_dfa.accepts(seq)
        seq_str = "".join(seq) if seq else "(empty)"
        ones = sum(1 for bit in seq if bit == "1")
        print(f"  {seq_str:8s} ({ones} ones): {'✓ accepted' if accepted else '✗ rejected'}")
    print()

    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

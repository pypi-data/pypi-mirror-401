# Testing Progress Tracker

This document tracks the testing coverage progress for pydantic_collab.

## Coverage Status Overview

| Module | Status | Test File | Notes |
|--------|--------|-----------|-------|
| `_utils.py` | 🔴 Not Tested | `test_utils.py` | Utility functions need unit tests |
| `_types.py` | 🟡 Partial | `test_types.py` | Settings & get_right_handoff_model need tests |
| `_viz.py` | 🔴 Not Tested | `test_viz.py` | Visualization (lower priority) |
| `collab.py` | 🟡 Partial | various | Decorators, error handling need more tests |
| `custom_collabs.py` | 🟡 Partial | `test_custom_collabs.py` | HierarchyCollab untested |

## Detailed Progress

### 1. `_utils.py` Functions

| Function | Tested | Notes |
|----------|--------|-------|
| `message_history_to_text()` | ❌ | Convert message history to text |
| `get_tool_calls()` | ❌ | Extract tool calls for specific agent |
| `get_context()` | ❌ | Build context string from handoff data |
| `default_build_agent_prompt()` | ❌ | Build agent instructions |
| `ensure_tuple()` | ❌ | Convert values to tuples |

### 2. `_types.py` Classes/Functions

| Item | Tested | Notes |
|------|--------|-------|
| `CollabAgent.__init__` variations | ❌ | Single item vs sequence |
| `CollabState.record_execution()` | ❌ | Record agent execution |
| `CollabRunResult.print_execution_flow()` | ❌ | Print formatted flow |
| `get_right_handoff_model()` | ❌ | Dynamic model generation |
| `CollabSettings` combinations | ❌ | force/allow/disallow options |

### 3. `custom_collabs.py` Classes

| Class | Tested | Notes |
|-------|--------|-------|
| `PipelineCollab` | ✅ | Tested in multiple files |
| `StarCollab` | ✅ | Basic tests exist |
| `MeshCollab` | ✅ | Basic tests exist |
| `HierarchyCollab` | ❌ | Not tested at all |

### 4. `collab.py` Features

| Feature | Tested | Notes |
|---------|--------|-------|
| Basic run/run_sync | ✅ | Well tested |
| Topology validation | ✅ | Comprehensive tests |
| `@tool` decorator | ❌ | Needs direct tests |
| `@tool_plain` decorator | ❌ | Needs direct tests |
| `@toolset` decorator | ❌ | Needs direct tests |
| Error handling in run | ❌ | Exception scenarios |
| Dependencies (`deps`) | ❌ | Complex dep mappings |
| Context manager | ❌ | `__aenter__`/`__aexit__` |

### 5. `_viz.py` Visualization

| Function | Tested | Notes |
|----------|--------|-------|
| `render_topology()` | ❌ | Requires viz dependencies |
| `_compute_layout()` | ❌ | Internal |
| `_compute_node_sizing()` | ❌ | Internal |

## Test Files Created

- [ ] `tests/test_utils.py` - Unit tests for `_utils.py`
- [ ] `tests/test_types.py` - Unit tests for `_types.py`
- [ ] `tests/test_custom_collabs.py` - Tests for custom Collab classes
- [ ] `tests/test_decorators.py` - Tests for tool/toolset decorators

## Session Progress

### Session 1 (Current)
- [x] Analyzed existing test coverage
- [x] Created TESTING.md
- [ ] `test_utils.py` - IN PROGRESS
- [ ] `test_types.py`
- [ ] `test_custom_collabs.py`

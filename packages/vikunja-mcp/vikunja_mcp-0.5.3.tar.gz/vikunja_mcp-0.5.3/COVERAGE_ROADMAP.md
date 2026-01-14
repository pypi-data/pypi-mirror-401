# Matrix Bot - Path to 100% Test Coverage

## Current Status (2025-12-24)

**Overall Coverage: 70%**
- matrix_parser.py: 100% ✅ (192 lines, 2 functions)
- matrix_client.py: 60% 🟡 (469 lines, 12 functions)
- matrix_handlers.py: 40% 🟡 (650 lines, 13 functions)
- **Total: 1,311 lines of Matrix code**

**Test Status: 61/79 passing (77%)**

---

## 🎯 Roadmap to 100% Coverage

### Phase 1: Fix Existing Tests (30 min) - Target: 80%

**Goal**: Get all 79 existing tests passing

#### Step 1.1: Install pytest-asyncio (5 min)
```bash
cd ~/vikunja-slack-bot
source .venv/bin/activate
uv pip install pytest-asyncio
```

**Expected**: Async test warnings disappear

#### Step 1.2: Fix Handler Test Mocking (15 min)
**Problem**: Tests try to mock functions that don't exist in matrix_handlers.py

**Files to check**:
- `src/vikunja_mcp/server.py` - where functions are actually defined
- `src/vikunja_mcp/matrix_handlers.py` - what's imported/exported

**Actions**:
1. Map which functions exist where
2. Update test imports to match reality
3. Fix mocking paths

**Expected**: 10-12 more handler tests pass (7 → 17-19 passing)

#### Step 1.3: Fix Client Async Tests (10 min)
**Problem**: Async tests need proper setup

**Actions**:
1. Add pytest-asyncio config to pyproject.toml
2. Fix async test decorators
3. Mock AsyncClient methods properly

**Expected**: 2 more client tests pass (17 → 19 passing)

**Phase 1 Result**: 78-79/79 tests passing, ~80% coverage

---

### Phase 2: Add Missing Handler Tests (45 min) - Target: 90%

**Goal**: Test all 13 functions in matrix_handlers.py

**Currently Untested Functions** (estimated):
1. `_execute_tool()` - Tool execution with TOOL_REGISTRY
2. `_parse_args_string()` - JSON schema parsing
3. `_format_tool_result()` - Result formatting
4. `_format_tasks_for_matrix()` - Task list formatting
5. `_format_projects_for_matrix()` - Project list formatting
6. `_handle_connect()` - Vikunja connection
7. `_handle_list_instances()` - Instance listing
8. `_handle_disconnect()` - Disconnect flow
9. `_handle_test_connection()` - Connection testing
10. `_handle_stats()` - Usage statistics

#### Step 2.1: Add Tool Execution Tests (15 min)
**File**: `tests/test_matrix_handlers.py`

**New tests** (~10 tests):
- Test `_execute_tool()` with valid tool
- Test `_execute_tool()` with invalid tool
- Test `_execute_tool()` with tool exception
- Test `_parse_args_string()` with valid JSON schema
- Test `_parse_args_string()` with invalid args
- Test `_format_tool_result()` for different result types
- Test `_format_tasks_for_matrix()` with task list
- Test `_format_tasks_for_matrix()` with empty list
- Test `_format_projects_for_matrix()` with projects
- Test `_format_projects_for_matrix()` with empty list

**Expected**: +10 tests, ~15% coverage increase

#### Step 2.2: Add Connection Handler Tests (15 min)
**File**: `tests/test_matrix_handlers.py`

**New tests** (~8 tests):
- Test `_handle_connect()` with valid URL and token
- Test `_handle_connect()` with invalid URL
- Test `_handle_connect()` with missing token
- Test `_handle_list_instances()` with instances
- Test `_handle_list_instances()` with no instances
- Test `_handle_disconnect()` success
- Test `_handle_test_connection()` success
- Test `_handle_test_connection()` failure

**Expected**: +8 tests, ~10% coverage increase

#### Step 2.3: Add Stats Handler Tests (15 min)
**File**: `tests/test_matrix_handlers.py`

**New tests** (~5 tests):
- Test `_handle_stats()` with usage data
- Test `_handle_stats()` with no data
- Test stats formatting
- Test stats calculation
- Test stats edge cases

**Expected**: +5 tests, ~5% coverage increase

**Phase 2 Result**: ~102 tests total, ~90% coverage

---

### Phase 3: Add Missing Client Tests (45 min) - Target: 95%

**Goal**: Test all 12 functions in matrix_client.py

**Currently Untested Functions** (estimated):
1. `login()` - Login flow
2. `start()` - Bot startup
3. `_custom_sync_loop()` - Sync loop
4. `_handle_message()` - Message callback
5. `_handle_invite()` - Invite handling
6. `send_message()` - Message sending
7. `send_thinking()` - Thinking indicator
8. `clear_thinking()` - Clear thinking indicator

#### Step 3.1: Add Login/Startup Tests (15 min)
**File**: `tests/test_matrix_client.py`

**New tests** (~6 tests):
- Test `login()` with password success
- Test `login()` with password failure
- Test `login()` with token (skip login)
- Test `start()` initialization
- Test `start()` with login failure
- Test `start()` with sync failure

**Expected**: +6 tests, ~10% coverage increase

#### Step 3.2: Add Message Handling Tests (15 min)
**File**: `tests/test_matrix_client.py`

**New tests** (~8 tests):
- Test `_handle_message()` in DM
- Test `_handle_message()` in room
- Test `_handle_message()` ignores old messages
- Test `_handle_message()` ignores own messages
- Test `_handle_invite()` auto-accept
- Test `_handle_invite()` from non-admin
- Test message filtering by timestamp
- Test message filtering by sender

**Expected**: +8 tests, ~10% coverage increase

#### Step 3.3: Add Message Sending Tests (15 min)
**File**: `tests/test_matrix_client.py`

**New tests** (~6 tests):
- Test `send_message()` success
- Test `send_message()` failure
- Test `send_thinking()` creates indicator
- Test `send_thinking()` tracks message ID
- Test `clear_thinking()` removes indicator
- Test `clear_thinking()` with no indicator

**Expected**: +6 tests, ~5% coverage increase

**Phase 3 Result**: ~122 tests total, ~95% coverage

---

### Phase 4: Integration & Edge Cases (30 min) - Target: 100%

**Goal**: Cover remaining edge cases and integration scenarios

#### Step 4.1: Add Sync Loop Tests (15 min)
**File**: `tests/test_matrix_client.py`

**New tests** (~5 tests):
- Test `_custom_sync_loop()` receives events
- Test `_custom_sync_loop()` handles errors
- Test `_custom_sync_loop()` reconnects
- Test `_custom_sync_loop()` updates next_batch
- Test `_custom_sync_loop()` timeout handling

**Expected**: +5 tests, ~3% coverage increase

#### Step 4.2: Add Error Path Tests (15 min)
**Files**: All test files

**New tests** (~8 tests):
- Test network errors in all async methods
- Test JSON parsing errors
- Test Matrix API errors
- Test rate limiting
- Test invalid room IDs
- Test malformed messages
- Test Unicode edge cases
- Test very long messages

**Expected**: +8 tests, ~2% coverage increase

**Phase 4 Result**: ~135 tests total, ~100% coverage

---

## 📊 Coverage Milestones

| Phase | Time | Tests | Coverage | Status |
|-------|------|-------|----------|--------|
| **Current** | - | 79 | 70% | ✅ Done |
| **Phase 1** | 30 min | 79 | 80% | 🎯 Fix existing |
| **Phase 2** | 45 min | 102 | 90% | 🎯 Handler tests |
| **Phase 3** | 45 min | 122 | 95% | 🎯 Client tests |
| **Phase 4** | 30 min | 135 | 100% | 🎯 Edge cases |
| **TOTAL** | **2.5 hours** | **135** | **100%** | 🏆 Complete |

---

## 🛠️ Implementation Strategy

### Approach: TDD + Incremental Coverage

1. **Write tests first** for each function
2. **Run tests** to see what fails
3. **Fix implementation** if needed
4. **Verify coverage** increases
5. **Commit frequently** (after each phase)

### Tools Needed

```bash
# Install dependencies
uv pip install pytest-asyncio pytest-mock pytest-cov

# Run tests with coverage
pytest tests/test_matrix_*.py --cov=src/vikunja_mcp --cov-report=term-missing --cov-report=html

# View HTML coverage report
open htmlcov/index.html  # or xdg-open on Linux
```

### Success Criteria

- ✅ All tests passing (100%)
- ✅ Coverage report shows 100% for all Matrix files
- ✅ No untested functions
- ✅ No untested branches
- ✅ All edge cases covered
- ✅ All error paths tested

---

## 📝 Tracking Progress

### Phase 1 Checklist
- [ ] Install pytest-asyncio
- [ ] Map handler function locations
- [ ] Fix handler test mocking
- [ ] Fix client async tests
- [ ] Verify 78-79/79 tests passing
- [ ] Commit: "test: Fix all existing tests (80% coverage)"

### Phase 2 Checklist
- [ ] Add tool execution tests (10 tests)
- [ ] Add connection handler tests (8 tests)
- [ ] Add stats handler tests (5 tests)
- [ ] Verify ~102 tests passing
- [ ] Commit: "test: Add handler tests (90% coverage)"

### Phase 3 Checklist
- [ ] Add login/startup tests (6 tests)
- [ ] Add message handling tests (8 tests)
- [ ] Add message sending tests (6 tests)
- [ ] Verify ~122 tests passing
- [ ] Commit: "test: Add client tests (95% coverage)"

### Phase 4 Checklist
- [ ] Add sync loop tests (5 tests)
- [ ] Add error path tests (8 tests)
- [ ] Verify ~135 tests passing
- [ ] Verify 100% coverage
- [ ] Commit: "test: Achieve 100% coverage"

---

## 🎯 Next Action

**Start Phase 1**: Fix existing tests to reach 80% coverage

```bash
cd ~/vikunja-slack-bot
source .venv/bin/activate

# Step 1: Install pytest-asyncio
uv pip install pytest-asyncio

# Step 2: Check function locations
grep -n "^def " src/vikunja_mcp/server.py | grep -E "(first_contact|user_welcomed|user_vikunja_token|is_admin)"

# Step 3: Run tests to see current failures
pytest tests/test_matrix_handlers.py -v --tb=short

# Step 4: Fix mocking based on findings
# (Update test file with correct import paths)
```

---

**Created**: 2025-12-24  
**Target**: 100% coverage in 2.5 hours  
**Current**: 70% coverage, 61/79 tests passing  
**Strategy**: TDD + Incremental + Frequent commits

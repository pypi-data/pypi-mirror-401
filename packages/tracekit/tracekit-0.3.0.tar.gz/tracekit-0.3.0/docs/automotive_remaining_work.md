# Automotive Module - Remaining Work & Enhancements

## Status: 3,596 lines implemented, 47/47 core tests passing

---

## PRIORITY 1: Critical Gaps (Must Fix)

### 1.1 Complete MDF Loader Implementation

**Current:** Stubbed, raises error
**Need:** Full asammdf integration
**Effort:** 2-3 hours
**Impact:** HIGH - MDF is primary format for CANedge and many automotive loggers

```python
# File: src/tracekit/automotive/loaders/mdf.py
# Current: Stub that raises "No CAN messages found"
# Need: Iterate through MDF groups/channels, extract CAN frames
```

### 1.2 Add Comprehensive Test Coverage

**Current:** 47 tests for core models/session/analysis, 0 for loaders/protocols
**Need:** 50+ additional tests
**Effort:** 4-6 hours
**Impact:** HIGH - Essential for reliability

**Missing Tests:**

- `test_blf_loader.py` - BLF file loading with synthetic data
- `test_asc_loader.py` - ASC parsing edge cases
- `test_mdf_loader.py` - MDF4 file loading
- `test_csv_loader.py` - CSV format variations
- `test_dbc_parser.py` - DBC parsing and decoding
- `test_dbc_generator.py` - DBC generation and round-trip
- `test_obd2_decoder.py` - OBD-II PID decoding
- `test_j1939_decoder.py` - J1939 PGN extraction
- `test_correlation.py` - Signal correlation analysis
- `test_checksum.py` - CRC/checksum detection

### 1.3 Integration Tests

**Current:** None
**Need:** End-to-end workflow validation
**Effort:** 3-4 hours
**Impact:** MEDIUM - Validates complete workflows

**Test Scenarios:**

- Load BLF → analyze → export DBC → reload DBC → decode
- Load CSV → test hypotheses → document → save .tkcan → reload
- Multiple formats → merge sessions → correlate signals
- Large file (10K+ messages) performance test

---

## PRIORITY 2: Phase 4 Features (Planned but Not Built)

### 2.1 State Machine Integration

**Effort:** 6-8 hours
**Impact:** HIGH - Key differentiator for protocol learning
**Dependencies:** Existing `inference/state_machine.py`

**Implementation:**

```python
# src/tracekit/automotive/can/state_machine.py
class CANStateMachine:
    """Learn CAN protocol state machines from message sequences."""
    def learn_from_session(self, session: CANSession, trigger_ids: list[int]) -> Automaton:
        # Extract message sequences around trigger IDs
        # Use existing StateMachineInferrer
        # Return learned state machine
```

**Use Cases:**

- Learn ignition sequence state machine
- Discover initialization sequences
- Identify state-dependent message patterns

### 2.2 Multi-Message Pattern Learning

**Effort:** 4-5 hours
**Impact:** MEDIUM - Useful for discovering message dependencies
**Dependencies:** Existing `inference/sequences.py`

**Implementation:**

- Detect message pairs that always occur together
- Find message sequences (A → B → C patterns)
- Temporal correlation (message A within 10ms of message B)

### 2.3 Stimulus-Response Mapping

**Effort:** 5-6 hours
**Impact:** MEDIUM - Very useful for control message identification

**Implementation:**

```python
class StimulusResponseAnalyzer:
    """Map user actions to CAN message changes."""
    def detect_responses(self,
                        baseline_session: CANSession,
                        stimulus_session: CANSession,
                        time_window_ms: float = 100) -> dict:
        # Compare sessions to find which messages changed
        # Return mapping of changes
```

---

## PRIORITY 3: Essential Protocol Expansions

### 3.1 Expand OBD-II Coverage

**Current:** 7 PIDs
**Target:** 50+ most common PIDs
**Effort:** 2-3 hours
**Impact:** MEDIUM - Better diagnostic coverage

**Add PIDs:**

- Fuel pressure, timing advance, MAF, O2 sensors
- Fuel trim, commanded EGR, catalyst temperature
- Control module voltage, ambient air temp
- Extended PIDs (0x20-0xFF)

### 3.2 Expand J1939 Coverage

**Current:** 11 PGN names
**Target:** 100+ common PGNs with signal definitions
**Effort:** 4-5 hours
**Impact:** MEDIUM - Essential for heavy-duty vehicles

**Add PGN Databases:**

- Engine parameters (torque, fuel rate, boost pressure)
- Transmission parameters (gear, clutch pressure)
- Vehicle dynamics (brake pressure, wheel speed)
- Aftertreatment (DPF status, DEF level)

### 3.3 UDS Protocol Support

**Effort:** 6-8 hours
**Impact:** MEDIUM - Important for advanced diagnostics

**Implementation:**

```python
# src/tracekit/automotive/uds/decoder.py
class UDSDecoder:
    """ISO 14229 UDS protocol decoder."""
    # Services: 0x10 (session), 0x22 (read), 0x2E (write), 0x27 (security), etc.
```

### 3.4 DTC Database

**Effort:** 3-4 hours
**Impact:** LOW-MEDIUM - Useful but not critical

**Add:**

- P, C, B, U code database (200+ common DTCs)
- Manufacturer-specific codes
- Repair recommendations

---

## PRIORITY 4: Enhancements & Polish

### 4.1 Visualization Capabilities

**Effort:** 8-10 hours
**Impact:** HIGH - Greatly improves usability

**Implement:**

```python
# src/tracekit/automotive/visualization/
- plot_signals() - Time series of decoded signals
- plot_correlation_matrix() - Heatmap of signal correlations
- plot_message_timing() - Message frequency/jitter visualization
- plot_bus_utilization() - CAN bus load over time
```

### 4.2 Enhanced Export Formats

**Effort:** 3-4 hours
**Impact:** MEDIUM - Improves interoperability

**Add:**

- CSV signal export (decoded signals to CSV)
- JSON export (structured message data)
- Parquet export (efficient columnar storage)
- PCAP export (for Wireshark analysis)

### 4.3 Performance Optimization

**Effort:** 4-6 hours
**Impact:** MEDIUM - Important for large files

**Optimizations:**

- Chunked file reading for files > 100MB
- Lazy loading of messages
- Parallel analysis of multiple message IDs
- Cache expensive computations (entropy, correlation)

### 4.4 Advanced Analysis Features

**Effort:** 6-8 hours
**Impact:** LOW-MEDIUM - Nice additions

**Add:**

- FFT/spectral analysis of periodic signals
- Outlier detection (Isolation Forest, DBSCAN)
- Signal type classification (ML-based)
- Automatic scale/offset inference

### 4.5 Documentation & Examples

**Effort:** 6-8 hours
**Impact:** HIGH - Essential for adoption

**Create:**

- User guide (Markdown in docs/automotive/)
- API reference (auto-generated from docstrings)
- Jupyter notebook tutorials
- Additional examples:
  - OBD-II correlation example
  - J1939 heavy-duty example
  - State machine learning example
  - Visualization example

### 4.6 CANSession Enhancements

**Effort:** 4-5 hours
**Impact:** MEDIUM

**Add:**

- `session.replay()` - Simulate message timing
- `session.inject()` - Add synthetic messages
- `session.window()` - Time-based slicing
- `session.compare()` - Statistical comparison between sessions
- `session.export_signals()` - Export decoded signals to CSV/DataFrame

### 4.7 Discovery Document Enhancements

**Effort:** 3-4 hours
**Impact:** LOW-MEDIUM

**Add:**

- `DiscoveryDocument.merge()` - Combine multiple .tkcan files
- `DiscoveryDocument.diff()` - Compare two documents
- `DiscoveryDocument.validate()` - Test against actual data
- Auto-confidence scoring based on evidence

---

## PRIORITY 5: Code Quality & Technical Debt

### 5.1 Error Handling & Validation

**Effort:** 2-3 hours
**Impact:** MEDIUM

**Improvements:**

- Validate CAN message data length
- Graceful handling of malformed files
- Better error messages with context
- Input validation in all public APIs

### 5.2 Type Hints & Documentation

**Effort:** 2-3 hours
**Impact:** LOW

**Improvements:**

- Complete type hints throughout
- Docstring completeness check
- Add usage examples to all docstrings

### 5.3 Configuration & Constants

**Effort:** 2 hours
**Impact:** LOW

**Improvements:**

- Move magic numbers to named constants
- Configurable thresholds (entropy, correlation, confidence)
- Configuration file support (.tracekitrc)

---

## Summary & Recommendations

### Immediate Actions (Next 1-2 days)

1. ✅ **Complete MDF loader** (2-3 hours) - CRITICAL
2. ✅ **Add loader tests** (3-4 hours) - CRITICAL
3. ✅ **Add protocol tests** (DBC, OBD-II, J1939) (2-3 hours) - CRITICAL
4. ✅ **Integration tests** (2-3 hours) - IMPORTANT

**Total:** ~10-13 hours for production-ready

### Short-term Enhancements (Next 1-2 weeks)

1. State machine integration (6-8 hours)
2. Visualization basics (4-5 hours)
3. Documentation & user guide (4-5 hours)
4. Expand OBD-II/J1939 coverage (4-6 hours)

**Total:** ~18-24 hours for feature-complete

### Long-term Nice-to-Haves (Future)

- UDS protocol support
- Advanced analysis (ML, FFT)
- Real-time streaming
- Performance optimization for huge files
- Additional export formats

---

## Testing Coverage Goals

| Component   | Current  | Target | Priority |
| ----------- | -------- | ------ | -------- |
| Core models | 13/13 ✅ | 13/13  | -        |
| Analysis    | 13/13 ✅ | 13/13  | -        |
| Session     | 12/12 ✅ | 12/12  | -        |
| Discovery   | 10/10 ✅ | 10/10  | -        |
| Loaders     | 0/4 ❌   | 15/15  | HIGH     |
| DBC         | 0/2 ❌   | 10/10  | HIGH     |
| OBD-II      | 0/1 ❌   | 8/8    | HIGH     |
| J1939       | 0/1 ❌   | 6/6    | MEDIUM   |
| Correlation | 0/1 ❌   | 5/5    | MEDIUM   |
| Integration | 0/0 ❌   | 5/5    | HIGH     |
| **Total**   | **47**   | **97** | -        |

---

## Lines of Code Estimates

| Component        | Current | Estimated Final |
| ---------------- | ------- | --------------- |
| Implemented      | 3,596   | -               |
| Tests needed     | +800    | 4,396           |
| Phase 4 features | +1,200  | 5,596           |
| Enhancements     | +1,500  | 7,096           |
| Documentation    | +500    | 7,596           |

**Current Completion:** ~47% of planned functionality
**With Priority 1-2:** ~70% of planned functionality
**Fully feature-complete:** ~100% (~7,600 lines total)

---

## Risk Assessment

**LOW RISK:**

- Current implementation is solid, tested, working
- Core workflow is proven with example
- No breaking changes needed

**MEDIUM RISK:**

- MDF loader complexity (asammdf API)
- Performance with very large files (> 1GB)
- Integration with existing state machine code

**MITIGATION:**

- Incremental implementation with tests
- Performance testing with synthetic large files
- Clear documentation of limitations

---

## Conclusion

**What we have:**

- Solid foundation (3,596 LOC, 47 tests passing)
- Core discovery workflow complete and tested
- Essential protocols (DBC, OBD-II, J1939) implemented
- Example demonstrates value

**What's missing:**

- Test coverage for loaders and protocols (~10 hours to fix)
- MDF loader implementation (~3 hours)
- Phase 4 advanced features (~20 hours)
- Documentation and polish (~10 hours)

**Recommendation:**
Focus on **Priority 1 items first** (~13 hours) to make the module production-ready, then incrementally add Priority 2-3 features based on user demand.

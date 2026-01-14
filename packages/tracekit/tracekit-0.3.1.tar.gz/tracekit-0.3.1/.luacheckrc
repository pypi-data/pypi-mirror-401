-- ============================================================================
-- Luacheck Configuration for TraceKit
-- ============================================================================
-- Configuration for luacheck static analyzer
-- Optimized for Wireshark Lua dissector development
-- ============================================================================

-- Global settings
std = "lua51"  -- Wireshark uses Lua 5.1
cache = true
codes = true

-- Line length limit
max_line_length = 120
max_code_line_length = 120
max_comment_line_length = 120

-- Ignore specific warnings
ignore = {
    "212", -- Unused argument (common in dissector callbacks)
}

-- Wireshark API globals (read-only)
read_globals = {
    -- Core Wireshark classes
    "Proto",
    "ProtoField",
    "ProtoExpert",
    "DissectorTable",
    "Dissector",

    -- Field types
    "base",
    "frametype",
    "ftypes",

    -- Expert info constants
    "PI_CHECKSUM",
    "PI_SEQUENCE",
    "PI_RESPONSE_CODE",
    "PI_REQUEST_CODE",
    "PI_UNDECODED",
    "PI_REASSEMBLE",
    "PI_MALFORMED",
    "PI_DEBUG",
    "PI_PROTOCOL",
    "PI_SECURITY",
    "PI_COMMENTS_GROUP",
    "PI_DECRYPTION_GROUP",
    "PI_ASSUMPTION_GROUP",
    "PI_DEPRECATED_GROUP",

    -- Severity levels
    "PI_CHAT",
    "PI_NOTE",
    "PI_WARN",
    "PI_ERROR",

    -- Utility functions
    "ByteArray",
    "Tvb",
    "TvbRange",
    "UInt64",

    -- Preferences
    "Pref",

    -- Common Wireshark functions
    "register_postdissector",
    "register_menu",

    -- Lua built-ins that might be flagged
    "table",
    "string",
    "math",
    "bit32",
}

-- File-specific configurations
files["generated_dissectors/*.lua"] = {
    -- Allow unused variables in generated code
    ignore = {
        "211", -- Unused local variable
        "212", -- Unused argument
        "213", -- Unused loop variable
    },

    -- Allow longer lines in generated code
    max_line_length = 150,
}

-- Exclude patterns (if needed in the future)
exclude_files = {
    "**/.venv/**",
    "**/node_modules/**",
    "**/build/**",
    "**/dist/**",
}

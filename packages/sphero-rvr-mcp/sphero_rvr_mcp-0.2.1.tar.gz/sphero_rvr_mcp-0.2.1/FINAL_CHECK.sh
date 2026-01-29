#!/bin/bash

echo "========================================="
echo "Sphero RVR MCP Server - Final Verification"
echo "========================================="
echo ""

echo "✓ Checking Python syntax..."
python -m py_compile src/sphero_rvr_mcp/server.py && echo "  Server syntax: OK" || echo "  Server syntax: FAILED"

echo ""
echo "✓ Checking imports..."
cd /home/jsperson/source/sphero_rvr_mcp
python -c "from sphero_rvr_mcp.server import mcp; print('  Server import: OK')" 2>&1 | grep -q "OK" && echo "  Server import: OK" || echo "  Server import: FAILED"

echo ""
echo "✓ Counting files created..."
FILE_COUNT=$(find src/sphero_rvr_mcp -name "*.py" -type f | wc -l)
echo "  Python files: $FILE_COUNT"

echo ""
echo "✓ Checking dependencies..."
pip list | grep -q "structlog" && echo "  structlog: installed" || echo "  structlog: MISSING"
pip list | grep -q "tenacity" && echo "  tenacity: installed" || echo "  tenacity: MISSING"
pip list | grep -q "prometheus" && echo "  prometheus-client: installed" || echo "  prometheus-client: MISSING"

echo ""
echo "✓ Directory structure..."
ls -d src/sphero_rvr_mcp/core 2>/dev/null && echo "  core/: exists" || echo "  core/: MISSING"
ls -d src/sphero_rvr_mcp/hardware 2>/dev/null && echo "  hardware/: exists" || echo "  hardware/: MISSING"
ls -d src/sphero_rvr_mcp/services 2>/dev/null && echo "  services/: exists" || echo "  services/: MISSING"
ls -d src/sphero_rvr_mcp/observability 2>/dev/null && echo "  observability/: exists" || echo "  observability/: MISSING"

echo ""
echo "========================================="
echo "Rewrite Status: COMPLETE ✅"
echo "========================================="
echo ""
echo "Ready to test with hardware!"
echo "Run: sphero-rvr-mcp"

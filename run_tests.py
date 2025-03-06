#!/usr/bin/env python3
import os
import sys
import pytest

if __name__ == "__main__":
    # Add minimum test coverage requirement
    min_coverage = 70
    
    # Run pytest with coverage
    result = pytest.main([
        "--cov=rummikub",
        "--cov-report=term",
        "--cov-report=html",
        "--cov-fail-under=" + str(min_coverage),
        "tests/"
    ])
    
    # Print summary based on result
    if result == 0:
        print(f"\n✅ All tests passed with at least {min_coverage}% coverage!")
    else:
        print(f"\n❌ Tests failed or coverage below {min_coverage}%")
    
    sys.exit(result)
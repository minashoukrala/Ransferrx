#!/usr/bin/env python3
"""
Comprehensive Test Runner

This script runs all comprehensive tests including:
- Malformed data tests
- Enhanced validator tests  
- Integration tests

Usage:
    python tests/run_comprehensive_tests.py
"""

import sys
import os
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import test modules
from test_malformed_data import main as test_malformed_data
from test_enhanced_validators import main as test_enhanced_validators
from test_integration import main as test_integration
from test_quantity_validator import main as test_quantity_validator
from test_controlled_substance_validator import main as test_controlled_substance_validator
from test_duplicate_validator import main as test_duplicate_validator
from test_pharmacy_validator import main as test_pharmacy_validator
from test_all_validators import main as test_all_validators

# Import performance monitoring
from app.utils.performance_monitor import get_performance_summary, system_health


class TestRunner:
    """Comprehensive test runner with detailed reporting."""
    
    def __init__(self):
        """Initialize the test runner."""
        self.start_time = datetime.now()
        self.results: Dict[str, Dict[str, Any]] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def run_test_category(self, category_name: str, test_function, is_async: bool = False) -> Dict[str, Any]:
        """
        Run a test category and record results.
        
        Args:
            category_name: Name of the test category
            test_function: Function to run the tests
            is_async: Whether the test function is async
            
        Returns:
            Dict[str, Any]: Test results
        """
        print(f"\n{'='*20} {category_name.upper()} {'='*20}")
        
        start_time = time.time()
        
        try:
            if is_async:
                success = asyncio.run(test_function())
            else:
                success = test_function()
            
            duration = time.time() - start_time
            
            result = {
                "success": success,
                "duration": duration,
                "timestamp": datetime.now().isoformat()
            }
            
            if success:
                print(f"✅ {category_name} tests PASSED ({duration:.3f}s)")
                self.passed_tests += 1
            else:
                print(f"❌ {category_name} tests FAILED ({duration:.3f}s)")
                self.failed_tests += 1
            
            self.total_tests += 1
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 {category_name} tests CRASHED ({duration:.3f}s): {e}")
            
            result = {
                "success": False,
                "duration": duration,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            self.failed_tests += 1
            self.total_tests += 1
            return result
    
    def run_all_tests(self) -> None:
        """Run all test categories."""
        print("🚀 COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Define test categories
        test_categories = [
            ("Malformed Data Tests", test_malformed_data, False),
            ("Enhanced Validator Tests", test_enhanced_validators, False),
            ("Integration Tests", test_integration, True),
            ("Quantity Validator Tests", test_quantity_validator, False),
            ("Controlled Substance Validator Tests", test_controlled_substance_validator, False),
            ("Duplicate Validator Tests", test_duplicate_validator, False),
            ("Pharmacy Validator Tests", test_pharmacy_validator, False),
            ("All Validators Integration Tests", test_all_validators, False),
        ]
        
        # Run each test category
        for category_name, test_function, is_async in test_categories:
            self.results[category_name] = self.run_test_category(category_name, test_function, is_async)
        
        # Record system health
        system_health.record_request(self.failed_tests == 0)
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive test report.
        
        Returns:
            Dict[str, Any]: Test report
        """
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        # Calculate success rate
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        # Get performance summary
        performance_summary = get_performance_summary()
        
        # Generate detailed results
        detailed_results = {}
        for category, result in self.results.items():
            detailed_results[category] = {
                "status": "PASSED" if result["success"] else "FAILED",
                "duration": f"{result['duration']:.3f}s",
                "timestamp": result["timestamp"]
            }
            if "error" in result:
                detailed_results[category]["error"] = result["error"]
        
        report = {
            "test_summary": {
                "total_categories": self.total_tests,
                "passed_categories": self.passed_tests,
                "failed_categories": self.failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "total_duration": f"{total_duration:.3f}s",
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat()
            },
            "detailed_results": detailed_results,
            "performance_summary": performance_summary,
            "overall_status": "PASSED" if self.failed_tests == 0 else "FAILED"
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """
        Print formatted test report.
        
        Args:
            report: Test report to print
        """
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Test Summary
        summary = report["test_summary"]
        print(f"📈 Test Summary:")
        print(f"   Total Categories: {summary['total_categories']}")
        print(f"   Passed: {summary['passed_categories']}")
        print(f"   Failed: {summary['failed_categories']}")
        print(f"   Success Rate: {summary['success_rate']}")
        print(f"   Total Duration: {summary['total_duration']}")
        print(f"   Start Time: {summary['start_time']}")
        print(f"   End Time: {summary['end_time']}")
        
        # Detailed Results
        print(f"\n📋 Detailed Results:")
        for category, result in report["detailed_results"].items():
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"   {status_icon} {category}: {result['status']} ({result['duration']})")
            if "error" in result:
                print(f"      Error: {result['error']}")
        
        # Performance Summary
        perf = report["performance_summary"]
        print(f"\n⚡ Performance Summary:")
        print(f"   System Status: {perf['system_health']['status']}")
        print(f"   Uptime: {perf['system_health']['uptime_seconds']:.1f}s")
        print(f"   Total Requests: {perf['system_health']['total_requests']}")
        print(f"   Error Rate: {perf['system_health']['error_rate_percent']:.1f}%")
        
        # Overall Status
        print(f"\n🎯 Overall Status: {report['overall_status']}")
        
        if report['overall_status'] == "PASSED":
            print("🎉 All tests passed! System is ready for production.")
        else:
            print("⚠️  Some tests failed. Please review and fix issues before deployment.")
    
    def save_report(self, report: Dict[str, Any], filename: Optional[str] = None) -> None:
        """
        Save test report to file.
        
        Args:
            report: Test report to save
            filename: Optional filename, defaults to timestamp-based name
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.json"
        
        import json
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Test report saved to: {filename}")


def main():
    """Run comprehensive test suite."""
    runner = TestRunner()
    
    try:
        # Run all tests
        runner.run_all_tests()
        
        # Generate and print report
        report = runner.generate_report()
        runner.print_report(report)
        
        # Save report
        runner.save_report(report)
        
        # Return success/failure
        return report["overall_status"] == "PASSED"
        
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        return False
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
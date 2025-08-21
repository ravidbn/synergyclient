#!/usr/bin/env python3
"""
Test runner for Android application
Executes all unit tests and integration tests with comprehensive reporting
"""
import sys
import os
import unittest
import time
import json
from io import StringIO
from datetime import datetime


class TestResult:
    """Test result container"""
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        self.skipped_tests = 0
        self.execution_time = 0.0
        self.failures = []
        self.errors = []


class ColoredTextTestResult(unittest.TextTestResult):
    """Enhanced test result with colored output and detailed reporting"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_results = TestResult()
        self.start_time = None
        
    def startTestRun(self):
        super().startTestRun()
        self.start_time = time.time()
        self._print_colored("=" * 70, 'blue')
        self._print_colored("SYNERGY ANDROID APPLICATION TEST SUITE", 'blue', bold=True)
        self._print_colored("=" * 70, 'blue')
        print(f"Test run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def stopTestRun(self):
        super().stopTestRun()
        end_time = time.time()
        self.test_results.execution_time = end_time - self.start_time
        self._generate_summary_report()

    def startTest(self, test):
        super().startTest(test)
        self.test_results.total_tests += 1

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.passed_tests += 1
        if self.verbosity > 1:
            self._print_colored(f"✓ {self._get_test_description(test)}", 'green')

    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.error_tests += 1
        self.test_results.errors.append((test, err))
        self._print_colored(f"✗ {self._get_test_description(test)} - ERROR", 'red')

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.failed_tests += 1
        self.test_results.failures.append((test, err))
        self._print_colored(f"✗ {self._get_test_description(test)} - FAILED", 'red')

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_results.skipped_tests += 1
        if self.verbosity > 1:
            self._print_colored(f"⚠ {self._get_test_description(test)} - SKIPPED: {reason}", 'yellow')

    def _get_test_description(self, test):
        """Get formatted test description"""
        return f"{test.__class__.__name__}.{test._testMethodName}"

    def _print_colored(self, text, color, bold=False):
        """Print colored text to console"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
        
        if bold:
            text = f'\033[1m{text}\033[0m'
        
        if color in colors:
            print(f"{colors[color]}{text}{colors['reset']}")
        else:
            print(text)

    def _generate_summary_report(self):
        """Generate comprehensive test summary report"""
        print("\n" + "=" * 70)
        self._print_colored("TEST EXECUTION SUMMARY", 'blue', bold=True)
        print("=" * 70)
        
        # Overall statistics
        print(f"Total Tests Run: {self.test_results.total_tests}")
        self._print_colored(f"Passed: {self.test_results.passed_tests}", 'green')
        self._print_colored(f"Failed: {self.test_results.failed_tests}", 'red')
        self._print_colored(f"Errors: {self.test_results.error_tests}", 'red')
        self._print_colored(f"Skipped: {self.test_results.skipped_tests}", 'yellow')
        print(f"Execution Time: {self.test_results.execution_time:.2f} seconds")
        
        # Calculate success rate
        if self.test_results.total_tests > 0:
            success_rate = (self.test_results.passed_tests / self.test_results.total_tests) * 100
            if success_rate >= 90:
                color = 'green'
            elif success_rate >= 70:
                color = 'yellow'
            else:
                color = 'red'
            self._print_colored(f"Success Rate: {success_rate:.1f}%", color)
        
        # Detailed failure/error reporting
        if self.test_results.failures:
            print("\n" + "-" * 70)
            self._print_colored("FAILURES:", 'red', bold=True)
            print("-" * 70)
            for test, traceback in self.test_results.failures:
                print(f"\nFAILED: {self._get_test_description(test)}")
                print(traceback[1])
        
        if self.test_results.errors:
            print("\n" + "-" * 70)
            self._print_colored("ERRORS:", 'red', bold=True)
            print("-" * 70)
            for test, traceback in self.test_results.errors:
                print(f"\nERROR: {self._get_test_description(test)}")
                print(traceback[1])
        
        # Overall result
        print("\n" + "=" * 70)
        if self.test_results.failed_tests == 0 and self.test_results.error_tests == 0:
            self._print_colored("ALL TESTS PASSED! ✓", 'green', bold=True)
        else:
            self._print_colored("SOME TESTS FAILED! ✗", 'red', bold=True)
        print("=" * 70)

    def export_results_json(self, filename):
        """Export test results to JSON file"""
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': self.test_results.total_tests,
                'passed_tests': self.test_results.passed_tests,
                'failed_tests': self.test_results.failed_tests,
                'error_tests': self.test_results.error_tests,
                'skipped_tests': self.test_results.skipped_tests,
                'execution_time': self.test_results.execution_time,
                'success_rate': (self.test_results.passed_tests / self.test_results.total_tests * 100) if self.test_results.total_tests > 0 else 0
            },
            'failures': [
                {
                    'test': self._get_test_description(test),
                    'traceback': str(traceback[1])
                }
                for test, traceback in self.test_results.failures
            ],
            'errors': [
                {
                    'test': self._get_test_description(test),
                    'traceback': str(traceback[1])
                }
                for test, traceback in self.test_results.errors
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)


class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.test_modules = [
            'test_protocol',
            'test_file_generator',
            'test_integration'
        ]
        
    def discover_tests(self, test_dir='.'):
        """Discover all test modules"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        for module_name in self.test_modules:
            try:
                # Import the test module
                module = __import__(module_name)
                
                # Load tests from the module
                module_suite = loader.loadTestsFromModule(module)
                suite.addTest(module_suite)
                
                print(f"✓ Loaded tests from {module_name}")
            except ImportError as e:
                print(f"✗ Failed to import {module_name}: {e}")
            except Exception as e:
                print(f"✗ Error loading tests from {module_name}: {e}")
        
        return suite

    def run_tests(self, verbosity=2, export_json=True):
        """Run all discovered tests"""
        print("Discovering test modules...")
        suite = self.discover_tests()
        
        if suite.countTestCases() == 0:
            print("No tests found!")
            return False
        
        print(f"Found {suite.countTestCases()} test cases\n")
        
        # Create custom test runner
        stream = sys.stdout
        runner = unittest.TextTestRunner(
            stream=stream,
            verbosity=verbosity,
            resultclass=ColoredTextTestResult
        )
        
        # Run the tests
        result = runner.run(suite)
        
        # Export results if requested
        if export_json:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_filename = f"test_results_{timestamp}.json"
            result.export_results_json(json_filename)
            print(f"\nTest results exported to: {json_filename}")
        
        # Return success status
        return len(result.failures) == 0 and len(result.errors) == 0

    def run_specific_test(self, test_class, test_method=None):
        """Run a specific test class or method"""
        if test_method:
            suite = unittest.TestSuite()
            suite.addTest(test_class(test_method))
        else:
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromTestCase(test_class)
        
        runner = unittest.TextTestRunner(verbosity=2, resultclass=ColoredTextTestResult)
        result = runner.run(suite)
        
        return len(result.failures) == 0 and len(result.errors) == 0

    def run_performance_tests(self):
        """Run performance-specific tests"""
        print("Running performance tests...")
        
        # Import performance test classes
        from test_integration import TestSystemPerformanceIntegration
        
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        
        # Add performance tests
        perf_tests = loader.loadTestsFromTestCase(TestSystemPerformanceIntegration)
        suite.addTest(perf_tests)
        
        runner = unittest.TextTestRunner(verbosity=2, resultclass=ColoredTextTestResult)
        result = runner.run(suite)
        
        return len(result.failures) == 0 and len(result.errors) == 0

    def run_smoke_tests(self):
        """Run a minimal set of smoke tests"""
        print("Running smoke tests...")
        
        # Import essential test classes
        from test_protocol import TestProtocolMessage
        from test_file_generator import TestFileGenerator
        
        suite = unittest.TestSuite()
        
        # Add critical tests
        suite.addTest(TestProtocolMessage('test_create_color_change_command'))
        suite.addTest(TestProtocolMessage('test_json_serialization_deserialization'))
        suite.addTest(TestFileGenerator('test_generate_small_file'))
        
        runner = unittest.TextTestRunner(verbosity=2, resultclass=ColoredTextTestResult)
        result = runner.run(suite)
        
        return len(result.failures) == 0 and len(result.errors) == 0


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Synergy Android Test Runner')
    parser.add_argument('--verbose', '-v', action='count', default=1,
                       help='Increase verbosity level')
    parser.add_argument('--no-json', action='store_true',
                       help='Do not export results to JSON')
    parser.add_argument('--performance', action='store_true',
                       help='Run performance tests only')
    parser.add_argument('--smoke', action='store_true',
                       help='Run smoke tests only')
    parser.add_argument('--module', '-m', type=str,
                       help='Run tests from specific module')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    try:
        if args.smoke:
            success = runner.run_smoke_tests()
        elif args.performance:
            success = runner.run_performance_tests()
        elif args.module:
            # Run specific module
            module = __import__(args.module)
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            
            test_runner = unittest.TextTestRunner(
                verbosity=args.verbose,
                resultclass=ColoredTextTestResult
            )
            result = test_runner.run(suite)
            success = len(result.failures) == 0 and len(result.errors) == 0
        else:
            success = runner.run_tests(
                verbosity=args.verbose,
                export_json=not args.no_json
            )
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during test execution: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
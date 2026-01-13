"""Test commands - Run various test suites."""

import sys
import os
import subprocess


def run_test_suite(suite_name: str):
    """Run a specific test suite.
    
    Args:
        suite_name: Name of the test suite to run
    """
    # Map suite names to test files
    test_files = {
        'vibe': 'test_vibe_system.py',
        'workflow': 'test_workflow.py',
        'installation': 'test_installation.py',
        'enhancements': 'test_enhancements.py',
        'enhanced-analysis': 'test_enhanced_analysis.py',
        'vibe-differences': 'test_vibe_differences.py',
        'workspace': 'test_workspace_simple.py',
    }
    
    if suite_name not in test_files:
        print(f"❌ Error: Unknown test suite '{suite_name}'")
        print("\nAvailable test suites:")
        for name in sorted(test_files.keys()):
            print(f"  - {name}")
        sys.exit(1)
    
    test_file = test_files[suite_name]
    
    print(f"\n🧪 Running {suite_name} tests...")
    print("=" * 60)
    
    # Get project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    test_path = os.path.join(project_root, test_file)
    
    if not os.path.exists(test_path):
        print(f"❌ Error: Test file not found: {test_path}")
        sys.exit(1)
    
    try:
        # Run the test file directly with python3
        result = subprocess.run(
            [sys.executable, test_path],
            cwd=project_root,
            capture_output=False,
            text=True
        )
        sys.exit(result.returncode)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_all_tests():
    """Run all available test suites."""
    print("\n🧪 Running All Test Suites...")
    print("=" * 60)
    
    test_files = [
        ('installation', 'test_installation.py'),
        ('workspace', 'test_workspace_simple.py'),
    ]
    
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    results = {}
    for suite_name, test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Running: {suite_name}")
        print('='*60)
        
        test_path = os.path.join(project_root, test_file)
        
        try:
            result = subprocess.run(
                [sys.executable, test_path],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            results[suite_name] = result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout: Test took longer than 60 seconds")
            results[suite_name] = False
        except Exception as e:
            print(f"❌ Failed: {e}")
            results[suite_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for suite, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {suite}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    sys.exit(0 if passed == total else 1)


def run_test_command(subcommand: str = None):
    """Main test command handler.
    
    Args:
        subcommand: The test subcommand to run
    """
    if not subcommand or subcommand in {"help", "-h", "--help"}:
        print("""
Usage: anox test <suite>

Test Suites:
  all                 Run all test suites
  vibe                Test vibe system and smartfix
  workflow            Test workflow commands
  installation        Test installation
  workspace           Test workspace functionality
  enhancements        Test enhancements
  enhanced-analysis   Test enhanced analysis
  vibe-differences    Test vibe differences
  help                Show this help message

Examples:
  anox test all                # Run all tests
  anox test vibe               # Run vibe system tests
  anox test workspace          # Run workspace tests
""")
        return
    
    if subcommand == "all":
        run_all_tests()
    else:
        run_test_suite(subcommand)

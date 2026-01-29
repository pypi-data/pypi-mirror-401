#!/usr/bin/env python3
"""
Comprehensive test script for pypeline-cli.

This script tests the full workflow of creating pypeline projects for both
Snowflake and Databricks platforms, including:
- Project initialization
- Pipeline creation (multiple pipelines)
- Processor creation (multiple processors per pipeline)
- Dependency syncing
- Verification that generated files contain proper platform-specific imports
  (snowflake.snowpark for Snowflake, pyspark for Databricks)

Usage:
    # Run all tests
    python scripts/test_full_workflow.py
    
    # Test only Snowflake
    python scripts/test_full_workflow.py --platform snowflake
    
    # Test only Databricks
    python scripts/test_full_workflow.py --platform databricks
    
    # Cleanup test directories
    python scripts/test_full_workflow.py --cleanup
    
    # Keep test directories after running (for inspection)
    python scripts/test_full_workflow.py --keep
"""

import subprocess
import sys
import os
import shutil
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Final


# =============================================================================
# Configuration
# =============================================================================

# Resolve symlinks to handle macOS /tmp -> /private/tmp
TEST_BASE_DIR: Final[Path] = Path("/tmp/pypeline_workflow_tests").resolve()

# Test project configurations
SNOWFLAKE_PROJECT = {
    "name": "snowflake_etl_project",
    "pipelines": [
        {
            "name": "customer_analytics",
            "processors": ["customer_loader", "customer_transformer", "customer_aggregator"]
        },
        {
            "name": "sales_reporting", 
            "processors": ["sales_extractor", "sales_calculator"]
        },
        {
            "name": "inventory_sync",
            "processors": ["inventory_fetcher"]
        }
    ]
}

DATABRICKS_PROJECT = {
    "name": "databricks_etl_project",
    "pipelines": [
        {
            "name": "data_lake_ingestion",
            "processors": ["raw_data_loader", "schema_validator", "delta_writer"]
        },
        {
            "name": "ml_feature_store",
            "processors": ["feature_extractor", "feature_transformer"]
        },
        {
            "name": "realtime_streaming",
            "processors": ["stream_processor"]
        }
    ]
}

# Expected import patterns for verification
SNOWFLAKE_IMPORTS = [
    r"from snowflake\.snowpark import DataFrame",
    r"from snowflake\.snowpark\.functions import",
    r"snowflake-snowpark-python",  # In dependencies
]

DATABRICKS_IMPORTS = [
    r"from pyspark\.sql import DataFrame",
    r"from pyspark\.sql\.functions import",
    r"pyspark>=",  # In dependencies
]


# =============================================================================
# Helper Functions
# =============================================================================

def get_pypeline_cli() -> str:
    """Get the path to the pypeline CLI."""
    venv_bin = Path(sys.executable).parent
    pypeline_path = venv_bin / "pypeline"
    
    if pypeline_path.exists():
        return str(pypeline_path)
    
    # Fall back to system pypeline
    system_pypeline = shutil.which("pypeline")
    if system_pypeline:
        return system_pypeline
    
    raise FileNotFoundError("pypeline CLI not found in venv or system PATH")


PYPELINE_CLI = get_pypeline_cli()


@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    passed: bool
    message: str


class TestRunner:
    """Manages test execution and reporting."""
    
    def __init__(self):
        self.results: list[TestResult] = []
        self.current_platform: str = ""
    
    def run_command(self, cmd: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess:
        """Run a command with live output or capture."""
        print(f"\n{'─'*60}")
        print(f"🔧 Running: {' '.join(cmd)}")
        print(f"📁 In: {cwd or os.getcwd()}")
        print('─'*60)
        
        if capture:
            result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, cwd=cwd)
        
        if result.returncode != 0:
            print(f"\n❌ Command failed with return code {result.returncode}")
            if capture and result.stderr:
                print(f"stderr: {result.stderr}")
        
        return result
    
    def add_result(self, name: str, passed: bool, message: str = ""):
        """Add a test result."""
        self.results.append(TestResult(name, passed, message))
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"\n{status}: {name}")
        if message:
            print(f"   {message}")
    
    def verify_file_contains(self, file_path: Path, patterns: list[str], description: str) -> bool:
        """Verify that a file contains the expected patterns."""
        if not file_path.exists():
            self.add_result(f"File exists: {file_path.name}", False, f"File not found: {file_path}")
            return False
        
        content = file_path.read_text()
        missing_patterns = []
        
        for pattern in patterns:
            if not re.search(pattern, content):
                missing_patterns.append(pattern)
        
        if missing_patterns:
            self.add_result(
                f"{description} in {file_path.name}",
                False,
                f"Missing patterns: {missing_patterns}"
            )
            return False
        
        self.add_result(f"{description} in {file_path.name}", True)
        return True
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)
        
        print(f"\nTotal Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed > 0:
            print("\n❌ Failed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  • {r.name}")
                    if r.message:
                        print(f"    {r.message}")
        
        print("\n" + "=" * 60)
        return failed == 0


def cleanup():
    """Delete all test directories."""
    if TEST_BASE_DIR.exists():
        print(f"🗑️  Removing test directory: {TEST_BASE_DIR}")
        shutil.rmtree(TEST_BASE_DIR)
        print("✅ Cleanup complete!")
    else:
        print(f"ℹ️  Nothing to clean up - {TEST_BASE_DIR} does not exist")


def print_directory_tree(path: Path, prefix: str = "", max_depth: int = 4, current_depth: int = 0):
    """Print a directory tree structure."""
    if current_depth >= max_depth:
        return
    
    # Skip these directories
    skip_dirs = {'__pycache__', '.venv', '.git', 'node_modules'}
    
    items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        next_prefix = "    " if is_last else "│   "
        
        if item.is_dir():
            if item.name in skip_dirs:
                continue
            print(f"{prefix}{current_prefix}{item.name}/")
            print_directory_tree(item, prefix + next_prefix, max_depth, current_depth + 1)
        else:
            print(f"{prefix}{current_prefix}{item.name}")


# =============================================================================
# Test Functions
# =============================================================================

def test_platform(runner: TestRunner, platform: str, project_config: dict):
    """Test full workflow for a platform."""
    
    print("\n" + "=" * 60)
    print(f"🚀 TESTING {platform.upper()} PLATFORM")
    print("=" * 60)
    
    runner.current_platform = platform
    project_name = project_config["name"]
    project_dir = TEST_BASE_DIR / platform
    project_path = project_dir / project_name
    
    # Clean up existing test project
    if project_dir.exists():
        print(f"🗑️  Removing existing test directory: {project_dir}")
        shutil.rmtree(project_dir)
    
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # Step 1: Initialize Project
    # =========================================================================
    print("\n" + "─" * 60)
    print("📦 STEP 1: Initialize Project")
    print("─" * 60)
    
    result = runner.run_command([
        PYPELINE_CLI, "init",
        "--destination", str(project_dir),
        "--name", project_name,
        "--platform", platform,
        "--author-name", "Test Author",
        "--author-email", "test@example.com",
        "--description", f"Test {platform} ETL project",
        "--license", "MIT",
        "--company-name", "Test Company",
        "--no-git",
    ])
    
    runner.add_result(
        f"[{platform}] Project initialization",
        result.returncode == 0,
        f"Created {project_name}"
    )
    
    if result.returncode != 0:
        print(f"❌ Failed to initialize project, skipping remaining tests for {platform}")
        return
    
    # =========================================================================
    # Step 2: Install Dependencies
    # =========================================================================
    print("\n" + "─" * 60)
    print("📦 STEP 2: Install Dependencies")
    print("─" * 60)
    
    result = runner.run_command(
        [PYPELINE_CLI, "install"],
        cwd=project_path
    )
    
    runner.add_result(
        f"[{platform}] Dependency installation",
        result.returncode == 0
    )
    
    # =========================================================================
    # Step 3: Create Pipelines
    # =========================================================================
    print("\n" + "─" * 60)
    print("📦 STEP 3: Create Pipelines")
    print("─" * 60)
    
    for pipeline_config in project_config["pipelines"]:
        pipeline_name = pipeline_config["name"]
        
        result = runner.run_command(
            [PYPELINE_CLI, "create-pipeline", "--name", pipeline_name],
            cwd=project_path
        )
        
        runner.add_result(
            f"[{platform}] Create pipeline: {pipeline_name}",
            result.returncode == 0
        )
        
        # Verify pipeline folder exists (project structure: project_name/pipelines/...)
        # Resolve paths to handle macOS /tmp -> /private/tmp symlink
        pipeline_folder = (project_path / project_name / "pipelines" / pipeline_name).resolve()
        folder_exists = pipeline_folder.exists()
        runner.add_result(
            f"[{platform}] Pipeline folder exists: {pipeline_name}",
            folder_exists,
            f"Path: {pipeline_folder}" if not folder_exists else ""
        )
    
    # =========================================================================
    # Step 4: Create Processors
    # =========================================================================
    print("\n" + "─" * 60)
    print("📦 STEP 4: Create Processors")
    print("─" * 60)
    
    processor_files: list[Path] = []
    
    for pipeline_config in project_config["pipelines"]:
        pipeline_name = pipeline_config["name"]
        
        for processor_name in pipeline_config["processors"]:
            result = runner.run_command(
                [PYPELINE_CLI, "create-processor", 
                 "--name", processor_name,
                 "--pipeline", pipeline_name],
                cwd=project_path
            )
            
            runner.add_result(
                f"[{platform}] Create processor: {processor_name} in {pipeline_name}",
                result.returncode == 0
            )
            
            # Track processor file for later verification (project structure: project_name/pipelines/...)
            # Resolve paths to handle macOS /tmp -> /private/tmp symlink
            processor_file = (
                project_path / project_name / "pipelines" / pipeline_name / 
                "processors" / f"{processor_name}_processor.py"
            ).resolve()
            processor_files.append(processor_file)
    
    # =========================================================================
    # Step 5: Sync Dependencies
    # =========================================================================
    print("\n" + "─" * 60)
    print("📦 STEP 5: Sync Dependencies")
    print("─" * 60)
    
    result = runner.run_command(
        [PYPELINE_CLI, "sync-deps"],
        cwd=project_path
    )
    
    runner.add_result(
        f"[{platform}] Sync dependencies",
        result.returncode == 0
    )
    
    # =========================================================================
    # Step 6: Verify Platform-Specific Imports
    # =========================================================================
    print("\n" + "─" * 60)
    print("📦 STEP 6: Verify Platform-Specific Imports")
    print("─" * 60)
    
    expected_imports = SNOWFLAKE_IMPORTS if platform == "snowflake" else DATABRICKS_IMPORTS
    unexpected_imports = DATABRICKS_IMPORTS if platform == "snowflake" else SNOWFLAKE_IMPORTS
    
    # Check processor files
    for processor_file in processor_files:
        if processor_file.exists():
            # Verify expected imports are present
            runner.verify_file_contains(
                processor_file,
                expected_imports[:2],  # DataFrame and functions imports
                f"[{platform}] Platform imports"
            )
            
            # Verify unexpected imports are NOT present
            content = processor_file.read_text()
            has_wrong_imports = any(re.search(p, content) for p in unexpected_imports[:2])
            runner.add_result(
                f"[{platform}] No wrong platform imports in {processor_file.name}",
                not has_wrong_imports,
                "Found wrong platform imports" if has_wrong_imports else ""
            )
    
    # Check dependencies file (in project root)
    deps_file = (project_path / "dependencies.py").resolve()
    if deps_file.exists():
        runner.verify_file_contains(
            deps_file,
            [expected_imports[2]],  # pyspark or snowflake-snowpark-python
            f"[{platform}] Platform dependency"
        )
    
    # Check ETL file (in project_name/utils/)
    etl_file = (project_path / project_name / "utils" / "etl.py").resolve()
    if etl_file.exists():
        content = etl_file.read_text()
        
        if platform == "snowflake":
            has_snowpark = "snowflake.snowpark" in content or "SnowflakeSession" in content.replace(" ", "")
            runner.add_result(
                f"[{platform}] ETL has Snowflake/Snowpark references",
                has_snowpark
            )
        else:
            # Databricks uses DatabricksSession from databricks.connect (not pyspark.SparkSession)
            has_databricks = "databricks" in content.lower() or "DatabricksSession" in content or "SparkSession" in content
            runner.add_result(
                f"[{platform}] ETL has Databricks/Spark references",
                has_databricks
            )
    
    # Check decorators file (in project_name/utils/)
    decorators_file = (project_path / project_name / "utils" / "decorators.py").resolve()
    if decorators_file.exists():
        content = decorators_file.read_text()
        
        if platform == "snowflake":
            has_snowpark = "snowflake" in content.lower() or "snowpark" in content.lower()
            runner.add_result(
                f"[{platform}] Decorators has Snowflake references",
                has_snowpark or "DataFrame" in content  # Some decorators may not have platform-specific imports
            )
        else:
            has_pyspark = "pyspark" in content or "spark" in content.lower()
            runner.add_result(
                f"[{platform}] Decorators has PySpark references",
                has_pyspark or "DataFrame" in content
            )
    
    # Check platform-specific utils file
    if platform == "snowflake":
        utils_file = (project_path / project_name / "utils" / "snowflake_utils.py").resolve()
        if utils_file.exists():
            content = utils_file.read_text()
            has_snowpark = "snowflake" in content.lower() or "snowpark" in content.lower()
            runner.add_result(
                f"[{platform}] snowflake_utils.py has Snowflake/Snowpark references",
                has_snowpark
            )
        else:
            runner.add_result(f"[{platform}] snowflake_utils.py exists", False, f"File not found: {utils_file}")
    else:
        utils_file = (project_path / project_name / "utils" / "databricks_utils.py").resolve()
        if utils_file.exists():
            content = utils_file.read_text()
            has_pyspark = "pyspark" in content or "spark" in content.lower() or "unity" in content.lower()
            runner.add_result(
                f"[{platform}] databricks_utils.py has PySpark/Databricks references",
                has_pyspark
            )
        else:
            runner.add_result(f"[{platform}] databricks_utils.py exists", False, f"File not found: {utils_file}")
    
    # Check table_cache.py for platform-specific DataFrame imports
    table_cache_file = (project_path / project_name / "utils" / "table_cache.py").resolve()
    if table_cache_file.exists():
        content = table_cache_file.read_text()
        if platform == "snowflake":
            has_correct_import = "snowflake.snowpark" in content
            runner.add_result(
                f"[{platform}] table_cache.py uses Snowpark DataFrame",
                has_correct_import
            )
        else:
            has_correct_import = "pyspark.sql" in content
            runner.add_result(
                f"[{platform}] table_cache.py uses PySpark DataFrame",
                has_correct_import
            )
    
    # =========================================================================
    # Step 7: Print Project Structure
    # =========================================================================
    print("\n" + "─" * 60)
    print("📂 PROJECT STRUCTURE")
    print("─" * 60)
    print(f"\n{project_path}")
    print_directory_tree(project_path)
    
    # =========================================================================
    # Step 8: Summary for Platform
    # =========================================================================
    print("\n" + "─" * 60)
    print(f"📋 {platform.upper()} PLATFORM SUMMARY")
    print("─" * 60)
    
    total_pipelines = len(project_config["pipelines"])
    total_processors = sum(len(p["processors"]) for p in project_config["pipelines"])
    
    print(f"  • Pipelines created: {total_pipelines}")
    print(f"  • Processors created: {total_processors}")
    print(f"  • Project path: {project_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test pypeline-cli full workflow for Snowflake and Databricks"
    )
    parser.add_argument(
        "--platform", 
        choices=["snowflake", "databricks", "both"],
        default="both",
        help="Platform to test (default: both)"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Delete test directories and exit"
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep test directories after running (for inspection)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("🧪 PYPELINE-CLI FULL WORKFLOW TEST")
    print("=" * 60)
    print(f"\nUsing pypeline CLI: {PYPELINE_CLI}")
    print(f"Test directory: {TEST_BASE_DIR}")
    
    if args.cleanup:
        cleanup()
        return
    
    runner = TestRunner()
    
    try:
        if args.platform in ("snowflake", "both"):
            test_platform(runner, "snowflake", SNOWFLAKE_PROJECT)
        
        if args.platform in ("databricks", "both"):
            test_platform(runner, "databricks", DATABRICKS_PROJECT)
        
        # Print overall summary
        all_passed = runner.print_summary()
        
        if not args.keep:
            print("\n💡 To inspect test projects, run with --keep flag")
            print(f"   Or view them at: {TEST_BASE_DIR}")
        else:
            print(f"\n📂 Test projects preserved at: {TEST_BASE_DIR}")
        
        sys.exit(0 if all_passed else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

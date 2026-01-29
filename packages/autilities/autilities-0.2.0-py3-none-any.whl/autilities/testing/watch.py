import sys
import time
import subprocess
from pathlib import Path
from typing import TypedDict, Unpack, Optional
from parlancy import PackagePath, RelativePath
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class TestRunner(FileSystemEventHandler):
    """Runs tests when Python files change."""

    def __init__(self, test_path: str, src_path: str):
        self.test_path = Path(test_path)
        self.src_path = Path(src_path)
        self.last_run = 0
        self.debounce_seconds = 1

    def on_modified(self, event):
        """Handle file modification events."""

        if event.is_directory:
            return

        if not event.src_path.endswith('.py'):
            return

        current_time = time.time()
        if current_time - self.last_run < self.debounce_seconds:
            return

        self.last_run = current_time
        print(f"\n{'='*80}")
        print(f"File changed: {event.src_path}")
        print(f"{'='*80}\n")
        self.run_tests()

    def run_tests(self):
        """Run pytest on the test directory."""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(self.test_path),
                    "-v",
                    "--tb=short",
                    "--color=yes",
                ],
                cwd=Path.cwd(),
                capture_output=False,
            )
            if result.returncode == 0:
                print(f"\n✓ All tests passed!\n")
            else:
                print(f"\n✗ Some tests failed.\n")
        except Exception as e:
            print(f"Error running tests: {e}")

class TestWatchArgs(TypedDict):
    root: Optional[PackagePath]
    test_path: Optional[RelativePath]
    src_path: Optional[RelativePath]

def watch( **kwargs: Unpack[TestWatchArgs]):
    """Main entry point for the test watcher."""

    package_root = kwargs.get("root", Path(__file__).parent.parent)
    test_path = package_root / kwargs.get("test_path", "tests")
    src_path = package_root / kwargs.get("src_path", "src")

    print(f"Starting autilities test watcher")
    print(f"Watching:")
    print(f"  Package: {package_root}")
    print(f"  Tests: {test_path}")
    print(f"  Source: {src_path}")
    print(f"\nPress Ctrl+C to stop\n")

    runner = TestRunner(str(test_path), str(src_path))
    runner.run_tests()

    observer = Observer()
    observer.schedule(runner, str(test_path), recursive=True)
    observer.schedule(runner, str(src_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping test watcher...")
        observer.stop()
    observer.join()

"""Simple import test for uploadToEventhouse

This test confirms that importing the module doesn't raise at module load
time even when the Azure Kusto packages are not installed. The test asserts
that the EventHouseUploader symbol exists on the module.
"""

def test_import_eventhouse_uploader():
    # Ensure menumover directory is importable during test runs
    import importlib
    import os
    import sys

    tests_dir = os.path.dirname(__file__)
    # Add the project root (parent of menumover) to sys.path so 'menumover' can be imported
    project_root = os.path.dirname(tests_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    mod = importlib.import_module('menumover.uploadToEventhouse')
    assert hasattr(mod, 'EventHouseUploader')
    cls = getattr(mod, 'EventHouseUploader')
    assert callable(cls)

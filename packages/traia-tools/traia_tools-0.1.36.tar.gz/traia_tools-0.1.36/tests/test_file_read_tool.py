import tempfile
import unittest
from pathlib import Path

from traia_tools.tools.file_read_tool.file_read_tool import FileReadTool


class TestFileReadTool(unittest.TestCase):
    def test_schema_only_allows_file_path(self):
        # NOTE: BaseTool (from crewai) is a Pydantic model; class-level access to
        # `args_schema` may not work reliably due to Pydantic's metaclass.
        # Instance access is stable.
        schema = FileReadTool().args_schema

        # The tool should advertise only `file_path` as a valid argument.
        self.assertEqual(set(schema.model_fields.keys()), {"file_path"})

        # The schema may ignore runtime-injected fields (like `security_context`).
        # We enforce "file_path only" at runtime inside `_run()`.
        schema.model_validate({"file_path": "x", "security_context": {"foo": "bar"}})

    def test_reads_default_file_when_provided_in_constructor(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "a.txt"
            path.write_text("hello", encoding="utf-8")

            tool = FileReadTool(file_path=str(path))
            self.assertEqual(tool.run(), "hello")

    def test_runtime_file_path_overrides_constructor_default(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            a = Path(tmp_dir) / "a.txt"
            b = Path(tmp_dir) / "b.txt"
            a.write_text("aaa", encoding="utf-8")
            b.write_text("bbb", encoding="utf-8")

            tool = FileReadTool(file_path=str(a))
            self.assertEqual(tool.run(file_path=str(b)), "bbb")

    def test_errors_when_no_file_path_available(self):
        tool = FileReadTool()
        self.assertIn("No file path provided", tool.run())

    def test_ignores_start_line_and_line_count_and_still_reads(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "a.txt"
            path.write_text("hello\nworld\n", encoding="utf-8")

            tool = FileReadTool()
            # Even if callers pass extra arguments (legacy / framework-injected),
            # we should still read the file as long as `file_path` is present.
            result = tool.run(file_path=str(path), start_line=2, line_count=1)
            self.assertEqual(result, "hello\nworld\n")

    def test_ignores_security_context_and_still_reads(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "a.txt"
            path.write_text("hello", encoding="utf-8")

            tool = FileReadTool()
            result = tool.run(file_path=str(path), security_context={"agent_fingerprint": "x"})
            self.assertEqual(result, "hello")


if __name__ == "__main__":
    unittest.main()


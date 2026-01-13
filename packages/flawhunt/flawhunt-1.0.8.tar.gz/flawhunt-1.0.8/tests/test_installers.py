import os
import sys
import types
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import importlib.util


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def setup_minimal_package(root: Path):
    # Create a minimal ai_terminal package to satisfy relative imports without executing __init__.py
    pkg = types.ModuleType('ai_terminal')
    pkg.__path__ = [str(root / 'ai_terminal')]
    sys.modules['ai_terminal'] = pkg

    # Inject a minimal langchain.tools.BaseTool to satisfy tools.py
    langchain_module = types.ModuleType('langchain')
    tools_submodule = types.ModuleType('langchain.tools')
    class DummyBaseTool:
        pass
    tools_submodule.BaseTool = DummyBaseTool
    langchain_module.tools = tools_submodule
    sys.modules['langchain'] = langchain_module
    sys.modules['langchain.tools'] = tools_submodule

    # Load ai_terminal.utils first
    load_module('ai_terminal.utils', root / 'ai_terminal' / 'utils.py')
    # Then load ai_terminal.tools
    tools_mod = load_module('ai_terminal.tools', root / 'ai_terminal' / 'tools.py')
    return tools_mod


class TestInstallersAndManager(unittest.TestCase):
    def setUp(self):
        # Temporary HOME to avoid writing to real user directories
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_home = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_package_manager_install_skip_and_retry(self):
        project_root = Path(__file__).resolve().parents[1]
        tools_mod = setup_minimal_package(project_root)
        PackageManagerTool = tools_mod.PackageManagerTool

        # Track calls
        call_state = {"apt_install_calls": 0, "apt_update_calls": 0}

        def fake_run(cmd, timeout=60):
            cmd_str = cmd if isinstance(cmd, str) else "".join(cmd)
            # Already installed check
            if cmd_str.startswith("dpkg -s curl"):
                return "Status: install ok installed\n"
            # Attempt install (first failure then success)
            if cmd_str.startswith("sudo apt-get install"):
                call_state["apt_install_calls"] += 1
                if call_state["apt_install_calls"] == 1:
                    return "E: Unable to locate package curl"
                return "curl installed successfully"
            # Update cache
            if cmd_str.startswith("sudo apt-get update"):
                call_state["apt_update_calls"] += 1
                return "Hit:1 http://archive.ubuntu.com"
            return ""

        with patch('ai_terminal.tools.run_subprocess', side_effect=fake_run):
            tool = PackageManagerTool(auto_install=True)
            # Skip path
            msg_skip = tool._install_package("apt", "curl")
            self.assertIn("already installed", msg_skip.lower())

            # Force not-installed path by making _is_installed return False
            with patch('ai_terminal.tools.PackageManagerTool._is_installed', return_value=False):
                msg_install = tool._install_package("apt", "curl")
                self.assertIn("successfully installed", msg_install.lower())
                self.assertEqual(call_state["apt_update_calls"], 1)

    def test_python_package_manager_skip_and_install(self):
        project_root = Path(__file__).resolve().parents[1]
        tools_mod = setup_minimal_package(project_root)
        PythonPackageManagerTool = tools_mod.PythonPackageManagerTool

        # Stub rich modules used inside the tool
        rich_module = types.ModuleType('rich')
        console_sub = types.ModuleType('rich.console')
        class DummyConsole:
            def print(self, *args, **kwargs):
                pass
        console_sub.Console = DummyConsole
        prompt_sub = types.ModuleType('rich.prompt')
        class DummyConfirm:
            @staticmethod
            def ask(*args, **kwargs):
                return True
        prompt_sub.Confirm = DummyConfirm
        sys.modules['rich'] = rich_module
        sys.modules['rich.console'] = console_sub
        sys.modules['rich.prompt'] = prompt_sub

        def fake_run(cmd, timeout=60):
            if "pip show requests" in cmd:
                return "Name: requests\nVersion: 2.31.0\n"
            if "pip install" in cmd:
                return "Successfully installed requests"
            if cmd.startswith("pip list"):
                return "requests 2.31.0"
            return ""

        with patch('ai_terminal.tools.run_subprocess', side_effect=fake_run):
            tool = PythonPackageManagerTool()
            # Skip when already present
            msg_skip = tool._run("install requests")
            self.assertIn("already installed", msg_skip.lower())

            # Now simulate not present, then install success
            def fake_run2(cmd, timeout=60):
                if "pip show requests" in cmd:
                    return ""  # not installed
                if "pip install" in cmd:
                    return "Successfully installed requests"
                return ""
            with patch('ai_terminal.tools.run_subprocess', side_effect=fake_run2):
                msg_installed = tool._run("install requests")
                self.assertIn("successfully installed", msg_installed.lower())

    def test_cybersec_manager_deps_and_go_install(self):
        project_root = Path(__file__).resolve().parents[1]
        tools_mod = setup_minimal_package(project_root)
        CyberSecurityToolManager = tools_mod.CyberSecurityToolManager
        # Patch HOME for manager files
        with patch('ai_terminal.tools.Path.home', return_value=self.tmp_home):
            
            # Dependency checks
            def fake_run(cmd, timeout=60):
                if "pkg-config --exists libpcap" in cmd:
                    return "OK\n"
                if "openssl version" in cmd:
                    return "OpenSSL 3.0.0\n"
                return ""

            def fake_which(binary):
                # Simulate typical binaries present
                present = {
                    "ruby": "/usr/bin/ruby",
                    "java": "/usr/bin/java",
                    "python3": "/usr/bin/python3",
                    "pip3": "/usr/bin/pip3",
                    "perl": "/usr/bin/perl",
                    "go": "/usr/bin/go",
                    "psql": "/usr/bin/psql",
                }
                return present.get(binary)

            with patch('ai_terminal.tools.run_subprocess', side_effect=fake_run), \
                 patch('ai_terminal.utils.shutil_which', side_effect=fake_which):
                mgr = CyberSecurityToolManager()
                deps = mgr._check_dependencies('nmap')
                self.assertTrue(deps.get('libpcap'))

            # Test go-based tool install path handling
            with patch('ai_terminal.tools.run_subprocess', return_value="installed"), \
                 patch('ai_terminal.utils.shutil_which', side_effect=lambda b: None if b == 'go' else None):
                mgr = CyberSecurityToolManager()
                msg = mgr._install_tool('gobuster')
                self.assertIn("required to install", msg.lower())

            # Simulate successful go install with binary in ~/go/bin
            gobin = self.tmp_home / "go" / "bin"
            gobin.mkdir(parents=True, exist_ok=True)
            (gobin / "gobuster").write_text("")
            with patch('ai_terminal.tools.run_subprocess', return_value="installed"), \
                 patch('ai_terminal.utils.shutil_which', side_effect=lambda b: "/usr/bin/go" if b == 'go' else None):
                mgr = CyberSecurityToolManager()
                msg2 = mgr._install_tool('gobuster')
                self.assertNotIn("installation failed", msg2.lower())


if __name__ == '__main__':
    unittest.main()
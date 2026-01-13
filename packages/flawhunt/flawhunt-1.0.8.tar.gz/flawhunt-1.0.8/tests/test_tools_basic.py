import sys
import types
from pathlib import Path
import unittest
from unittest.mock import patch, mock_open
import importlib.util


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def setup_minimal_package(root: Path):
    pkg = types.ModuleType('ai_terminal')
    pkg.__path__ = [str(root / 'ai_terminal')]
    sys.modules['ai_terminal'] = pkg

    # Minimal BaseTool
    langchain_module = types.ModuleType('langchain')
    tools_submodule = types.ModuleType('langchain.tools')
    class DummyBaseTool:
        pass
    tools_submodule.BaseTool = DummyBaseTool
    langchain_module.tools = tools_submodule
    sys.modules['langchain'] = langchain_module
    sys.modules['langchain.tools'] = tools_submodule

    # Load utils then tools
    load_module('ai_terminal.utils', root / 'ai_terminal' / 'utils.py')
    tools_mod = load_module('ai_terminal.tools', root / 'ai_terminal' / 'tools.py')
    return tools_mod


class TestToolsBasic(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.tools_mod = setup_minimal_package(self.root)

    def test_get_install_command_mac_linux_distros(self):
        mgr_cls = self.tools_mod.CyberSecurityToolManager
        with patch('ai_terminal.tools.get_platform_info', return_value={'system': 'darwin'}):
            mgr = mgr_cls()
            cmd = mgr._get_install_command('nmap')
            self.assertIn('brew install --quiet nmap', cmd)

        # Ubuntu/Debian
        debian_content = 'NAME=Ubuntu\nVERSION=22.04\nID=ubuntu\n'
        with patch('ai_terminal.tools.get_platform_info', return_value={'system': 'linux'}), \
             patch('builtins.open', mock_open(read_data=debian_content)):
            mgr = mgr_cls()
            cmd = mgr._get_install_command('nmap')
            self.assertIn('apt-get install -y --no-install-recommends nmap', cmd)

        # Fedora/RHEL/CentOS
        fedora_content = 'NAME=Fedora\nID=fedora\n'
        with patch('ai_terminal.tools.get_platform_info', return_value={'system': 'linux'}), \
             patch('builtins.open', mock_open(read_data=fedora_content)):
            mgr = mgr_cls()
            cmd = mgr._get_install_command('nmap')
            self.assertIn('yum install -y nmap', cmd)

        # Arch
        arch_content = 'NAME=Arch Linux\nID=arch\n'
        with patch('ai_terminal.tools.get_platform_info', return_value={'system': 'linux'}), \
             patch('builtins.open', mock_open(read_data=arch_content)):
            mgr = mgr_cls()
            cmd = mgr._get_install_command('nmap')
            self.assertIn('pacman -S --noconfirm nmap', cmd)

    def test_register_existing_tool_updates_db(self):
        mgr_cls = self.tools_mod.CyberSecurityToolManager
        # Patch HOME to a temp dir
        tmp_home = Path(self.root) / '.tmp_test_home'
        tmp_home.mkdir(exist_ok=True)
        with patch('ai_terminal.tools.Path.home', return_value=tmp_home), \
             patch.object(mgr_cls, '_parse_tool_manual', return_value='Usage: nmap ...'), \
             patch.object(mgr_cls, '_extract_tool_knowledge', return_value={'usage_examples': ['nmap -sV'] }):
            mgr = mgr_cls()
            msg = mgr._register_existing_tool('nmap', '/usr/bin/nmap')
            self.assertIn('Successfully registered existing tool', msg)
            self.assertIn('nmap', mgr.tools_db['installed_tools'])
            self.assertTrue(mgr.tools_db['installed_tools']['nmap']['manual_parsed'])


if __name__ == '__main__':
    unittest.main()
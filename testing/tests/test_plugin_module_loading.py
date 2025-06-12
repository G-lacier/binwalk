import os
import textwrap
import binwalk.core.plugin as plugin
import binwalk.core.module as module


def test_user_plugin_loading(tmp_path, monkeypatch):
    plugin_dir = tmp_path / "binwalk" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "dummy.py"
    plugin_file.write_text(textwrap.dedent(
        """
        import binwalk.core.plugin
        class Plugin(binwalk.core.plugin.Plugin):
            \"\"\"Dummy plugin\"\"\"
            def init(self):
                self.module.loaded = True
        """
    ))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    parent = type("Dummy", (), {})()
    p = plugin.Plugins(parent=parent)
    info = p.list_plugins()
    assert "dummy" in info['user']['modules']
    p.load_plugins()
    assert getattr(parent, "loaded", False)


def test_user_module_discovery(tmp_path, monkeypatch):
    mod_dir = tmp_path / "binwalk" / "modules"
    mod_dir.mkdir(parents=True)
    mod_file = mod_dir / "mymod.py"
    mod_file.write_text(textwrap.dedent(
        """
        class Dummy(object):
            PRIORITY = 1
            def run(self):
                pass
        """
    ))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    m = module.Modules()
    result = m.list("run")
    names = [cls.__name__ for cls in result]
    assert "Dummy" in names


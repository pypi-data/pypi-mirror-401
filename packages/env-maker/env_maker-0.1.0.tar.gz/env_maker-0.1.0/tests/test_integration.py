import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath("src"))

from env_maker.main import main
from env_maker import utils

# Mock args
class Args:
    pass

def test_integration():
    # consistent cleanup
    files = ['.env.test', '.env.example', '.env.json']
    for f in files:
        if os.path.exists(f):
            os.remove(f)

    # Create dummy .env
    with open('.env.test', 'w') as f:
        f.write("# This is a comment\n")
        f.write("FOO=bar\n")
        f.write("\n")
        f.write("BAZ=qux\n")

    print("Running example creation test...")
    # Simulate CLI call for example
    sys.argv = ['env-maker', '.env.test', '.env.example']
    main()
    
    with open('.env.example', 'r') as f:
        content = f.read()
        print("Output .env.example:\n" + content)
        assert "FOO=XXXX" in content
        assert "BAZ=XXXX" in content
        assert "# This is a comment" in content

    print("\nRunning JSON conversion test...")
    try:
        import yaml
        import tomli_w
    except ImportError:
        print("Skipping conversion tests because dependencies (PyYAML, tomli-w) are missing.")
        return

    sys.argv = ['env-maker', '.env.test', '.env.json', '--indent', '2']
    main()
    
    with open('.env.json', 'r') as f:
        content = f.read()
        print("Output .env.json:\n" + content)
        assert '"FOO": "bar"' in content
        assert '"BAZ": "qux"' in content

    print("\nTests passed!")

    # Cleanup
    for f in files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    test_integration()

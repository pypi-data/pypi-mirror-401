from pathlib import Path
from io import StringIO
import sys

p = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(p))

from mauztoolslib.pllib import java_to_python

def test_java_to_python():
    java_code = """
    public class Test {
        public static void main(String[] args) {
            int x = 5;
            boolean flag = true;
            if (x > 0) {
                System.out.println("Positive");
            } else if (x < 0) {
                System.out.println("Negative");
            } else {
                System.out.println("Zero");
            }

            for (int i = 0; i < 3; i++) {
                System.out.println(i);
            }

            while (flag) {
                flag = false;
            }
        }

        public void greet(String name) {
            System.out.println("Hello " + name);
        }
    }
    """

    print("=== Original Java-Code ===")
    print(java_code)

    python_code = java_to_python(java_code)

    print("\n=== Konvertierter Python-Code ===")
    print(python_code)
    
# Test starten
if __name__ == "__main__":
    test_java_to_python()

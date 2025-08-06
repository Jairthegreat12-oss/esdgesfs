import os

# --- Configuration ---
# WARNING: A high length_factor (e.g., > 10000) will create VERY large files 
# and may take a long time to run. Start with a small number like 100.
LENGTH_FACTOR = 5000 
OUTPUT_DIRECTORY = "longest_code_generated"

# --- Helper Function ---
def create_output_directory():
    """Create the directory to store the generated code files."""
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        print(f"Created directory: {OUTPUT_DIRECTORY}")

# --- Generator for Java ---
def generate_java_code():
    """
    Generates a Java file with deeply nested if-else statements.
    This creates structural length and complexity. The JVM has limits on method size,
    so this will eventually fail to compile, which is part of the concept.
    """
    filename = os.path.join(OUTPUT_DIRECTORY, "TheLongestJavaClass.java")
    print("Generating absurdly long Java code...")
    with open(filename, 'w') as f:
        f.write("public class TheLongestJavaClass {\n")
        f.write("    public static void main(String[] args) {\n")
        f.write("        long startTime = System.nanoTime();\n")
        f.write("        int x = 0;\n")

        # Create deeply nested if statements
        for i in range(LENGTH_FACTOR):
            indent = ' ' * (8 + i * 4)
            f.write(f"{indent}if (x == {i}) {{\n")
            f.write(f"{indent}    // Level {i + 1}\n")

        # Close all the braces
        for i in range(LENGTH_FACTOR):
            indent = ' ' * (8 + (LENGTH_FACTOR - 1 - i) * 4)
            f.write(f"{indent}}}\n")

        f.write("        long endTime = System.nanoTime();\n")
        f.write("        long duration = (endTime - startTime) / 1000000; // milliseconds\n")
        f.write(f"        System.out.println(\"Navigated {LENGTH_FACTOR} nested ifs.\");\n")
        f.write("        System.out.println(\"Execution time: \" + duration + \" ms.\");\n")
        f.write("    }\n")
        f.write("}\n")
    print(f"Generated {filename}")

# --- Generator for JavaScript ---
def generate_javascript_code():
    """
    Generates a JavaScript file with a massively long, deeply nested array.
    Accessing an element deep inside this structure would be a challenge.
    """
    filename = os.path.join(OUTPUT_DIRECTORY, "longest_array.js")
    print("Generating absurdly long JavaScript code...")
    with open(filename, 'w') as f:
        f.write("// A structurally very long JavaScript file.\n")
        f.write("console.log('Starting to build the colossal array...');\n\n")
        
        f.write("let deepestArray = ['The Core'];\n")
        
        # Nest the array inside itself thousands of times
        for i in range(LENGTH_FACTOR):
            f.write(f"deepestArray = [deepestArray, 'Layer {i+1}'];\n")
            if (i+1) % 1000 == 0:
                f.write(f"console.log('Constructed layer {i+1}...');\n")

        f.write("\nconsole.log('Colossal array construction complete.');\n")
        f.write("console.log(`Total depth: {LENGTH_FACTOR}`);\n")
        f.write("console.log('To access the core, you would need ' + " + str(LENGTH_FACTOR) + " + ' sets of [0]');\n")
        
        # Create the accessor string dynamically
        accessor = ''.join(['[0]' for _ in range(LENGTH_FACTOR)])
        f.write(f"// Example: console.log(deepestArray{accessor}[0]);\n")
        f.write("console.log('Successfully created the longest JavaScript array literal program.');\n")
    print(f"Generated {filename}")

# --- Generator for C++ ---
def generate_cpp_code():
    """
    Generates C++ code that uses template metaprogramming to calculate a value
    at compile time. This creates an absurdly long type name and forces the compiler
    to work extremely hard, making the "code" long in terms of compile-time processing.
    """
    filename = os.path.join(OUTPUT_DIRECTORY, "longest_compile.cpp")
    print("Generating absurdly long C++ code...")
    with open(filename, 'w') as f:
        f.write("#include <iostream>\n")
        f.write("#include <chrono>\n\n")
        f.write("// This code is long in terms of compile-time work and type name length.\n")
        f.write("// It computes a value using recursive templates.\n\n")

        f.write("template<int N>\n")
        f.write("struct LongestTypeName {\n")
        f.write("    static const long long value = 1 + LongestTypeName<N - 1>::value;\n")
        f.write("};\n\n")

        f.write("template<>\n")
        f.write("struct LongestTypeName<0> {\n")
        f.write("    static const long long value = 1;\n")
        f.write("};\n\n")

        f.write("int main() {\n")
        f.write("    auto start = std::chrono::high_resolution_clock::now();\n\n")
        f.write("    // The type of 'result' is extremely long, e.g., LongestTypeName<...<LongestTypeName<0>>...>\n")
        f.write(f"    long long result = LongestTypeName<{LENGTH_FACTOR}>::value;\n\n")
        
        f.write("    auto stop = std::chrono::high_resolution_clock::now();\n")
        f.write("    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);\n\n")
        
        f.write("    std::cout << \"This program forced the C++ compiler to instantiate {LENGTH_FACTOR} templates.\" << std::endl;\n")
        f.write("    std::cout << \"Calculated Value: \" << result << std::endl;\n")
        f.write("    std::cout << \"Runtime Execution took: \" << duration.count() << \" ms (most work was at compile time).\" << std::endl;\n")
        
        f.write("    return 0;\n")
        f.write("}\n")
    print(f"Generated {filename}")

# --- Main Execution ---
if __name__ == "__main__":
    print("--- The Ultimate Code Generator ---")
    print(f"Using a Length Factor of: {LENGTH_FACTOR}\n")
    create_output_directory()
    print("-" * 20)
    
    generate_java_code()
    print("-" * 20)
    
    generate_javascript_code()
    print("-" * 20)
    
    generate_cpp_code()
    print("-" * 20)
    
    print("\nAll long source code files have been generated successfully!")
    print(f"Check the '{OUTPUT_DIRECTORY}' directory.")


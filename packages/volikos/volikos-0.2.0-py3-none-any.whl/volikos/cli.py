import click
import json
import subprocess
import os
import sys
import warnings
from .lexer import Lexer
from .parser import Parser
from .codegen import CodeGen

MANIFEST_NAME = "vlk.json"

def load_manifest():
    """Attempts to load the manifest file from the current directory."""
    if not os.path.exists(MANIFEST_NAME):
        return {}
    try:
        with open(MANIFEST_NAME, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        click.secho(f"Error: {MANIFEST_NAME} is invalid JSON.", fg='red')
        sys.exit(1)

def resolve_config(filename_arg, target_arg, verbose_arg):
    """
    Combines CLI arguments with Manifest defaults.
    Returns (entry_file, target, verbose)
    """
    manifest = load_manifest()
    
    # 1. Resolve Entry File
    entry = filename_arg
    if not entry:
        entry = manifest.get("entry")
    
    if not entry:
        click.secho("Error: No file specified and no 'vlk.json' entry found.", fg='red')
        sys.exit(1)

    # 2. Resolve Target
    target = target_arg
    if not target:
        target = manifest.get("target", "native") # Default to host architecture

    # 3. Resolve Verbose
    verbose = verbose_arg
    if not verbose and manifest.get("verbose", False):
        verbose = True

    return entry, target, verbose

def get_ast(source_code, verbose=False):
    """Parses source code into an AST, optionally silencing warnings."""
    
    # Rply emits warnings during parser generation. We silence them unless verbose is True.
    with warnings.catch_warnings():
        if not verbose:
            warnings.filterwarnings("ignore", category=Warning, module="rply")
        
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(source_code)
        parser = Parser()
        pg = parser.parse() # This triggers the build() warnings
        return pg.parse(tokens)

@click.group()
def cli():
    """Volikos Compiler CLI"""
    pass

@cli.command()
def init():
    """Initialize a new Volikos project interactively."""
    click.secho("Initializing new Volikos project...", fg='cyan', bold=True)
    
    project_name = click.prompt("Project Name", default=os.path.basename(os.getcwd()))
    version = click.prompt("Version", default="0.1.0")
    entry_file = click.prompt("Entrypoint File", default="main.vlk")
    target = click.prompt("Default Target", default="native")
    
    manifest_data = {
        "name": project_name,
        "version": version,
        "entry": entry_file,
        "target": target,
        "verbose": False
    }
    
    if os.path.exists(MANIFEST_NAME):
        if not click.confirm(f"{MANIFEST_NAME} already exists. Overwrite?"):
            click.echo("Aborted.")
            return

    with open(MANIFEST_NAME, 'w') as f:
        json.dump(manifest_data, f, indent=4)
    
    if not os.path.exists(entry_file):
        with open(entry_file, 'w') as f:
            f.write(f"# {project_name} v{version}\n")
            f.write("func main() {\n")
            f.write('    print("Hello, Volikos!");\n')
            f.write("}\n")
        click.secho(f"Created {entry_file}", fg='green')
    
    click.secho(f"Success! Project '{project_name}' initialized.", fg='green', bold=True)

@cli.command()
@click.argument('filename', required=False)
@click.option('--verbose', is_flag=True, help="Show compiler warnings")
def check(filename, verbose):
    """Check syntax errors."""
    target_file, _, is_verbose = resolve_config(filename, None, verbose)
    
    try:
        with open(target_file, 'r') as f:
            code = f.read()
        get_ast(code, is_verbose)
        click.secho(f"Syntax OK: {target_file} \u2713", fg='green')
    except FileNotFoundError:
        click.secho(f"Error: File '{target_file}' not found.", fg='red')
    except Exception as e:
        click.secho(f"Syntax Error: {e}", fg='red')

@cli.command()
@click.argument('filename', required=False)
@click.option('--out', default='output.ll', help='Output IR file name')
@click.option('--target', default=None, help='Compilation target (e.g., wasm32)')
@click.option('--verbose', is_flag=True, help="Show compiler warnings")
def gen(filename, out, target, verbose):
    """Generate LLVM IR."""
    target_file, target_triple, is_verbose = resolve_config(filename, target, verbose)

    try:
        with open(target_file, 'r') as f:
            code = f.read()
            
        ast = get_ast(code, is_verbose)
        codegen = CodeGen(target_triple) # Pass target to codegen
        codegen.generate(ast)
        
        with open(out, 'w') as f:
            f.write(str(codegen.module))
            
        click.secho(f"Generated LLVM IR: {out} ({target_triple})", fg='green')
    except Exception as e:
        click.secho(f"Codegen Error: {e}", fg='red')

def _build_process(target_file, out_name, target_triple, is_verbose):
    """Shared build logic for 'build' and 'run'."""
    ir_file = f"{out_name}.ll"
    
    # 1. Generate IR
    click.echo(f"Compiling {target_file} for {target_triple}...")
    try:
        with open(target_file, 'r') as f:
            code = f.read()
        ast = get_ast(code, is_verbose)
        codegen = CodeGen(target_triple)
        codegen.generate(ast)
        with open(ir_file, 'w') as f:
            f.write(str(codegen.module))
    except Exception as e:
        click.secho(f"Codegen failed: {e}", fg='red')
        return False

    # 2. Invoke Clang
    clang_args = ["clang", ir_file, "-o", out_name, "-Wno-override-module"]
    
    # Handle Targets
    if target_triple != "native":
        clang_args.append(f"--target={target_triple}")
        # WASM specific handling (simplified)
        if "wasm" in target_triple:
             clang_args += ["-nostdlib", "-Wl,--no-entry", "-Wl,--export-all"]

    if is_verbose:
        click.echo(f"Running: {' '.join(clang_args)}")

    try:
        subprocess.run(clang_args, check=True)
        return True
    except FileNotFoundError:
        click.secho("Error: 'clang' not found. Please install LLVM/Clang.", fg='red')
    except subprocess.CalledProcessError:
        click.secho("Error: Clang failed to compile.", fg='red')
    finally:
        if os.path.exists(ir_file):
            os.remove(ir_file)
    return False

@cli.command()
@click.argument('filename', required=False)
@click.option('--out', default=None, help='Output binary name')
@click.option('--target', default=None, help='Compilation target')
@click.option('--verbose', is_flag=True, help="Show compiler warnings")
@click.option('--force', is_flag=True, help="Overwrite existing binary without asking")
def build(filename, out, target, verbose, force):
    """Compile to executable."""
    target_file, target_triple, is_verbose = resolve_config(filename, target, verbose)
    
    if out is None:
        manifest = load_manifest()
        out = manifest.get("name", "program")
        if target_triple and "wasm" in target_triple:
            out += ".wasm"

    # Overwrite check
    if os.path.exists(out) and not force:
        if not click.confirm(f"Binary '{out}' already exists. Overwrite?"):
            click.echo("Build aborted.")
            return

    if _build_process(target_file, out, target_triple, is_verbose):
        click.secho(f"Build Successful! \u2713 -> ./{out}", fg='green', bold=True)

@cli.command()
@click.argument('filename', required=False)
@click.option('--target', default=None, help='Compilation target')
@click.option('--verbose', is_flag=True, help="Show compiler warnings")
def run(filename, target, verbose):
    """Build and run the program."""
    target_file, target_triple, is_verbose = resolve_config(filename, target, verbose)
    
    # Temp output name
    out_name = "volikos_run_temp" 
    if os.path.exists(out_name):
         if not click.confirm(f"Temporary file '{out_name}' exists. Overwrite?"):
            return

    if _build_process(target_file, out_name, target_triple, is_verbose):
        click.secho(f"Running ./{out_name}...", fg='cyan')
        click.echo("---")
        try:
            # If WASM, we can't just ./run it easily without a runtime like wasmtime
            if "wasm" in target_triple:
                click.secho("Note: WASM files cannot be executed directly. Use a runtime like 'wasmtime'.", fg='yellow')
            else:
                subprocess.run([f"./{out_name}"])
        except Exception as e:
            click.secho(f"Execution failed: {e}", fg='red')
        finally:
            if os.path.exists(out_name):
                os.remove(out_name)

if __name__ == '__main__':
    cli()
#!/usr/bin/env python3
"""
waygrounddocgen - CLI tool for generating documentation using Cursor AI

A language-agnostic documentation generator that uses Cursor CLI to:
1. Discover logical modules/components in any repository
2. Generate documentation for each module in parallel

Usage:
    waygrounddocgen discover /path/to/repo              # Discover modules
    waygrounddocgen generate /path/to/repo              # Full pipeline
    waygrounddocgen generate /path/to/repo --parallel 4 # With parallelism
    waygrounddocgen generate --modules modules.json     # From existing discovery

Requirements:
    - Cursor CLI installed and available in PATH
    - cursor command available (install from Cursor settings)
"""

import argparse
import fcntl
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from importlib.resources import files
except ImportError:
    # Python < 3.9 fallback
    from importlib_resources import files


def get_prompts_dir() -> Path:
    """Get the path to the prompts directory within the package."""
    return files("waygrounddocgen") / "prompts"


class CursorCLI:
    """Wrapper for Cursor CLI operations."""
    
    # Possible command names for Cursor CLI
    CURSOR_COMMANDS = ["cursor", "cursor-agent"]
    _detected_command = None
    
    @classmethod
    def get_command(cls) -> Optional[str]:
        """Find the available cursor CLI command."""
        if cls._detected_command:
            return cls._detected_command
        
        for cmd in cls.CURSOR_COMMANDS:
            try:
                result = subprocess.run(
                    [cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    cls._detected_command = cmd
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        return None
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if cursor CLI is available."""
        return cls.get_command() is not None
    
    @classmethod
    def is_logged_in(cls) -> bool:
        """Check if user is logged into cursor-agent."""
        cmd = cls.get_command()
        if not cmd:
            return False
        
        try:
            result = subprocess.run(
                [cmd, "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
            return "Not logged in" not in output and "logged in" in output.lower()
        except:
            return False
    
    @classmethod
    def get_login_status(cls) -> str:
        """Get detailed login status."""
        cmd = cls.get_command()
        if not cmd:
            return "CLI not found"
        
        try:
            result = subprocess.run(
                [cmd, "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip() or result.stderr.strip()
        except Exception as e:
            return f"Error: {e}"
    
    @classmethod
    def run_prompt(cls, prompt: str, working_dir: str, timeout: int = 600, stream: bool = True, debug: bool = False) -> dict:
        """
        Run a prompt using Cursor CLI (cursor-agent).
        
        Args:
            prompt: The prompt text to send to Cursor
            working_dir: Working directory for the command
            timeout: Timeout in seconds
            stream: If True, stream output in real-time
            
        Returns:
            dict with 'success', 'output', 'error' keys
        """
        cursor_cmd = cls.get_command()
        if not cursor_cmd:
            return {
                "success": False,
                "output": "",
                "error": "Cursor CLI not found"
            }
        
        try:
            # cursor-agent syntax: cursor-agent --print --workspace <path> "prompt"
            cmd = [
                cursor_cmd,
                "--print",
                "--workspace", working_dir,
                prompt
            ]
            
            if debug:
                print("\n🔧 DEBUG: Running command:")
                print(f"   {cursor_cmd} --print --workspace {working_dir} \"<prompt>\"")
                print(f"   Prompt length: {len(prompt)} chars")
                print(f"   Timeout: {timeout}s")
                print()
            
            if stream:
                # Stream output in real-time
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.DEVNULL,  # Prevent waiting for stdin
                    text=True,
                    cwd=working_dir,
                    bufsize=0  # Unbuffered
                )
                
                output_chars = []
                stderr_chars = []
                
                print("\n" + "─" * 60)
                print("🤖 Cursor AI thinking...")
                print("─" * 60 + "\n", flush=True)
                
                # Track if we've received any output
                has_output = False
                spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
                spinner_idx = 0
                last_spinner_time = time.time()
                start_time = time.time()
                
                # Use select for non-blocking read
                while True:
                    # Check if process is done
                    return_code = process.poll()
                    
                    # Try to read from stdout
                    try:
                        # Set stdout to non-blocking
                        fd = process.stdout.fileno()
                        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                        
                        try:
                            chunk = process.stdout.read(1024)
                            if chunk is not None and chunk:
                                has_output = True
                                print(chunk, end='', flush=True)
                                output_chars.append(chunk)
                        except (IOError, BlockingIOError, TypeError):
                            pass
                        
                        # Also read stderr
                        fd_err = process.stderr.fileno()
                        fl_err = fcntl.fcntl(fd_err, fcntl.F_GETFL)
                        fcntl.fcntl(fd_err, fcntl.F_SETFL, fl_err | os.O_NONBLOCK)
                        
                        try:
                            err_chunk = process.stderr.read(1024)
                            if err_chunk is not None and err_chunk:
                                print(f"\033[33m{err_chunk}\033[0m", end='', flush=True)
                                stderr_chars.append(err_chunk)
                        except (IOError, BlockingIOError, TypeError):
                            pass
                            
                    except Exception:
                        pass
                    
                    # Show spinner with elapsed time
                    current_time = time.time()
                    elapsed = int(current_time - start_time)
                    if current_time - last_spinner_time > 0.2:
                        if has_output:
                            # Just show elapsed time on a new line occasionally
                            pass
                        else:
                            print(f"\r{spinner[spinner_idx]} Waiting for response... ({elapsed}s elapsed)    ", end='', flush=True)
                        spinner_idx = (spinner_idx + 1) % len(spinner)
                        last_spinner_time = current_time
                    
                    # If process is done and no more output, break
                    if return_code is not None:
                        # Read any remaining output
                        try:
                            remaining = process.stdout.read()
                            if remaining is not None and remaining:
                                print(remaining, end='', flush=True)
                                output_chars.append(remaining)
                        except:
                            pass
                        break
                    
                    time.sleep(0.05)  # Small delay to prevent CPU spin
                
                if not has_output:
                    print("\r" + " " * 30 + "\r", end='')  # Clear spinner line
                
                print("\n" + "─" * 60 + "\n")
                
                output = ''.join(output_chars)
                stderr = ''.join(stderr_chars)
                
                if return_code == 0:
                    return {
                        "success": True,
                        "output": output,
                        "error": None
                    }
                else:
                    return {
                        "success": False,
                        "output": output,
                        "error": stderr or f"Exit code: {return_code}"
                    }
            else:
                # Capture output without streaming
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=working_dir
                )
                
                if result.returncode == 0:
                    return {
                        "success": True,
                        "output": result.stdout,
                        "error": None
                    }
                else:
                    return {
                        "success": False,
                        "output": result.stdout,
                        "error": result.stderr or f"Exit code: {result.returncode}"
                    }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"Timeout after {timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }


class PromptLoader:
    """Loads prompt templates from files."""
    
    def __init__(self, prompts_dir: Path = None):
        self.prompts_dir = prompts_dir or get_prompts_dir()
    
    def load(self, prompt_name: str) -> str:
        """Load a prompt template by name."""
        prompt_file = self.prompts_dir / f"{prompt_name}.md"
        # Handle both Path and Traversable objects from importlib.resources
        if hasattr(prompt_file, 'read_text'):
            return prompt_file.read_text(encoding='utf-8')
        else:
            # Fallback for regular Path objects
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
    
    def render(self, prompt_name: str, **kwargs) -> str:
        """Load and render a prompt template with variables."""
        template = self.load(prompt_name)
        for key, value in kwargs.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template


def discover_modules(repo_path: str, output_file: Optional[str] = None, stream: bool = True, debug: bool = False) -> dict:
    """
    Run Cursor to discover modules/components in the repository.
    
    Args:
        repo_path: Path to the repository
        output_file: Optional file to save results
        stream: If True, show Cursor's thinking in real-time
        debug: If True, show debug information
        
    Returns:
        dict with discovered modules
    """
    # Check login status first
    if not CursorCLI.is_logged_in():
        cmd = CursorCLI.get_command()
        print("❌ Not logged in to Cursor")
        print(f"   Run: {cmd} login")
        return {"modules": [], "error": "Not logged in"}
    
    print("🔍 Discovering modules using Cursor AI...")
    print(f"   Repository: {repo_path}")
    
    loader = PromptLoader()
    prompt = loader.render("discover", REPO_PATH=repo_path)
    
    # For discovery, write to a non-hidden directory (cursor-agent can't write to hidden dirs)
    output_path = output_file or str(Path(repo_path) / "docs" / "modules.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Modify prompt to include output instructions
    prompt += f"\n\nSave the JSON output to: {output_path}"
    
    print("   Running Cursor AI for module discovery...")
    result = CursorCLI.run_prompt(prompt, repo_path, timeout=600, stream=stream, debug=debug)
    
    if not result["success"]:
        print(f"   ❌ Discovery failed: {result['error']}")
        return {"components": [], "error": result["error"]}
    
    # Helper to normalize data (support both "modules" and "components")
    def normalize_data(data):
        # Support both old "modules" and new "components" format
        if "components" in data and "modules" not in data:
            data["modules"] = data["components"]
        elif "modules" in data and "components" not in data:
            data["components"] = data["modules"]
        return data
    
    # Try multiple possible output paths
    possible_paths = [
        output_path,
        str(Path(repo_path) / "docs" / "modules.json"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                data = normalize_data(data)
                count = len(data.get('components', data.get('modules', [])))
                print(f"   ✅ Discovered {count} functional components")
                print(f"   📄 Saved to: {path}")
                return data
            except json.JSONDecodeError as e:
                print(f"   ⚠️  Could not parse {path}: {e}")
    
    # If no file output, try to parse from stdout
    output = result["output"]
    try:
        # Look for JSON in the output (support both modules and components)
        import re
        json_match = re.search(r'\{[\s\S]*("modules"|"components")[\s\S]*\}', output)
        if json_match:
            data = json.loads(json_match.group())
            data = normalize_data(data)
            # Save to file
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            count = len(data.get('components', data.get('modules', [])))
            print(f"   ✅ Discovered {count} functional components")
            return data
    except:
        pass
    
    print("   ⚠️  No components discovered. Please check the output.")
    return {"components": [], "repo_path": repo_path}


def generate_doc_for_module(
    module: dict, 
    repo_path: str, 
    output_dir: str,
    loader: PromptLoader,
    stream: bool = True,
    template: str = "generate_doc"
) -> dict:
    """
    Generate documentation for a single module using Cursor.
    
    Args:
        module: Module definition dict
        repo_path: Repository path
        output_dir: Output directory for docs
        loader: PromptLoader instance
        stream: If True, show Cursor's thinking in real-time
        template: Prompt template to use (generate_doc or comprehensive)
        
    Returns:
        dict with generation results
    """
    module_name = module.get("name", "unknown")
    module_path = module.get("path", "")
    module_description = module.get("description", "")
    module_files = ", ".join(module.get("files", [])[:10])  # First 10 files
    
    # Extract additional component data for functional components
    entry_points = module.get("entry_points", [])
    services = module.get("services", [])
    repositories = module.get("repositories", [])
    related_topics = module.get("related_topics", [])
    external_deps = module.get("external_dependencies", [])
    
    try:
        prompt = loader.render(
            template,
            MODULE_NAME=module_name,
            MODULE_PATH=module_path,
            MODULE_DESCRIPTION=module_description,
            MODULE_FILES=module_files,
            REPO_PATH=repo_path
        )
        
        # Add component context if available (for functional components)
        if entry_points or services or related_topics:
            prompt += "\n\n## Additional Component Context\n\n"
            
            if entry_points:
                prompt += "**Entry Points from Discovery:**\n"
                for ep in entry_points[:10]:  # Limit to 10
                    if isinstance(ep, dict):
                        ep_type = ep.get("type", "unknown")
                        if ep_type == "api":
                            prompt += f"- API: {ep.get('method', '')} {ep.get('path', '')} → {ep.get('handler', '')}\n"
                        elif ep_type == "kafka":
                            prompt += f"- Kafka: {ep.get('topic', '')} → {ep.get('handler', '')}\n"
                        else:
                            prompt += f"- {ep_type}: {ep.get('handler', ep)}\n"
                    else:
                        prompt += f"- {ep}\n"
                prompt += "\n"
            
            if services:
                prompt += f"**Services Used:** {', '.join(services)}\n\n"
            
            if repositories:
                prompt += f"**Repositories:** {', '.join(repositories)}\n\n"
            
            if related_topics:
                prompt += f"**Related Kafka Topics:** {', '.join(related_topics)}\n\n"
            
            if external_deps:
                prompt += f"**External Dependencies:** {', '.join(external_deps)}\n\n"
        
        # Add output path instruction
        output_file = os.path.join(output_dir, f"{module_name}.md")
        prompt += f"\n\nSave the documentation to: {output_file}"
        
        result = CursorCLI.run_prompt(prompt, repo_path, timeout=600, stream=stream)
        
        if result["success"]:
            # Check if output file was created
            if os.path.exists(output_file):
                return {
                    "module": module_name,
                    "status": "success",
                    "output_file": output_file,
                    "message": "Documentation generated"
                }
            else:
                # Try to extract content from output and save manually
                content = result["output"]
                if content:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return {
                        "module": module_name,
                        "status": "success",
                        "output_file": output_file,
                        "message": "Documentation extracted from output"
                    }
                
                return {
                    "module": module_name,
                    "status": "partial",
                    "message": "Cursor completed but no output file found"
                }
        else:
            return {
                "module": module_name,
                "status": "error",
                "error": result["error"]
            }
            
    except Exception as e:
        return {
            "module": module_name,
            "status": "error",
            "error": str(e)
        }


def generate_docs(
    repo_path: str,
    modules_file: Optional[str] = None,
    output_dir: Optional[str] = None,
    parallel: int = 4,
    modules_filter: Optional[list] = None,
    stream: bool = True,
    template: str = "generate_doc"
) -> dict:
    """
    Generate documentation for all modules.
    
    Args:
        repo_path: Repository path
        modules_file: Optional pre-existing modules.json file
        output_dir: Output directory for documentation
        parallel: Number of parallel workers
        modules_filter: Optional list of module names to generate
        stream: If True, show Cursor's thinking in real-time
        template: Prompt template to use (generate_doc or comprehensive)
        
    Returns:
        dict with generation results
    """
    repo_path = str(Path(repo_path).resolve())
    output_dir = output_dir or os.path.join(repo_path, "docs", "generated")
    os.makedirs(output_dir, exist_ok=True)
    
    loader = PromptLoader()
    
    # Step 1: Get components/modules
    if modules_file and os.path.exists(modules_file):
        print(f"📂 Loading components from: {modules_file}")
        with open(modules_file, 'r') as f:
            data = json.load(f)
    else:
        data = discover_modules(repo_path, stream=stream)
    
    # Support both "modules" and "components" keys
    modules = data.get("components", data.get("modules", []))
    
    if not modules:
        print("❌ No components to document")
        return {"success": False, "error": "No components found"}
    
    # Apply filter if provided
    if modules_filter:
        modules = [m for m in modules if m.get("name") in modules_filter]
        print(f"   Filtered to {len(modules)} components")
    
    print(f"\n📝 Generating documentation for {len(modules)} components...")
    print(f"   Output: {output_dir}")
    print(f"   Template: {template}")
    print(f"   Parallelism: {parallel}")
    print()
    
    # Step 2: Generate docs in parallel
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {
            executor.submit(
                generate_doc_for_module, 
                module, 
                repo_path, 
                output_dir,
                loader,
                stream,
                template
            ): module 
            for module in modules
        }
        
        for future in as_completed(futures):
            module = futures[future]
            result = future.result()
            results.append(result)
            
            status_icon = {
                "success": "✅",
                "partial": "⚠️",
                "error": "❌"
            }.get(result.get("status"), "❓")
            
            print(f"   {status_icon} {result['module']}")
            if result.get("error"):
                print(f"      Error: {result['error']}")
    
    elapsed = time.time() - start_time
    
    # Step 3: Generate index
    print("\n📑 Generating index...")
    generate_index(modules, results, output_dir)
    
    # Summary
    success_count = sum(1 for r in results if r.get("status") == "success")
    partial_count = sum(1 for r in results if r.get("status") == "partial")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    print("\n" + "=" * 50)
    print("✨ DOCUMENTATION GENERATION COMPLETE")
    print("=" * 50)
    print(f"\n📊 Results:")
    print(f"   ✅ Success:  {success_count}")
    print(f"   ⚠️  Partial:  {partial_count}")
    print(f"   ❌ Errors:   {error_count}")
    print(f"   ⏱️  Time:     {elapsed:.1f}s")
    print(f"\n📁 Output: {output_dir}")
    
    return {
        "success": True,
        "results": results,
        "output_dir": output_dir,
        "elapsed": elapsed
    }


def generate_index(modules: list, results: list, output_dir: str):
    """Generate an index/README for the documentation."""
    index_content = f"""# Documentation Index

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Modules

| Module | Path | Status |
|--------|------|--------|
"""
    
    for module in sorted(modules, key=lambda m: m.get("name", "")):
        name = module.get("name", "unknown")
        path = module.get("path", "")
        
        result = next((r for r in results if r.get("module") == name), {})
        status = result.get("status", "pending")
        status_icon = {"success": "✅", "partial": "⚠️", "error": "❌"}.get(status, "⏳")
        
        if status == "success":
            index_content += f"| [{name}]({name}.md) | `{path}` | {status_icon} |\n"
        else:
            index_content += f"| {name} | `{path}` | {status_icon} |\n"
    
    index_file = os.path.join(output_dir, "README.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"   Saved: {index_file}")


def publish_to_outline(
    file_path: str,
    title: Optional[str] = None,
    collection_id: Optional[str] = None,
    folder: str = "Team Engineering",
    stream: bool = True,
    debug: bool = False
) -> dict:
    """
    Publish a markdown document to Outline via Cursor MCP.
    
    Args:
        file_path: Path to the markdown file
        title: Document title (derived from filename if not provided)
        collection_id: Outline collection ID
        folder: Folder path in Outline
        stream: If True, show progress
        debug: If True, show debug information
        
    Returns:
        dict with publish results
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return {"success": False, "error": "File not found"}
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Derive title from filename if not provided
    if not title:
        title = Path(file_path).stem
        # Add date
        title = f"{title} Documentation - {datetime.now().strftime('%Y-%m-%d')}"
    
    print("📤 Publishing to Outline...")
    print(f"   File: {file_path}")
    print(f"   Title: {title}")
    print(f"   Folder: {folder}")
    print(f"   Content length: {len(content)} chars")
    
    # Build the prompt for cursor-agent to publish via MCP
    # Use a more direct instruction format
    prompt = f"""You MUST use the Outline MCP tool to create a document. This is a required action.

TASK: Create a document in Outline with these EXACT parameters:

- Title: {title}
- Folder/Collection: {folder}
- Publish: true

DOCUMENT CONTENT TO PUBLISH:
```markdown
{content}
```

IMPORTANT:
1. Call the `mcp_Zapier_outline_create_document` MCP tool NOW
2. Pass the title as: "{title} - {datetime.now().strftime('%Y-%m-%d')}"
3. Pass the text as the markdown content above
4. Set publish to "true"
5. If you need a collection ID, use the folder path "{folder}" in the instructions parameter

DO NOT ask for confirmation. DO NOT summarize. Just call the MCP tool and report the result.
"""
    
    if debug:
        print("\n🔧 DEBUG: Prompt being sent:")
        print("─" * 40)
        print(f"Prompt length: {len(prompt)} chars")
        print(f"Content length: {len(content)} chars")
        print("─" * 40)
    
    # Run via cursor-agent with --approve-mcps flag to auto-approve MCP calls
    cursor_cmd = CursorCLI.get_command()
    
    if debug:
        print(f"\n🔧 DEBUG: Using command: {cursor_cmd}")
        print(f"🔧 DEBUG: Flags: --approve-mcps, -f, --sandbox disabled")
    
    # Use a modified run that includes flags for non-interactive mode
    try:
        cmd = [
            cursor_cmd,
            "--print",
            "--approve-mcps",      # Auto-approve MCP server calls
            "-f",                  # Force allow commands
            "--workspace", os.getcwd(),
            prompt
        ]
        
        if debug:
            print(f"🔧 DEBUG: Full command: {' '.join(cmd[:7])} \"<prompt>\"")
        
        if stream:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,  # Prevent waiting for stdin
                text=True,
                cwd=os.getcwd(),
                bufsize=0
            )
            
            output_chars = []
            stderr_chars = []
            
            print("\n" + "─" * 60)
            print("🤖 Cursor AI thinking...")
            print("─" * 60 + "\n", flush=True)
            
            has_output = False
            spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            spinner_idx = 0
            last_spinner_time = time.time()
            start_time = time.time()
            
            while True:
                return_code = process.poll()
                
                try:
                    fd = process.stdout.fileno()
                    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                    
                    try:
                        chunk = process.stdout.read(1024)
                        if chunk is not None and chunk:
                            has_output = True
                            print(chunk, end='', flush=True)
                            output_chars.append(chunk)
                    except (IOError, BlockingIOError, TypeError):
                        pass
                    
                    fd_err = process.stderr.fileno()
                    fl_err = fcntl.fcntl(fd_err, fcntl.F_GETFL)
                    fcntl.fcntl(fd_err, fcntl.F_SETFL, fl_err | os.O_NONBLOCK)
                    
                    try:
                        err_chunk = process.stderr.read(1024)
                        if err_chunk is not None and err_chunk:
                            print(f"\033[33m{err_chunk}\033[0m", end='', flush=True)
                            stderr_chars.append(err_chunk)
                    except (IOError, BlockingIOError, TypeError):
                        pass
                        
                except Exception as e:
                    if debug:
                        print(f"\n🔧 DEBUG: Read error: {e}")
                    pass  # Continue even on errors
                
                current_time = time.time()
                elapsed = int(current_time - start_time)
                if current_time - last_spinner_time > 0.2:
                    if not has_output:
                        print(f"\r{spinner[spinner_idx]} Waiting for response... ({elapsed}s elapsed)    ", end='', flush=True)
                    spinner_idx = (spinner_idx + 1) % len(spinner)
                    last_spinner_time = current_time
                
                if return_code is not None:
                    try:
                        remaining = process.stdout.read()
                        if remaining is not None and remaining:
                            print(remaining, end='', flush=True)
                            output_chars.append(remaining)
                    except:
                        pass
                    break
                
                time.sleep(0.05)
            
            if not has_output:
                print("\r" + " " * 50 + "\r", end='')
            
            print("\n" + "─" * 60 + "\n")
            
            output = ''.join(output_chars)
            stderr = ''.join(stderr_chars)
            
            if debug:
                print(f"🔧 DEBUG: Return code: {return_code}")
                print(f"🔧 DEBUG: Output length: {len(output)} chars")
                print(f"🔧 DEBUG: Stderr length: {len(stderr)} chars")
                if stderr:
                    print(f"🔧 DEBUG: Stderr content: {stderr[:500]}")
            
            # Check if the output indicates success or failure
            output_lower = output.lower()
            if "cancelled" in output_lower or "failed" in output_lower or "error" in output_lower:
                print(f"   ⚠️  MCP call may have failed. Check output above.")
                return {"success": False, "error": "MCP call may have failed", "output": output}
            elif "created" in output_lower or "published" in output_lower or "success" in output_lower:
                print("   ✅ Published to Outline successfully!")
                return {"success": True, "title": title, "output": output}
            else:
                print("   ⚠️  Could not determine if publish succeeded. Check output above.")
                return {"success": False, "error": "Unknown result", "output": output}
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation using Cursor AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover modules in a repository
  waygrounddocgen discover /path/to/repo
  
  # Generate documentation (discover + generate)
  waygrounddocgen generate /path/to/repo
  
  # Generate with custom parallelism
  waygrounddocgen generate /path/to/repo --parallel 8
  
  # Generate from existing modules.json
  waygrounddocgen generate /path/to/repo --modules modules.json
  
  # Generate for specific modules only
  waygrounddocgen generate /path/to/repo --filter auth,users,payments
  
  # Use comprehensive template (comprehensive docs with diagrams)
  waygrounddocgen generate /path/to/repo --template comprehensive
  
  # Publish a doc to Outline
  waygrounddocgen publish docs/generated/MyComponent.md --folder "Team Engineering"
  
  # Evaluate documentation quality
  waygrounddocgen evaluate --modules modules.json --docs-dir docs/generated/
  
  # Evaluate with auto-retry on failure
  waygrounddocgen evaluate --modules modules.json --docs-dir docs/generated/ --auto-retry
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Discover command
    discover_parser = subparsers.add_parser(
        "discover", 
        help="Discover modules/components in a repository"
    )
    discover_parser.add_argument(
        "repo_path",
        help="Path to the repository"
    )
    discover_parser.add_argument(
        "--output", "-o",
        help="Output file for modules.json (default: docs/modules.json)"
    )
    discover_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress streaming output (hide Cursor's thinking)"
    )
    discover_parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Show debug information (command being run, etc.)"
    )
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate documentation (runs discovery if needed)"
    )
    generate_parser.add_argument(
        "repo_path",
        help="Path to the repository"
    )
    generate_parser.add_argument(
        "--modules", "-m",
        help="Path to existing modules.json file"
    )
    generate_parser.add_argument(
        "--output", "-o",
        help="Output directory for documentation"
    )
    generate_parser.add_argument(
        "--parallel", "-p",
        type=int,
        default=4,
        help="Number of parallel Cursor tasks (default: 4)"
    )
    generate_parser.add_argument(
        "--filter", "-f",
        help="Comma-separated list of module names to generate"
    )
    generate_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress streaming output (hide Cursor's thinking)"
    )
    generate_parser.add_argument(
        "--template", "-t",
        default="generate_doc",
        choices=["generate_doc", "comprehensive"],
        help="Prompt template to use (default: generate_doc)"
    )
    
    # Check command
    check_parser = subparsers.add_parser(
        "check",
        help="Check if Cursor CLI is available"
    )
    
    # Publish command
    publish_parser = subparsers.add_parser(
        "publish",
        help="Publish documentation to Outline via MCP"
    )
    publish_parser.add_argument(
        "file",
        help="Path to the markdown file to publish"
    )
    publish_parser.add_argument(
        "--title", "-t",
        help="Document title (default: derived from filename)"
    )
    publish_parser.add_argument(
        "--collection", "-c",
        help="Outline collection ID to publish to"
    )
    publish_parser.add_argument(
        "--folder", "-f",
        default="Team Engineering",
        help="Folder path in Outline (default: Team Engineering)"
    )
    publish_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress streaming output"
    )
    publish_parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Show debug information"
    )
    
    # Evaluate command
    evaluate_parser = subparsers.add_parser(
        "evaluate",
        help="Evaluate documentation quality against modules.json"
    )
    evaluate_parser.add_argument(
        "--modules", "-m",
        required=True,
        help="Path to modules.json file"
    )
    evaluate_parser.add_argument(
        "--docs-dir", "-d",
        default="docs/generated",
        help="Directory containing generated docs (default: docs/generated)"
    )
    evaluate_parser.add_argument(
        "--module",
        help="Evaluate specific module by name"
    )
    evaluate_parser.add_argument(
        "--auto-retry",
        action="store_true",
        help="Automatically retry failed evaluations"
    )
    evaluate_parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="Maximum retry attempts (default: 2)"
    )
    evaluate_parser.add_argument(
        "--save-fixes",
        action="store_true",
        help="Save regenerated docs when auto-retry succeeds"
    )
    evaluate_parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip LLM evaluation (Phase 2)"
    )
    evaluate_parser.add_argument(
        "--config", "-c",
        help="Path to config.yaml"
    )
    evaluate_parser.add_argument(
        "--report", "-r",
        help="Output JSON report to file"
    )
    evaluate_parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="CI/CD mode: exit 1 on failure"
    )
    evaluate_parser.add_argument(
        "--repo-path",
        default=".",
        help="Repository root path (default: .)"
    )
    
    args = parser.parse_args()
    
    if args.command == "check" or args.command is None:
        cmd = CursorCLI.get_command()
        if cmd:
            print(f"✅ Cursor CLI is available: {cmd}")
            
            # Check login status
            if CursorCLI.is_logged_in():
                print("✅ Logged in to Cursor")
            else:
                print("⚠️  Not logged in to Cursor")
                print(f"   Run: {cmd} login")
            sys.exit(0)
        else:
            print("❌ Cursor CLI not found")
            print("   Install with: curl https://cursor.com/install -fsS | bash")
            print("   Or from GUI: Cursor Settings > General > Command Line")
            sys.exit(1)
    
    elif args.command == "discover":
        stream = not args.quiet
        debug = args.debug
        result = discover_modules(args.repo_path, args.output, stream=stream, debug=debug)
        if result.get("modules"):
            print(json.dumps(result, indent=2))
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.command == "generate":
        modules_filter = None
        if args.filter:
            modules_filter = [m.strip() for m in args.filter.split(",")]
        
        stream = not args.quiet
        result = generate_docs(
            repo_path=args.repo_path,
            modules_file=args.modules,
            output_dir=args.output,
            parallel=args.parallel,
            modules_filter=modules_filter,
            stream=stream,
            template=args.template
        )
        
        sys.exit(0 if result.get("success") else 1)
    
    elif args.command == "publish":
        result = publish_to_outline(
            file_path=args.file,
            title=args.title,
            collection_id=args.collection,
            folder=args.folder,
            stream=not args.quiet,
            debug=args.debug
        )
        sys.exit(0 if result.get("success") else 1)
    
    elif args.command == "evaluate":
        # Import evaluator here to avoid loading it when not needed
        from .eval.evaluator import DocumentationEvaluator, print_summary
        
        # Validate --save-fixes requires --auto-retry
        if args.save_fixes and not args.auto_retry:
            print("Error: --save-fixes requires --auto-retry")
            sys.exit(1)
        
        # Initialize evaluator
        evaluator = DocumentationEvaluator(
            config_path=args.config,
            repo_path=args.repo_path,
        )
        
        # Run evaluation
        if args.module:
            # Single module evaluation
            modules = evaluator.load_modules(args.modules)
            module = next((m for m in modules if m.get("name") == args.module), None)
            
            if not module:
                print(f"Module '{args.module}' not found in {args.modules}")
                sys.exit(1)
            
            slug = module.get("slug", args.module.lower().replace(" ", "-"))
            doc_path = module.get("expected_doc_path", f"{args.docs_dir}/{slug}.md")
            full_path = os.path.join(args.repo_path, doc_path)
            
            if not os.path.exists(full_path):
                print(f"Documentation not found: {doc_path}")
                sys.exit(1)
            
            with open(full_path, encoding="utf-8") as f:
                doc_content = f.read()
            
            if args.auto_retry:
                results = evaluator.evaluate_with_retry(
                    module, doc_content, args.max_retries
                )
                if args.save_fixes and results.get("regenerated_content"):
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(results["regenerated_content"])
                    print(f"Fixed documentation saved to: {doc_path}")
            else:
                results = evaluator.evaluate_module(
                    module, doc_content, run_llm=not args.no_llm
                )
            
            print(f"\n{'PASSED' if results.get('passed') else 'FAILED'}")
            
            if args.report:
                with open(args.report, "w") as f:
                    json.dump(results, f, indent=2)
                print(f"Report saved to: {args.report}")
            
            if args.ci_mode and not results.get("passed"):
                sys.exit(1)
        
        else:
            # Evaluate all modules
            results = evaluator.evaluate_all(
                modules_path=args.modules,
                docs_dir=args.docs_dir,
                auto_retry=args.auto_retry,
                max_retries=args.max_retries,
                run_llm=not args.no_llm,
                save_fixes=args.save_fixes,
            )
            
            print_summary(results)
            
            if args.report:
                with open(args.report, "w") as f:
                    json.dump(results, f, indent=2)
                print(f"\nReport saved to: {args.report}")
            
            if args.ci_mode and not results.get("overall_pass"):
                sys.exit(1)
        
        sys.exit(0)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()


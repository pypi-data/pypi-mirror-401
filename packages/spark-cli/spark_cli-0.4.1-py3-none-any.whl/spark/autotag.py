"""Intelligent auto-tagging for snippets"""
import os
from pathlib import Path
from typing import List, Set


# Common tool keywords and their tags
TOOL_KEYWORDS = {
    # Container & Orchestration
    "docker": "docker",
    "docker-compose": "docker,compose",
    "kubectl": "kubernetes,k8s",
    "podman": "podman,containers",
    
    # Version Control
    "git": "git",
    "hg": "mercurial",
    "svn": "svn",
    
    # Package Managers
    "npm": "npm,node",
    "yarn": "yarn,node",
    "pnpm": "pnpm,node",
    "pip": "pip,python",
    "pip3": "pip,python",
    "poetry": "poetry,python",
    "cargo": "cargo,rust",
    "go": "go,golang",
    "maven": "maven,java",
    "gradle": "gradle,java",
    
    # Languages
    "python": "python",
    "python3": "python",
    "node": "node,javascript",
    "nodejs": "node,javascript",
    "npm": "npm,node",
    "java": "java",
    "javac": "java",
    "gcc": "c",
    "g++": "cpp",
    "rustc": "rust",
    "go": "go",
    
    # Databases
    "psql": "postgresql,database",
    "mysql": "mysql,database",
    "mongodb": "mongodb,database",
    "redis": "redis,database",
    "sqlite": "sqlite,database",
    
    # Web Servers & Tools
    "nginx": "nginx,web",
    "apache": "apache,web",
    "curl": "curl,http",
    "wget": "wget,http",
    
    # Cloud & DevOps
    "aws": "aws,cloud",
    "gcloud": "gcp,cloud",
    "az": "azure,cloud",
    "terraform": "terraform,iac",
    "ansible": "ansible,automation",
    
    # Build Tools
    "make": "make,build",
    "cmake": "cmake,build",
    "gradle": "gradle,build",
    "maven": "maven,build",
    
    # Testing
    "pytest": "pytest,test,python",
    "jest": "jest,test,javascript",
    "mocha": "mocha,test,javascript",
    "junit": "junit,test,java",
    
    # Other
    "ssh": "ssh,remote",
    "scp": "scp,remote",
    "rsync": "rsync,sync",
    "tar": "tar,archive",
    "zip": "zip,archive",
    "gzip": "gzip,archive",
    
    # Shell & System
    "bash": "bash,shell",
    "zsh": "zsh,shell",
    "fish": "fish,shell",
    "systemctl": "systemd,linux",
    "service": "service,linux",
    
    # Text Processing
    "grep": "grep,text",
    "sed": "sed,text",
    "awk": "awk,text",
    "find": "find,file",
    
    # Monitoring & Performance
    "htop": "htop,monitoring",
    "top": "top,monitoring",
    "ps": "ps,process",
    "netstat": "netstat,network",
}


def detect_tool_tags(command: str) -> Set[str]:
    """Detect tool-related tags from command"""
    command_lower = command.lower()
    tags = set()
    
    # Check for tool keywords
    for keyword, tag_string in TOOL_KEYWORDS.items():
        if keyword in command_lower:
            tags.update(tag_string.split(","))
    
    return tags


def detect_language_tags(command: str) -> Set[str]:
    """Detect programming language from command"""
    command_lower = command.lower()
    tags = set()
    
    # Language-specific patterns
    if any(x in command_lower for x in ["python", "pip", "pyenv", "virtualenv", "venv"]):
        tags.add("python")
    
    if any(x in command_lower for x in ["npm", "yarn", "pnpm", "node", "npx"]):
        tags.add("javascript")
        tags.add("node")
    
    if any(x in command_lower for x in ["cargo", "rustc", "rustup"]):
        tags.add("rust")
    
    if any(x in command_lower for x in ["go ", "golang", "go mod"]):
        tags.add("go")
    
    if any(x in command_lower for x in ["java", "javac", "maven", "gradle"]):
        tags.add("java")
    
    if any(x in command_lower for x in ["sql", "psql", "mysql", "sqlite"]):
        tags.add("sql")
    
    return tags


def detect_context_tags() -> Set[str]:
    """Detect tags based on current working directory context"""
    tags = set()
    
    try:
        cwd = Path.cwd()
        cwd_str = str(cwd).lower()
        cwd_parts = cwd.parts
        
        # Check for common project directories
        if "project" in cwd_str or "projects" in cwd_str or "workspace" in cwd_str or "code" in cwd_str:
            # Try to detect project type from directory name
            if any(x in cwd_str for x in ["api", "backend", "server", "service"]):
                tags.add("backend")
            elif any(x in cwd_str for x in ["web", "frontend", "client", "ui", "app"]):
                tags.add("frontend")
            elif any(x in cwd_str for x in ["mobile", "ios", "android"]):
                tags.add("mobile")
            elif any(x in cwd_str for x in ["data", "ml", "ai", "machine-learning"]):
                tags.add("data")
        
        # Check for specific frameworks in directory name
        if "django" in cwd_str:
            tags.add("django")
            tags.add("python")
        elif "flask" in cwd_str:
            tags.add("flask")
            tags.add("python")
        elif "fastapi" in cwd_str:
            tags.add("fastapi")
            tags.add("python")
        elif "react" in cwd_str:
            tags.add("react")
            tags.add("javascript")
        elif "vue" in cwd_str:
            tags.add("vue")
            tags.add("javascript")
        elif "angular" in cwd_str:
            tags.add("angular")
            tags.add("javascript")
        elif "next" in cwd_str:
            tags.add("nextjs")
            tags.add("javascript")
        elif "nuxt" in cwd_str:
            tags.add("nuxt")
            tags.add("javascript")
        
        # Check for package.json, requirements.txt, etc. in current or parent dirs
        for parent in [cwd] + list(cwd.parents)[:3]:  # Check current and up to 3 parent dirs
            if (parent / "package.json").exists():
                tags.add("javascript")
                tags.add("node")
            if (parent / "requirements.txt").exists() or (parent / "pyproject.toml").exists():
                tags.add("python")
            if (parent / "Cargo.toml").exists():
                tags.add("rust")
            if (parent / "go.mod").exists():
                tags.add("go")
            if (parent / "pom.xml").exists():
                tags.add("java")
                tags.add("maven")
            if (parent / "build.gradle").exists():
                tags.add("java")
                tags.add("gradle")
        
        # Check for environment
        if any(x in cwd_str for x in ["dev", "development", "local"]):
            tags.add("dev")
        elif any(x in cwd_str for x in ["prod", "production", "live"]):
            tags.add("prod")
        elif any(x in cwd_str for x in ["test", "testing", "qa"]):
            tags.add("test")
        elif any(x in cwd_str for x in ["staging", "stage"]):
            tags.add("staging")
        
    except Exception:
        # If we can't detect context, just return empty set
        pass
    
    return tags


def generate_auto_tags(command: str, include_context: bool = True) -> str:
    """
    Generate automatic tags for a command.
    
    Args:
        command: The command to analyze
        include_context: Whether to include directory context tags
        
    Returns:
        Comma-separated string of tags
    """
    all_tags = set()
    
    # Detect tool tags
    all_tags.update(detect_tool_tags(command))
    
    # Detect language tags
    all_tags.update(detect_language_tags(command))
    
    # Detect context tags (optional)
    if include_context:
        all_tags.update(detect_context_tags())
    
    # Remove empty strings and sort
    all_tags = {tag.strip() for tag in all_tags if tag.strip()}
    
    return ",".join(sorted(all_tags))


def merge_tags(manual_tags: str = None, auto_tags: str = None) -> str:
    """
    Merge manual and auto tags, removing duplicates.
    
    Args:
        manual_tags: Comma-separated manual tags
        auto_tags: Comma-separated auto tags
        
    Returns:
        Comma-separated merged tags
    """
    all_tags = set()
    
    if manual_tags:
        all_tags.update(tag.strip() for tag in manual_tags.split(",") if tag.strip())
    
    if auto_tags:
        all_tags.update(tag.strip() for tag in auto_tags.split(",") if tag.strip())
    
    return ",".join(sorted(all_tags))


import argparse
import sys
from .parser import Parser
from .builder import Builder
from .synchronizer import Synchronizer
from .exporter import Exporter
from .validator import Validator
from .git_integration import GitIntegration
from .local_ai import LocalAI

def main():
    parser = argparse.ArgumentParser(description="AIForge: Bidirectional AI-Project Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ai2project
    p_ai2proj = subparsers.add_parser("ai2project", help="Convert AI dump to project")
    p_ai2proj.add_argument("dump_file", help="Input dump file")
    p_ai2proj.add_argument("project_name", help="Output project directory")
    p_ai2proj.add_argument("--mode", choices=['clean', 'merge'], default='clean', help="Build mode")

    # project2ai
    p_proj2ai = subparsers.add_parser("project2ai", help="Convert project to AI-friendly file")
    p_proj2ai.add_argument("project_dir", help="Project directory")
    p_proj2ai.add_argument("output_file", help="Output markdown file")
    p_proj2ai.add_argument("--max-tokens", type=int, default=4000, help="Max tokens per chunk")

    # sync
    p_sync = subparsers.add_parser("sync", help="Synchronize project with new dump")
    p_sync.add_argument("new_dump", help="New dump file")
    p_sync.add_argument("project_dir", help="Project directory")
    p_sync.add_argument("--mode", choices=['patch', 'replace', 'append'], default='patch')
    p_sync.add_argument("--non-interactive", action='store_true', help="Disable interactive merge")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate project structure")
    p_val.add_argument("project_dir", help="Project directory")

    # init-git
    p_git = subparsers.add_parser("init-git", help="Initialize Git hooks")
    p_git.add_argument("project_dir", help="Project directory")

    # refine
    p_refine = subparsers.add_parser("refine", help="Refine project with local AI")
    p_refine.add_argument("project_dir", help="Project directory")
    p_refine.add_argument("--model", required=True, help="Model name (e.g. mistralai/Mistral-7B-Instruct-v0.1)")

    args = parser.parse_args()

    if args.command == "ai2project":
        print(f"Converting {args.dump_file} to {args.project_name}...")
        parser_obj = Parser()
        data = parser_obj.parse(args.dump_file)
        builder = Builder()
        builder.build(data, args.project_name, args.mode)
    
    elif args.command == "project2ai":
        exporter = Exporter()
        exporter.export(args.project_dir, args.output_file, args.max_tokens)
    
    elif args.command == "sync":
        parser_obj = Parser()
        new_data = parser_obj.parse(args.new_dump)
        syncer = Synchronizer()
        syncer.sync(args.project_dir, new_data, args.mode, not args.non_interactive)

    elif args.command == "validate":
        validator = Validator()
        res = validator.validate(args.project_dir)
        print(res)

    elif args.command == "init-git":
        git_int = GitIntegration()
        git_int.init_git(args.project_dir)

    elif args.command == "refine":
        ai = LocalAI()
        ai.refine(args.project_dir, args.model)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
